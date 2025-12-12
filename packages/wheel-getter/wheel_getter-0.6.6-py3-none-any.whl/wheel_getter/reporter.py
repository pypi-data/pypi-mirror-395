import logging
import msgspec
from pip._internal.utils import compatibility_tags
from rich import print
from wheel_filename import ParsedWheelFilename


logger = logging.getLogger("wheel_getter")


class Reporter(msgspec.Struct):
    warnings: list[str] = []
    errors: list[str] = []
    
    def warning(self, message: str, *inserts: str) -> None:
        logger.warning(message, *inserts)
        self.warnings.append(message % inserts)
    
    def error(self, message: str, *inserts: str) -> None:
        logger.error(message, *inserts)
        self.errors.append(message % inserts)
    
    def report(self) -> int:
        weight = 0
        for m in self.warnings:
            print(f"[magenta]warning: {m}")
            weight = logging.WARNING
        for m in self.errors:
            print(f"[red]error: {m}")
            weight = logging.ERROR
        return weight


class TagMatcher:
    """Matches (parsed) filenames of wheels against a list of applicable tags."""
    
    # This class is here in the reporter module to avoid dependency problems
    # (with typing)
    # it should be elsewhere
    
    def __init__(self,
            python: str,
            ) -> None:
        self.python = python
        self.interpreters: set[str] = set()
        max_minor = int(python.split(".")[1])
        for i in range(max_minor + 1):
            self.interpreters.add(f"py3{i}")
            self.interpreters.add(f"cp3{i}")
        self.tags = compatibility_tags.get_supported()
    
    def match_parsed_filename(self,
            name: ParsedWheelFilename,
            ) -> int | None:
        """Returns an integer weight if filename matches, None otherwise."""
        check_platform = "any" not in name.platform_tags
        check_abi = "none" not in name.abi_tags
        check_python = "py3" not in name.python_tags
        for i, tag in enumerate(self.tags):
            if tag.interpreter not in self.interpreters:
                continue
            if check_platform:
                if tag.platform not in name.platform_tags:
                    continue
            if check_python:
                if tag.interpreter not in name.python_tags:
                    continue
            if check_abi:
                if tag.abi not in name.abi_tags:
                    continue
            return i
        return None
