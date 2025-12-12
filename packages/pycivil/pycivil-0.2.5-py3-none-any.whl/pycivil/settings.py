from importlib.resources import files
from pathlib import Path

from pydantic_settings import BaseSettings

BASE_PATH = Path(__file__).parent.parent.parent

class ServerSettings(BaseSettings):
    latex_templates_path: Path = Path(str(files("pycivil") / "templates" / "latex"))
    codeaster_templates_path: Path = Path(str(files("pycivil") / "templates" / "codeaster"))
    midas_templates_path: Path = Path(str(files("pycivil") / "templates" / "midas"))
    codeaster_container: str = "0.0.0.0:8100"
    codeaster_launcher: str = "CONTAINER"
