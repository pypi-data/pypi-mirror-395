import argparse
import pathlib
import numpy as np
from . import bin_reader


def main(path: str | None = None, directory: str | None = None):
    if not path and not directory:
        match _parse_args():
            case argparse.Namespace(path=path, directory=directory):
                pass

    if directory:
        dir_path = pathlib.Path(directory)
        paths = sorted(p for p in dir_path.glob("*.bin") if p.is_file())
        if not paths:
            print(f"No .bin files found in {dir_path}")
            return
        print(f"Scanning directory {dir_path} ({len(paths)} file(s))")
    else:
        paths = [pathlib.Path(path)]

    for p in paths:
        try:
            bursts = bin_reader.read_scan(p)
        except Exception as exc:  # pragma: no cover
            print(f"{p.name}: parse failed ({exc})")
            continue
        if not bursts:
            print(f"{p.name}: duplicates: none (no bursts parsed)")
            continue
        duplicate_pairs = _find_adjacent_duplicates(bursts)
        dup_list = ", ".join(f"{a}->{b}" for a, b, _, _ in duplicate_pairs) if duplicate_pairs else "none"
        print(f"{p.name}: duplicates: {dup_list}")
        if duplicate_pairs:
            ascii_preview = _duplicates_ascii(duplicate_pairs, len(bursts))
            print(f"{p.name}: ascii: {ascii_preview}")


def _find_adjacent_duplicates(bursts):
    """Return list of (prev_idx, idx, prev_ts, ts) where adjacent data are identical."""
    duplicates = []
    prev_data = bursts[0]["data"]
    for idx, burst in enumerate(bursts[1:], start=1):
        if prev_data.shape == burst["data"].shape and np.array_equal(prev_data, burst["data"]):
            duplicates.append((idx - 1, idx, bursts[idx - 1]["timestamp"], burst["timestamp"]))
        prev_data = burst["data"]
    return duplicates


def _duplicates_ascii(duplicate_pairs, total_bursts):
    """Return ASCII map per burst: '.' normal, '!' if burst is duplicate of previous."""
    if total_bursts == 0:
        return ""
    marks = ["." for _ in range(total_bursts)]
    dup_targets = {b for _, b, _, _ in duplicate_pairs}
    for i in dup_targets:
        if 0 < i < total_bursts:
            marks[i] = "!"
    return "".join(marks)


def _parse_args():
    parser = argparse.ArgumentParser(description="Parse burst .bin files")
    parser.add_argument("-p", "--path", type=str, help="Single .bin file to parse")
    parser.add_argument("-d", "--dir", "--directory", dest="directory", type=str, help="Directory of .bin files to parse")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    main(args.path, args.directory)