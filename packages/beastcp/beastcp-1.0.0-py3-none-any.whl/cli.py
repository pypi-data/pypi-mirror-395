import os
import shutil
import hashlib
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import click
from pathlib import Path


def sha256sum(file_path, block_size=1024 * 1024):
    """Calculate SHA256 for file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(block_size):
            h.update(chunk)
    return h.hexdigest()


def copy_file(src, dst, resume=True, verify=True):
    """Copy a single file with progress bar, resume, verify."""
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)

    total = src.stat().st_size
    copied = 0

    mode = "wb"

    # Resume
    if dst.exists() and resume:
        copied = dst.stat().st_size
        if copied < total:
            mode = "ab"  # append for resume
        else:
            # if already copied fully, skip
            return "exists"

    with open(src, "rb") as fsrc, open(dst, mode) as fdst, tqdm(
        total=total, initial=copied, unit="B", unit_scale=True,
        desc=f"Copying {src.name}", ascii=True
    ) as pbar:

        if copied > 0:
            fsrc.seek(copied)

        while True:
            chunk = fsrc.read(1024 * 1024)  # 1MB
            if not chunk:
                break
            fdst.write(chunk)
            pbar.update(len(chunk))

    if verify:
        if sha256sum(src) != sha256sum(dst):
            raise click.ClickException(f"❌ Hash mismatch for {src}")

    return "copied"


def copy_directory(src, dst, workers=4, **kwargs):
    """Copy directory in parallel."""
    src = Path(src)
    dst = Path(dst)

    files = [p for p in src.rglob("*") if p.is_file()]

    click.echo(f"📁 Found {len(files)} files, copying using {workers} threads")

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [
            ex.submit(copy_file, file, dst / file.relative_to(src), **kwargs)
            for file in files
        ]
        for f in futures:
            f.result()


@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.argument("dst", type=click.Path())
@click.option("--threads", "-t", default=4, help="Parallel file copy threads.")
@click.option("--no-resume", is_flag=True, help="Disable resume capability.")
@click.option("--no-verify", is_flag=True, help="Disable SHA256 verification.")
@click.option("--force", "-f", is_flag=True, help="Force overwrite files.")
def cli(src, dst, threads, no_resume, no_verify, force):
    """
    🚀 BEASTCP: A beast-mode cp/rsync + tqdm command with resume, verify,
    threading, and beautiful progress.
    """
    src = Path(src)
    dst = Path(dst)

    if dst.exists() and not force:
        raise click.ClickException("❌ Destination exists. Use --force to overwrite.")

    options = dict(resume=not no_resume, verify=not no_verify)

    if src.is_file():
        copy_file(src, dst, **options)
    else:
        copy_directory(src, dst, workers=threads, **options)

    click.echo("✅ Done — BEAST MODE COPY COMPLETE!")
