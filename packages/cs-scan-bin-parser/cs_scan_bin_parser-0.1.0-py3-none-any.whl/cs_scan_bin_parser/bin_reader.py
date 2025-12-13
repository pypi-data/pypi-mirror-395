import os
import pathlib
from collections import Counter
from datetime import datetime, timedelta, timezone

import numpy as np

WINDOWS_EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)

# Header layout per C# writer:
#   int64  filetime   (8 bytes)
#   float  xpos       (4 bytes)
#   float  zpos       (4 bytes)
#   ushort pixels     (2 bytes)
#   ushort channels   (2 bytes)
HEADER_SIZE = 8 + 4 + 4 + 2 + 2  # 20 bytes


def _detect_record_size(buf: bytes) -> int | None:
    """Detect fixed record size by repeated timestamp prefix."""
    if len(buf) < HEADER_SIZE:
        return None
    ts = buf[:8]
    positions = []
    start = 0
    # Grab first ~20 occurrences to infer spacing
    while len(positions) < 20:
        i = buf.find(ts, start)
        if i == -1:
            break
        positions.append(i)
        start = i + 1
    if len(positions) < 2:
        return None
    deltas = [b - a for a, b in zip(positions, positions[1:])]
    # Most common positive delta
    common = Counter(d for d in deltas if d > HEADER_SIZE)
    if not common:
        return None
    record_size, _ = common.most_common(1)[0]
    return record_size


def _iter_records(buf: memoryview, record_size: int):
    header_dtype = np.dtype([
        ("filetime",   "<i8"),
        ("xpos",       "<f4"),
        ("zpos",       "<f4"),
        ("pixels",     "<u2"),
        ("channels",   "<u2"),
    ])

    payload_slot = record_size - HEADER_SIZE
    count = len(buf) // record_size
    for i in range(count):
        start = i * record_size
        rec = buf[start:start + record_size]
        header = np.frombuffer(rec, dtype=header_dtype, count=1)[0]
        n = int(header["pixels"]) * int(header["channels"])
        data_bytes = n * 2  # uint16 payload
        if data_bytes > payload_slot or data_bytes == 0:
            # Implausible header; stop to avoid misalignment
            break
        payload = rec[HEADER_SIZE:HEADER_SIZE + data_bytes]
        if len(payload) < data_bytes:
            break
        data = np.frombuffer(payload, dtype="<u2", count=n).reshape(
            header["pixels"], header["channels"]
        )
        yield header, data


def read_scan(path):
    data = pathlib.Path(path).read_bytes()
    record_size = _detect_record_size(data)
    if not record_size:
        raise ValueError("Could not detect record size from timestamp spacing")

    mv = memoryview(data)
    bursts = []
    for header, data in _iter_records(mv, record_size):
        ts = WINDOWS_EPOCH + timedelta(microseconds=header["filetime"] / 10)
        bursts.append({
            "timestamp": ts,
            "xpos": float(header["xpos"]),
            "zpos": float(header["zpos"]),
            "pixels": int(header["pixels"]),
            "channels": int(header["channels"]),
            "data": data,  # shape: (pixels, channels), dtype uint16
        })
    return bursts

# Example:
# bursts = read_scan("path/to/file.bin")
# print(len(bursts), bursts[0]["timestamp"], bursts[0]["data"].shape)