import re
from autopypi.cfg import Config
from autopypi.log import Logger
from autopypi.git import git

class ver:
    
    def __init__(self, path=None, cfg=None, log=None):
        self.cfg = cfg or Config(path)
        self.log = log or Logger()
        self.git = git(path, self.log)
    
    def get(self):
        prj = self.cfg.get_project_config()
        if prj:
            return prj.get("version")
        return None
    
    def parse(self, v):
        p = r"^(\d+)\.(\d+)\.(\d+)(?:([ab]|rc)(\d+))?(?:\.post(\d+))?(?:\.dev(\d+))?$"
        m = re.match(p, v)
        
        if not m:
            return None
        
        return {
            "maj": int(m.group(1)),
            "min": int(m.group(2)),
            "pat": int(m.group(3)),
            "pre": m.group(4),
            "pre_n": int(m.group(5)) if m.group(5) else None,
            "post": int(m.group(6)) if m.group(6) else None,
            "dev": int(m.group(7)) if m.group(7) else None
        }
    
    def fmt(self, p):
        v = f"{p['maj']}.{p['min']}.{p['pat']}"
        
        if p.get("pre") and p.get("pre_n") is not None:
            v += f"{p['pre']}{p['pre_n']}"
        
        if p.get("post") is not None:
            v += f".post{p['post']}"
        
        if p.get("dev") is not None:
            v += f".dev{p['dev']}"
        
        return v
    
    def bump(self, t="patch"):
        cur = self.get()
        
        if not cur:
            self.log.err("Could not get current version")
            return None
        
        p = self.parse(cur)
        
        if not p:
            self.log.err(f"Could not parse version: {cur}")
            return None
        
        p["pre"] = None
        p["pre_n"] = None
        p["post"] = None
        p["dev"] = None
        
        if t == "major":
            p["maj"] += 1
            p["min"] = 0
            p["pat"] = 0
        elif t == "minor":
            p["min"] += 1
            p["pat"] = 0
        elif t == "patch":
            p["pat"] += 1
        elif t == "alpha":
            p["pat"] += 1
            p["pre"] = "a"
            p["pre_n"] = 1
        elif t == "beta":
            p["pat"] += 1
            p["pre"] = "b"
            p["pre_n"] = 1
        elif t == "rc":
            p["pat"] += 1
            p["pre"] = "rc"
            p["pre_n"] = 1
        elif t == "post":
            p["post"] = 1
        elif t == "dev":
            p["dev"] = 1
        
        return self.fmt(p)
    
    def set(self, nv):
        self.log.hdr("Updating Version")
        
        cur = self.get()
        self.log.inf(f"Current: {cur}")
        self.log.inf(f"New: {nv}")
        
        if not self.parse(nv):
            self.log.err(f"Invalid version format: {nv}")
            return False
        
        if self.cfg.update_version(nv):
            self.log.ok(f"Version updated to {nv}")
            return True
        
        self.log.err("Failed to update version")
        return False
    
    def bump_set(self, t="patch"):
        nv = self.bump(t)
        
        if not nv:
            return None
        
        if self.set(nv):
            return nv
        
        return None
    
    def cmp(self, v1, v2):
        p1 = self.parse(v1)
        p2 = self.parse(v2)
        
        if not p1 or not p2:
            return 0
        
        for k in ["maj", "min", "pat"]:
            if p1[k] > p2[k]:
                return 1
            elif p1[k] < p2[k]:
                return -1
        
        return 0
    
    def newer(self, v1, v2):
        return self.cmp(v1, v2) > 0
    
    def next(self):
        cur = self.get()
        
        if not cur:
            return {}
        
        return {
            "patch": self.bump("patch"),
            "minor": self.bump("minor"),
            "major": self.bump("major"),
            "alpha": self.bump("alpha"),
            "beta": self.bump("beta"),
            "rc": self.bump("rc")
        }
    
    def show(self):
        cur = self.get()
        nxt = self.next()
        
        self.log.inf(f"Current version: {cur}")
        self.log.inf("")
        self.log.inf("Next version options:")
        
        for t, v in nxt.items():
            self.log.inf(f"  {t:8} -> {v}")
    
    def valid(self, v):
        return self.parse(v) is not None
    
    def suggest(self):
        cms = self.git.commits()
        
        has_brk = False
        has_feat = False
        has_fix = False
        
        for cm in cms:
            lo = cm.lower()
            if "breaking" in lo or "!" in lo:
                has_brk = True
            elif lo.startswith("feat"):
                has_feat = True
            elif lo.startswith("fix"):
                has_fix = True
        
        if has_brk:
            return "major"
        elif has_feat:
            return "minor"
        elif has_fix:
            return "patch"
        
        return "patch"
