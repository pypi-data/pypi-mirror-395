from typing import Optional
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    USER_AGENT: str = 'ws-bom-robot'
    robot_env: str = 'local'
    robot_user: str = 'user'
    robot_password: str = 'password'
    robot_data_folder: str = './.data'
    robot_data_db_folder: str = 'vector_db'
    robot_data_db_folder_src: str = 'src'
    robot_data_db_folder_out: str = 'out'
    robot_data_db_folder_store: str = 'store'
    robot_data_db_retention_days: float = 60
    robot_data_attachment_folder: str = 'attachment'
    robot_data_attachment_retention_days: float = 1
    robot_ingest_max_threads: int = 1 # safe choice to 1, avoid potential process-related issues with Docker
    robot_loader_max_threads: int = 1
    robot_task_max_total_parallelism: int = 2 * (os.cpu_count() or 1)
    robot_task_retention_days: float = 1
    robot_task_strategy: str = 'memory' # memory / db
    robot_task_mp_enable: bool = True
    robot_task_mp_method: str = 'spawn' # spawn / fork
    robot_task_mp_max_retries: int = 1
    robot_task_mp_retry_delay: float = 60 # seconds
    robot_cron_strategy: str = 'memory' # memory / db
    robot_cms_host: str = ''
    robot_cms_auth: str = ''
    robot_cms_db_folder: str = 'llmVectorDb'
    robot_cms_kb_folder: str ='llmKbFile'
    ANTHROPIC_API_KEY: str = ''
    DEEPSEEK_API_KEY: str = ''
    OPENAI_API_KEY: str = '' # used also for saas dall-e api
    OLLAMA_API_URL: str = 'http://localhost:11434'
    GROQ_API_KEY: str = ''
    GOOGLE_API_KEY: str = ''
    GOOGLE_APPLICATION_CREDENTIALS: str = '' # path to google credentials iam file, e.d. ./.secrets/google-credentials.json
    WATSONX_URL: str = ''
    WATSONX_APIKEY: str = ''
    WATSONX_PROJECTID: str = ''
    NEBULY_API_URL: str ='https://backend.nebuly.com/'
    LANGSMITH_API_KEY: str = '' # app-wide api key to run evaluation
    model_config = ConfigDict(
        env_file='./.env',
        extra='ignore',
        case_sensitive=False
    )
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # env
        os.environ["USER_AGENT"] = self.USER_AGENT
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY
        os.environ["OLLAMA_API_URL"] = self.OLLAMA_API_URL
        os.environ["ANTHROPIC_API_KEY"] = self.ANTHROPIC_API_KEY
        os.environ["DEEPSEEK_API_KEY"] = self.DEEPSEEK_API_KEY
        os.environ["GROQ_API_KEY"] = self.GROQ_API_KEY
        os.environ["GOOGLE_API_KEY"] = self.GOOGLE_API_KEY
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.GOOGLE_APPLICATION_CREDENTIALS
        os.environ["WATSONX_URL"] = self.WATSONX_URL
        os.environ["WATSONX_APIKEY"] = self.WATSONX_APIKEY
        os.environ["WATSONX_PROJECTID"] = self.WATSONX_PROJECTID
        os.environ["NEBULY_API_URL"] = self.NEBULY_API_URL
        os.environ["LANGSMITH_API_KEY"] = self.LANGSMITH_API_KEY
        # dir
        os.makedirs(self.robot_data_folder, exist_ok=True)
        for subfolder in [self.robot_data_db_folder, self.robot_data_attachment_folder, 'db']:
            os.makedirs(os.path.join(self.robot_data_folder, subfolder), exist_ok=True)

    class RuntimeOptions(BaseModel):
        @staticmethod
        def _get_sys_arg(arg: str, default: int) -> int:
            """
            Returns the number of worker processes to use for the application.

            This function inspects the command-line arguments to determine the number
            of worker processes to use. It looks for the "--workers" argument and
            returns the subsequent value as an integer.
            Sample of command-line arguments:
            fastapi dev main.py --port 6001
            fastapi run main.py --port 6001 --workers 4
            uvicorn main:app --port 6001 --workers 4

            Returns:
                Optional[int]: The number of worker processes to use, or 1 if
                               the argument is not found or the value is invalid.
            """
            import sys
            try:
                for i, argv in enumerate(sys.argv):
                    if argv == f"--{arg}" and i + 1 < len(sys.argv):
                        return int(sys.argv[i + 1])
            except (ValueError, IndexError):
                pass
            return default
        debug: bool
        tcp_port: int = _get_sys_arg("port", 6001)
        loader_show_progress: bool
        loader_silent_errors: bool
        number_of_workers: int = _get_sys_arg("workers", 1)
        is_multi_process: bool = _get_sys_arg("workers", 1) > 1

    def runtime_options(self) -> RuntimeOptions:
      """_summary_
      Returns:
          _runtime_options:
            return degug flag and loader options based on the robot environment.
            the loader options is usefull to minimizing sytem requirements/dependencies for local development
      """
      if self.robot_env == "local":
        return self.RuntimeOptions(debug=True,loader_show_progress=True, loader_silent_errors=True)
      elif self.robot_env == "development":
        return self.RuntimeOptions(debug=True,loader_show_progress=True, loader_silent_errors=False)
      else:
        return self.RuntimeOptions(debug=False,loader_show_progress=False, loader_silent_errors=True)

# global instance
config = Settings()

