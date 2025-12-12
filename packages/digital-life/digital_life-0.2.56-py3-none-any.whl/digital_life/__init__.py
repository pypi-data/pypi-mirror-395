from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(".env", override=True)

from .log import Log
Log_ = Log()
logger = Log_.logger


# logger.usecase("hsldfjk")
# logger.datacol("hsldfjk")
