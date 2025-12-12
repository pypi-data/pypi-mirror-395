import os
import sys
import argparse
from autopypi import __version__
from autopypi.bld import bld
from autopypi.upl import upl
from autopypi.chk import chk
from autopypi.cfg import Config
from autopypi.log import Logger
from autopypi.git import git
from autopypi.ver import ver
from autopypi.bat import bat
from autopypi.ci import ci
from autopypi.srv import srv
from autopypi.col import c
from autopypi.utl import Utils

def main():
    c.init()
    
    parser = argparse.ArgumentParser(
        prog="autopypi",
        description="AutoPyPI - Automated Python Package Publishing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  autopypi build              Build source and wheel distributions
  autopypi upload -t TOKEN    Upload to PyPI with token
  autopypi release            Build, check, and upload
  autopypi start TOKEN        Set token and auto-publish
  autopypi server             Start web interface
  autopypi batch build ./     Build all packages in directory
        """
    )
    
    parser.add_argument("-v", "--version", action="version", version=f"AutoPyPI {__version__}")
    parser.add_argument("-V", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-p", "--path", default=".", help="Project path")
    
    sub = parser.add_subparsers(dest="cmd", help="Commands")
    
    b = sub.add_parser("build", help="Build package")
    b.add_argument("--sdist", action="store_true", help="Build source only")
    b.add_argument("--wheel", action="store_true", help="Build wheel only")
    b.add_argument("--no-clean", action="store_true", help="Skip cleaning")
    
    sub.add_parser("check", help="Check package")
    
    u = sub.add_parser("upload", help="Upload package")
    u.add_argument("--token", "-t", help="PyPI API token")
    u.add_argument("--username", "-u", help="PyPI username")
    u.add_argument("--password", help="PyPI password")
    u.add_argument("--test", action="store_true", help="Upload to TestPyPI")
    u.add_argument("--sdist-only", action="store_true", help="Upload sdist only")
    u.add_argument("--wheel-only", action="store_true", help="Upload wheel only")
    u.add_argument("--skip-check", action="store_true", help="Skip pre-upload check")
    
    r = sub.add_parser("release", help="Build, check, upload, and tag")
    r.add_argument("--token", "-t", help="PyPI API token")
    r.add_argument("--username", "-u", help="PyPI username")
    r.add_argument("--password", help="PyPI password")
    r.add_argument("--test", action="store_true", help="Upload to TestPyPI")
    r.add_argument("--bump", choices=["major", "minor", "patch", "alpha", "beta", "rc"], help="Bump version")
    r.add_argument("--tag", action="store_true", help="Create git tag")
    r.add_argument("--push-tag", action="store_true", help="Push git tag")
    
    st = sub.add_parser("start", help="Set token and auto-publish all packages")
    st.add_argument("token", help="PyPI API token")
    st.add_argument("--test", action="store_true", help="Upload to TestPyPI")
    st.add_argument("--dir", default=".", help="Directory to scan")
    
    tk = sub.add_parser("token", help="Set token and auto-publish")
    tk.add_argument("token", help="PyPI API token")
    tk.add_argument("--test", action="store_true", help="Upload to TestPyPI")
    
    v = sub.add_parser("version", help="Manage version")
    v.add_argument("action", nargs="?", choices=["show", "set", "bump"], default="show")
    v.add_argument("value", nargs="?", help="Version value or bump type")
    
    tg = sub.add_parser("tag", help="Create git tag")
    tg.add_argument("--push", action="store_true", help="Push tag to remote")
    tg.add_argument("--message", "-m", help="Tag message")
    
    bt = sub.add_parser("batch", help="Batch operations")
    bt.add_argument("action", choices=["build", "upload", "release", "check", "clean"])
    bt.add_argument("directory", nargs="?", default=".", help="Directory with projects")
    bt.add_argument("--token", "-t", help="PyPI API token")
    bt.add_argument("--test", action="store_true", help="Use TestPyPI")
    bt.add_argument("--parallel", action="store_true", help="Parallel processing")
    
    cv = sub.add_parser("ci", help="Generate CI config")
    cv.add_argument("platform", nargs="?", choices=["github", "gitlab", "gh", "gl", "all"], default="all")
    
    sv = sub.add_parser("server", help="Start web server")
    sv.add_argument("--host", default="0.0.0.0", help="Server host")
    sv.add_argument("--port", type=int, default=5000, help="Server port")
    sv.add_argument("--debug", action="store_true", help="Debug mode")
    
    sub.add_parser("clean", help="Clean build directories")
    sub.add_parser("info", help="Show package info")
    
    h = sub.add_parser("history", help="Show upload history")
    h.add_argument("--limit", type=int, default=10, help="Number of entries")
    
    args = parser.parse_args()
    
    if not args.cmd:
        parser.print_help()
        return 0
    
    path = os.path.abspath(args.path)
    log = Logger(verbose=args.verbose if hasattr(args, "verbose") else False)
    
    if args.cmd == "build":
        log.logo()
        b = bld(path, log=log)
        src = not args.wheel or args.sdist
        whl = not args.sdist or args.wheel
        res = b.run(src=src, whl=whl, cln=not args.no_clean)
        b.show()
        return 0 if res else 1
    
    elif args.cmd == "check":
        log.logo()
        ck = chk(path, log=log)
        ok = ck.run()
        return 0 if ok else 1
    
    elif args.cmd == "upload":
        log.logo()
        up = upl(path, log=log)
        
        if args.sdist_only:
            ok = up.sdist_only(tok=args.token, usr=args.username, pwd=args.password, test=args.test, chk_first=not args.skip_check)
        elif args.wheel_only:
            ok = up.wheel_only(tok=args.token, usr=args.username, pwd=args.password, test=args.test, chk_first=not args.skip_check)
        else:
            ok = up.run(tok=args.token, usr=args.username, pwd=args.password, test=args.test, chk_first=not args.skip_check)
        return 0 if ok else 1
    
    elif args.cmd == "release":
        log.logo()
        
        if args.bump:
            v = ver(path, log=log)
            nv = v.bump_set(args.bump)
            if not nv:
                return 1
        
        b = bld(path, log=log)
        res = b.run()
        
        if not res or not (res.get("sdist") or res.get("wheel")):
            return 1
        
        ck = chk(path, log=log)
        if not ck.run():
            return 1
        
        up = upl(path, log=log)
        ok = up.run(tok=args.token, usr=args.username, pwd=args.password, test=args.test)
        
        if ok and (args.tag or args.push_tag):
            cfg = Config(path)
            prj = cfg.get_project_config()
            if prj and prj.get("version"):
                g = git(path, log=log)
                if args.push_tag:
                    g.release(prj["version"])
                else:
                    g.tag(f"v{prj['version']}")
        
        return 0 if ok else 1
    
    elif args.cmd == "start" or args.cmd == "token":
        log.logo()
        log.hdr("Auto-Publish Mode")
        
        tok = args.token
        test = args.test
        d = args.dir if hasattr(args, "dir") else "."
        
        bt_obj = bat(d, log=log)
        prjs = bt_obj.discover()
        
        if not prjs:
            log.err("No projects found")
            return 1
        
        log.inf(f"Found {len(prjs)} project(s)")
        bt_obj.show()
        
        log.hdr("Building All Packages")
        build_res = bt_obj.build_all()
        
        fail_build = [p for p, r in build_res.items() if not r.get("ok")]
        if fail_build:
            log.wrn(f"{len(fail_build)} project(s) failed to build")
        
        ok_prjs = [p for p, r in build_res.items() if r.get("ok")]
        bt_obj.prjs = ok_prjs
        
        log.hdr("Uploading All Packages")
        upl_res = bt_obj.upload_all(tok=tok, test=test)
        
        ok_cnt = sum(1 for r in upl_res.values() if r.get("ok"))
        log.ok(f"Published {ok_cnt}/{len(ok_prjs)} package(s)")
        
        return 0
    
    elif args.cmd == "version":
        v = ver(path, log=log)
        
        if args.action == "show":
            v.show()
        elif args.action == "set" and args.value:
            ok = v.set(args.value)
            return 0 if ok else 1
        elif args.action == "bump" and args.value:
            nv = v.bump_set(args.value)
            return 0 if nv else 1
        else:
            v.show()
        return 0
    
    elif args.cmd == "tag":
        log.logo()
        cfg = Config(path)
        prj = cfg.get_project_config()
        
        if not prj or not prj.get("version"):
            log.err("Could not get version")
            return 1
        
        g = git(path, log=log)
        
        if args.push:
            ok = g.release(prj["version"], args.message)
        else:
            ok = g.tag(f"v{prj['version']}", args.message)
        
        return 0 if ok else 1
    
    elif args.cmd == "batch":
        log.logo()
        bt_obj = bat(args.directory, log=log)
        bt_obj.discover()
        
        if not bt_obj.prjs:
            log.err("No projects found")
            return 1
        
        bt_obj.show()
        
        if args.action == "build":
            res = bt_obj.build_all(parallel=args.parallel)
        elif args.action == "upload":
            res = bt_obj.upload_all(tok=args.token, test=args.test, parallel=args.parallel)
        elif args.action == "release":
            res = bt_obj.release_all(tok=args.token, test=args.test)
        elif args.action == "check":
            res = bt_obj.check_all()
        elif args.action == "clean":
            bt_obj.clean_all()
            return 0
        
        fail = sum(1 for r in bt_obj.res.values() if not r.get("ok"))
        return 1 if fail else 0
    
    elif args.cmd == "ci":
        log.logo()
        cv_obj = ci(path, log=log)
        
        if args.platform in ["github", "gh"]:
            cv_obj.github()
        elif args.platform in ["gitlab", "gl"]:
            cv_obj.gitlab()
        else:
            cv_obj.all()
        return 0
    
    elif args.cmd == "server":
        sv_obj = srv(host=args.host, port=args.port, path=path)
        sv_obj.run(debug=args.debug)
        return 0
    
    elif args.cmd == "clean":
        log.logo()
        Utils.clean_build_dirs(path)
        log.ok("Cleaned build directories")
        return 0
    
    elif args.cmd == "info":
        log.logo()
        cfg = Config(path)
        prj = cfg.get_project_config()
        
        if prj:
            txt = f"""Name: {prj.get('name', 'N/A')}
Version: {prj.get('version', 'N/A')}
Description: {prj.get('description', 'N/A')}
License: {prj.get('license', 'N/A')}
Python: {prj.get('requires_python', 'N/A')}"""
            log.box("Package Info", txt)
            
            b = bld(path)
            b.show()
        else:
            log.err("Could not read project configuration")
            return 1
        return 0
    
    elif args.cmd == "history":
        log.logo()
        up = upl(path, log=log)
        up.show_history()
        return 0
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
