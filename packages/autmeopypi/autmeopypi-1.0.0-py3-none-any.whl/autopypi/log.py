import os
import json
import logging
from datetime import datetime
from autopypi.utl import Utils
from autopypi.col import c

class Logger:
    
    def __init__(self, name="autopypi", log_dir=None, verbose=False):
        self.name = name
        self.verbose = verbose
        self.log_dir = log_dir or os.path.join(os.getcwd(), ".autopypi", "logs")
        self.history = []
        self._setup()
        c.init()
    
    def _setup(self):
        Utils.ensure_dir(self.log_dir)
        self.log_file = os.path.join(self.log_dir, f"{Utils.timestamp()}.log")
        
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = []
        
        fh = logging.FileHandler(self.log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        self.logger.addHandler(fh)
        
        if self.verbose:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(ch)
    
    def _rec(self, lvl, msg):
        entry = {
            "ts": datetime.now().isoformat(),
            "lvl": lvl,
            "msg": msg
        }
        self.history.append(entry)
    
    def dbg(self, msg):
        self.logger.debug(msg)
        self._rec("DBG", msg)
        if self.verbose:
            print(c.dbg(msg))
    
    def inf(self, msg):
        self.logger.info(msg)
        self._rec("INF", msg)
        print(c.inf(msg))
    
    def ok(self, msg):
        self.logger.info(f"OK: {msg}")
        self._rec("OK", msg)
        print(c.ok(msg))
    
    def wrn(self, msg):
        self.logger.warning(msg)
        self._rec("WRN", msg)
        print(c.wrn(msg))
    
    def err(self, msg):
        self.logger.error(msg)
        self._rec("ERR", msg)
        print(c.err(msg))
    
    def hdr(self, msg):
        self.logger.info(f"=== {msg} ===")
        self._rec("HDR", msg)
        print(c.hdr(msg))
    
    def bar(self, cur, tot, msg=""):
        br = c.bar(cur, tot)
        print(f"\r{br} {msg}", end="", flush=True)
        if cur >= tot:
            print()
    
    def stp(self, num, tot, msg):
        ico = c.ico("run")
        st = f"{c.lw}[{num}/{tot}]{c.r}"
        print(f"{ico} {st} {c.cy}{msg}{c.r}")
        self.logger.info(f"Step {num}/{tot}: {msg}")
    
    def res(self, ok, msg):
        ico = c.ico("ok" if ok else "err")
        col = c.g if ok else c.red
        print(f"    {ico} {col}{msg}{c.r}")
        lvl = "OK" if ok else "ERR"
        self.logger.info(f"{lvl}: {msg}")
    
    def tbl(self, hdrs, rows):
        wids = [max(len(str(h)), max(len(str(r[i])) for r in rows)) + 2 
                for i, h in enumerate(hdrs)]
        
        hl = c.row(hdrs, wids)
        sep = "-" * sum(wids)
        
        print(f"\n{c.b}{hl}{c.r}")
        print(f"{c.d}{sep}{c.r}")
        
        for row in rows:
            print(c.row(row, wids))
        print()
    
    def box(self, ttl, txt):
        print(c.box(ttl, txt))
    
    def logo(self):
        print(c.logo())
    
    def get(self, lvl=None):
        if lvl:
            return [e for e in self.history if e["lvl"] == lvl]
        return self.history
    
    def save(self, path=None):
        if not path:
            path = os.path.join(self.log_dir, f"rpt_{Utils.timestamp()}.json")
        
        rpt = {
            "at": datetime.now().isoformat(),
            "file": self.log_file,
            "cnt": len(self.history),
            "sum": {
                "err": len(self.get("ERR")),
                "wrn": len(self.get("WRN")),
                "ok": len(self.get("OK"))
            },
            "log": self.history
        }
        
        Utils.write_json(path, rpt)
        return path
    
    def clr(self):
        self.history = []
    
    def logs(self, lim=None):
        lgs = sorted(
            Utils.find_files(self.log_dir, "*.log"),
            key=os.path.getmtime,
            reverse=True
        )
        if lim:
            lgs = lgs[:lim]
        return lgs
    
    def clean(self, keep=10):
        lgs = self.logs()
        for lg in lgs[keep:]:
            os.remove(lg)
        return len(lgs) - keep
