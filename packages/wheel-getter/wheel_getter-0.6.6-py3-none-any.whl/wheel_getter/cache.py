import datetime
from pathlib import Path
import sqlite3
import xdg_base_dirs

from .checksums import get_checksum


APP_NAME = "wheel-getter"
CACHE_DB = xdg_base_dirs.xdg_cache_home() / APP_NAME / "downloads.db"
WHEEL_DIR = xdg_base_dirs.xdg_cache_home() / APP_NAME / "wheels"
SDIST_DIR = xdg_base_dirs.xdg_cache_home() / APP_NAME / "sdists"


class CacheDatabase:
    def __init__(self) -> None:
        WHEEL_DIR.mkdir(parents=True, exist_ok=True)
        SDIST_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_DB.parent.mkdir(parents=True, exist_ok=True)
        
        if not CACHE_DB.exists():
            con = sqlite3.connect(CACHE_DB, detect_types=sqlite3.PARSE_DECLTYPES)
            con.execute("CREATE TABLE wheel ("
                    "name TEXT PRIMARY KEY, "
                    "downloaded DATETIME, "
                    "last_used DATETIME, "
                    "uri TEXT, "
                    "size INTEGER, "
                    "hash TEXT)")  # no comma after last column!
            con.execute("CREATE TABLE sdist ("
                    "name TEXT PRIMARY KEY, "
                    "downloaded DATETIME, "
                    "last_used DATETIME, "
                    "uri TEXT)")  # no comma after last column!
            con.commit()
        else:
            con = sqlite3.connect(CACHE_DB, detect_types=sqlite3.PARSE_DECLTYPES)
        self.con = con
    
    def close(self) -> None:
        self.con.close()
    
    def find_wheel(self,
            name: str,
            size: int,
            hash: str,
            ) -> Path | None:
        wheel_path = WHEEL_DIR / name
        now = datetime.datetime.now(datetime.UTC).isoformat()
        # XXX look for wheel, size and hash in database
        if wheel_path.exists():
            self.con.execute(
                    "UPDATE wheel SET last_used = ? WHERE name = ?",
                    (now, name),
                    )
            self.con.commit()
            return wheel_path
        return None
    
    def find_sdist(self,
            name: str,
            ) -> Path | None:
        sdist_path = SDIST_DIR / name
        now = datetime.datetime.now(datetime.UTC).isoformat()
        # XXX look for sdist in database?
        if sdist_path.exists():
            self.con.execute(
                    "UPDATE sdist SET last_used = ? WHERE name = ?",
                    (now, name),
                    )
            self.con.commit()
            return sdist_path
        return None
    
    def add_wheel(self, name, data, uri) -> Path:
        wheel_path = WHEEL_DIR / name
        wheel_size = len(data)
        wheel_hash = get_checksum(data)
        wheel_path.write_bytes(data)
        now = datetime.datetime.now(datetime.UTC).isoformat()
        self.con.execute(
                "INSERT OR REPLACE INTO wheel ("
                "name, downloaded, last_used, uri, size, hash"
                ") VALUES (?, ?, ?, ?, ?, ?)",
                (name, now, now, uri, wheel_size, wheel_hash),
                )
        self.con.commit()
        return wheel_path
    
    def add_sdist(self, name, data, uri) -> Path:
        sdist_path = SDIST_DIR / name
        sdist_path.write_bytes(data)
        now = datetime.datetime.now(datetime.UTC).isoformat()
        self.con.execute(
                "INSERT OR REPLACE INTO sdist ("
                "name, downloaded, last_used, uri"
                ") VALUES (?, ?, ?, ?)",
                (name, now, now, uri),
                )
        self.con.commit()
        return sdist_path
    
    def purge(self, min_days=30) -> None:
        now = datetime.datetime.now(datetime.UTC)
        oldest = (now - datetime.timedelta(days=min_days)).isoformat()
        
        # purge wheels
        cur = self.con.execute("SELECT name FROM wheel WHERE last_used < ?", oldest)
        for name in cur.fetchmany():
            (WHEEL_DIR / name).unlink(missing_ok=True)
            self.con.execute("DELETE FROM wheel WHERE name = ?", name)
        
        # purge sdists
        cur = self.con.execute("SELECT name FROM sdist WHERE last_used < ?", oldest)
        for name in cur.fetchmany():
            (SDIST_DIR / name).unlink(missing_ok=True)
            self.con.execute("DELETE FROM sdist WHERE name = ?", name)
