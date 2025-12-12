from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(".env", override=True)
import logging
from .log import Log
Log_ = Log(console_level = logging.WARNING, # 显示控制台的等级 WARNING
             log_file_name="app.log")
logger = Log_.logger

from .prompt_craft import AsyncIntel, Intel
