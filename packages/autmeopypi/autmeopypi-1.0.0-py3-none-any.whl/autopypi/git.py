import os
import re
from autopypi.utl import Utils
from autopypi.log import Logger

class git:
    
    def __init__(self, path=None, log=None):
        self.path = path or os.getcwd()
        self.log = log or Logger()
    
    def is_repo(self):
        return Utils.dir_exists(os.path.join(self.path, ".git"))
    
    def init(self):
        if self.is_repo():
            return True
        res = Utils.run_cmd(["git", "init"], cwd=self.path)
        return res and res.returncode == 0
    
    def branch(self):
        res = Utils.run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=self.path)
        if res and res.returncode == 0:
            return res.stdout.strip()
        return None
    
    def remote(self):
        res = Utils.run_cmd(["git", "remote", "get-url", "origin"], cwd=self.path)
        if res and res.returncode == 0:
            return res.stdout.strip()
        return None
    
    def tags(self):
        res = Utils.run_cmd(["git", "tag", "--list"], cwd=self.path)
        if res and res.returncode == 0:
            return res.stdout.strip().split("\n")
        return []
    
    def latest(self):
        res = Utils.run_cmd(["git", "describe", "--tags", "--abbrev=0"], cwd=self.path)
        if res and res.returncode == 0:
            return res.stdout.strip()
        return None
    
    def tag(self, name, msg=None):
        self.log.stp(1, 2, f"Creating tag: {name}")
        
        cmd = ["git", "tag", "-a", name, "-m", msg] if msg else ["git", "tag", name]
        res = Utils.run_cmd(cmd, cwd=self.path)
        
        if res and res.returncode == 0:
            self.log.res(True, f"Tag {name} created")
            return True
        
        self.log.res(False, "Failed to create tag")
        return False
    
    def push(self, name):
        self.log.stp(2, 2, f"Pushing tag: {name}")
        
        res = Utils.run_cmd(["git", "push", "origin", name], cwd=self.path)
        
        if res and res.returncode == 0:
            self.log.res(True, "Tag pushed to origin")
            return True
        
        self.log.res(False, "Failed to push tag")
        return False
    
    def release(self, ver, msg=None):
        self.log.hdr(f"Creating Release Tag v{ver}")
        
        name = f"v{ver}"
        
        if name in self.tags():
            self.log.wrn(f"Tag {name} already exists")
            return False
        
        if not msg:
            msg = f"Release version {ver}"
        
        if not self.tag(name, msg):
            return False
        
        if not self.push(name):
            return False
        
        self.log.ok(f"Release {name} created and pushed")
        return True
    
    def commits(self, tag=None):
        if not tag:
            tag = self.latest()
        
        cmd = ["git", "log", "--oneline"] if not tag else ["git", "log", f"{tag}..HEAD", "--oneline"]
        res = Utils.run_cmd(cmd, cwd=self.path)
        
        if res and res.returncode == 0:
            lns = res.stdout.strip().split("\n")
            return [ln for ln in lns if ln]
        return []
    
    def changelog(self, tag=None):
        cms = self.commits(tag)
        
        if not cms:
            return "No changes since last release"
        
        cats = {"feat": [], "fix": [], "docs": [], "style": [], "refactor": [], "test": [], "chore": [], "other": []}
        
        for cm in cms:
            pts = cm.split(" ", 1)
            if len(pts) < 2:
                continue
            
            h, msg = pts
            matched = False
            for pfx in cats:
                if msg.lower().startswith(f"{pfx}:") or msg.lower().startswith(f"{pfx}("):
                    cats[pfx].append(msg)
                    matched = True
                    break
            
            if not matched:
                cats["other"].append(msg)
        
        ttls = {"feat": "Features", "fix": "Bug Fixes", "docs": "Documentation", "style": "Style",
                "refactor": "Refactoring", "test": "Tests", "chore": "Chores", "other": "Other Changes"}
        
        log = []
        for k, t in ttls.items():
            if cats[k]:
                log.append(f"\n### {t}\n")
                for m in cats[k]:
                    log.append(f"- {m}")
        
        return "\n".join(log)
    
    def dirty(self):
        res = Utils.run_cmd(["git", "status", "--porcelain"], cwd=self.path)
        if res and res.returncode == 0:
            return bool(res.stdout.strip())
        return False
    
    def gh_info(self):
        url = self.remote()
        if not url:
            return None
        
        pts = [r"github\.com[:/]([^/]+)/([^/.]+)", r"github\.com/([^/]+)/([^/]+?)(?:\.git)?$"]
        
        for p in pts:
            m = re.search(p, url)
            if m:
                return {
                    "owner": m.group(1),
                    "repo": m.group(2).replace(".git", ""),
                    "url": f"https://github.com/{m.group(1)}/{m.group(2).replace('.git', '')}"
                }
        return None
    
    def gl_info(self):
        url = self.remote()
        if not url:
            return None
        
        pts = [r"gitlab\.com[:/]([^/]+)/([^/.]+)", r"gitlab\.com/([^/]+)/([^/]+?)(?:\.git)?$"]
        
        for p in pts:
            m = re.search(p, url)
            if m:
                return {
                    "owner": m.group(1),
                    "repo": m.group(2).replace(".git", ""),
                    "url": f"https://gitlab.com/{m.group(1)}/{m.group(2).replace('.git', '')}"
                }
        return None
