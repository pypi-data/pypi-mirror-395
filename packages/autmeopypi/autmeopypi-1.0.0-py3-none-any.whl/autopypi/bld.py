import os
import sys
import shutil
from autopypi.utl import Utils
from autopypi.cfg import Config
from autopypi.log import Logger
from autopypi.col import c

class bld:
    
    def __init__(self, path=None, cfg=None, log=None):
        self.path = path or os.getcwd()
        self.cfg = cfg or Config(self.path)
        self.log = log or Logger()
        self.dist = os.path.join(self.path, "dist")
        self.build = os.path.join(self.path, "build")
    
    def chk_req(self):
        self.log.stp(1, 4, "Checking requirements")
        
        if not self.cfg.has_pyproject() and not self.cfg.has_setup_py():
            self.log.res(False, "No pyproject.toml or setup.py found")
            return False
        
        self.log.res(True, "Project configuration found")
        
        Utils.ensure_dependencies()
        self.log.res(True, "Dependencies installed")
        
        return True
    
    def clean(self):
        self.log.stp(2, 4, "Cleaning previous builds")
        
        dirs = [self.dist, self.build]
        
        for p in Utils.find_files(self.path, "*.egg-info"):
            dirs.append(p)
        
        cnt = 0
        for d in dirs:
            if Utils.dir_exists(d):
                Utils.remove_dir(d)
                cnt += 1
        
        self.log.res(True, f"Cleaned {cnt} directories")
        return True
    
    def sdist(self):
        self.log.stp(3, 4, "Building source distribution")
        
        res = Utils.run_cmd(
            [sys.executable, "-m", "build", "--sdist", self.path],
            cwd=self.path
        )
        
        if res and res.returncode == 0:
            files = Utils.find_files(self.dist, "*.tar.gz")
            if files:
                sz = Utils.format_size(Utils.get_size(files[0]))
                self.log.res(True, f"Source distribution created ({sz})")
                return files[0]
        
        self.log.res(False, "Failed to build source distribution")
        if res and res.stderr:
            self.log.err(res.stderr)
        return None
    
    def wheel(self):
        self.log.stp(4, 4, "Building wheel distribution")
        
        res = Utils.run_cmd(
            [sys.executable, "-m", "build", "--wheel", self.path],
            cwd=self.path
        )
        
        if res and res.returncode == 0:
            files = Utils.find_files(self.dist, "*.whl")
            if files:
                sz = Utils.format_size(Utils.get_size(files[0]))
                self.log.res(True, f"Wheel distribution created ({sz})")
                return files[0]
        
        self.log.res(False, "Failed to build wheel distribution")
        if res and res.stderr:
            self.log.err(res.stderr)
        return None
    
    def run(self, src=True, whl=True, cln=True):
        self.log.hdr("Building Package")
        
        prj = self.cfg.get_project_config()
        if prj:
            self.log.inf(f"Package: {prj.get('name', 'Unknown')}")
            self.log.inf(f"Version: {prj.get('version', 'Unknown')}")
        
        if not self.chk_req():
            return None
        
        if cln:
            self.clean()
        else:
            Utils.ensure_dir(self.dist)
        
        out = {"sdist": None, "wheel": None}
        
        if src:
            out["sdist"] = self.sdist()
        
        if whl:
            out["wheel"] = self.wheel()
        
        done = [k for k, v in out.items() if v]
        if done:
            self.log.ok(f"Build complete: {', '.join(done)}")
        else:
            self.log.err("Build failed")
        
        return out
    
    def files(self):
        fs = []
        if Utils.dir_exists(self.dist):
            fs.extend(Utils.find_files(self.dist, "*.tar.gz"))
            fs.extend(Utils.find_files(self.dist, "*.whl"))
        return fs
    
    def info(self):
        fs = self.files()
        inf = {"dist": self.dist, "files": [], "size": 0}
        
        for f in fs:
            sz = Utils.get_size(f)
            inf["files"].append({
                "path": f,
                "name": os.path.basename(f),
                "size": sz,
                "fmt": Utils.format_size(sz),
                "hash": Utils.file_hash(f)
            })
            inf["size"] += sz
        
        inf["fmt"] = Utils.format_size(inf["size"])
        return inf
    
    def show(self):
        inf = self.info()
        
        if not inf["files"]:
            self.log.wrn("No distribution files found")
            return
        
        hdrs = ["File", "Size", "SHA256"]
        rows = [[f["name"], f["fmt"], f["hash"][:16] + "..."] for f in inf["files"]]
        
        self.log.tbl(hdrs, rows)
        self.log.inf(f"Total size: {inf['fmt']}")
