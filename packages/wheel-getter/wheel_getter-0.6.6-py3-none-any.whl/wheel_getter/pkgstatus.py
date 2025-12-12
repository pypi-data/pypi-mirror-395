"""Provides information about installed packages and their status."""


from datetime import datetime as dt
import functools
import json
import logging
import msgspec
import os
from pathlib import Path
import platform
import subprocess
import sys
from urllib.parse import urlparse
from wheel_filename import parse_wheel_filename

from .actions import Action, Download
from .checksums import verify_checksum
from .reporter import Reporter, TagMatcher


logger = logging.getLogger("wheel_getter")


class Options(msgspec.Struct):
    wheelhouse: Path
    base_dir: Path
    python: str
    debug: bool
    dry_run: bool
    matcher: TagMatcher
    reporter: Reporter


class PackageSource(msgspec.Struct):
    registry: str | None = None
    editable: str | None = None
    virtual: str | None = None
    
    def resolve_editable(self, base_dir: Path) -> Path | None:
        """Converts location of editable installation to Path object and resolves it."""
        if self.editable is None:
            return None
        else:
            return (base_dir / self.editable).resolve()


class PackageSdist(msgspec.Struct):
    url: str
    hash: str  # format: "sha256:<hash>"
    size: int
    upload_time: dt | None = None  # format: "2024-11-30T04:30:14.439Z"


class PackageWheel(msgspec.Struct):
    url: str | None = None
    hash: str = ""  # format: "sha256:<hash>"
    size: int = 0
    path: str = ""
    upload_time: dt | None = None  # format: "2024-11-30T04:30:14.439Z"


class PackageInfo(msgspec.Struct):
    name: str
    version: str
    source: PackageSource
    wheels: list[PackageWheel] = []
    sdist: PackageSdist | None = None


class UvLockfile(msgspec.Struct):
    version: int
    revision: int
    package: list[PackageInfo]


class PackageListItem(msgspec.Struct):
    """Information about an installed module provided by `uv pip list`"""
    name: str
    version: str
    location: Path | None = None
    info: PackageInfo | None = None  # to be supplied from other sources


def package_item_action(
        item: PackageListItem,
        options: Options,
        ) -> Action | None:
    """Creates an Action object for a PackageListItem."""
    
    if False:
        # is a locally built wheel present in the wheelhouse?
        info_name = options.wheelhouse / f"{item.name}-{item.version}.info"
        if info_name.exists():
            try:
                metadata = json.load(open(info_name))
                filename = options.wheelhouse / metadata.get("filename", "")
                hash = metadata.get("hash", "")
                size = metadata.get("size", 0)
                if filename.exists():
                    content = filename.read_bytes()
                    if len(content) == size and verify_checksum(content, hash):
                        logger.info("suitable wheel found for %s", item.name)
                        return None
            except Exception:
                pass
    
    make_action = functools.partial(Action,
            name=item.name,
            version=item.version,
            target_directory=options.wheelhouse,
            python=options.python,
            dry_run=options.dry_run,
            )
    
    # If there are wheels,
    # - check them all
    # - discard non-matching wheels
    # - of the remaining ones, take the best one if any
    # - check if it has to be downloaded (get url) or copied (get source)
    #   and where it goes
    if item.info is not None and item.info.wheels:
        matched_wheels: list[tuple[int, PackageWheel]] = []
        for wheel in item.info.wheels:
            if wheel.url is None:
                # local file
                wheel_filename = wheel.path
            else:
                # file to be downloaded
                wheel_filename = Path(urlparse(wheel.url).path).name
            parsed_filename = parse_wheel_filename(wheel_filename)
            if (w := options.matcher.match_parsed_filename(parsed_filename)) is not None:
                matched_wheels.append((w, wheel))
        if matched_wheels:
            matched_wheels.sort()
            w, wheel = matched_wheels[0]
            if wheel.url is None:
                # local file
                wheel_filename = wheel.path
                if item.info.source.registry is None:
                    options.reporter.error("no source registry for %s", item.name)
                    return None
                source_path = Path(item.info.source.registry) / wheel_filename
                action = make_action(
                        download=Download.NONE,
                        source_path=source_path,
                        wheel_name=wheel_filename,
                        )
            else:
                # file to be downloaded
                wheel_filename = Path(urlparse(wheel.url).path).name
                download = Download.WHEEL
                url = wheel.url
                action = make_action(
                        download=download,
                        url=url,
                        wheel_name=wheel_filename,
                        wheel_size=wheel.size,
                        wheel_hash=wheel.hash,
                        )
            return action
        else:
            logger.info(
                    "None of the available wheels for %s were usable – trying to build",
                    item.name)
    
    if item.info is not None and item.info.source is not None:
        # try finding a wheel in an editable project
        if item.info.source.virtual:
            # virtual packages probably have to be ignored …
            return None
        if item.info.source.editable:
            logger.debug("package %s is editable", item.name)
            edit_path = options.base_dir / item.info.source.editable
            if (dist_path := edit_path / "dist").exists():
                for dist_name in dist_path.glob("*.whl"):
                    # check all wheels in the project/dist/ directory
                    # (they can accumulate there over time)
                    parsed_dist_name = parse_wheel_filename(dist_name.name)
                    dist_project = parsed_dist_name.project.replace("_", "-")
                    if (dist_project != item.name or
                            parsed_dist_name.version != item.version):
                        continue
                    m = options.matcher.match_parsed_filename(parsed_dist_name)
                    if m is None:
                        # the wheel seems unusable
                        continue
                    wheel_name = dist_name.name
                    action = make_action(
                            download=Download.NONE,
                            source_path=dist_name,
                            wheel_name=wheel_name,
                            )
                    return action
    
    if item.info is not None and item.info.sdist is not None:
        # try to download a source archive and build from it
        sdist = item.info.sdist
        if sdist.url is None or sdist.hash is None or sdist.size is None:
            options.reporter.error("cannot build package %s, no sdist", item.name)
            return None
        action = make_action(
                download=Download.SDIST,
                url=sdist.url,
                wheel_hash=sdist.hash,
                wheel_size=sdist.size,
                )
        return action
    
    options.reporter.error("no way to satisfy requirement for %s (%s)",
            item.name, item.version)
    return None


def get_installed_packages(
        lockfile_dir: Path,
        reporter: Reporter,
        ) -> list[PackageListItem]:
    """Returns a list of PackageListItem objects for installed packages."""
    try:
        r = subprocess.run(
                ["uv", "export", "--project", str(lockfile_dir)],
                capture_output=True,
                check=True,
                )
    except subprocess.CalledProcessError:
        reporter.error("could not list installed modules")
        raise ValueError("could not list installed modules")
    
    platform_info = dict(
            implementation_name=platform.python_implementation(),
            os_name=os.name,
            platform_machine=platform.machine(),
            platform_python_implementation=platform.python_implementation(),
            python_full_version=f"{sys.version_info.major}.{sys.version_info.minor}",
            sys_platform=sys.platform,
            # what else??
            )
    
    result: list[PackageListItem] = []
    for line in r.stdout.decode().splitlines():
        pkg: PackageListItem | None = None
        if line.startswith(" "):
            continue
        elif line.startswith("-e"):
            option, path = line.split()
            base = lockfile_dir / path
            if (pyp_path := base / "pyproject.toml").exists():
                logger.debug("found editable installation at %s", base)
                pyp = msgspec.toml.decode(pyp_path.read_bytes())
                try:
                    name = pyp["project"]["name"]
                    version = pyp["project"]["version"]
                except KeyError:
                    reporter.error(
                            "project information not found in %s",
                            str(pyp_path),
                            )
                    continue
                pkg = PackageListItem(name=name, version=version)
            else:
                logger.warning("pyproject.toml not found at %s", base)
        elif line.strip().startswith("#"):
            continue
        else:
            raw_spec = line.strip().rstrip("\\").strip()
            if ";" in raw_spec:
                ver_spec, cond = raw_spec.split(";", 1)
                # if not eval(cond, None, platform_info):
                #     continue
            else:
                ver_spec = raw_spec
            spec = ver_spec.split()[0]
            logger.debug("found dependency on %s", spec)
            if "==" not in spec:
                logger.error("unrecognized version spec “%s”", spec)
                continue
            name, version = spec.split("==")
            pkg = PackageListItem(name=name, version=version)
        if pkg is not None:
            result.append(pkg)
    
    return result


def get_lockfile_data(
        lockfile_dir: Path,
        reporter: Reporter,
        ) -> UvLockfile:
    """Reads a uv lockfile and returns important information."""
    lf_path = lockfile_dir / "uv.lock"
    lf_data = msgspec.toml.decode(lf_path.read_bytes(), type=UvLockfile)
    if lf_data.version > 1:
        reporter.warning("incompatible version %s of uv lockfile found")
        # try carrying on regardless
    
    return lf_data


def get_locklist(
        lockfile_dir: Path,
        reporter: Reporter,
        ) -> list[PackageListItem]:
    """Gets a list of extended information on installed packages."""
    lf_data = get_lockfile_data(lockfile_dir, reporter=reporter)
    
    pkg_dict = {pkg.name: pkg for pkg in lf_data.package}
    
    pkg_list = get_installed_packages(lockfile_dir, reporter=reporter)
    for pkg in pkg_list:
        pkg.info = pkg_dict.get(pkg.name)
        if pkg.info is None:
            reporter.warning("package %s not found in lockfile", pkg.name)
        # we shouldn't experience KeyError here as lockfile and list of
        # installed packages come from the same source – but it happens
    
    return pkg_list
