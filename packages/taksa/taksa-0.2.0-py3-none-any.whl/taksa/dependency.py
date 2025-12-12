import os, sys, subprocess, hashlib, tarfile, shutil, glob, progressbar, urllib.request, shutil, requests, argparse
from pathlib import Path
from subprocess import run
from multiprocessing import cpu_count
from ctypes import *
from glob import glob
from io import StringIO
from typing import List, Dict, Optional, Tuple

from urllib.parse import urlparse
from .configuration import Configuration
from .configuration import BuildType




### Green color message
def info(msg):
    print("\033[32m[INFO] " + msg + "\033[00m", flush=True)

### Red color message + abort
def fatal(msg):
    print("\033[31m[FATAL] " + msg + "\033[00m", flush=True)
    sys.exit(2)

### Equivalent to mkdir -p
def mkdir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def cd(path):
    os.chdir(os.path.join(os.getcwd(), path))




class Dependency:
    def __init__(self):
        self.dependencies = [Dependency]
    def download(self):
        pass
    def remove(self):
        pass
    def make(self, build_type: BuildType):
        pass
    def clean(self, build_type: BuildType):
        pass
    def configure(self, build_type: BuildType):
        pass
    def build(self, build_type: BuildType):
        pass
    def install(self, build_type: BuildType):
        pass
    pass


class CppCMakeDependency(Dependency):
    def __init__(self, git_url: str):
        self.custom_build_flags: Dict[str, str] = {}
        pwd = str(os.getcwd())
        self.tp = os.path.join(pwd, Configuration.THIRDPARTY_DIR_NAME)

        parsed_uri = urlparse(git_url)
        self.name = Path(os.path.basename(parsed_uri.path)).stem
        self.path = os.path.join(self.tp, self.name)
        self.git_url = git_url

        self.version: str | None = None
        self.tag_prefix: str = ""

        self._configure_temporary_pathes()

    def set_version(self, version_str: str):
        self.version = version_str
        return self

    def set_tag_prefix(self, prefix: str):
        self.tag_prefix = prefix
        return self

    def set_custom_build_flags(self, flags: Dict[str, str]):
        self.custom_build_flags = flags
        return self

    def download(self):
        if os.path.exists(self.path) and len(os.listdir(self.path)) != 0:
            return

        info(f"Clone {self.name} into {self.path}")

        if self.version is None:
            run(["git", "clone", self.git_url, self.path])
            return

        tag = f"{self.tag_prefix}{self.version}"

        clone_result = run([
            "git", "clone", "--recursive",
            "-b", tag,
            self.git_url, self.path
        ])

        if clone_result.returncode != 0:
            info(
                f"Cloning with tag '{tag}' failed. "
                f"Retrying with raw version '{self.version}'"
            )

            run([
                "git", "clone", "--recursive",
                "-b", self.version,
                self.git_url, self.path
            ])

    def remove(self):
        if os.path.exists(self.path) and os.path.isdir(self.path):
            shutil.rmtree(self.path)

    def make(self, build_type: BuildType):
        self.configure(build_type)
        self.build(build_type)
        self.install(build_type)

    def build(self, build_type: BuildType):
        build_path = self._get_build_dir_path(build_type)
        if not os.path.exists(build_path):
            raise FileNotFoundError("Build directory not found: " + build_path)
        if len(os.listdir(build_path)) != 0:
            info(f"{build_path} is not empty, skip make -j {str(Configuration.NPROC)}")
            return
        os.chdir(build_path)
        run(["make", "-j", str(Configuration.NPROC)], check=True)
        os.chdir(self.tp)

    def configure(self, build_type: BuildType):
        build_path = self._get_build_dir_path(build_type)
        install_path = self._get_install_dir_path(build_type)

        if os.path.exists(build_path):
            shutil.rmtree(build_path)
        mkdir(build_path)

        os.chdir(build_path)
        run([
            "cmake",
            f"-DCMAKE_INSTALL_PREFIX={install_path}",
            f"-DCMAKE_BUILD_TYPE={build_type.to_str()}",
            *[
                f"-D{custom_flag}={custom_value}"
                for custom_flag, custom_value in self.custom_build_flags.items()
            ],
            ".."
        ], check=True)
        os.chdir(self.tp)

    def install(self, build_type: BuildType):
        build_path = self._get_build_dir_path(build_type)
        install_path = self._get_install_dir_path(build_type)
        if not os.path.exists(build_path):
            raise FileNotFoundError("Build directory not found: " + build_path)
        if os.path.exists(install_path) and len(os.listdir(install_path)) != 0:
            info(f"Install directory {install_path} is not empty, skip make install")
            return
        os.chdir(build_path)
        run(["make", "install"], check=True)
        os.chdir(self.tp)

    def _configure_temporary_pathes(self):
        self.build_path = os.path.join(self.path, Configuration.BUILD_DIR_NAME)
        self.install_path = os.path.join(self.path, Configuration.INSTALL_DIR_NAME)

    def _get_build_dir_path(self, build_type: BuildType):
        return self.build_path + build_type.to_path()

    def _get_install_dir_path(self, build_type: BuildType):
        return self.install_path + build_type.to_path()

class HppCMakeDependency(Dependency):
    def __init__(
        self,
        name: str,
        target_dir_name: Optional[str] = None,
    ):
        super().__init__()
        pwd = str(os.getcwd())
        self.tp = os.path.join(pwd, Configuration.THIRDPARTY_DIR_NAME)

        self.name = name

        self.path = os.path.join(self.tp, target_dir_name or name)

        self.version: str | None = None

        self.git_url: Optional[str] = None
        self.git_tag_prefix: str = ""
        self._copy_mappings: List[Tuple[str, str]] = []

        self.single_header_url: Optional[str] = None
        self.single_header_filename: Optional[str] = None

    def set_version(self, version_str: str):
        self.version = version_str
        return self

    def set_git_source(
        self,
        git_url: str,
        tag_prefix: str = "",
        copy_mappings: Optional[List[Tuple[str, str]]] = None,
    ):
        """
        git_url: repo URL
        tag_prefix: prefix to prepend to version (e.g. "v" -> tag "v1.2.3")
        copy_mappings: list of (src_rel, dst_rel) relative paths inside repo.

        src_rel is relative to the cloned repo root.
        dst_rel is relative to self.path.
        """
        self.git_url = git_url
        self.git_tag_prefix = tag_prefix
        self._copy_mappings = copy_mappings or []
        return self

    def set_single_header_source(
        self,
        header_url: str,
        header_filename: Optional[str] = None,
    ):
        self.single_header_url = header_url
        if header_filename is not None:
            self.single_header_filename = header_filename
        else:
            parsed = urlparse(header_url)
            self.single_header_filename = os.path.basename(parsed.path)
        return self

    def download(self):
        if os.path.exists(self.path) and os.listdir(self.path):
            return

        mkdir(self.path)

        if self.single_header_url is not None:
            self._download_single_header()
        elif self.git_url is not None:
            self._download_from_git()
        else:
            fatal(f"HppCMakeDependency '{self.name}' has no download source configured")

    def remove(self):
        if os.path.exists(self.path) and os.path.isdir(self.path):
            shutil.rmtree(self.path)

    def make(self, build_type: BuildType):
        self.download()

    def clean(self, build_type: BuildType):
        self.remove()

    def configure(self, build_type: BuildType):
        pass

    def build(self, build_type: BuildType):
        pass

    def install(self, build_type: BuildType):
        pass

    def _download_single_header(self):
        assert self.single_header_url is not None
        assert self.single_header_filename is not None

        info(f"Downloading single header for '{self.name}' from {self.single_header_url}")
        dst = os.path.join(self.path, self.single_header_filename)
        urllib.request.urlretrieve(self.single_header_url, dst)

    def _download_from_git(self):
        assert self.git_url is not None

        from subprocess import run

        repo_tmp_path = self.path + "_repo"

        if os.path.exists(repo_tmp_path):
            shutil.rmtree(repo_tmp_path)

        tag = None
        if self.version is not None:
            tag = f"{self.git_tag_prefix}{self.version}"

        info(f"Cloning '{self.name}' from {self.git_url}")
        clone_cmd = ["git", "clone", "--recursive"]
        if tag is not None:
            clone_cmd += ["-b", tag]
        clone_cmd += [self.git_url, repo_tmp_path]

        result = run(clone_cmd)
        if result.returncode != 0:
            fatal(f"Failed to clone {self.git_url} (tag='{tag}')")

        for src_rel, dst_rel in self._copy_mappings:
            src = os.path.join(repo_tmp_path, src_rel)
            dst = os.path.join(self.path, dst_rel)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                mkdir(os.path.dirname(dst))
                shutil.copy2(src, dst)

        shutil.rmtree(repo_tmp_path)

    @classmethod
    def from_git(
        cls,
        name: str,
        git_url: str,
        version: str,
        copy_mappings: List[Tuple[str, str]],
        tag_prefix: str = "",
        target_dir_name: Optional[str] = None,
    ) -> "HppCMakeDependency":
        dep = cls(name=name, target_dir_name=target_dir_name)
        dep.set_version(version)
        dep.set_git_source(git_url=git_url, tag_prefix=tag_prefix, copy_mappings=copy_mappings)
        return dep

    @classmethod
    def from_single_header(
        cls,
        name: str,
        header_url: str,
        header_filename: Optional[str] = None,
        target_dir_name: Optional[str] = None,
    ) -> "HppCMakeDependency":
        dep = cls(name=name, target_dir_name=target_dir_name)
        dep.set_single_header_source(header_url=header_url, header_filename=header_filename)
        return dep
