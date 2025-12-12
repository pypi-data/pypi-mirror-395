import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from autopypi.bld import bld
from autopypi.upl import upl
from autopypi.chk import chk
from autopypi.cfg import Config
from autopypi.log import Logger
from autopypi.utl import Utils

class bat:
    
    def __init__(self, base=None, log=None):
        self.base = base or os.getcwd()
        self.log = log or Logger()
        self.prjs = []
        self.res = {}
    
    def discover(self, path=None):
        path = path or self.base
        prjs = []
        
        if Config(path).has_pyproject() or Config(path).has_setup_py():
            prjs.append(path)
        
        for item in os.listdir(path):
            p = os.path.join(path, item)
            if os.path.isdir(p):
                cfg = Config(p)
                if cfg.has_pyproject() or cfg.has_setup_py():
                    prjs.append(p)
        
        self.prjs = prjs
        return prjs
    
    def add(self, path):
        if path not in self.prjs:
            self.prjs.append(path)
    
    def remove(self, path):
        if path in self.prjs:
            self.prjs.remove(path)
    
    def build_all(self, parallel=False, src=True, whl=True):
        self.log.hdr("Batch Build")
        self.log.inf(f"Building {len(self.prjs)} project(s)")
        
        res = {}
        
        if parallel:
            with ThreadPoolExecutor(max_workers=4) as ex:
                futs = {ex.submit(self._build, p, src, whl): p for p in self.prjs}
                
                for fut in as_completed(futs):
                    prj = futs[fut]
                    try:
                        res[prj] = fut.result()
                    except Exception as e:
                        res[prj] = {"ok": False, "err": str(e)}
        else:
            for prj in self.prjs:
                res[prj] = self._build(prj, src, whl)
        
        self.res = res
        self._summary("Build")
        return res
    
    def _build(self, path, src, whl):
        try:
            b = bld(path)
            r = b.run(src=src, whl=whl)
            return {"ok": bool(r and (r.get("sdist") or r.get("wheel"))), "sdist": r.get("sdist") if r else None, "wheel": r.get("wheel") if r else None}
        except Exception as e:
            return {"ok": False, "err": str(e)}
    
    def upload_all(self, tok=None, usr=None, pwd=None, test=False, parallel=False):
        self.log.hdr("Batch Upload")
        self.log.inf(f"Uploading {len(self.prjs)} project(s)")
        
        res = {}
        
        if parallel:
            with ThreadPoolExecutor(max_workers=2) as ex:
                futs = {ex.submit(self._upload, p, tok, usr, pwd, test): p for p in self.prjs}
                
                for fut in as_completed(futs):
                    prj = futs[fut]
                    try:
                        res[prj] = fut.result()
                    except Exception as e:
                        res[prj] = {"ok": False, "err": str(e)}
        else:
            for prj in self.prjs:
                res[prj] = self._upload(prj, tok, usr, pwd, test)
        
        self.res = res
        self._summary("Upload")
        return res
    
    def _upload(self, path, tok, usr, pwd, test):
        try:
            u = upl(path)
            ok = u.run(tok=tok, usr=usr, pwd=pwd, test=test)
            return {"ok": ok}
        except Exception as e:
            return {"ok": False, "err": str(e)}
    
    def release_all(self, tok=None, usr=None, pwd=None, test=False, tag=False):
        self.log.hdr("Batch Release")
        
        build_res = self.build_all()
        
        fail = [p for p, r in build_res.items() if not r.get("ok")]
        if fail:
            self.log.wrn(f"{len(fail)} project(s) failed to build")
        
        ok = [p for p, r in build_res.items() if r.get("ok")]
        self.prjs = ok
        
        upl_res = self.upload_all(tok=tok, usr=usr, pwd=pwd, test=test)
        
        return {"build": build_res, "upload": upl_res}
    
    def check_all(self):
        self.log.hdr("Batch Check")
        
        res = {}
        
        for prj in self.prjs:
            c = chk(prj)
            ok = c.run()
            res[prj] = {"ok": ok, "issues": c.issues, "warns": c.warns}
        
        self.res = res
        self._summary("Check")
        return res
    
    def _summary(self, op):
        self.log.inf("")
        self.log.hdr(f"{op} Summary")
        
        ok_cnt = sum(1 for r in self.res.values() if r.get("ok"))
        fail_cnt = len(self.res) - ok_cnt
        
        hdrs = ["Project", "Status", "Details"]
        rows = []
        
        for prj, r in self.res.items():
            nm = os.path.basename(prj)
            st = "OK" if r.get("ok") else "FAIL"
            
            det = ""
            if r.get("err"):
                det = r["err"][:50]
            elif r.get("sdist") or r.get("wheel"):
                pts = []
                if r.get("sdist"):
                    pts.append("sdist")
                if r.get("wheel"):
                    pts.append("wheel")
                det = ", ".join(pts)
            
            rows.append([nm, st, det])
        
        self.log.tbl(hdrs, rows)
        self.log.inf(f"OK: {ok_cnt}, FAIL: {fail_cnt}")
    
    def clean_all(self):
        self.log.hdr("Batch Clean")
        
        for prj in self.prjs:
            Utils.clean_build_dirs(prj)
            self.log.inf(f"Cleaned: {os.path.basename(prj)}")
    
    def info(self):
        lst = []
        
        for prj in self.prjs:
            cfg = Config(prj)
            pc = cfg.get_project_config()
            
            lst.append({
                "path": prj,
                "name": pc.get("name") if pc else None,
                "ver": pc.get("version") if pc else None
            })
        
        return lst
    
    def show(self):
        lst = self.info()
        
        if not lst:
            self.log.inf("No projects found")
            return
        
        hdrs = ["Project", "Name", "Version"]
        rows = [[os.path.basename(p["path"]), p["name"] or "N/A", p["ver"] or "N/A"] for p in lst]
        
        self.log.tbl(hdrs, rows)
