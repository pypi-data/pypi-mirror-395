import os
import sys
from autopypi.utl import Utils
from autopypi.cfg import Config
from autopypi.log import Logger
from autopypi.chk import chk

class upl:
    
    PYPI = "https://upload.pypi.org/legacy/"
    TEST = "https://test.pypi.org/legacy/"
    
    def __init__(self, path=None, cfg=None, log=None):
        self.path = path or os.getcwd()
        self.cfg = cfg or Config(self.path)
        self.log = log or Logger()
        self.checker = chk(self.path, self.cfg, self.log)
        self.dist = os.path.join(self.path, "dist")
    
    def _cmd(self, fs, url, usr, pwd):
        cmd = [sys.executable, "-m", "twine", "upload"]
        cmd.extend(["--repository-url", url])
        
        if usr and pwd:
            cmd.extend(["--username", usr])
            cmd.extend(["--password", pwd])
        
        if self.cfg.get("skip_existing"):
            cmd.append("--skip-existing")
        
        if self.cfg.get("verbose"):
            cmd.append("--verbose")
        
        if self.cfg.get("non_interactive"):
            cmd.append("--non-interactive")
        
        cmd.extend(fs)
        return cmd
    
    def run(self, tok=None, usr=None, pwd=None, test=False, fs=None, chk_first=True):
        repo = "TestPyPI" if test else "PyPI"
        self.log.hdr(f"Uploading to {repo}")
        
        if fs:
            dist_fs = fs
        else:
            dist_fs = []
            dist_fs.extend(Utils.find_files(self.dist, "*.tar.gz"))
            dist_fs.extend(Utils.find_files(self.dist, "*.whl"))
        
        if not dist_fs:
            self.log.err("No distribution files found")
            return False
        
        self.log.inf(f"Found {len(dist_fs)} file(s) to upload")
        
        if chk_first:
            if not self.checker.run():
                self.log.err("Pre-upload check failed")
                return False
        
        creds = self.cfg.get_credentials(tok, usr, pwd)
        
        if not creds:
            self.log.err("No credentials provided")
            self.log.inf("Use --token, --username/--password, or set PYPI_TOKEN env var")
            return False
        
        url = self.TEST if test else self.PYPI
        
        if creds.get("pypirc"):
            self.log.inf("Using credentials from ~/.pypirc")
            cmd = [sys.executable, "-m", "twine", "upload"]
            if test:
                cmd.extend(["--repository", "testpypi"])
            cmd.extend(dist_fs)
        else:
            cmd = self._cmd(dist_fs, url, creds.get("username"), creds.get("password"))
        
        self.log.stp(1, 1, "Uploading packages")
        
        safe = cmd.copy()
        for i, a in enumerate(safe):
            if a == "--password" and i + 1 < len(safe):
                safe[i + 1] = "***"
        self.log.dbg(f"Command: {' '.join(safe)}")
        
        res = Utils.run_cmd(cmd, cwd=self.path)
        
        if res and res.returncode == 0:
            self.log.res(True, f"Successfully uploaded to {repo}")
            
            prj = self.cfg.get_project_config()
            if prj:
                nm = prj.get("name", "")
                if test:
                    link = f"https://test.pypi.org/project/{nm}/"
                else:
                    link = f"https://pypi.org/project/{nm}/"
                self.log.inf(f"View at: {link}")
            
            self._save(True, dist_fs, repo)
            return True
        
        self.log.res(False, "Upload failed")
        if res:
            if res.stdout:
                self.log.err(res.stdout)
            if res.stderr:
                self.log.err(res.stderr)
        
        self._save(False, dist_fs, repo, res.stderr if res else "Unknown error")
        return False
    
    def sdist_only(self, **kw):
        fs = Utils.find_files(self.dist, "*.tar.gz")
        return self.run(fs=fs, **kw)
    
    def wheel_only(self, **kw):
        fs = Utils.find_files(self.dist, "*.whl")
        return self.run(fs=fs, **kw)
    
    def _save(self, ok, fs, repo, err=None):
        log_dir = os.path.join(self.path, ".autopypi", "uploads")
        Utils.ensure_dir(log_dir)
        
        log_f = os.path.join(log_dir, f"upload_{Utils.timestamp()}.json")
        
        data = {
            "ts": Utils.timestamp(),
            "ok": ok,
            "repo": repo,
            "files": [os.path.basename(f) for f in fs],
            "err": err
        }
        
        Utils.write_json(log_f, data)
    
    def history(self, lim=10):
        log_dir = os.path.join(self.path, ".autopypi", "uploads")
        
        if not Utils.dir_exists(log_dir):
            return []
        
        logs = sorted(
            Utils.find_files(log_dir, "*.json"),
            key=os.path.getmtime,
            reverse=True
        )[:lim]
        
        hist = []
        for lg in logs:
            try:
                hist.append(Utils.read_json(lg))
            except:
                pass
        
        return hist
    
    def show_history(self):
        hist = self.history()
        
        if not hist:
            self.log.inf("No upload history found")
            return
        
        hdrs = ["Date", "Repository", "Status", "Files"]
        rows = [
            [h["ts"], h["repo"], "OK" if h["ok"] else "FAIL", ", ".join(h["files"])]
            for h in hist
        ]
        
        self.log.tbl(hdrs, rows)
