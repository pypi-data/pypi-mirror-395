import asyncio
import base64
from datetime import datetime, timezone
from math import floor
import httpx
import logging
from standardwebhooks import Webhook
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from typing import Optional
from ws_bom_robot_app.config import config
from ws_bom_robot_app.llm.models.base import IdentifiableEntity

class WebhookNotifier:
    MAX_RETRIES = 10
    BASE_DELAY = 5  # seconds
    MAX_DELAY = 120  # maximum delay between retries

    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=BASE_DELAY, max=MAX_DELAY),
        retry=retry_if_exception_type((httpx.HTTPError, asyncio.TimeoutError)),
        after=lambda retry_state: logging.warning(
            f"Webhook notification attempt {retry_state.attempt_number} failed "
            f"for endpoint {retry_state.args[1]}"
        )
    )
    async def notify_webhook(
        self,
        data: IdentifiableEntity,
        endpoint: str,
        timeout: Optional[float] = 30.0
    ) -> None:
        """
        Notify a signed webhook. App credentials are used to sign the webhook.
        Args:
            task: The task result to send
            endpoint: Webhook URL to notify
            timeout: Request timeout in seconds
        Raises:
            Exception: If all retry attempts fail
        """
        wh = Webhook(base64.b64encode((config.robot_user + ':' + config.robot_password).encode('utf-8')).decode('utf-8'))
        _data = data.model_dump_json()
        _datetime = datetime.now(tz=timezone.utc)
        _signature = wh.sign(data.id,_datetime,_data)
        _headers = {
            'webhook-id': data.id,
            'webhook-timestamp': str(floor(_datetime.replace(tzinfo=timezone.utc).timestamp())),
            'webhook-signature': _signature
            }
        async with httpx.AsyncClient(headers=_headers,verify=False,timeout=timeout) as client:
          response = await client.post(endpoint, data=_data)
          response.raise_for_status()

