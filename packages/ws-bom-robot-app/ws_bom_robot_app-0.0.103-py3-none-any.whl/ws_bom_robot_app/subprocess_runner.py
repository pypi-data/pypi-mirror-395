import logging
import multiprocessing as mp
from multiprocessing.connection import Connection
import dill as _pickler
import types, traceback
import asyncio, sys
from ws_bom_robot_app.config import config

def _worker_run_pickled(serialized_task: bytes, conn: Connection):
    """
    Unpickle the object (should be an awaitable or callable), run it inside its own asyncio loop,
    capture return value or exception and send back via conn.send((ok_flag, payload_serialized)).
    This runs in a separate process and must be top-level for multiprocessing.
    """
    import os
    # mark as a subprocess
    os.environ['IS_ROBOT_APP_SUBPROCESS'] = 'true'
    try:
        if _pickler is None:
            raise RuntimeError("No pickler available in worker process.")

        obj = _pickler.loads(serialized_task)

        # If obj is a coroutine object, run directly; if it's a callable, call it and maybe await result.
        async def _wrap_and_run(o):
            if asyncio.iscoroutine(o):
                return await o
            elif isinstance(o, types.FunctionType) or callable(o):
                # call it; if returns coroutine, await it
                result = o()
                if asyncio.iscoroutine(result):
                    return await result
                return result
            else:
                # not callable / awaitable
                return o

        # Run inside asyncio.run (fresh loop)
        result = asyncio.run(_wrap_and_run(obj))
        # try to pickle result for sending, if fails, str() it
        try:
            payload = _pickler.dumps(("ok", result))
        except Exception:
            payload = _pickler.dumps(("ok", str(result)))
        conn.send_bytes(payload)
    except Exception as e:
        # send back the error details
        try:
            tb = traceback.format_exc()
            payload = _pickler.dumps(("err", {"error": str(e), "traceback": tb}))
            conn.send_bytes(payload)
        except Exception:
            # last resort: send plain text
            try:
                conn.send_bytes(b'ERR:' + str(e).encode("utf-8"))
            except Exception:
                pass
    finally:
        try:
            conn.close()
        except Exception:
            pass
async def _recv_from_connection_async(conn: Connection):
    """
    Blocking recv wrapped for asyncio using a threadpool.
    We expect worker to use conn.send_bytes(payload) — we use conn.recv_bytes() to get bytes.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, conn.recv_bytes)  # blocking call inside executor
def _start_subprocess_for_coroutine(coroutine_obj):
    """
    Try to start a subprocess that will run the provided coroutine/callable.
    Returns tuple (process, parent_conn, used_subprocess_flag)
    If cannot serialize, returns (None, None, False)
    """
    def _get_mp_start_method():
        """Get the multiprocessing start method.

        For Windows + Jupyter compatibility, 'spawn' is required
        'spawn' guarantees that every worker starts fresh and doesn't carry Python heap or native allocations from the parent.
        'fork' to get faster startup and lower initial memory cost, carries over everything in parent memory, including global variables and open resources: can be unsafe with threads, async loops

        Returns:
            str: The multiprocessing start method.
        """
        if sys.platform == "win32":
            return "spawn"
        return config.robot_task_mp_method

    try:
        serialized = _pickler.dumps(coroutine_obj)
    except Exception:
        # cannot serialize the coroutine/callable -> fall back to in-process
        return (None, None, False)

    parent_conn, child_conn = mp.Pipe(duplex=False)

    ctx = mp.get_context(_get_mp_start_method())
    p = ctx.Process(target=_worker_run_pickled, args=(serialized, child_conn), daemon=False)
    p.start()
    # close child conn in parent process
    try:
        child_conn.close()
    except Exception:
        pass
    return (p, parent_conn, True)
