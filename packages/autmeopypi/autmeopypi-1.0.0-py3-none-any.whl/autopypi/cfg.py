import os
import json
import toml
from pathlib import Path
from autopypi.utl import Utils

class Config:
    
    DEFAULT_CONFIG = {
        "pypi_url": "https://upload.pypi.org/legacy/",
        "testpypi_url": "https://test.pypi.org/legacy/",
        "auto_clean": True,
        "auto_tag": False,
        "log_enabled": True,
        "log_dir": ".autopypi/logs",
        "dist_dir": "dist",
        "build_dir": "build",
        "check_before_upload": True,
        "verbose": False,
        "timeout": 300,
        "retry_count": 3,
        "parallel_uploads": False,
        "sign_packages": False,
        "sign_identity": None,
        "repository_url": None,
        "skip_existing": False,
        "non_interactive": False
    }
    
    def __init__(self, project_path=None):
        self.project_path = project_path or os.getcwd()
        self.config_file = os.path.join(self.project_path, ".autopypi", "config.json")
        self.config = self.DEFAULT_CONFIG.copy()
        self._load()
    
    def _load(self):
        if Utils.file_exists(self.config_file):
            try:
                user_config = Utils.read_json(self.config_file)
                self.config.update(user_config)
            except:
                pass
    
    def save(self):
        Utils.ensure_dir(os.path.dirname(self.config_file))
        Utils.write_json(self.config_file, self.config)
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save()
    
    def reset(self):
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
    
    def has_pyproject(self):
        return Utils.file_exists(os.path.join(self.project_path, "pyproject.toml"))
    
    def has_setup_py(self):
        return Utils.file_exists(os.path.join(self.project_path, "setup.py"))
    
    def has_setup_cfg(self):
        return Utils.file_exists(os.path.join(self.project_path, "setup.cfg"))
    
    def get_project_config(self):
        if self.has_pyproject():
            return self._parse_pyproject()
        elif self.has_setup_py():
            return self._parse_setup_py()
        return None
    
    def _parse_pyproject(self):
        path = os.path.join(self.project_path, "pyproject.toml")
        try:
            data = toml.load(path)
            project = data.get("project", {})
            return {
                "name": project.get("name"),
                "version": project.get("version"),
                "description": project.get("description"),
                "authors": project.get("authors", []),
                "requires_python": project.get("requires-python"),
                "dependencies": project.get("dependencies", []),
                "classifiers": project.get("classifiers", []),
                "keywords": project.get("keywords", []),
                "license": project.get("license"),
                "readme": project.get("readme"),
                "urls": project.get("urls", {}),
                "scripts": project.get("scripts", {}),
                "entry_points": project.get("entry-points", {})
            }
        except:
            return None
    
    def _parse_setup_py(self):
        path = os.path.join(self.project_path, "setup.py")
        try:
            content = Utils.read_file(path)
            import ast
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if hasattr(node.func, "id") and node.func.id == "setup":
                        return self._extract_setup_args(node)
            return None
        except:
            return None
    
    def _extract_setup_args(self, node):
        result = {}
        for kw in node.keywords:
            if isinstance(kw.value, ast.Constant):
                result[kw.arg] = kw.value.value
            elif isinstance(kw.value, ast.List):
                result[kw.arg] = [
                    e.value for e in kw.value.elts 
                    if isinstance(e, ast.Constant)
                ]
        return result
    
    def update_version(self, new_version):
        if self.has_pyproject():
            path = os.path.join(self.project_path, "pyproject.toml")
            data = toml.load(path)
            if "project" in data:
                data["project"]["version"] = new_version
            with open(path, "w") as f:
                toml.dump(data, f)
            return True
        elif self.has_setup_py():
            path = os.path.join(self.project_path, "setup.py")
            content = Utils.read_file(path)
            import re
            content = re.sub(
                r'version\s*=\s*["\'][^"\']+["\']',
                f'version="{new_version}"',
                content
            )
            Utils.write_file(path, content)
            return True
        return False
    
    def get_credentials(self, token=None, username=None, password=None):
        if token:
            return {"username": "__token__", "password": token}
        
        if username and password:
            return {"username": username, "password": password}
        
        env_token = os.environ.get("PYPI_TOKEN") or os.environ.get("TWINE_PASSWORD")
        if env_token:
            return {"username": "__token__", "password": env_token}
        
        env_user = os.environ.get("TWINE_USERNAME")
        env_pass = os.environ.get("TWINE_PASSWORD")
        if env_user and env_pass:
            return {"username": env_user, "password": env_pass}
        
        pypirc = os.path.expanduser("~/.pypirc")
        if Utils.file_exists(pypirc):
            return {"pypirc": True}
        
        return None
    
    def get_repository_url(self, test=False):
        if self.config.get("repository_url"):
            return self.config["repository_url"]
        return self.config["testpypi_url"] if test else self.config["pypi_url"]
    
    def create_pypirc(self, username, password, test=False):
        pypirc_path = os.path.expanduser("~/.pypirc")
        repo_name = "testpypi" if test else "pypi"
        url = self.get_repository_url(test)
        content = f"""[distutils]
index-servers =
    {repo_name}

[{repo_name}]
repository = {url}
username = {username}
password = {password}
"""
        Utils.write_file(pypirc_path, content)
        os.chmod(pypirc_path, 0o600)
        return pypirc_path
    
    def to_dict(self):
        return self.config.copy()
    
    def __repr__(self):
        return f"Config({self.project_path})"
