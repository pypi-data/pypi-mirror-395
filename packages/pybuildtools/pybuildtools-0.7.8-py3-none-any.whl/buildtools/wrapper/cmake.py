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

import subprocess
from typing import Dict, List, Optional

from buildtools.bt_logging import log
from buildtools.os_utils import ENV, BuildEnv, cmd
from buildtools.types import StrOrPath


class CMake:
    @classmethod
    def GetVersion(
        cls,
        CMAKE: StrOrPath = "cmake",
        user: Optional[str | int] = None,
        group: Optional[str | int] = None,
    ) -> Optional[str]:
        rev = subprocess.check_output([str(CMAKE), "--version"], stderr=subprocess.STDOUT, user=user, group=group)
        if rev:
            return rev.decode("utf-8").split()[2]

    def __init__(self) -> None:
        self.flags: Dict[str, str] = {}
        self.generator: str = None

    def setFlag(self, key: str, val: str) -> None:
        log.info(f"CMake: {key} = {val}")
        self.flags[key] = val

    def build(
        self,
        CMAKE: StrOrPath = "cmake",
        dir: StrOrPath = ".",
        env: Optional[BuildEnv] = None,
        target: Optional[str] = None,
        moreflags: Optional[List[str]] = None,
        env_dump: bool = False,
        user: Optional[str | int] = None,
        group: Optional[str | int] = None,
    ):
        if moreflags is None:
            moreflags = []
        if env is None:
            env = ENV.toDict()
        flags = ["--build", str(dir)]
        if target is not None:
            moreflags += ["--target", target]

        flags += moreflags

        with log.info("Running CMake --build:"):
            if env_dump:
                BuildEnv.dump(env)
            return cmd(
                [str(CMAKE)] + flags,
                env=env,
                critical=True,
                echo=True,
                user=user,
                group=group,
            )

    def run(
        self,
        CMAKE: StrOrPath = "cmake",
        env: Optional[BuildEnv] = None,
        dir: StrOrPath = ".",
        moreflags: Optional[List[str]] = None,
        env_dump: bool = False,
        user: Optional[str | int] = None,
        group: Optional[str | int] = None,
    ) -> None:
        if env is None:
            env = ENV.toDict()
        if moreflags is None:
            moreflags = []
        flags = []

        if self.generator is not None:
            flags += ["-G", self.generator]

        for key, value in self.flags.items():
            flags += [f"-D{key}={value}"]

        flags += moreflags

        with log.info("Running CMake:"):
            if env_dump:
                BuildEnv.dump(env)
            return cmd(
                [str(CMAKE)] + flags + [str(dir)],
                env=env,
                critical=True,
                echo=True,
                user=user,
                group=group,
            )
        return False
