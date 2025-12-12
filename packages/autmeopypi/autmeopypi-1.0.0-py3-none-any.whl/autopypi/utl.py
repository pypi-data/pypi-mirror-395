import os
import sys
import shutil
import subprocess
import hashlib
import json
import re
import platform
import tempfile
from pathlib import Path
from datetime import datetime

class Utils:
    
    @staticmethod
    def run_cmd(cmd, cwd=None, capture=True, check=False):
        try:
            result = subprocess.run(
                cmd,
                shell=isinstance(cmd, str),
                cwd=cwd,
                capture_output=capture,
                text=True,
                check=check
            )
            return result
        except subprocess.CalledProcessError as e:
            return e
        except Exception as e:
            return None
    
    @staticmethod
    def file_exists(path):
        return os.path.isfile(path)
    
    @staticmethod
    def dir_exists(path):
        return os.path.isdir(path)
    
    @staticmethod
    def ensure_dir(path):
        os.makedirs(path, exist_ok=True)
        return path
    
    @staticmethod
    def remove_dir(path):
        if os.path.exists(path):
            shutil.rmtree(path)
    
    @staticmethod
    def copy_file(src, dst):
        shutil.copy2(src, dst)
    
    @staticmethod
    def copy_dir(src, dst):
        shutil.copytree(src, dst)
    
    @staticmethod
    def read_file(path, mode="r"):
        with open(path, mode) as f:
            return f.read()
    
    @staticmethod
    def write_file(path, content, mode="w"):
        with open(path, mode) as f:
            f.write(content)
    
    @staticmethod
    def read_json(path):
        with open(path, "r") as f:
            return json.load(f)
    
    @staticmethod
    def write_json(path, data, indent=2):
        with open(path, "w") as f:
            json.dump(data, f, indent=indent)
    
    @staticmethod
    def file_hash(path, algo="sha256"):
        h = hashlib.new(algo)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    
    @staticmethod
    def get_python_version():
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    
    @staticmethod
    def get_platform():
        return platform.system().lower()
    
    @staticmethod
    def is_termux():
        return os.path.exists("/data/data/com.termux")
    
    @staticmethod
    def is_android():
        return Utils.is_termux() or "android" in platform.platform().lower()
    
    @staticmethod
    def get_temp_dir():
        return tempfile.gettempdir()
    
    @staticmethod
    def get_home_dir():
        return str(Path.home())
    
    @staticmethod
    def timestamp():
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    @staticmethod
    def parse_version(version_str):
        match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_str)
        if match:
            return tuple(map(int, match.groups()))
        return (0, 0, 0)
    
    @staticmethod
    def bump_version(version_str, bump_type="patch"):
        major, minor, patch = Utils.parse_version(version_str)
        if bump_type == "major":
            return f"{major + 1}.0.0"
        elif bump_type == "minor":
            return f"{major}.{minor + 1}.0"
        else:
            return f"{major}.{minor}.{patch + 1}"
    
    @staticmethod
    def find_files(directory, pattern):
        from glob import glob
        return glob(os.path.join(directory, pattern), recursive=True)
    
    @staticmethod
    def get_size(path):
        if os.path.isfile(path):
            return os.path.getsize(path)
        total = 0
        for root, dirs, files in os.walk(path):
            for f in files:
                total += os.path.getsize(os.path.join(root, f))
        return total
    
    @staticmethod
    def format_size(size):
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    @staticmethod
    def clean_build_dirs(path):
        dirs_to_remove = ["build", "dist", "*.egg-info"]
        for pattern in dirs_to_remove:
            for d in Utils.find_files(path, pattern):
                Utils.remove_dir(d)
    
    @staticmethod
    def validate_package_name(name):
        pattern = r"^[a-zA-Z][a-zA-Z0-9_-]*$"
        return bool(re.match(pattern, name))
    
    @staticmethod
    def get_installed_packages():
        result = Utils.run_cmd([sys.executable, "-m", "pip", "list", "--format=json"])
        if result and result.returncode == 0:
            return json.loads(result.stdout)
        return []
    
    @staticmethod
    def is_package_installed(name):
        packages = Utils.get_installed_packages()
        return any(p["name"].lower() == name.lower() for p in packages)
    
    @staticmethod
    def install_package(name):
        return Utils.run_cmd([sys.executable, "-m", "pip", "install", name])
    
    @staticmethod
    def ensure_dependencies():
        deps = ["build", "twine", "wheel", "setuptools"]
        for dep in deps:
            if not Utils.is_package_installed(dep):
                Utils.install_package(dep)
