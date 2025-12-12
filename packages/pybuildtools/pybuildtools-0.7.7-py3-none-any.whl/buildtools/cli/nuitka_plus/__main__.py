"""
BLURB GOES HERE.

Copyright (c) 2015 - 2025 Rob "N3X15" Nelson <nexisentertainment@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import json
import os
import sys


def main() -> None:
    print(f"buildtools.cli.nuitka_plus subprocess spawned. PID={os.getpid()}")
    print(f"Opening {sys.argv[1]}...")
    data: dict
    with open(sys.argv[1], "r") as f:
        data = json.load(f)

    args = data["args"]
    print(f"Setting sys.argv = [sys.argv[0]] + {args!r}...")
    sys.argv = [sys.argv[0]] + args

    print(f"Setting os.environ['PATH'] = {data['environ']['PATH']!r}...")
    os.environ["PATH"] = data["environ"]["PATH"]

    print(f"Invoking nuitka.__main__.main()...")
    import nuitka.__main__ as nkmain

    nkmain.main()


if __name__ == "__main__":
    main()
