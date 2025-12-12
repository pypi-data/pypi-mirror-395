from enum import Enum
import json
import logging
import msgspec
import niquests
from pathlib import Path
import shutil
import subprocess
import sys
from typing import cast
from urllib.parse import urlparse
from wheel_filename import parse_wheel_filename


from .cache import CacheDatabase
from .checksums import get_checksum, verify_checksum
from .copyfiles import copy_files


logger = logging.getLogger("wheel_getter")


class Download(Enum):
    NONE = 0
    WHEEL = 1
    SDIST = 2


class Downloader:
    def __init__(self) -> None:
        self.session = niquests.Session(multiplexed=True)
    
    def add_download(self, uri: str) -> niquests.models.ResponsePromise:
        rp = self.session.get(uri)
        return rp
    
    def execute(self) -> None:
        self.session.gather()


class Copier:
    def __init__(self, target_dir: Path) -> None:
        self.target_dir = target_dir
        self.source_files: list[Path] = []
    
    def add_copy(self, src: Path) -> None:
        self.source_files.append(src)
    
    def execute(self, clean: bool = False) -> None:
        copy_files(self.target_dir, self.source_files, clean=clean)


def execute_actions(
        actions: list["Action"],
        destination: Path,
        dry_run: bool = False,
        ) -> None:
    cdb = CacheDatabase()
    dl = Downloader()
    cp = Copier(destination)
    
    no_dry_actions: list["Action"] = []
    for action in actions:
        if dry_run or action.dry_run:
            action.do_dry_run()
        else:
            no_dry_actions.append(action)
    if not no_dry_actions:
        return
    actions = no_dry_actions
    
    # try to find all files in the cache
    for action in actions:
        action.check_cache(cdb)
        action.check_local(cdb)
    for action in actions:
        action.request_download(dl)
    dl.execute()
    for action in actions:
        action.process_download(cdb)
    for action in actions:
        action.build_wheel(cdb)
    for action in actions:
        if action.failed or action.wheel_filename is None:
            # report
            continue
        cp.add_copy(action.wheel_filename)
    cp.execute()


class Action(msgspec.Struct):
    """Description of an action (download / copy / build wheel)"""
    
    # general (required) attributes
    name: str  # package name
    version: str  # package version
    target_directory: Path  # where the wheels are collected
    python: str  # Python version
    
    # execution options
    dry_run: bool = False
    
    # task options / data
    download: Download = Download.NONE
    download_request: niquests.models.ResponsePromise | niquests.models.Response | None = None
    build: bool = False
    url: str | None = None
    source_path: Path | None = None
    wheel_name: str = ""
    wheel_size: int = 0
    wheel_hash: str = ""
    wheel_filename: Path | None = None
    sdist_filename: Path | None = None
    add_to_cache: bool = False
    
    # results and status information
    failed: bool = False
    message_weight: int = 0
    message: str = ""
    download_status: int = 0
    
    def check_cache(self,
            cdb: CacheDatabase,
            ) -> None:
        if self.download == Download.WHEEL:
            r = cdb.find_wheel(
                    self.wheel_name,
                    size=self.wheel_size,
                    hash=self.wheel_hash,
                    )
            if r is not None:
                self.wheel_filename = r
        elif self.download == Download.SDIST:
            name = Path(cast(str, urlparse(self.url).path)).name
            r = cdb.find_sdist(
                    name,
                    )
            if r is not None:
                self.sdist_filename = r
        else:
            pass  # no download
    
    def check_local(self,
            cdb: CacheDatabase,
            ) -> None:
        if self.download == Download.NONE:
            data = self.source_path.read_bytes()
            self.wheel_filename = cdb.add_wheel(self.wheel_name, data, "")
    
    def request_download(self,
            downloader: Downloader,
            ) -> None:
        if self.url is None:
            return
        if self.download == Download.WHEEL and self.wheel_filename is None:
            self.download_request = downloader.add_download(self.url)
        elif self.download == Download.SDIST and self.sdist_filename is None:
            self.download_request = downloader.add_download(self.url)
        # else: no download requested
        return
    
    def process_download(self,
            cdb: CacheDatabase,
            ) -> None:
        response = self.download_request
        if response is None:
            # no download
            return
        if not response.ok:
            self.failed = True
            self.message_weight = logging.ERROR
            self.message = f"Download from {self.url} failed: {response.reason}"
            self.download_status = cast(int, response.status_code)
            return
        if self.download == Download.WHEEL:
            data = cast(bytes, response.content)
            ok = self.check_wheel(data)
            if not ok:
                return
            self.wheel_filename = cdb.add_wheel(self.wheel_name, data, self.url)
        elif self.download == Download.SDIST:
            data = cast(bytes, response.content)
            name = Path(cast(str, urlparse(self.url).path)).name
            self.sdist_filename = cdb.add_sdist(name, data, self.url)
        return
    
    def build_wheel(self,
            cdb: CacheDatabase,
            ) -> None:
        """Builds a wheel from an sdist."""
        if self.download != Download.SDIST or self.wheel_filename is not None:
            return
        workdir = self.target_directory.absolute() / f"tmp-{self.name}"
        workdir.mkdir(exist_ok=True)
        filepath = self.sdist_filename
        if filepath is None:
            print(f"XXX sdist not found: {filepath}")
            return  # XXX
        
        try:
            result = subprocess.run(
                    ["uv", "build",
                        "--wheel",
                        "--no-config",
                        "--python", self.python,
                        "--out-dir", workdir / "dist",
                        str(filepath),
                        ],
                    capture_output=True,
                    )
            if result.returncode:
                print(result.stdout)
                print(result.stderr, file=sys.stderr)
                self.failed = True
                self.message = f"failed to build wheel for {self.name}"
                return
            wheel_found = False
            wheel_path = Path("")  # make pyright happy; this is always overwritten
            for path in (workdir / "dist").glob("*.whl"):
                parsed = parse_wheel_filename(path.name)
                parsed_project = parsed.project.replace("_", "-")
                if parsed_project != self.name or parsed.version != self.version:
                    print(f"{parsed_project=}, {parsed.version=} – {self.name=}, {self.version=}")
                    continue
                wheel_path = path
                wheel_found = True
                break
            if not wheel_found:
                self.failed = True
                self.message = f"no wheel for {self.name} found after build"
                return
            self.wheel_name = wheel_path.name
            data = wheel_path.read_bytes()
            
        finally:
            try:
                shutil.rmtree(workdir)
            except OSError:
                pass
        self.wheel_filename = cdb.add_wheel(self.wheel_name, data, self.url)
    
    def do_dry_run(self,
            ) -> None:
        """Simulates the action."""
        if self.download == Download.SDIST:
            logger.info(
                    "Would download sdist for %s from %s",
                    self.name, self.url)
        elif self.download == Download.WHEEL:
            logger.info(
                    "Would download wheel for %s from %s",
                    self.name,  self.url)
        elif self.source_path is not None:
            logger.info(
                    "Would copy wheel for %s from %s",
                    self.name, self.source_path)
        if self.build:
            logger.info(
                    "Would build wheel for %s",
                    self.name)
        return
    
    def check_wheel(self, data: bytes) -> bool:
        """Checks wheel size and hash sum."""
        if self.wheel_size and self.wheel_size != len(data):
            self.failed = True
            self.message_weight = logging.ERROR
            self.message = (
                    f"wrong wheel size detected for {self.name}: "
                    f"{len(data)} (expected: {self.wheel_size})"
                    )
            return False
        if self.wheel_hash and not verify_checksum(data, self.wheel_hash):
            self.failed = True
            self.message_weight = logging.ERROR
            self.message = f"checksum failure for {self.name}"
            return False
        return True
