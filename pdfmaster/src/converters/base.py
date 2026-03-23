from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union


class BaseConverter(ABC):
    @abstractmethod
    def convert(
        self, input_path: Union[str, Path], output_path: Union[str, Path]
    ) -> Path:
        pass

    @staticmethod
    def validate_input(path: Union[str, Path]) -> Path:
        if isinstance(path, str):
            path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")
        return path
