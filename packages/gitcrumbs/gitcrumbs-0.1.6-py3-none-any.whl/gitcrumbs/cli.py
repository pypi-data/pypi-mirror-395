from __future__ import annotations
import os
import shutil
import time
from pathlib import Path
import typer
from typing import Optional
from rich.table import Table
from rich import print as rprint
from rich.markup import escape

from gitcrumbs import __version__
from gitcrumbs.utils import (
    ensure_repo_root,
    connect_db,
    init_schema,
    create_snapshot,
    list_snapshots,
    compute_fingerprint,
    load_tracker_state,
    atomic_write_json,
    restore_snapshot,
    NotAGitRepo,
    BareRepoUnsupported,
    index_locked,
    in_merge_or_rebase,
    restore_lock_path,
    state_dir,
    compute_diff_sets,
    patch_for_file_between_snapshots,
    normalize_snapshot_path_arg,
    PathOutsideRepo,
    maybe_snapshot_current_state,
    write_file_to_stdout,
    resolve_snapshot_id,
    rename_snapshot,
    SnapshotNotFound,
)

app = typer.Typer(
    help=("gitcrumbs — record durable working-tree snapshots for a Git repo, "
          "list/diff/restore them, and auto-track stable changes."))


def _anchor_after_restore(repo: Path, snap_id: int):
    fp = compute_fingerprint(repo)
    state = load_tracker_state(repo)
    state.update({
        "baseline_fingerprint": fp,
        "baseline_snapshot_id": snap_id,
        "suppress_until_change": True,
        "restored_from_snapshot_id": snap_id,
        "last_seen_fingerprint": fp,
        "last_seen_time": time.time(),
    })
    atomic_write_json(Path(repo / ".git/gitcrumbs/tracker_state.json"), state)


def _ordered_snapshot_ids(repo: Path):
    rows = list_snapshots(repo)
    return [sid for (sid, *_rest) in rows]


def _render_patch_colored(patch: str) -> None:
    for line in patch.splitlines():
        esc = escape(line)
        if line.startswith("@@"):
            rprint(f"[cyan]{esc}[/cyan]")
        elif line.startswith("+++") or line.startswith("---"):
            rprint(f"[bold]{esc}[/bold]")
        elif line.startswith("+"):
            rprint(f"[green]{esc}[/green]")
        elif line.startswith("-"):
            rprint(f"[red]{esc}[/red]")
        else:
            rprint(esc)


@app.command(help="Initialize .git/gitcrumbs/ (creates SQLite DB and config).")
def init():
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)
    conn = connect_db(repo)
    init_schema(conn)
    conn.close()
    print(f"Initialized gitcrumbs at {repo} (.git/gitcrumbs)")


@app.command(help="Create a snapshot of the current working state (manual).")
def snapshot():
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)
    snap_id = create_snapshot(repo)
    fp = compute_fingerprint(repo)
    state = load_tracker_state(repo)
    state.update({
        "baseline_fingerprint": fp,
        "baseline_snapshot_id": snap_id,
        "suppress_until_change": False,
        "restored_from_snapshot_id": None,
        "last_seen_fingerprint": fp,
        "last_seen_time": time.time(),
    })
    atomic_write_json(Path(repo / ".git/gitcrumbs/tracker_state.json"), state)
    print(f"Snapshot created: {snap_id}")


@app.command(help="Show all snapshots with summary info (chronological).")
def timeline():
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)
    rows = list_snapshots(repo)
    if not rows:
        print("No snapshots yet.")
        raise typer.Exit(0)

    # # = numeric ID (stable internal), Label = optional user label
    t = Table("#", "Label", "Created", "Branch", "Summary", "Resumed-From")
    for sid, created, branch, summary, restored_from, user_label in rows:
        display_id = user_label or str(sid)
        t.add_row(
            str(sid),
            display_id,
            created,
            branch or "?",
            summary or "",
            str(restored_from) if restored_from else "",
        )
    rprint(t)


@app.command(
    help="Show tracker status and the current snapshot cursor (baseline).")
def status():
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)
    rows = list_snapshots(repo)
    last = rows[-1] if rows else None
    state = load_tracker_state(repo)
    print(f"Repo: {repo}")
    print(f"Last snapshot: {last[0] if last else 'None'}")
    print(f"Tracker baseline set: {bool(state.get('baseline_fingerprint'))}")
    print(f"Suppress-until-change: {state.get('suppress_until_change')}")
    print(f"Cursor snapshot id: {state.get('baseline_snapshot_id')}")


def _snapshot_if_dirty(repo: Path):
    snap = maybe_snapshot_current_state(repo)
    if snap is not None:
        print(f"Created snapshot {snap} for unrecorded changes.")


@app.command(
    help="Compare two snapshots. With --file-path, emit a patch for that file."
)
def diff(
    a: str = typer.Argument(..., help="First snapshot ID or label."),
    b: str = typer.Argument(..., help="Second snapshot ID or label."),
    file_path: Path = typer.Option(
        None,
        "--file-path",
        "-f",
        help="Path to a file to show its patch between snapshots A and B.",
    ),
    all: bool = typer.Option(
        False,
        "--all",
        help=("Show all file names in the summary "
              "(ignored if --file-path is provided)."),
    ),
):
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)

    try:
        a_id = resolve_snapshot_id(repo, a)
        b_id = resolve_snapshot_id(repo, b)
    except SnapshotNotFound as e:
        print(str(e))
        raise typer.Exit(2)

    if file_path is not None:
        try:
            normalized = normalize_snapshot_path_arg(repo, file_path)
        except PathOutsideRepo as pe:
            print(str(pe))
            raise typer.Exit(2)

        patch, warn = patch_for_file_between_snapshots(repo, a_id, b_id,
                                                       normalized)
        if warn:
            print(warn)
            raise typer.Exit(0)
        _render_patch_colored(patch)
        return

    added, deleted, modified = compute_diff_sets(repo, a_id, b_id)
    header = "Files" if all else "Files (first 5 shown)"
    t = Table("Category", "Count", header)

    def show(lst):
        return ", ".join(lst) if all else ", ".join(lst[:5])

    t.add_row(
        "[green]Added[/green]",
        str(len(added)),
        show(added),
        style="green",
    )
    t.add_row(
        "[red]Deleted[/red]",
        str(len(deleted)),
        show(deleted),
        style="red",
    )
    t.add_row(
        "[yellow]Modified[/yellow]",
        str(len(modified)),
        show(modified),
        style="yellow",
    )
    rprint(t)


@app.command(
    help="Restore to a specific snapshot (purges extra files by default).")
def restore(
    snap: str = typer.Argument(
        ...,
        help="Snapshot ID or label to restore to.",
    ),
    purge: bool = typer.Option(
        False,
        "--purge/--no-purge",
        help="Delete files not in the snapshot (default: purge).",
        show_default=True,
    ),
):
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)

    _snapshot_if_dirty(repo)

    try:
        snap_id = resolve_snapshot_id(repo, snap)
    except SnapshotNotFound as e:
        print(str(e))
        raise typer.Exit(2)

    if index_locked(repo):
        print(
            "Index appears locked (ongoing Git operation). Skipping restore.")
        raise typer.Exit(3)

    restore_snapshot(repo, snap_id, purge=purge)
    _anchor_after_restore(repo, snap_id)
    print(f"Restored snapshot {snap_id}. (purge={'on' if purge else 'off'}) "
          "Anchored; next durable change will create a new latest snapshot.")


# Navigation helpers ---------------------------------------------------------
@app.command(
    help="Restore the next snapshot after the current cursor (alias: n).")
def next(purge: bool = typer.Option(
    False,
    "--purge/--no-purge",
    help="Delete files not in the target snapshot (default: purge).",
    show_default=True,
), ):
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)

    _snapshot_if_dirty(repo)

    ids = _ordered_snapshot_ids(repo)
    if not ids:
        print("No snapshots yet.")
        raise typer.Exit(1)

    state = load_tracker_state(repo)
    cur = state.get("baseline_snapshot_id")

    target: Optional[int] = None
    if cur is None:
        target = ids[0]
    else:
        try:
            idx = ids.index(cur)
            target = ids[idx + 1] if idx + 1 < len(ids) else None
        except ValueError:
            greater = [i for i in ids if i > cur]
            target = greater[0] if greater else None

    if target is None:
        print("Already at the latest snapshot; no next snapshot available.")
        raise typer.Exit(0)

    if index_locked(repo):
        print(
            "Index appears locked (ongoing Git operation). Skipping restore.")
    else:
        restore_snapshot(repo, target, purge=purge)
        _anchor_after_restore(repo, target)
        print(
            f"Restored snapshot {target}. (purge={'on' if purge else 'off'})")


@app.command(name="n", hidden=True)
def _next_alias(purge: bool = typer.Option(
    False,
    "--purge/--no-purge",
    help="Delete files not in the target snapshot (default: purge).",
    show_default=True,
), ):
    return next(purge=purge)


@app.command(
    help="Restore the previous snapshot before the current cursor (alias: p).")
def previous(purge: bool = typer.Option(
    False,
    "--purge/--no-purge",
    help="Delete files not in the target snapshot (default: purge).",
    show_default=True,
), ):
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)

    _snapshot_if_dirty(repo)

    ids = _ordered_snapshot_ids(repo)
    if not ids:
        print("No snapshots yet.")
        raise typer.Exit(1)

    state = load_tracker_state(repo)
    cur = state.get("baseline_snapshot_id")

    target: Optional[int] = None
    if cur is None:
        target = ids[-1]
    else:
        try:
            idx = ids.index(cur)
            target = ids[idx - 1] if idx - 1 >= 0 else None
        except ValueError:
            smaller = [i for i in ids if i < cur]
            target = smaller[-1] if smaller else None

    if target is None:
        print(
            "Already at the earliest snapshot; no previous snapshot available."
        )
        raise typer.Exit(0)

    if index_locked(repo):
        print(
            "Index appears locked (ongoing Git operation). Skipping restore.")
    else:
        restore_snapshot(repo, target, purge=purge)
        _anchor_after_restore(repo, target)
        print(
            f"Restored snapshot {target}. (purge={'on' if purge else 'off'})")


@app.command(name="p", hidden=True)
def _previous_alias(purge: bool = typer.Option(
    False,
    "--purge/--no-purge",
    help="Delete files not in the target snapshot (default: purge).",
    show_default=True,
), ):
    return previous(purge=purge)


@app.command(
    help=("Continuously track the repo; snapshot only when durable changes "
          "stabilize."))
def track(
    scan_interval: int = typer.Option(30, help="Polling interval in seconds."),
    snapshot_after: int = typer.Option(
        90, help="Required time in seconds before creating a snapshot."),
):
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)

    state_path = Path(repo / ".git/gitcrumbs/tracker_state.json")
    print(
        f"Tracking repo at {repo} "
        f"(scan_interval={scan_interval}s, snapshot_after={snapshot_after}s). "
        "Ctrl-C to stop.")
    try:
        while True:
            state = load_tracker_state(repo)

            if (restore_lock_path(repo).exists() or index_locked(repo)
                    or in_merge_or_rebase(repo)):
                time.sleep(scan_interval)
                continue

            fp = compute_fingerprint(repo)
            now = time.time()

            if fp != state.get("last_seen_fingerprint"):
                state["last_seen_fingerprint"] = fp
                state["last_seen_time"] = now

            stable = (state.get("last_seen_time") is not None
                      and (now - state["last_seen_time"] >= snapshot_after))
            baseline = state.get("baseline_fingerprint")
            different_from_baseline = (baseline is None) or (fp != baseline)

            if stable:
                if state.get("suppress_until_change"):
                    if different_from_baseline:
                        snap_id = create_snapshot(
                            repo,
                            restored_from_snapshot_id=state.get(
                                "restored_from_snapshot_id"),
                        )
                        state.update({
                            "baseline_fingerprint": fp,
                            "baseline_snapshot_id": snap_id,
                            "suppress_until_change": False,
                            "restored_from_snapshot_id": None,
                        })
                        print(f"Snapshot created: {snap_id}")
                else:
                    if different_from_baseline:
                        snap_id = create_snapshot(
                            repo,
                            restored_from_snapshot_id=state.get(
                                "restored_from_snapshot_id"),
                        )
                        state.update({
                            "baseline_fingerprint": fp,
                            "baseline_snapshot_id": snap_id,
                            "restored_from_snapshot_id": None,
                        })
                        print(f"Snapshot created: {snap_id}")

            atomic_write_json(state_path, state)
            time.sleep(scan_interval)
    except KeyboardInterrupt:
        print("Stopped tracking.")


@app.command(help="Print file contents for PATH at snapshot ID / Label to stdout.")
def show_file(
    snap: str = typer.Argument(
        ...,
        help="Snapshot ID or label.",
    ),
    file_path: str = typer.Argument(
        ...,
        help="Repo-relative or absolute path",
    ),
):
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)

    try:
        snap_id = resolve_snapshot_id(repo, snap)
    except SnapshotNotFound as e:
        print(str(e))
        raise typer.Exit(2)

    try:
        write_file_to_stdout(snap_id, Path(file_path))
    except Exception as e:
        print(str(e))
        raise typer.Exit(2)


@app.command(
    help=("Remove .git/gitcrumbs from this repo (DB and metadata only; "
          "safe for Git history)."))
def remove(
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Do not prompt for confirmation.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be removed without deleting.",
    ),
):
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)

    sdir = state_dir(repo)
    if not sdir.exists():
        print("Nothing to remove. (.git/gitcrumbs does not exist)")
        raise typer.Exit(0)

    total_files = 0
    total_bytes = 0
    for root, _dirs, files in os.walk(sdir):
        for f in files:
            total_files += 1
            try:
                total_bytes += (Path(root) / f).stat().st_size
            except OSError:
                pass

    size_mb = total_bytes / (1024 * 1024) if total_bytes else 0.0
    print(f"This will remove {total_files} files (~{size_mb:.2f} MB) "
          f"under {sdir}")

    if dry_run:
        print("Dry-run: no changes made.")
        raise typer.Exit(0)

    if not yes:
        confirm = typer.confirm(f"Proceed to remove {sdir}?")
        if not confirm:
            print("Aborted.")
            raise typer.Exit(1)

    try:
        shutil.rmtree(sdir)
        print(f"Removed {sdir}")
    except Exception as e:
        print(f"Failed to remove {sdir}: {e}")
        raise typer.Exit(1)


@app.command(help="Rename a snapshot with a new ID (label).")
def rename(
    existing: str = typer.Argument(
        ...,
        help="Existing snapshot ID or label.",
    ),
    new_id: str = typer.Argument(
        ...,
        help="New Label.",
    ),
):
    try:
        repo = ensure_repo_root()
    except (NotAGitRepo, BareRepoUnsupported) as e:
        print(str(e))
        raise typer.Exit(2)

    try:
        snap_id = resolve_snapshot_id(repo, existing)
    except SnapshotNotFound as e:
        print(str(e))
        raise typer.Exit(2)

    try:
        rename_snapshot(repo, snap_id, new_id)
    except ValueError as ve:
        print(str(ve))
        raise typer.Exit(2)
    except SnapshotNotFound as e:
        print(str(e))
        raise typer.Exit(2)

    print(f"Changed snapshot label from '{existing}' to '{new_id}'.")


@app.callback(invoke_without_command=True)
def main(version: bool = typer.Option(
    False,
    "--version",
    "-V",
    help="Show gitcrumbs version and exit.",
    is_eager=True,
), ):
    if version:
        typer.echo(f"gitcrumbs, version {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
