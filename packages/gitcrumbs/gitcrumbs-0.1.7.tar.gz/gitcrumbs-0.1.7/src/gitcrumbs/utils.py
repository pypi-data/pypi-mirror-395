from __future__ import annotations
import os
import json
import sqlite3
import subprocess
import hashlib
import sys
import time
import tempfile
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# -------- Exceptions --------
class ShellError(RuntimeError):
    ...


class NotAGitRepo(RuntimeError):
    ...


class BareRepoUnsupported(RuntimeError):
    ...


class PathOutsideRepo(ValueError):
    ...


class SnapshotNotFound(RuntimeError):
    ...


# -------- Shell helpers --------
def run_git(
    repo: Path,
    *args: str,
    check: bool = True,
    text: bool = True,
) -> str:
    cmd = ["git", "-C", str(repo), *args]
    p = subprocess.run(cmd, capture_output=True, text=text)
    if check and p.returncode != 0:
        raise ShellError(f"git {' '.join(args)} failed:\n{p.stderr}")
    return p.stdout


def try_git(repo: Path, *args: str) -> tuple[str, int, str]:
    p = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )
    return p.stdout, p.returncode, p.stderr


def try_git_bytes(repo: Path, *args: str) -> tuple[bytes, int, bytes]:
    """
    Run a git command and return raw bytes for stdout/stderr.

    Used for commands that may emit binary data (e.g., 'git cat-file blob'),
    to avoid Windows console decoding issues when text=True.
    """
    p = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=False,
    )
    return p.stdout, p.returncode, p.stderr


# -------- Repo discovery & safety --------
def ensure_repo_root(cwd: Optional[Path] = None) -> Path:
    cwd = Path.cwd() if cwd is None else Path(cwd)
    out, rc, _ = try_git(cwd, "rev-parse", "--show-toplevel")
    if rc != 0 or not out.strip():
        raise NotAGitRepo("Not inside a Git working tree.")
    root = Path(out.strip())
    bare, rc2, _ = try_git(root, "rev-parse", "--is-bare-repository")
    if rc2 == 0 and bare.strip() == "true":
        raise BareRepoUnsupported(
            "Bare repositories are not supported (no working tree).")
    return root


def git_dir(repo: Path) -> Path:
    out = run_git(repo, "rev-parse", "--git-dir").strip()
    return (repo / out).resolve()


def state_dir(repo: Path) -> Path:
    d = git_dir(repo) / "gitcrumbs"
    d.mkdir(parents=True, exist_ok=True)
    return d


def db_path(repo: Path) -> Path:
    return state_dir(repo) / "gitcrumbs.db"


def tracker_state_path(repo: Path) -> Path:
    return state_dir(repo) / "tracker_state.json"


def restore_lock_path(repo: Path) -> Path:
    return state_dir(repo) / "restore.lock"


def index_locked(repo: Path) -> bool:
    return (git_dir(repo) / "index.lock").exists()


def in_merge_or_rebase(repo: Path) -> bool:
    g = git_dir(repo)
    return any((g / p).exists()
               for p in ["MERGE_HEAD", "rebase-merge", "rebase-apply"])


# -------- SQLite --------
def connect_db(repo: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path(repo))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS snapshot (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      branch TEXT,
      head_commit TEXT,
      summary TEXT,
      restored_from_snapshot_id INTEGER NULL,
      user_label TEXT UNIQUE,
      FOREIGN KEY(restored_from_snapshot_id) REFERENCES snapshot(id)
    );

    CREATE TABLE IF NOT EXISTS file_state (
      snapshot_id INTEGER,
      path TEXT,
      status TEXT,            -- 'T' tracked, 'U' untracked, 'D' deleted
      blob_sha TEXT,          -- git object id for content at snapshot time (if applicable)
      size INTEGER NULL,
      mtime INTEGER NULL,
      PRIMARY KEY(snapshot_id, path),
      FOREIGN KEY(snapshot_id) REFERENCES snapshot(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS meta (
      key TEXT PRIMARY KEY,
      value TEXT
    );
    """)

    # Migration: for pre-existing DBs without user_label column.
    try:
        conn.execute("ALTER TABLE snapshot ADD COLUMN user_label TEXT;")
    except sqlite3.OperationalError:
        # Column already exists, safe to ignore.
        pass

    conn.commit()


# -------- JSON tracker state --------
def atomic_write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path)


def load_tracker_state(repo: Path) -> dict:
    p = tracker_state_path(repo)
    default = {
        "baseline_fingerprint": None,
        "baseline_snapshot_id": None,
        "suppress_until_change": False,
        "restored_from_snapshot_id": None,
        "last_seen_fingerprint": None,
        "last_seen_time": None,
    }
    if not p.exists():
        return dict(default)
    try:
        return json.loads(p.read_text())
    except Exception:
        return dict(default)


# -------- Git state helpers --------
def current_branch_and_head(repo: Path) -> tuple[str, str]:
    b_out, b_rc, _ = try_git(repo, "symbolic-ref", "--quiet", "--short",
                             "HEAD")
    branch = b_out.strip() if b_rc == 0 and b_out.strip() else "DETACHED"
    h_out, h_rc, _ = try_git(repo, "rev-parse", "--verify", "HEAD")
    head = h_out.strip() if h_rc == 0 and h_out.strip() else "UNBORN"
    return branch, head


# -------- Manifest & fingerprint --------
def compute_manifest(
        repo: Path) -> Tuple[Dict[str, Tuple[str, str, int, int]], List[str]]:
    manifest: Dict[str, Tuple[str, str, int, int]] = {}

    # Tracked from index
    ls = run_git(repo, "ls-files", "-s", "-z")
    items = [x for x in ls.split("\0") if x]
    for ent in items:
        try:
            head, path = ent.split("\t", 1)
            parts = head.split()
            blob = parts[1]
            p = repo / path
            try:
                st = p.stat()
                size, mtime = st.st_size, int(st.st_mtime)
            except FileNotFoundError:
                size, mtime = 0, 0
            manifest[path] = ("T", blob, size, mtime)
        except Exception:
            continue

    # Unstaged modifications
    diff_files = run_git(repo, "diff-files", "--name-only", "-z")
    for path in [x for x in diff_files.split("\0") if x]:
        p = repo / path
        if p.exists():
            blob = run_git(repo, "hash-object", "-w", "--", path).strip()
            st = p.stat()
            manifest[path] = ("T", blob, st.st_size, int(st.st_mtime))
        else:
            manifest[path] = ("D", "DELETED", 0, 0)

    # Tracked deletions
    deleted = run_git(repo, "ls-files", "-d", "-z")
    for path in [x for x in deleted.split("\0") if x]:
        manifest[path] = ("D", "DELETED", 0, 0)

    # Untracked (exclude ignored)
    untracked = run_git(repo, "ls-files", "-o", "--exclude-standard", "-z")
    for path in [x for x in untracked.split("\0") if x]:
        p = repo / path
        if p.is_file():
            try:
                blob = run_git(repo, "hash-object", "-w", "--", path).strip()
                st = p.stat()
                manifest[path] = ("U", blob, st.st_size, int(st.st_mtime))
            except ShellError:
                try:
                    st = p.stat()
                    manifest[path] = ("U", "UNHASHED", st.st_size,
                                      int(st.st_mtime))
                except FileNotFoundError:
                    pass
        elif p.is_symlink():
            try:
                target = os.readlink(p)
                blob = hashlib.sha256(
                    ("SYMLINK->" + target).encode()).hexdigest()
                st = p.lstat()
                manifest[path] = ("U", blob, st.st_size, int(st.st_mtime))
            except OSError:
                pass

    order = sorted(manifest.keys())
    return manifest, order


def compute_fingerprint(repo: Path) -> str:
    branch, head = current_branch_and_head(repo)
    manifest, order = compute_manifest(repo)
    lines: List[str] = [f"branch={branch}", f"head={head}"]
    for path in order:
        status, blob, size, mtime = manifest[path]
        if status == "T" or status == "D":
            lines.append(f"{status}|{path}|{blob}")
        else:  # 'U'
            lines.append(f"{status}|{path}|{blob}|{size}|{mtime}")
    data = ("\n".join(lines)).encode()
    return hashlib.sha256(data).hexdigest()


# -------- Snapshot ops --------
def create_snapshot(
    repo: Path,
    restored_from_snapshot_id: Optional[int] = None,
) -> int:
    conn = connect_db(repo)
    init_schema(conn)
    branch, head = current_branch_and_head(repo)
    manifest, order = compute_manifest(repo)
    mods = sum(1 for p in order if manifest[p][0] == "T")
    adds = sum(1 for p in order if manifest[p][0] == "U")
    dels = sum(1 for p in order if manifest[p][0] == "D")
    summary = f"{adds} added, {mods} tracked/modified, {dels} deleted"
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO snapshot(branch, head_commit, summary, restored_from_snapshot_id)
        VALUES(?,?,?,?)
        """,
        (branch, head, summary, restored_from_snapshot_id),
    )
    snap_id = int(cur.lastrowid)
    if order:
        rows = []
        for path in order:
            status, blob, size, mtime = manifest[path]
            rows.append((snap_id, path, status, blob, size, mtime))
        cur.executemany(
            """
            INSERT INTO file_state(snapshot_id, path, status, blob_sha, size, mtime)
            VALUES(?,?,?,?,?,?)
            """,
            rows,
        )
    conn.commit()
    conn.close()
    return snap_id


def list_snapshots(repo: Path):
    conn = connect_db(repo)
    init_schema(conn)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, created_at, branch, summary, restored_from_snapshot_id, user_label
        FROM snapshot
        ORDER BY id ASC
        """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_snapshot_manifest(repo: Path, snap_id: int):
    conn = connect_db(repo)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT path, status, blob_sha, size, mtime
        FROM file_state
        WHERE snapshot_id=?
        """,
        (snap_id, ),
    )
    out: Dict[str, Tuple[str, str, int, int]] = {}
    for path, status, blob, size, mtime in cur.fetchall():
        out[path] = (
            status,
            blob,
            size if size is not None else 0,
            mtime if mtime is not None else 0,
        )
    conn.close()
    return out


def branch_exists(repo: Path, name: str) -> bool:
    out, rc, _ = try_git(repo, "show-ref", "--verify", f"refs/heads/{name}")
    return rc == 0


def restore_snapshot(repo: Path, snap_id: int, purge: bool = False) -> None:
    lock = restore_lock_path(repo)
    try:
        lock.write_text(str(time.time()))
    except Exception:
        pass
    try:
        conn = connect_db(repo)
        cur = conn.cursor()
        cur.execute("SELECT branch, head_commit FROM snapshot WHERE id=?",
                    (snap_id, ))
        row = cur.fetchone()
        conn.close()
        if not row:
            raise RuntimeError(f"Snapshot {snap_id} not found")
        branch, head = row
        if head != "UNBORN":
            if branch != "DETACHED" and branch_exists(repo, branch):
                try_git(repo, "checkout", branch)
            else:
                try_git(repo, "checkout", "--detach", head)
        manifest = get_snapshot_manifest(repo, snap_id)
        wanted_paths = set(manifest.keys())
        for path, (status, blob, _, _) in manifest.items():
            p = repo / path
            p.parent.mkdir(parents=True, exist_ok=True)
            if status == "D":
                try:
                    if p.exists():
                        p.unlink()
                except Exception:
                    pass
                continue
            if blob in ("UNHASHED", "DELETED"):
                continue
            out, rc, err = try_git_bytes(repo, "cat-file", "blob", blob)
            if rc != 0:
                try:
                    note = p.with_suffix(p.suffix + ".gitcrumbs.missing")
                    err_text = err.decode("utf-8", errors="replace")
                    note.write_text(f"Missing blob {blob}\n{err_text}")
                except Exception:
                    pass
                continue
            tmp = p.with_suffix(p.suffix + ".gitcrumbs.tmp")
            tmp.write_bytes(out)
            tmp.replace(p)
        if purge:
            for root, dirs, files in os.walk(repo):
                if ".git" in dirs:
                    dirs.remove(".git")
                for f in files:
                    rel = str(Path(root, f).relative_to(repo))
                    if rel not in wanted_paths:
                        try:
                            (repo / rel).unlink()
                        except Exception:
                            pass
    finally:
        try:
            if lock.exists():
                lock.unlink()
        except Exception:
            pass


# -------- Path normalization helpers --------
def _is_subpath(child: Path, parent: Path) -> bool:
    try:
        child_resolved = child.resolve()
        parent_resolved = parent.resolve()
    except FileNotFoundError:
        child_resolved = child.absolute()
        parent_resolved = parent.absolute()
    try:
        child_resolved.relative_to(parent_resolved)
        return True
    except Exception:
        return False


def normalize_snapshot_path_arg(repo: Path, user_path: Path) -> str:
    repo = repo.resolve()
    if user_path.is_absolute():
        up = user_path
        if not _is_subpath(up, repo):
            raise PathOutsideRepo(
                f"Path '{user_path}' is outside the repository ({repo}).")
        rel = up.resolve().relative_to(repo)
        return rel.as_posix()
    else:
        candidate = (repo / user_path).resolve()
        if not _is_subpath(candidate, repo):
            raise PathOutsideRepo(
                f"Path '{user_path}' escapes the repository root ({repo}).")
        rel = candidate.relative_to(repo)
        return rel.as_posix()


# -------- Diff helpers --------
def _write_blob_to_temp(repo: Path, blob: Optional[str]) -> str:
    fd, path = tempfile.mkstemp(prefix="gitcrumbs_", suffix=".tmp")
    os.close(fd)
    if blob is None:
        return path
    out, rc, err = try_git_bytes(repo, "cat-file", "blob", blob)
    if rc != 0:
        err_text = err.decode("utf-8", errors="ignore")
        with open(path, "w", encoding="utf-8", errors="ignore") as f:
            f.write(f"[gitcrumbs] failed to read blob {blob}:\n{err_text}")
        return path
    with open(path, "wb") as f:
        f.write(out)
    return path


def _diff_two_files(path_a: str, path_b: str, label_a: str,
                    label_b: str) -> str:
    cmd = ["git", "diff", "--no-index", "--binary", "--", path_a, path_b]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode not in (0, 1):
        return f"[gitcrumbs] git diff failed:\n{p.stderr}"
    patch = p.stdout.replace(path_a, label_a).replace(path_b, label_b)
    return patch or "(no differences)\n"


def compute_diff_sets(repo: Path, a: int,
                      b: int) -> Tuple[List[str], List[str], List[str]]:
    A = get_snapshot_manifest(repo, a)
    B = get_snapshot_manifest(repo, b)
    setA, setB = set(A.keys()), set(B.keys())
    added = sorted(list(setB - setA))
    deleted = sorted(list(setA - setB))
    modified: List[str] = []
    for p in sorted(setA & setB):
        if A[p][0] != B[p][0] or A[p][1] != B[p][1]:
            modified.append(p)
    return added, deleted, modified


def patch_for_file_between_snapshots(
    repo: Path,
    a: int,
    b: int,
    path_arg: str | Path,
) -> Tuple[str, Optional[str]]:
    rel_path = normalize_snapshot_path_arg(repo, Path(path_arg))
    A = get_snapshot_manifest(repo, a)
    B = get_snapshot_manifest(repo, b)
    a_entry = A.get(rel_path)
    b_entry = B.get(rel_path)

    def blob_from(entry):
        if entry is None:
            return None
        status, blob, *_ = entry
        if status == "D":
            return None
        if blob in ("UNHASHED", "DELETED"):
            return blob
        return blob

    blob_a = blob_from(a_entry)
    blob_b = blob_from(b_entry)
    if blob_a == "UNHASHED" or blob_b == "UNHASHED":
        return (
            "",
            f"{rel_path}: cannot produce a content diff because one side is UNHASHED "
            "(untracked or unreadable during snapshot).",
        )
    path_a = _write_blob_to_temp(repo, blob_a)
    path_b = _write_blob_to_temp(repo, blob_b)
    try:
        label_a = (f"snapshot:{a}:{rel_path}"
                   if blob_a is not None else f"snapshot:{a}:/dev/null")
        label_b = (f"snapshot:{b}:{rel_path}"
                   if blob_b is not None else f"snapshot:{b}:/dev/null")
        patch = _diff_two_files(path_a, path_b, label_a, label_b)
        return patch, None
    finally:
        for p in (path_a, path_b):
            try:
                os.remove(p)
            except OSError:
                pass


# -------- Snapshot-on-demand before navigation --------
def maybe_snapshot_current_state(repo: Path) -> Optional[int]:
    """If the working tree differs from the last baseline fingerprint, create a snapshot.
    Returns the new snapshot id, or None if no snapshot was created.
    Skips snapshotting during restore/merge/rebase or when the index is locked.
    """
    if restore_lock_path(repo).exists() or index_locked(
            repo) or in_merge_or_rebase(repo):
        return None
    fp = compute_fingerprint(repo)
    state = load_tracker_state(repo)
    if state.get("baseline_fingerprint") != fp:
        snap_id = create_snapshot(
            repo,
            restored_from_snapshot_id=state.get("restored_from_snapshot_id"),
        )
        state.update({
            "baseline_fingerprint": fp,
            "baseline_snapshot_id": snap_id,
            "suppress_until_change": False,
            "restored_from_snapshot_id": None,
            "last_seen_fingerprint": fp,
            "last_seen_time": time.time(),
        })
        atomic_write_json(tracker_state_path(repo), state)
        return snap_id
    return None


def write_file_to_stdout(snap_id: int, file_path: Path):
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise e

    try:
        rel = normalize_snapshot_path_arg(repo, file_path)
    except PathOutsideRepo as pe:
        print(str(pe))
        raise pe

    manifest = get_snapshot_manifest(repo, snap_id)
    entry: Optional[tuple[str, str, int, int]] = manifest.get(rel)
    if entry is None:
        # file absent in this snapshot (e.g., Added in the other side)
        # print nothing, exit so the caller can treat as empty
        return

    status, blob, *_ = entry
    if status == "D":
        # deleted in this snapshot -> empty content
        return

    if blob in ("UNHASHED", "DELETED"):
        # captured as unreadable/unhashed, treat as empty
        return

    out, rc, _ = try_git_bytes(repo, "cat-file", "blob", blob)
    if rc != 0:
        # could not read object -> empty
        return

    # Write bytes as-is; Typer/print would coerce/escape
    if isinstance(out, bytes):
        sys.stdout.buffer.write(out)
    else:
        sys.stdout.write(out)


def resolve_snapshot_id(repo: Path, id_or_label: str | int) -> int:
    """
    Map a user-facing snapshot identifier (numeric ID or user_label)
    to the underlying numeric snapshot.id.
    """
    conn = connect_db(repo)
    init_schema(conn)
    cur = conn.cursor()

    # Try numeric ID first if it looks like an integer
    value: Optional[int] = None
    if isinstance(id_or_label, int):
        value = id_or_label
    elif isinstance(id_or_label, str) and id_or_label.isdigit():
        value = int(id_or_label)

    if value is not None:
        cur.execute("SELECT id FROM snapshot WHERE id = ?", (value, ))
        row = cur.fetchone()
        if row:
            conn.close()
            return int(row[0])

    # Fallback: treat it as a label
    label = str(id_or_label)
    cur.execute("SELECT id FROM snapshot WHERE user_label = ?", (label, ))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise SnapshotNotFound(f"Snapshot '{id_or_label}' does not exist.")
    return int(row[0])


def rename_snapshot(repo: Path, snap_id: int, new_label: str) -> None:
    """Assign or update the user_label for a snapshot."""
    conn = connect_db(repo)
    init_schema(conn)
    cur = conn.cursor()

    # Ensure snapshot exists
    cur.execute("SELECT id FROM snapshot WHERE id = ?", (snap_id, ))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise SnapshotNotFound(f"Snapshot {snap_id} does not exist.")

    # Ensure label isn't used by some other snapshot
    if new_label.isnumeric():
        cur.execute("SELECT id FROM snapshot WHERE id = ?", (int(new_label), ))
        existingID = cur.fetchone()
    else:
        existingID = None
    cur.execute("SELECT id FROM snapshot WHERE user_label = ?", (new_label, ))
    existingLabel = cur.fetchone()
    if (existingID
            and existingID[0] != snap_id) or (existingLabel
                                              and existingLabel[0] != snap_id):
        conn.close()
        raise ValueError(f"Snapshot name '{new_label}' is already in use.")

    cur.execute(
        "UPDATE snapshot SET user_label = ? WHERE id = ?",
        (new_label, snap_id),
    )
    conn.commit()
    conn.close()
