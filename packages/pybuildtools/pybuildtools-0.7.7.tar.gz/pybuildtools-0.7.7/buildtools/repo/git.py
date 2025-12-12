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
Created on Mar 28, 2015

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
import os
from typing import Dict, List, Optional

from buildtools.bt_logging import log
from buildtools.os_utils import ENV, BuildEnv, Chdir, cmd_out
from buildtools.repo.base import SCMRepository
from buildtools.types import StrOrPath
from buildtools.wrapper.git import Git


class GitRemoteInfo(object):
    def __init__(self):
        self.id = ""
        self.fetch_uri = ""
        self.push_uri = ""
        self.head_branch = "master"
        self.branches = []
        self.fetched = False

    def findBranch(self, name):
        if name == "HEAD":
            name = self.head_branch
        elif "/" not in name:
            return self.findBranch("refs/heads/" + name)
        return name


class GitRepository(SCMRepository):
    """Logical representation of a git repository."""

    def __init__(
        self,
        path: str,
        origin_uri: str,
        quiet: bool = True,
        noisy_clone: bool = False,
        submodule: bool = False,
        owner: Optional[str | int] = None,
        group: Optional[str | int] = None,
        git_executable: StrOrPath = "git",
    ) -> None:
        super().__init__(
            path,
            quiet=quiet,
            noisy_clone=noisy_clone,
            owner=owner,
            group=group,
        )

        self.git_executable: StrOrPath = git_executable

        # Known remotes.
        origin = GitRemoteInfo()
        origin.id = "origin"
        origin.fetch_uri = origin.push_uri = origin_uri
        origin.head_branch = "HEAD"
        self.remotes = self.orig_remotes = {"origin": origin}
        self.submodule = submodule

        # Git configuration variables.
        self.config_vars: Dict[str, str] = {}

        self.current_branch: Optional[str] = None
        self.current_commit: Optional[str] = None
        self.remote_commit: Optional[str] = None

        self.noPasswordEnv: BuildEnv = ENV.clone()
        self.noPasswordEnv.noisy = True
        self.noPasswordEnv.set("GIT_TERMINAL_PROMPT", "0")

    def _git(self, args: List[str], echo: bool = False) -> Optional[str]:
        return cmd_out(
            [str(self.git_executable)] + args,
            echo=echo,
            env=self.noPasswordEnv,
            user=self.owner,
            group=self.group,
        )

    def _syncRemote(self, remoteID: str, quiet: Optional[bool] = None) -> GitRemoteInfo:
        """
        $ git remote show origin
        * remote origin
          Fetch URL: https://github.com/d3athrow/vgstation13.git
          Push  URL: https://github.com/d3athrow/vgstation13.git
          HEAD branch: Bleeding-Edge
          Remote branches:
            Bleeding-Edge                                         tracked
        returns:
          GitRemoteInfo()
        """
        o = GitRemoteInfo()
        o.id = remoteID
        if quiet is None:
            quiet = self.quiet
        out = self._git(["remote", "show", remoteID], echo=not quiet)
        in_branches = False
        if out is not None:
            for oline in out.split("\n"):
                line = oline.strip()
                if not quiet:
                    print(oline)
                components = line.split()
                if not in_branches:
                    if line.startswith("Fetch URL:"):
                        o.fetch_uri = components[2]
                    if line.startswith("Push URL:"):
                        o.push_uri = components[2]
                    if line.startswith("HEAD branch:"):
                        o.head_branch = components[2]
                    if line.startswith("Remote branches:"):
                        in_branches = True
                else:
                    o.branches.append(line.split(" ")[0])
        o.fetched = True
        return o

    def UpdateRemotes(
        self,
        remote=None,
        quiet=None,
    ) -> bool:
        if quiet is None:
            quiet = self.quiet
        if remote is not None:
            self.remotes[remote] = self._syncRemote(remote, quiet=quiet)
            return True
        out = self._git(["remote", "show"], echo=not quiet)
        if out is None:
            return True
        for oline in out.split("\n"):
            line = oline.strip()
            if not quiet or not quiet:
                print(oline)
            if line == "":
                continue
            if line.startswith("fatal:"):
                log.error("[git] " + line)
                return False
            self.remotes[line] = self._syncRemote(line, quiet=quiet)
        return True

    def GetRepoState(
        self,
        remote: Optional[str] = None,
        quiet: Optional[bool] = None,
    ):
        if quiet is None:
            quiet = self.quiet
        self.current_branch = None
        self.current_commit = None
        if not os.path.isdir(self.path):
            log.warn("Could not find %s.", self.path)
            return
        with Chdir(self.path, noisy=not quiet):
            if self.UpdateRemotes(remote, quiet=quiet):
                self.current_branch = Git.GetBranch(
                    quiet=not quiet,
                    sudo_as=str(self.owner) if self.owner is not None else None,
                )
                self.current_commit = Git.GetCommit(
                    short=False,
                    quiet=not quiet,
                    sudo_as=str(self.owner) if self.owner is not None else None,
                )

    def GetRemoteState(
        self,
        remote: str = "origin",
        branch: str = "HEAD",
        quiet: Optional[str] = None,
    ):
        if quiet is None:
            quiet = self.quiet
        with Chdir(self.path, noisy=not quiet):
            ret = self._git(
                ["fetch", "-q", "--all", "--prune", "--tags"],
                echo=not quiet,
            )
            if not ret:
                return False

            for line in ret.split("\n"):
                # if not quiet:
                #    print(line)
                line = line.strip()
                if line == "":
                    continue
                if line.startswith("fatal:"):
                    log.error("[git] " + line)
                    return False
            for _remote in self.remotes.values():
                _remote.fetched = False
            self.UpdateRemotes(remote=remote, quiet=quiet)
            if branch == "HEAD":
                branch = self.remotes[remote].findBranch(branch)
            remoteinfo = Git.LSRemote(remote, branch, quiet=quiet)
            if remoteinfo is None:
                return False
            if branch == "HEAD":
                ref = "HEAD"
            elif "/" not in branch:
                ref = "refs/heads/" + branch
            if ref in remoteinfo:
                self.remote_commit = remoteinfo[ref]
        return True

    def ResolveTag(self, tag: str) -> Optional[str]:
        with Chdir(self.path, noisy=not self.quiet):
            return self._resolveTagNoChdir(tag)

    def _resolveTagNoChdir(self, tag: str, quiet: Optional[bool] = None) -> Optional[str]:
        if quiet is None:
            quiet = self.quiet
        ret = self._git(
            ["rev-list", "-n", "1", "refs/tags/{}".format(tag)],
            echo=not quiet,
        )
        if not ret:
            return None
        for line in ret.split("\n"):
            line = line.strip()
            if line == "":
                continue
            if line.startswith("fatal:"):
                log.error("[git] " + line)
                return None
            return line.strip()
        return None

    def CheckForUpdates(
        self,
        remote: str = "origin",
        branch: str = "HEAD",
        commit: Optional[str] = None,
        tag: Optional[str] = None,
        quiet: Optional[bool] = None,
    ) -> bool:
        if quiet is None:
            quiet = self.quiet
        if not quiet:
            log.info("Checking %s for updates...", self.path)
        if not os.path.isdir(self.path):
            return True
        if tag is not None:
            commit = self.ResolveTag(tag)
        with log:
            self.GetRepoState(remote, quiet=quiet)
            if not self.GetRemoteState(remote, branch, quiet=quiet):
                return False
            if branch is not None and self.current_branch != branch:
                if not quiet:
                    log.info("Branch is wrong! %s (L) != %s (R)", self.current_branch, branch)
                return True
            targetCommit = commit is not None or self.remote_commit
            if self.current_commit != targetCommit:
                if not quiet:
                    log.info(
                        "Commit is out of date! %s (L) != %s (R)",
                        self.current_commit,
                        targetCommit,
                    )
                return True
        return False

    def UsesLFS(self) -> bool:
        gitattributes = os.path.join(self.path, ".gitattributes")
        if os.path.isfile(gitattributes):
            # *.zip filter=lfs diff=lfs merge=lfs -text
            with open(gitattributes, "r") as f:
                for line in f:
                    if "filter=lfs" in line:
                        return True
                    if "diff=lfs" in line:
                        return True
                    if "merge=lfs" in line:
                        return True
        return False

    def Pull(
        self,
        remote: str = "origin",
        branch: str = "HEAD",
        commit: Optional[str] = None,
        tag: Optional[str] = None,
        cleanup: bool = False,
    ) -> None:
        if branch == "HEAD":
            branch = self.remotes[remote].head_branch
        if self.submodule:
            log.error("Submodules should not call Pull!")
            return
        if not os.path.isdir(self.path):
            self._git(
                ["clone", self.remotes[remote].fetch_uri, self.path],
                echo=not self.quiet or self.noisy_clone,
            )
        with Chdir(self.path, noisy=not self.quiet):
            if cleanup:
                self._git(["clean", "-fdx"], echo=not self.quiet)
                self._git(["reset", "--hard"], echo=not self.quiet)
            if self.current_branch != branch:
                ref = "remotes/{}/{}".format(remote, branch)
                self._git(
                    ["checkout", "-B", branch, ref, "--"],
                    echo=not self.quiet,
                )
            if tag is not None:
                commit = self._resolveTagNoChdir(tag)
            if commit is not None:
                self._git(["checkout", commit], echo=not self.quiet)
            else:
                if self.current_commit != self.remote_commit:
                    self._git(
                        ["reset", "--hard", "{}/{}".format(remote, branch)],
                        echo=not self.quiet,
                    )
            # if self.UsesLFS():
            #     log.info("git-lfs detected!")
            #     self._git(["lfs", "pull"], echo=not self.quiet)
        return

    def UpdateSubmodules(self, remote: bool = False) -> None:
        with log.info("Updating submodules in %s...", self.path):
            with Chdir(self.path, noisy=not self.quiet):
                if os.path.isfile(".gitmodules"):
                    more_flags = []
                    if remote:
                        more_flags.append("--remote")
                    self._git(
                        ["submodule", "update", "--init", "--recursive"] + more_flags,
                        echo=not self.quiet,
                    )

    def Update(self, cleanup: bool = False) -> None:
        return self.Pull(cleanup=cleanup)
