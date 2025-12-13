from pydantic import BaseModel, Field, validator
from typing import List

DEFAULT_EXT = [".py", ".json"]
DEFAULT_EXCLUDE = ["venv", "__pycache__", ".git"]
DEFAULT_SPECIAL_JSON = ["config_ui.json"]


class DiagnoseConfig(BaseModel):
    include_ext: List[str] = Field(default_factory=lambda: DEFAULT_EXT.copy())
    exclude_dirs: List[str] = Field(default_factory=lambda: DEFAULT_EXCLUDE.copy())
    exclude_files: List[str] = Field(default_factory=list)
    include_files: List[str] = Field(default_factory=list)
    special_json: List[str] = Field(default_factory=lambda: DEFAULT_SPECIAL_JSON.copy())

    # валидация расширений
    @validator("include_ext", each_item=True)
    def validate_ext(cls, v):
        if not v.startswith("."):
            raise ValueError(f"Расширение '{v}' должно начинаться с точки")
        return v

    # валидация директорий
    @validator("exclude_dirs", each_item=True)
    def validate_dir(cls, v):
        if "/" in v or "\\" in v:
            raise ValueError(f"Имя директории '{v}' должно быть только именем, без пути")
        return v

    @validator("exclude_files", "include_files", each_item=True)
    def validate_filename(cls, v):
        if "/" in v or "\\" in v:
            raise ValueError(f"Имя файла '{v}' должно быть только именем файла")
        return v
