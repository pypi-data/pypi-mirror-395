import asyncio
import cyclopts
import logging
import niquests
import os
from pathlib import Path
from rich import print
from rich.logging import RichHandler
import sys

from .actions import execute_actions
from .pkgstatus import get_locklist, package_item_action, Action, Options
from .reporter import Reporter, TagMatcher
from . import VERSION


logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger("wheel_getter")
reporter = Reporter()
app = cyclopts.App(
        name = "wheel-getter",
        version = VERSION,
        config = [
            cyclopts.config.Env("WHEEL_GETTER_"),
            cyclopts.config.Yaml(
                "wheel_getter_config.yaml",
                search_parents = True,
                use_commands_as_keys = False,
                ),
            ]
        )


@app.default
def get_wheels(
        wheelhouse: Path = Path("wheels"),
        # lockfile: Path = Path("uv.lock"),
        project: Path | None = None,
        directory: Path | None = None,
        clear: bool = False,
        python: str | None = None,
        debug: bool = False,
        dry_run: bool = False,
        ) -> None:
    """Gets and/or builds wheels if necessary, putting them in the wheelhouse."""
    if debug:
        logger.setLevel(logging.DEBUG)
    
    if directory is not None:
        os.chdir(directory)
        logger.debug("changed to %s", directory)
    
    if project is None:
        base_dir = Path.cwd()
        while not (base_dir / "pyproject.toml").exists():
            parent = base_dir.parent
            if parent == base_dir:
                logger.error("no project found")
                raise ValueError("no project found")
            base_dir = parent
    else:
        base_dir = project
        if not (base_dir / "pyproject.toml").exists():
            logger.error("%s is not a package directory", project)
            raise ValueError("no project found")
    logger.debug("using base directory %s", base_dir)
    
    if python is None:
        if (pin_file := base_dir / ".python-version").exists():
            python_version = pin_file.read_text().strip()
        else:
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        logger.info("working with Python version %s", python_version)
    else:
        python_version = python
    py_marker = f"cp{python_version.replace('.', '')}"
    logger.debug("using python marker %s", py_marker)
    
    lockfile = base_dir / "uv.lock"
    if not lockfile.exists():
        logger.error("no lockfile found at %s", base_dir)
        raise ValueError("no lockfile found")
    locklist = get_locklist(base_dir, reporter=reporter)
    
    if not wheelhouse.exists():
        if dry_run:
            print(f"[green]would create wheelhouse “{wheelhouse}”")
        else:
            wheelhouse.mkdir(parents=True, exist_ok=True)
            logging.info("created wheelhouse directory “%s”", wheelhouse)
    if clear:
        if dry_run:
            print(f"[green]would remove all files from “{wheelhouse}”")
        else:
            subprocess.run(["rm", "-rf", f"{wheelhouse}/*"], check=True)
            logging.info("removed all files from “%s”", wheelhouse)
    
    matcher = TagMatcher(python=python_version)
    
    options = Options(wheelhouse=wheelhouse, base_dir=base_dir, python=python_version,
            debug=debug, dry_run=dry_run, matcher=matcher, reporter=reporter)
    
    actions: list[Action] = []
    for item in locklist:
        action = package_item_action(item, options=options)
        if action is not None:
            actions.append(action)
    
    execute_actions(actions, destination=wheelhouse, dry_run=dry_run)
    for action in actions:
        if action.failed:
            reporter.error(action.message)
    
    reporter.report()
