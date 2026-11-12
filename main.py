"""Entry for the make.fun "Coolest Art" competition.

Copies the bundled entry.png (resolved from __file__) to /output/entry.png,
which is the destination the grader mounts, and best-effort to ./entry.png and
./output/entry.png when the checkout happens to be writable. Standard library
only, no network access.
"""

import os
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

DESTINATIONS = (
    ("/output/entry.png", True),
    ("entry.png", False),
    (os.path.join("output", "entry.png"), True),
)


def read_entry():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.png"), "rb") as fh:
        return fh.read()


def write_entry(data):
    written = []
    for dest, needs_dir in DESTINATIONS:
        try:
            if needs_dir:
                os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as fh:
                fh.write(data)
        except OSError:
            continue
        written.append(dest)
    return written


def main():
    try:
        data = read_entry()
    except OSError as exc:
        sys.stderr.write("main.py: cannot read entry.png: %s\n" % (exc,))
        return 1

    if not data.startswith(PNG_SIGNATURE):
        sys.stderr.write("main.py: entry.png is missing the PNG signature, refusing to ship\n")
        return 1

    written = write_entry(data)
    if not written:
        sys.stderr.write("main.py: no writable destination, entry.png not shipped\n")
        return 1

    print("shipped entry.png (%d bytes) -> %s" % (len(data), ", ".join(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
