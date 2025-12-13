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

from enum import Enum, IntEnum


class LogPrefixes(Enum):
    RUNNING = "[~]"
    QUESTION = "[?]"
    BAD = "[-]"
    GOOD = "[+]"
    WARNING = "[!]"
    ERROR = "[*]"
    CRITICAL = "[X]"


class SysExits(IntEnum):
    # https://sites.uclouvain.be/SystInfo/usr/include/sysexits.h.html

    OK = 0
    USAGE = 64  # Command Line Usage
    DATAERR = 65  # Data format error
    NOINPUT = 66  # Could not open input
    NOUSER = 67  # Addressee not found
    NOHOST = 68  # Could not find hostname
    UNAVAILABLE = 69  # Service unavailable
    SOFTWARE = 70  # Software error
    OSERR = 71  # System error (fork issues, etc)
    OSFILE = 72  # Critical OS file missing
    CANTCREATE = 73  # Can't create new file
    IOERR = 74  # I/O error
    TEMPFAIL = 75  # Try again
    PROTOCOL = 76  # Protocol error
    NOPERM = 77  # Permission denied
    CONFIG = 78  # Configuration error
