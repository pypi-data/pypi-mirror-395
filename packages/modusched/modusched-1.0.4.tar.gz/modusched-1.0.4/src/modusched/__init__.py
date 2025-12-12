from dotenv import load_dotenv, find_dotenv
from modusched.core import BianXieAdapter,ArkAdapter
# TODO 深度思考
# TODO 视觉理解
# TODO GUI Agent

dotenv_path = find_dotenv()
load_dotenv(".env", override=True)

__all__ = [
    "BianXieAdapter",
    "ArkAdapter",
]
