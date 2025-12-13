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

"""
General-Purpose Utilities.

Copyright (c) 2015 - 2024 Rob "N3X15" Nelson <nexisentertainment@gmail.com>

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

import binascii
import hashlib
import mimetypes
import mmap
import sys
import time
from pathlib import Path
from typing import Any, BinaryIO, Type, Union

from buildtools.types import StrOrPath


def getClass(thing: Any) -> Type:
    return thing.__class__


def getClassName(thing: Any) -> str:
    return getClass(thing).__name__


def bool2yn(b: bool) -> str:
    return "Y" if b else "N"


def is_python_3() -> bool:
    return sys.version_info[0] >= 3


if is_python_3():

    def bytes2str(b: bytes) -> str:
        if isinstance(b, bytes):
            return b.decode("utf-8")
        else:
            return str(b)

else:

    def bytes2str(b):
        return str(b)


def hashfile(afile: Union[str, Path, BinaryIO], hasher: Any, blocksize: int = 4096) -> str:
    if isinstance(afile, (str, Path)):
        with open(afile, "rb") as f:
            return hashfile(f, hasher, blocksize)
    # elif isinstance(afile, BinaryIO):
    else:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
        return hasher.hexdigest()


def md5sum(filename: StrOrPath, blocksize: int = 4096) -> str:
    with open(filename, "rb") as f:
        return hashfile(f, hashlib.md5(), blocksize)


def sha256sum(filename: StrOrPath, blocksize: int = 4096) -> str:
    with open(filename, "rb") as f:
        return hashfile(f, hashlib.sha256(), blocksize)


def img2blob(filename: StrOrPath) -> str:
    mime, _ = mimetypes.guess_type(filename)
    with open(filename, "rb") as fp:
        data64 = binascii.b2a_base64(fp.read())
    return "data:{MIME};base64,{DATA}".format(MIME=mime, DATA=data64.decode("ascii"))


def get_num_lines(file_path: StrOrPath) -> int:
    with open(file_path, "r+") as fp:
        with mmap.mmap(fp.fileno(), 0) as buf:
            lines: int = 0
            while buf.readline():
                lines += 1
            return lines


def current_milli_time() -> int:
    return int(round(time.time() * 1000))
