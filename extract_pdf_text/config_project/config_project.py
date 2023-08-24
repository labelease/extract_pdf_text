import os
from pathlib import Path

from dynaconf import settings

dir_root = Path(__file__).absolute().parent

list_files = [
    str(Path(dir_root, "settings.toml")),
    str(Path(dir_root, ".secrets.toml")),
]

os.environ["ENV_FOR_DYNACONF"] = "development"
os.environ["SETTINGS_FILE_FOR_DYNACONF"] = ";".join(list_files)
