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
OS Utilities.

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

import codecs
import filecmp
import glob
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import typing
import zipfile
from functools import reduce
from pathlib import Path
from subprocess import CalledProcessError
from typing import Dict, Iterable, List, NamedTuple, Optional, Union

import psutil
import tqdm

from buildtools.bt_logging import log
from buildtools.types import StrOrPath, SupportsIn

REG_EXCESSIVE_WHITESPACE: re.Pattern = re.compile(r"\s{2,}")
PLATFORM: str = platform.system()
PATH_7ZA: Optional[os.PathLike] = None


def clock():
    if sys.platform == "win32":
        return time.clock()
    else:
        return time.time()


def getElapsed(start: int) -> str:
    return "%d:%02d:%02d.%03d" % reduce(
        lambda ll, b: divmod(ll[0], b) + ll[1:],
        [((clock() - start) * 1000,), 1000, 60, 60],
    )


def secondsToStr(t: int) -> str:
    """
    Take integer seconds, return formatted string.
    """
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class BuildEnv:
    def __init__(self, initial: Optional[Dict[str, str]] = None, noisy: bool = False) -> None:
        self._env: Dict[str, str]
        self.keymap: Dict[str, str]
        if initial is not None:
            self._keymap = {k.casefold(): k for k in initial.keys()}
            self._env = {k.casefold(): str(v) for k, v in initial.items()}
        else:
            self._keymap = {k.casefold(): k for k in os.environ.keys()}
            self._env = {k.casefold(): str(v) for k, v in os.environ.items()}
        self.noisy: bool = True

    def set(self, key: str, val: str, noisy: Optional[bool] = None) -> None:
        if noisy is None:
            noisy = self.noisy
        val = str(val)
        if noisy:
            log.info("Environment: {} = {}".format(key, val))
        self._keymap[key.casefold()] = key
        self._env[key.casefold()] = val

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        key = key.casefold()
        if key not in self._env:
            return default
        return self._env[key]

    def toDict(self) -> Dict[str, str]:
        return {self._keymap[k]: v for k, v in self._env.items()}

    def merge(self, newvars: Dict[str, str]) -> None:
        self._keymap.update({k.casefold(): k for k in newvars.keys()})
        self._env.update({k.casefold(): str(v) for k, v in newvars.items()})

    def prependTo(
        self,
        key: str,
        value: str,
        delim: Optional[str] = None,
        noisy: Optional[bool] = None,
    ) -> None:
        if delim is None:
            delim = os.pathsep
        if noisy is None:
            noisy = self.noisy
        okey = key
        key = key.casefold()
        if noisy:
            log.info("Environment: {1} prepended to {0}".format(okey, value))
        self._keymap[key] = okey
        self._env[key] = delim.join([str(value)] + self._env.get(key, "").split(delim))

    def appendTo(
        self,
        key: str,
        value: str,
        delim: Optional[str] = None,
        noisy: Optional[bool] = None,
    ) -> None:
        if delim is None:
            delim = os.pathsep
        if noisy is None:
            noisy = self.noisy
        okey = key
        key = key.casefold()
        if noisy:
            log.info("Environment: {1} appended to {0}".format(okey, value))
        self._keymap[key] = okey
        self._env[key] = delim.join(self._env.get(key, "").split(delim) + [str(value)])

    def clone(self) -> "BuildEnv":
        be = BuildEnv()
        be._keymap = self._keymap
        be._env = self._env
        return be

    def dumpToLog(self, keys: Optional[Iterable[str]] = None) -> None:
        if keys is None:
            keys = self._env.keys()
        self.dump(self._env, map(lambda k: k.casefold(), keys))

    def which(self, command: str, skip_paths: Optional[Iterable[StrOrPath]] = None) -> Optional[Path]:
        if skip_paths is None:
            skip_paths = []
        fpath, _ = os.path.split(command)
        if fpath:
            if is_executable(command):
                return Path(command)
        else:
            for pathstr in self.get("PATH", "").split(os.pathsep):
                pathstr = pathstr.strip('"')
                path = Path(pathstr)
                if Path(pathstr.casefold()) in set(map(lambda x: Path(str(x).casefold()), skip_paths)):
                    continue
                exe_file = path / command
                if sys.platform == "win32":
                    for ext in self.get("PATHEXT").split(os.pathsep):
                        proposed_file = exe_file
                        if not proposed_file.suffix == ext:
                            proposed_file = proposed_file.with_suffix(ext)
                            if proposed_file.is_file():
                                exe_file = proposed_file
                                # print('{}: {}'.format(exe_file,ext))
                                break
                if is_executable(exe_file):
                    return exe_file
        return None

    def assertWhich(self, command: str, skip_paths: Optional[Iterable[StrOrPath]] = None) -> Optional[Path]:
        if skip_paths is None:
            skip_paths = []
        fullpath = self.which(command, skip_paths)
        with log.info("Checking if %s exists...", command):
            if fullpath is None:
                raise RuntimeError(f"{command!r} is not in PATH!")
            else:
                log.info("Found: %s", fullpath)
        return fullpath

    def removeDuplicatedEntries(self, key: str, noisy: Optional[str] = None, delim: Optional[str] = None) -> None:
        if delim is None:
            delim = os.pathsep
        if noisy is None:
            noisy = self.noisy
        newlist: List[str] = []
        okey = key
        key = key.casefold()
        for entry in self._env[key].split(delim):
            entry = entry.strip('"')
            if entry in newlist:
                if noisy:
                    log.info("Build env: Removing %r from %s: duplicated entry.", entry, okey)
                continue
            newlist += [entry]
        self._env[key] = delim.join(newlist)

    @classmethod
    def dump(cls, env: Dict[str, str], keys: Optional[Iterable[str]] = None) -> None:
        for key, value in sorted(env.items()):
            if keys is not None and key.casefold() not in map(lambda x: x.casefold(), keys):
                continue
            log.info('+{0}="{1}"'.format(key, value))


def ensureDirExists(path: StrOrPath, mode: int = 0o777, noisy: bool = False) -> None:
    path = Path(path)
    if not os.path.isdir(path):
        os.makedirs(path, mode)
        if noisy:
            log.info("Created %s.", path)


class DeferredLogEntry:
    def __init__(self, label: str) -> None:
        self.label: str = label

    def toStr(self, entryVars: Dict[str, str]) -> str:
        return self.label.format(**entryVars)


class TimeExecution:
    def __init__(self, label: Union[str, DeferredLogEntry]) -> None:
        self.start_time: Optional[int] = None
        self.vars: Dict[str, str] = {}
        self.label: DeferredLogEntry
        if isinstance(label, str):
            self.label = DeferredLogEntry("Completed in {elapsed}s - {label}")
            self.vars["label"] = label
        elif isinstance(label, DeferredLogEntry):
            self.label = label

    def __enter__(self):
        self.start_time = clock()
        return self

    def __exit__(self, typeName, value, traceback):
        self.vars["elapsed"] = secondsToStr(clock() - self.start_time)
        with log:
            log.info(self.label.toStr(self.vars))
        return False


class Chdir:
    def __init__(self, newdir: StrOrPath, noisy: bool = True):
        self.pwd: Path = Path.cwd()
        self.chdir: Path = Path(newdir)
        self.noisy: bool = noisy

    def __enter__(self):
        try:
            if Path.cwd() != self.chdir:
                os.chdir(self.chdir)
                if self.noisy:
                    log.info(f"cd {self.chdir}")
        except Exception as e:
            log.critical(f"Failed to chdir to {self.chdir}.")
            log.exception(e)
            sys.exit(1)
        return self

    def __exit__(self, typeName, value, traceback):
        try:
            if Path.cwd() != self.pwd:
                os.chdir(self.pwd)
                if self.noisy:
                    log.info(f"cd {self.pwd}")
        except Exception as e:
            log.critical(f"Failed to chdir to {self.pwd}.")
            log.exception(e)
            sys.exit(1)
        return False


def is_executable(fpath: StrOrPath) -> bool:
    """
    Returns true if the path is a file and has os.X_OK permissions.
    """
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(command: str, skip_paths: Optional[Iterable[StrOrPath]] = None) -> Optional[Path]:
    """
    Returns path of the given command, if it exists in PATH. Otherwise, return value is None.
    """
    return ENV.which(command, skip_paths=skip_paths)


def assertWhich(program: str, skip_paths: Optional[Iterable[StrOrPath]] = None) -> Optional[Path]:
    """
    Raises an exception if program isn't found in PATH.
    """
    return ENV.assertWhich(program, skip_paths=skip_paths)


def _cmd_handle_env(env: Optional[BuildEnv]) -> Dict[str, str]:
    o: Dict[str, str] = {}
    if env is None:
        o = ENV.toDict().copy()
    if isinstance(env, BuildEnv):
        o = env.toDict().copy()
    elif isinstance(env, dict):
        # Fix a bug where env vars get some weird types.
        o = {str(k): str(v) for k, v in env.items()}
    return o


def _cmd_handle_args(command: Iterable[str], globbify: bool) -> List[str]:
    # Shell-style globbin'.
    new_args = []  # command[0]]
    for arg in command:  # 1:
        arg = str(arg)
        if globbify:
            if "~" in arg:
                arg = os.path.expanduser(arg)
            if "*" in arg or "?" in arg:
                new_args += glob.glob(arg)
                continue

        new_args += [arg]
    return new_args


def find_process(pid: int) -> Optional[psutil.Process]:
    for proc in psutil.process_iter():
        try:
            if proc.pid == pid:
                if proc.status() == psutil.STATUS_ZOMBIE:
                    log.warn("Detected zombie process #%s, skipping.", proc.pid)
                    continue
                return proc
        except psutil.AccessDenied:
            continue
    return None


def check_output(*popenargs, timeout=None, acceptable_exit_codes: SupportsIn[int] = [0], **kwargs):
    """
    Python 3.6 subprocess.check_output(), modded to accept more exit codes.
    """
    if "stdout" in kwargs:
        raise ValueError("stdout argument not allowed, it will be overridden.")

    if "input" in kwargs and kwargs["input"] is None:
        # Explicitly passing input=None was previously equivalent to passing an
        # empty string. That is maintained here for backwards compatibility.
        kwargs["input"] = "" if kwargs.get("universal_newlines", False) else b""
    return run(
        *popenargs,
        stdout=subprocess.PIPE,
        timeout=timeout,
        check=True,
        acceptable_exit_codes=acceptable_exit_codes,
        **kwargs,
    ).stdout


def check_call(*popenargs, acceptable_exit_codes: SupportsIn[int] = [0], **kwargs):
    """
    Python 3.6 subprocess.check_call(), modded to accept more exit codes.
    """
    retcode = subprocess.call(*popenargs, **kwargs)
    if retcode not in acceptable_exit_codes:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd)
    return 0


def run(
    *popenargs,
    input=None,
    timeout=None,
    check=False,
    acceptable_exit_codes: SupportsIn[int] = [0],
    **kwargs,
) -> subprocess.CompletedProcess:
    """
    Python 3.6 subprocess.run(), modded to accept more exit codes.
    """
    with subprocess.Popen(*popenargs, **kwargs) as process:
        try:
            stdout, stderr = process.communicate(input, timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            raise subprocess.TimeoutExpired(
                process.args,
                timeout,
                output=stdout,  # pylint: disable=E1101
                stderr=stderr,
            )
        except:
            process.kill()
            process.wait()
            raise
        retcode = process.poll()
        if check and retcode not in acceptable_exit_codes:
            raise CalledProcessError(
                retcode,
                process.args,  # pylint: disable=E1101
                output=stdout,
                stderr=stderr,
            )
    return subprocess.CompletedProcess(process.args, retcode, stdout, stderr)  # pylint: disable=E1101


def cmd(
    command: List[str],
    echo: bool = False,
    env: Optional[BuildEnv] = None,
    show_output: bool = True,
    critical: bool = False,
    globbify: bool = True,
    acceptable_exit_codes: SupportsIn[int] = [0],
    user: Optional[str | int] = None,
    group: Optional[str | int] = None,
) -> bool:
    new_env = _cmd_handle_env(env)
    command = _cmd_handle_args(command, globbify)
    if echo:
        log.info("$ " + _args2str(command))

    output = ""
    try:
        if show_output:
            code = subprocess.call(command, env=new_env, shell=False, user=user, group=group)
            # print(repr(code))
            success = code in acceptable_exit_codes
            if critical and not success:
                raise CalledProcessError(code, command)
            return success
        else:
            # Using our own customized check_output for acceptable_exit_codes.
            output = check_output(
                command,
                env=new_env,
                stderr=subprocess.STDOUT,
                acceptable_exit_codes=acceptable_exit_codes,
                user=user,
                group=group,
            )
            return True
    except CalledProcessError as cpe:
        log.error(cpe.output)
        if critical:
            raise cpe
        log.error(cpe)
        return False
    except Exception as e:
        log.error(e)
        log.error(output)
        if critical:
            raise e
        log.error(e)
        return False


class _CmdOutputResponse(NamedTuple):
    stdout: bytes
    stderr: bytes


def cmd_output(
    command: List[str],
    echo: bool = False,
    env: Optional[BuildEnv] = None,
    critical: bool = False,
    globbify: bool = True,
    user: Optional[str | int] = None,
    group: Optional[str | int] = None,
) -> Optional[_CmdOutputResponse]:
    new_env = _cmd_handle_env(env)
    command = _cmd_handle_args(command, globbify)
    if echo:
        log.info("$ " + _args2str(command))

    try:
        o = subprocess.Popen(
            command,
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            user=user,
            group=group,
        ).communicate()
        if o is not None:
            stdout, stderr = o
            return _CmdOutputResponse(stdout, stderr)
    except Exception as e:
        log.error(repr(command))
        if critical:
            raise e
        log.error(e)
    return None


def cmd_out(
    command: List[str],
    echo: bool = False,
    env: Optional[BuildEnv] = None,
    critical: bool = False,
    globbify: bool = True,
    encoding: str = "utf-8",
    user: Optional[str | int] = None,
    group: Optional[str | int] = None,
) -> Optional[str]:

    new_env = _cmd_handle_env(env)
    command = _cmd_handle_args(command, globbify)
    if echo:
        log.info("$ " + _args2str(command))

    try:
        p = subprocess.Popen(
            command,
            env=new_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            close_fds=True,
            user=user,
            group=group,
        )
        if p.stdout is not None:
            return p.stdout.read().decode(encoding)
    except Exception as e:
        log.error(repr(command))
        if critical:
            raise e
        log.error(e)
    return None


def cmd_daemonize(
    command: List[str],
    echo: bool = False,
    env: Optional[BuildEnv] = None,
    critical: bool = False,
    globbify: bool = True,
    win_tempfile_dir: Optional[Path] = None,
    user: Optional[str | int] = None,
    group: Optional[str | int] = None,
):
    new_env = _cmd_handle_env(env)
    command = _cmd_handle_args(command, globbify)
    if echo:
        log.info("& " + _args2str(command))

    try:
        if os.name == "nt":
            # HACK
            batchfile: Path
            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".bat", dir=win_tempfile_dir) as tf:
                tf.write(" ".join(command))
                batchfile = Path(tf.name)
            os.startfile(batchfile)
        else:
            subprocess.Popen(command, env=new_env)
        return True
    except Exception as e:
        log.error(repr(command))
        if critical:
            raise e
        log.error(e)
        return False


def old_copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.path.getmtime(src) - os.path.getmtime(dst) > 1:
                shutil.copy2(s, d)


def canCopy(src, dest, **op_args):
    """
    :param ignore_mtime bool:
        Ignore file modification timestamps.
    :param ignore_filecmp bool:
        Disable byte-to-byte comparison AND os.stat checks.
    :param ignore_bytecmp bool:
        Do not check each file byte-for-byte, perform shallow os.stat checks.
    """
    if not os.path.isfile(dest):
        return True
    if not op_args.get("ignore_mtime", False):
        if os.path.getmtime(src) - os.path.getmtime(dest) > 1.0:
            return True
    if not op_args.get("ignore_filecmp", False):
        if not filecmp.cmp(src, dest, op_args.get("ignore_bytecmp", False)):
            return True
    return False


def single_copy(fromfile: str, newroot: str, **op_args):
    """
    :param as_file bool:
        Copy to new name rather than to new directory. False by default.
    :param verbose bool:
        Log copying action.
    :param ignore_mtime bool:
        Ignore file modification timestamps.
    :param ignore_filecmp bool:
        Disable byte-to-byte comparison AND os.stat checks.
    :param ignore_bytecmp bool:
        Do not check each file byte-for-byte, perform shallow os.stat checks.
    """
    newfile = os.path.join(newroot, os.path.basename(fromfile))
    if op_args.get("as_file", False) or "." in newroot:
        newfile = newroot
    if canCopy(fromfile, newfile, **op_args):
        if op_args.get("verbose", False):
            log.info("Copying {} -> {}".format(fromfile, newfile))
        shutil.copy2(fromfile, newfile)


def copytree(fromdir, todir, ignore=None, verbose=False, ignore_mtime=False, progress=False):
    if progress:
        count = {"a": 0}

        def incrementCount(a, b, **c):
            count["a"] += 1

        optree(
            fromdir,
            todir,
            incrementCount,
            ignore,
            verbose=False,
            ignore_mtime=ignore_mtime,
        )
        optree(
            fromdir,
            todir,
            single_copy,
            ignore,
            verbose=verbose,
            ignore_mtime=ignore_mtime,
            tqdm_total=count["a"],
            tqdm_desc="Copying...",
            progress=True,
        )
    else:
        optree(
            fromdir,
            todir,
            single_copy,
            ignore,
            verbose=verbose,
            ignore_mtime=ignore_mtime,
        )


def optree(fromdir, todir, op, ignore=None, **op_args):
    if ignore is None:
        ignore = []
    gen = []
    # print('ignore=' + repr(ignore))
    for root, _, files in os.walk(fromdir):
        path = root.split(os.sep)
        start = len(fromdir)
        if root[start:].startswith(os.sep):
            start += 1
        substructure = root[start:]
        assert not substructure.startswith(os.sep)
        newroot = os.path.join(todir, substructure)
        if any([(x + "/" in ignore) for x in path]):
            if op_args.get("verbose", False):
                log.info("Skipping {}".format(substructure))
            continue
        # if not os.path.isdir(newroot):
        #    if op_args.get('verbose', False):
        #        log.info(u'mkdir {}'.format(newroot))
        #    os.makedirs(newroot)
        for filename in files:
            fromfile = os.path.join(root, filename)
            _, ext = os.path.splitext(os.path.basename(fromfile))
            if ext in ignore:
                if op_args.get("verbose", False):
                    log.info("Skipping {} ({})".format(fromfile, ext))
                continue
            gen += [(fromfile, newroot)]
    # print(len(gen))
    prog = None
    if op_args.get("progress", False):
        prog = tqdm.tqdm(
            gen,
            desc=op_args.get("tqdm_desc", "Operating..."),
            total=op_args.get("tqdm_total", 0),
            leave=True,
            ascii=sys.platform.startswith("win"),  # *shakes fist*
            unit="file",
        )

    for fromfile, newroot in gen:
        if not os.path.isdir(newroot):
            if op_args.get("verbose", False):
                log.info("mkdir {}".format(newroot))
            os.makedirs(newroot)
        op(fromfile, newroot, **op_args)
        if prog:
            prog.update(1)
    if prog:
        prog.close()


def safe_rmtree(dirpath):
    for root, dirs, files in os.walk(dirpath, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def RemoveExcessiveWhitespace(text):
    return REG_EXCESSIVE_WHITESPACE.sub("", text)


def sizeof_fmt(num):
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def standardize_path(path):
    pathchunks = path.split("/")
    path = pathchunks[0]
    for chunk in pathchunks[1:]:
        path = os.path.join(path, chunk)
    return path


REG_DRIVELETTER = re.compile(r"^([A-Z]):\\")


def cygpath(inpath):
    chunks = inpath.split("\\")
    chunks[0] = chunks[0].lower()[:-1]
    return "/cygdrive/" + "/".join(chunks)


"""
def _autoescape(string):
    if ' ' in string:
        return '"' + string + '"'
    else:
        return string
"""


def _args2str(cmdlist):
    # return ' '.join([_autoescape(x) for x in cmdlist])
    return " ".join([shlex.quote(x) for x in cmdlist])


def decompressFile(archive: os.PathLike, to: os.PathLike = ".", env=None, path7za: os.PathLike = "7za"):
    """
    Decompresses the file to the current working directory.

    Uses 7za for .7z and .rar files. (p7zip)
    """

    archive = str(archive)
    to = str(to)
    path7za = str(path7za)

    if env is None:
        env = ENV
    # print('Trying to decompress ' + archive)
    lc = archive.lower()
    if lc.endswith(".tar.gz") or lc.endswith(".tgz"):
        with tarfile.open(archive, mode="r:gz") as arch:
            arch.extractall(to)
        return True
    elif lc.endswith(".bz2") or lc.endswith(".tbz"):
        with tarfile.open(archive, mode="r:bz2") as arch:
            arch.extractall(to)
        return True
    elif lc.endswith(".tar.xz"):
        with tarfile.open(archive, mode="r:xz") as arch:
            arch.extractall(to)
        return True
    elif lc.endswith(".tar.7z"):
        cmd(
            [path7za, "x", "-aoa", "-o" + to, "--", archive],
            echo=True,
            show_output=False,
            critical=True,
        )
        with tarfile.open(archive[:-3], mode="r") as arch:
            arch.extractall(to)
        os.remove(archive[:-3])
        return True
    elif lc.endswith(".gz"):
        with tarfile.open(archive, mode="r:gz") as arch:
            arch.extractall(to)
    elif lc.endswith(".7z"):
        if PLATFORM == "Windows":
            archive = cygpath(archive)
        cmd(
            [path7za, "x", "-aoa", "-o" + to, "--", archive],
            echo=True,
            show_output=False,
            critical=True,
        )
    elif lc.endswith(".zip"):
        with zipfile.ZipFile(archive) as arch:
            arch.extractall(to)
        return True
    elif lc.endswith(".rar"):
        cmd(
            [path7za, "x", "-aoa", "-o" + to, "--", archive],
            echo=True,
            show_output=False,
            critical=True,
        )
    else:
        log.critical("decompressFile(): Unknown file extension: %s", archive)
    return False


def del_empty_dirs(src_dir: str, quiet=False) -> int:
    """
    Removes empty directories.

    :param src_dir:
        Root of directory tree to search for empty directories.
    :param quiet:
        Squelches log messages about removing empty directories.
    :returns:
        Count of removed directories.
    """
    ndeleted = -1
    totalDel = 0
    while ndeleted != 0:
        ndeleted = 0
        # Listing the files
        for dirpath, dirnames, filenames in os.walk(src_dir, topdown=False):
            # print(dirpath, src_dir)
            if dirpath == src_dir:
                continue
            # print(dirpath, len(dirnames), len(filenames))
            if len(filenames) == 0 and len(dirnames) == 0:
                if not quiet:
                    log.info("Removing %s (empty)...", dirpath)
                os.rmdir(dirpath)
                ndeleted += 1
                totalDel += 1
    return totalDel


def get_file_list(root_dir: str, start: str = None, prefix: str = "") -> list:
    """
    Gets all files in a directory, including in subdirectories.
    :param root_dir:
        Root of directory tree to search for files.
    :param start:
        start parameter for `os.path.relpath()`.
    :param prefix:
        Prefix to append to each returned file path.
    :returns:
        List of files.
    """
    output = []
    if start is None:
        start = root_dir
    for root, _, files in os.walk(root_dir):
        for filename in files:
            rpath = os.path.relpath(os.path.abspath(os.path.join(root, filename)), start)
            if prefix is not None:
                rpath = os.path.join(prefix, rpath)
            output += [rpath]
    return output


def detect_encoding(filename: str) -> typing.List:
    """
    Attempts to detect encoding of filename using chardet.
    """
    import chardet

    toread = min(32, os.path.getsize(filename))
    raw = b""
    with open(filename, "rb") as f:
        raw = f.read(toread)
    encoding = "utf-8-sig"
    bom = False
    if raw.startswith(codecs.BOM_UTF8):
        bom = True
        encoding = "utf-8-sig"
    else:
        result = chardet.detect(raw)
        encoding = result["encoding"]
        if encoding in ("utf-8", "ascii"):
            encoding = "utf-8-sig"
        if encoding in ("cp1252", "Windows-1252"):
            encoding = "cp1252"
    return encoding


def fix_encoding(filename, encoding="utf-8-sig"):
    # log.info('chardet guesses: {}'.format(encoding))
    if encoding in ("utf-8-sig", "cp1252"):
        with codecs.open(filename, "r", encoding=encoding) as inf:
            with codecs.open(filename + ".utf8", "w", encoding="utf-8-sig") as outf:
                for line in ftfy.fix_file(
                    inf,
                    fix_entities=False,
                    fix_latin_ligatures=False,
                    fix_character_width=False,
                    uncurl_quotes=False,
                ):
                    outf.write(line)
        # This is here because Windows 10 was locking files randomly.
        attempt = 0
        while attempt < 5:
            attempt += 1
            try:
                if os.path.isfile(filename):
                    os.remove(filename)
                break
            except PermissionError:
                log.error(
                    "[%d/%d] Failed to delete %s, trying again in 1s.",
                    attempt,
                    5,
                    filename,
                )
                time.sleep(0.5)
        shutil.move(filename + ".utf8", filename)
    return encoding


def is_windows():
    return platform.system() == "Windows"


def is_linux():
    return platform.system() == "Linux"


# def is_osx():
# Ha Ha fuck macs.


ENV = BuildEnv()

# Platform-specific extensions
if platform.system() == "Windows":
    import buildtools._os_utils_win32

    buildtools._os_utils_win32.cmd_output = cmd_output
    buildtools._os_utils_win32.ENV = ENV
    from buildtools._os_utils_win32 import WindowsEnv, getVSVars
else:
    import buildtools._os_utils_linux

    buildtools._os_utils_linux.cmd_output = cmd_output
    buildtools._os_utils_linux.ENV = ENV
    from buildtools._os_utils_linux import DpkgSearchFiles, GetDpkgShlibs, InstallDpkgPackages
