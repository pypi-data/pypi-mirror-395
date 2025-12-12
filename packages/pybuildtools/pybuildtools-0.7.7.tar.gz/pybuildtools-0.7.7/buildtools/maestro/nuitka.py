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
Nuitka BuildTarget

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

import datetime
import importlib.abc
import importlib.util
import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Optional, Set, Tuple, Union

# import subprocess_tee
from nuitka.plugins import Plugins as NuitkaPlugins
from nuitka.plugins.PluginBase import NuitkaPluginBase

from buildtools import os_utils
from buildtools.maestro.base_target import SingleBuildTarget

from buildtools.bt_logging import IndentLogger  # isort: skip

log = IndentLogger(logging.getLogger(__name__))

DEBUG: bool = False


class NuitkaTarget(SingleBuildTarget):
    BT_LABEL = "NUITKA"

    _CACHED_ALWAYS_ENABLED_PLUGINS: Optional[Set[str]] = None

    def __init__(
        self,
        entry_point: Union[str, Path],
        package_name: str,
        files: List[Union[str, Path]],
        dependencies: List[Union[str, Path]] = [],
        tmp_dir: Optional[Union[str, Path]] = None,
        single_file: bool = True,
        nuitka_subdir: Optional[Union[str, Path]] = None,
    ) -> None:
        if tmp_dir is None:
            tmp_dir = Path(".tmp")
        else:
            tmp_dir = Path(tmp_dir)
        self.python_path: Path = Path(sys.executable)
        self.entry_point: Path = Path(entry_point)
        self.package_name: str = package_name
        self.out_dir: Path = tmp_dir / "nuitka"
        if nuitka_subdir:
            self.out_dir = self.out_dir / nuitka_subdir
        self.dist_dir: Path = self.out_dir / f"{self.package_name}.dist"
        self.singlefile: bool = single_file
        self.executable_mangled: Path = self.dist_dir / self.package_name if not single_file else (self.out_dir / self.package_name).with_suffix(".bin")

        if os.name == "nt":
            self.executable_mangled = self.executable_mangled.with_suffix(".exe")

        self.windows_disable_console: bool = False
        #: See Nuitka --windows-icon-from-ico for format
        self.windows_icon_from_ico: List[Union[str, Path]] = []
        self.windows_icon_from_exe: Optional[Union[str, Path]] = None
        self.windows_onefile_splash_image: Optional[Union[str, Path]] = None
        self.windows_uac_admin: bool = False
        self.windows_uac_uiaccess: bool = False

        self.product_name: str = "FIXME: Nuitka Executable"
        self.company_name: str = "FIXME: Nuitka Executable Contributors"
        self.file_version: Tuple[int, int, int, int] = (0, 0, 0, 0)
        self.product_version: Tuple[int, int, int, int] = (0, 0, 0, 0)
        self.file_description: str = "FIXME: Review target.product_name, target.company_name, target.file_version, target.trademarks, and target.file_description."
        self.trademarks: str = f"FIXME: Trademarks are the property of their respective owners. Set --trademarks."
        self.copyright: str = f"FIXME: Copyright ©{datetime.datetime.now().year} Company Name Here. All Rights Reserved. Set --copyright"

        self.linux_onefile_icon: Optional[Union[str, Path]] = None

        super().__init__(
            target=str(self.executable_mangled),
            files=list(map(str, files)),
            dependencies=list(map(str, dependencies)),
        )

        self.included_packages: Set[str] = set()
        self.included_modules: Set[str] = set()
        self.included_plugin_directories: Set[Path] = set()
        self.included_plugin_files: Set[str] = set()
        self.enabled_plugins: Set[str] = set()
        self._always_active_plugins: Set[str] = self.getAlwaysActivePluginNames()
        self.nofollow_imports: bool = False
        self.follow_import_to: List[str] = []
        self.nofollow_import_to: List[str] = []
        self.pgo: bool = False
        self.lto: bool = False
        self.python_flags: str = ""
        self.onefile_tempdir_spec: Optional[str] = None

        self.other_opts: List[str] = []

        self.legacy_launch: bool = False

    def getAlwaysActivePluginNames(self) -> Set[str]:
        if self._CACHED_ALWAYS_ENABLED_PLUGINS is None:
            log.debug(f"_CACHED_ALWAYS_ENABLED_PLUGINS is None, calculating...")
            self._CACHED_ALWAYS_ENABLED_PLUGINS = set()
            try:
                NuitkaPlugins.loadPlugins()
                # print(repr(NuitkaPlugins.getActivePlugins()))
                for plugin_name in sorted(NuitkaPlugins.plugin_name2plugin_classes):
                    plugin: NuitkaPluginBase = NuitkaPlugins.plugin_name2plugin_classes[plugin_name][0]
                    if plugin.isAlwaysEnabled():
                        self._CACHED_ALWAYS_ENABLED_PLUGINS.add(plugin.plugin_name)
            except Exception as e:
                log.critical("Error interfacing with Nuitka:")
                log.critical(e)
            log.debug(f"_CACHED_ALWAYS_ENABLED_PLUGINS = {self._CACHED_ALWAYS_ENABLED_PLUGINS!r}")
        return self._CACHED_ALWAYS_ENABLED_PLUGINS

    def getPathOfModuleOrDie(self, module_name: str) -> Path:
        if (modspec := importlib.util.find_spec(module_name)) is None:
            raise Exception(f"{module_name} could not be imported by importlib.util.find_spec. Check that you imported all dependencies.")
        ldr: importlib.abc.Loader = modspec.loader
        if not hasattr(ldr, "get_filename"):
            raise Exception(f"{module_name} is frozen or built-in and has no location on disk.")
        return Path(ldr.get_filename())

    def launchNuitkaFromCLI(
        self,
        opts: List[str],
        show_output: bool = True,
        user: Optional[str | int] = None,
        group: Optional[str | int] = None,
    ) -> subprocess.CompletedProcess:
        cmd: List[str] = [str(sys.executable), "-m", "nuitka"] + opts
        # os_utils.cmd(cmd, echo=self.should_echo_commands(), show_output=True, critical=True, globbify=False)
        return subprocess.run(
            cmd,
            stderr=subprocess.STDOUT,
            check=True,
            # tee=show_output,
            user=user,
            group=group,
        )

    def launchNuitkaWithNuitkaPlus(
        self,
        opts: List[str],
        show_output: bool = True,
        user: Optional[str | int] = None,
        group: Optional[str | int] = None,
    ) -> subprocess.CompletedProcess:
        # PATH_NUITKA_MAIN = self.getPathOfModuleOrDie('nuitka.__main__')
        PATH_NUITKA = self.getPathOfModuleOrDie("nuitka").parent.absolute()
        PATH_NUITKA_PLUS = self.getPathOfModuleOrDie("buildtools.cli.nuitka_plus").absolute()

        # See nuitka.utils.ReExecute.reExecuteNuitka.
        # This is pretty much verbatim, with a few tweaks for compatibility and standards.
        args: List[str] = [
            sys.executable,
            sys.executable,
        ]  # Not sure why this is set twice...

        # if sys.version_info >= (3, 7) and sys.flags.utf8_mode:
        # Version is always true, so removed.
        if sys.flags.utf8_mode:
            args += ["-X", "utf8"]

        # if "nuitka.__main__" in sys.modules:
        #     our_filename = sys.modules["nuitka.__main__"].__file__
        # else:
        #     our_filename = sys.modules["__main__"].__file__

        # args += ["-S", our_filename]
        args += ["-S", str(PATH_NUITKA_PLUS)]

        # os.environ["NUITKA_BINARY_NAME"] = sys.modules["__main__"].__file__
        os.environ["NUITKA_BINARY_NAME"] = str(PATH_NUITKA_PLUS)

        # os.environ["NUITKA_PACKAGE_HOME"] = os.path.dirname(
        #     os.path.abspath(sys.modules["nuitka"].__path__[0])
        # )
        os.environ["NUITKA_PACKAGE_HOME"] = str(PATH_NUITKA)

        # if pgo_filename is not None:
        #     args.append("--pgo-python-input=%s" % pgo_filename)
        # else:
        #     os.environ["NUITKA_SYS_PREFIX"] = sys.prefix
        os.environ["NUITKA_SYS_PREFIX"] = sys.prefix

        # # Same arguments as before.
        # args += sys.argv[1:]
        args += opts

        from nuitka.importing.PreloadedPackages import detectPreLoadedPackagePaths, detectPthImportedPackages

        os.environ["NUITKA_NAMESPACES"] = repr(detectPreLoadedPackagePaths())

        if "site" in sys.modules:
            site_filename = sys.modules["site"].__file__
            if site_filename.endswith(".pyc"):
                site_filename = site_filename[:-4] + ".py"

            os.environ["NUITKA_SITE_FILENAME"] = site_filename

            # Note: As side effect, this might modify the "sys.path" too.
            os.environ["NUITKA_PTH_IMPORTED"] = repr(detectPthImportedPackages())

        os.environ["NUITKA_PYTHONPATH"] = repr(sys.path)

        # In some environments, initial "sys.path" does not contain enough to load
        # "ast" module, which however we use to decode "NUITKA_PYTHONPATH", this
        # helps solve the chicken and egg problem.
        import ast

        os.environ["NUITKA_PYTHONPATH_AST"] = os.path.dirname(ast.__file__)

        if sys.flags.no_site:
            os.environ["NUITKA_NOSITE_FLAG"] = "1"

        os.environ["PYTHONHASHSEED"] = "0"

        os.environ["NUITKA_REEXECUTION"] = "1"

        # We use this instead of execl.
        tfn: Optional[str] = None
        try:
            with NamedTemporaryFile(mode="w+t", delete=False) as tf:
                data = {
                    "args": opts,
                    "environ": {
                        "PATH": os.environ["PATH"],
                    },
                }
                json.dump(data, tf)
                tfn = tf.name
            nuitka_cmd: List[str] = [
                str(sys.executable),
                "-m",
                "buildtools.cli.nuitka_plus",
                tfn,
            ]
            # os_utils.cmd(nuitka_cmd, echo=True, show_output=True, critical=True, globbify=False)
            return subprocess.run(
                nuitka_cmd,
                stderr=subprocess.STDOUT,
                check=True,
                # tee=show_output,
                user=user,
                group=group,
            )
        finally:
            if tfn and os.path.isfile(tfn):
                os.unlink(tfn)

    def getCommandLine(self) -> List[str]:
        opts: List[str] = [
            "--prefer-source-code",
            "--assume-yes-for-downloads",
        ]
        if os.name != "nt":
            opts.append("--static-libpython=yes")
        if self.nofollow_imports:
            opts.append("--nofollow-imports")
        if len(self.follow_import_to) > 0:
            # opts.append(f'--follow-import-to='+(','.join(self.recurse_to)))
            opts += [f"--follow-import-to={x}" for x in self.follow_import_to]
        if len(self.nofollow_import_to) > 0:
            # opts.append(f'--follow-import-to='+(','.join(self.recurse_to)))
            opts += [f"--nofollow-import-to={x}" for x in self.nofollow_import_to]
        for pkg in sorted(self.included_packages):
            opts.append(f"--include-package={pkg}")
        for pkg in sorted(self.included_modules):
            opts.append(f"--include-module={pkg}")
        for pd in sorted(self.included_plugin_directories):
            opts.append(f"--include-plugin-directory={pd}")
        for pf in sorted(self.included_plugin_files):
            opts.append(f"--include-plugin-files={pf}")
        # print('ENABLED', repr(self.enabled_plugins))
        # print('ALWAYS', repr(self._always_active_plugins))
        for plug in sorted(self.enabled_plugins - self._always_active_plugins):
            opts.append(f"--enable-plugin={plug}")
        if self.lto:
            opts.append("--lto=yes")
        if self.pgo:
            opts.append("--pgo")
        if len(self.python_flags) > 0:
            opts.append("--python-flags=" + self.python_flags)
        opts += [
            f"--output-dir={self.out_dir}",
            # '--show-progress', # *screaming*
            "--standalone",
        ]
        if self.singlefile:
            opts += ["--onefile"]
            if self.onefile_tempdir_spec is not None:
                opts.append(f"--onefile-tempdir-spec={self.onefile_tempdir_spec}")
            if os_utils.is_linux():
                if self.linux_onefile_icon is not None:
                    opts.append(f"--linux-onefile-icon={self.linux_onefile_icon}")
            if os_utils.is_windows():
                if self.windows_onefile_splash_image is not None:
                    opts.append(f"--onefile-windows-splash-screen-image={self.windows_onefile_splash_image}")

        if os_utils.is_windows():
            if self.windows_disable_console:
                opts.append("--windows-disable-console")
            if self.windows_icon_from_exe:
                opts.append(f"--windows-icon-from-exe={self.windows_icon_from_exe}")
            if len(self.windows_icon_from_ico) > 0:
                for ico_spec in self.windows_icon_from_ico:
                    opts.append(f"--windows-icon-from-ico={ico_spec}")
            if self.windows_uac_admin:
                opts.append("--windows-uac-admin")
            if self.windows_uac_uiaccess:
                opts.append("--windows-uac-uiaccess")
        opts += [
            f"--product-name={self.product_name}",
            f"--product-version=" + (".".join(map(str, self.product_version))),
            f"--company-name={self.company_name}",
            f"--file-version=" + (".".join(map(str, self.file_version))),
            f"--file-description={self.file_description}",
            f"--trademarks={self.trademarks}",
            f"--copyright={self.copyright}",
        ]
        opts += self.other_opts
        opts.append(str(self.entry_point))
        return opts

    def build(self, show_output: bool = True, user: Optional[str | int] = None, group: Optional[str | int] = None) -> None:
        if self.legacy_launch:
            self.launchNuitkaFromCLI(
                opts=self.getCommandLine(),
                show_output=show_output,
                user=user,
                group=group,
            )
        else:
            self.launchNuitkaWithNuitkaPlus(
                opts=self.getCommandLine(),
                show_output=show_output,
                user=user,
                group=group,
            )
