# beastcp

`beastcp` is a high-performance file copying and synchronization utility written in Python.  
It combines the familiar behavior of the Unix `cp` command with advanced features such as:

- Progress bars using `tqdm`
- Resume support for interrupted copies
- Hash verification for data integrity
- Multi-threaded copying for directories
- Automatic directory creation
- Safe and force-overwrite modes
- Efficient chunked I/O for large files
- Optional thread configuration and verification settings

`beastcp` is designed for users who frequently copy large files or datasets and want a reliable, observable, and tunable tool.

## Features

### File Copying
- Copies files of any size with a progress bar.
- Supports resuming partially copied files.
- Verifies file integrity using SHA-256 hashing.

### Directory Copying
- Recursively copies entire directories.
- Uses multithreading to improve speed when copying many files.
- Creates destination directory structure automatically.

### Resilience Features
- Resume mode prevents re-copying already-transferred data.
- Verification ensures the output matches the source exactly.

### Command-Line Interface
- Customizable options via CLI flags.
- Compatible with Unix-like systems and Windows.

## Installation

Install from PyPI:

```
pip install beastcp
```

This provides a command-line executable:

```
beastcp
```

## Usage

### Copy a file

```
beastcp source.bin /path/to/destination.bin
```

### Copy a folder with custom number of threads

```
beastcp dataset/ /backup/dataset/ --threads 8
```

### Force overwrite an existing destination

```
beastcp data.zip /backup/data.zip --force
```

### Disable resume or verification

```
beastcp bigfile.iso /mnt/drive/ --no-resume --no-verify
```

## Full CLI Reference

```
beastcp SRC DST [OPTIONS]

Options:
  -t, --threads INTEGER     Number of parallel copy threads (default: 4)
  --no-resume               Disable resume support
  --no-verify               Disable SHA-256 verification
  -f, --force               Allow overwriting the destination
  --help                    Show this message and exit
```

## Example

Copying a directory with progress indicators:

```
beastcp /data/archive/ /backup/archive/ --threads 6
```

Copying a very large file with verification disabled:

```
beastcp movie.mkv /media/storage/ --no-verify
```

## How It Works

### For file copying:
- Reads the source in fixed-size chunks (1 MB by default)
- Writes each chunk to the destination
- Updates a progress bar
- Optionally resumes from last written byte
- Optionally performs SHA-256 hash comparison

### For directory copying:
- Scans files recursively
- Spawns multiple threads for parallel copying
- Uses the same file copying routine for each file

This design allows `beastcp` to efficiently copy both large singular files and many small files.
