import sys
import os

class c:
    
    r = "\033[0m"
    b = "\033[1m"
    d = "\033[2m"
    u = "\033[4m"
    bl = "\033[5m"
    rv = "\033[7m"
    h = "\033[8m"
    
    k = "\033[30m"
    red = "\033[31m"
    g = "\033[32m"
    y = "\033[33m"
    blu = "\033[34m"
    m = "\033[35m"
    cy = "\033[36m"
    w = "\033[37m"
    
    bk = "\033[40m"
    br = "\033[41m"
    bg = "\033[42m"
    by = "\033[43m"
    bb = "\033[44m"
    bm = "\033[45m"
    bc = "\033[46m"
    bw = "\033[47m"
    
    lk = "\033[90m"
    lr = "\033[91m"
    lg = "\033[92m"
    ly = "\033[93m"
    lb = "\033[94m"
    lm = "\033[95m"
    lc = "\033[96m"
    lw = "\033[97m"
    
    @classmethod
    def init(cls):
        if sys.platform == "win32":
            os.system("")
        return cls
    
    @classmethod
    def ok(cls, msg):
        return f"{cls.lg}{cls.b}[OK]{cls.r} {cls.g}{msg}{cls.r}"
    
    @classmethod
    def err(cls, msg):
        return f"{cls.lr}{cls.b}[ERR]{cls.r} {cls.red}{msg}{cls.r}"
    
    @classmethod
    def wrn(cls, msg):
        return f"{cls.ly}{cls.b}[WRN]{cls.r} {cls.y}{msg}{cls.r}"
    
    @classmethod
    def inf(cls, msg):
        return f"{cls.lc}{cls.b}[INF]{cls.r} {cls.cy}{msg}{cls.r}"
    
    @classmethod
    def dbg(cls, msg):
        return f"{cls.lm}{cls.b}[DBG]{cls.r} {cls.m}{msg}{cls.r}"
    
    @classmethod
    def hdr(cls, msg):
        line = "=" * (len(msg) + 4)
        return f"\n{cls.lb}{cls.b}{line}\n  {msg}  \n{line}{cls.r}\n"
    
    @classmethod
    def bar(cls, cur, tot, wid=50):
        pct = cur / tot
        fil = int(wid * pct)
        br = "█" * fil + "░" * (wid - fil)
        return f"{cls.cy}[{br}] {cls.lw}{pct*100:.1f}%{cls.r}"
    
    @classmethod
    def row(cls, cols, wids):
        rw = ""
        for i, col in enumerate(cols):
            rw += f"{cls.w}{str(col):<{wids[i]}}{cls.r} "
        return rw
    
    @classmethod
    def box(cls, ttl, txt):
        lns = txt.split("\n")
        ml = max(len(ttl), max(len(l) for l in lns)) + 4
        tp = f"╔{'═' * ml}╗"
        md = f"╠{'═' * ml}╣"
        bt = f"╚{'═' * ml}╝"
        tl = f"║ {cls.b}{ttl:<{ml-2}}{cls.r} ║"
        res = f"{cls.lb}{tp}\n{tl}\n{md}\n"
        for ln in lns:
            res += f"║ {ln:<{ml-2}} ║\n"
        res += f"{bt}{cls.r}"
        return res
    
    @classmethod
    def grad(cls, txt, sc, ec):
        cols = [cls.red, cls.y, cls.g, cls.cy, cls.blu, cls.m]
        res = ""
        for i, ch in enumerate(txt):
            col = cols[i % len(cols)]
            res += f"{col}{ch}"
        return f"{res}{cls.r}"
    
    @classmethod
    def logo(cls):
        return f"""
{cls.lc}{cls.b}
    _         _        ____        ____ ___ 
   / \\  _   _| |_ ___ |  _ \\ _   _|  _ \\_ _|
  / _ \\| | | | __/ _ \\| |_) | | | | |_) | | 
 / ___ \\ |_| | || (_) |  __/| |_| |  __/| | 
/_/   \\_\\__,_|\\__\\___/|_|    \\__, |_|  |___|
                             |___/          
{cls.r}
{cls.lw}    v1.0.0 | mero | @QP4RM{cls.r}
"""
    
    @classmethod
    def spin(cls):
        return ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    @classmethod
    def ico(cls, st):
        icos = {
            "ok": f"{cls.g}✓{cls.r}",
            "err": f"{cls.red}✗{cls.r}",
            "wrn": f"{cls.y}⚠{cls.r}",
            "inf": f"{cls.cy}ℹ{cls.r}",
            "pnd": f"{cls.w}○{cls.r}",
            "run": f"{cls.blu}●{cls.r}"
        }
        return icos.get(st, "")
