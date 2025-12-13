# nercone-fullcopy
Bit-exact, metadata-preserving copy utility for disks, images, partitions, or volumes.

## Usage

**Example:**

```bash
python -m nercone_fullcopy /dev/sda disk-image.raw -b 8M --hash sha512
```

**Options:**

- `-b, --block-size` – Block size for copy operations (default `4M`).
- `--size` – Explicit copy size if auto-detection fails.
- `--hash` – Hash algorithm for verification (default `sha256`).
- `--skip-verify` – Skip integrity verification (not recommended).
- `--force` – Overwrite an existing destination regular file.
- `--no-flush` – Do not `fsync` after writing (faster but less safe).

**Warning:** Cloning block devices may require root privileges. Use with caution.
