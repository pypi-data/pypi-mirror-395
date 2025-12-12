import os
import sys
import re
from autopypi.utl import Utils
from autopypi.cfg import Config
from autopypi.log import Logger

class chk:
    
    def __init__(self, path=None, cfg=None, log=None):
        self.path = path or os.getcwd()
        self.cfg = cfg or Config(self.path)
        self.log = log or Logger()
        self.dist = os.path.join(self.path, "dist")
        self.issues = []
        self.warns = []
    
    def dist_files(self):
        self.log.stp(1, 5, "Checking distribution files")
        
        fs = []
        fs.extend(Utils.find_files(self.dist, "*.tar.gz"))
        fs.extend(Utils.find_files(self.dist, "*.whl"))
        
        if not fs:
            self.issues.append("No distribution files found in dist/")
            self.log.res(False, "No distribution files found")
            return False
        
        self.log.res(True, f"Found {len(fs)} distribution file(s)")
        return True
    
    def twine(self):
        self.log.stp(2, 5, "Running twine check")
        
        res = Utils.run_cmd(
            [sys.executable, "-m", "twine", "check", f"{self.dist}/*"],
            cwd=self.path
        )
        
        if res and res.returncode == 0:
            self.log.res(True, "Twine check passed")
            return True
        
        if res and res.stdout:
            for ln in res.stdout.split("\n"):
                if "warning" in ln.lower():
                    self.warns.append(ln.strip())
                elif "error" in ln.lower() or "failed" in ln.lower():
                    self.issues.append(ln.strip())
        
        self.log.res(False, "Twine check failed")
        return False
    
    def meta(self):
        self.log.stp(3, 5, "Checking package metadata")
        
        prj = self.cfg.get_project_config()
        
        if not prj:
            self.issues.append("Could not parse project configuration")
            self.log.res(False, "Could not parse configuration")
            return False
        
        req = ["name", "version"]
        miss = [f for f in req if not prj.get(f)]
        
        if miss:
            self.issues.append(f"Missing required fields: {', '.join(miss)}")
            self.log.res(False, f"Missing: {', '.join(miss)}")
            return False
        
        rec = ["description", "authors", "license"]
        miss_rec = [f for f in rec if not prj.get(f)]
        
        if miss_rec:
            self.warns.append(f"Missing recommended fields: {', '.join(miss_rec)}")
        
        self.log.res(True, "Required metadata present")
        return True
    
    def ver_fmt(self):
        self.log.stp(4, 5, "Checking version format")
        
        prj = self.cfg.get_project_config()
        ver = prj.get("version", "") if prj else ""
        
        pep = r"^(\d+!)?\d+(\.\d+)*((a|b|rc)\d+)?(\.post\d+)?(\.dev\d+)?$"
        
        if not re.match(pep, ver):
            self.warns.append(f"Version '{ver}' may not be PEP 440 compliant")
            self.log.res(False, f"Version format warning: {ver}")
            return False
        
        self.log.res(True, f"Version {ver} is valid")
        return True
    
    def readme(self):
        self.log.stp(5, 5, "Checking README")
        
        rfs = ["README.md", "README.rst", "README.txt", "README"]
        found = None
        
        for rf in rfs:
            p = os.path.join(self.path, rf)
            if Utils.file_exists(p):
                found = p
                break
        
        if not found:
            self.warns.append("No README file found")
            self.log.res(False, "No README found")
            return False
        
        txt = Utils.read_file(found)
        if len(txt) < 100:
            self.warns.append("README is very short")
        
        self.log.res(True, f"Found {os.path.basename(found)}")
        return True
    
    def lic(self):
        lfs = ["LICENSE", "LICENSE.txt", "LICENSE.md", "LICENCE"]
        
        for lf in lfs:
            if Utils.file_exists(os.path.join(self.path, lf)):
                return True
        
        self.warns.append("No LICENSE file found")
        return False
    
    def run(self):
        self.log.hdr("Checking Package")
        self.issues = []
        self.warns = []
        
        res = {
            "dist": self.dist_files(),
            "twine": self.twine() if self.dist_files() else False,
            "meta": self.meta(),
            "ver": self.ver_fmt(),
            "readme": self.readme(),
            "lic": self.lic()
        }
        
        if self.warns:
            self.log.wrn(f"Found {len(self.warns)} warning(s)")
            for w in self.warns:
                self.log.wrn(f"  - {w}")
        
        if self.issues:
            self.log.err(f"Found {len(self.issues)} issue(s)")
            for i in self.issues:
                self.log.err(f"  - {i}")
            return False
        
        self.log.ok("All checks passed")
        return True
    
    def report(self):
        return {
            "issues": self.issues.copy(),
            "warns": self.warns.copy(),
            "ok": len(self.issues) == 0
        }
