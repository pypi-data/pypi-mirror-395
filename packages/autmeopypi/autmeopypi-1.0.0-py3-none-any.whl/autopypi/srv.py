import os
import sys
import json
import threading
from autopypi.bld import bld
from autopypi.upl import upl
from autopypi.chk import chk
from autopypi.cfg import Config
from autopypi.log import Logger
from autopypi.ver import ver
from autopypi.git import git
from autopypi.bat import bat
from autopypi.ci import ci

class srv:
    
    def __init__(self, host="0.0.0.0", port=5000, path=None):
        self.host = host
        self.port = port
        self.path = path or os.getcwd()
        self.app = None
        self.log = Logger()
    
    def create(self):
        try:
            from flask import Flask, request, jsonify, render_template_string
        except ImportError:
            self.log.err("Flask not installed. Run: pip install flask")
            return None
        
        app = Flask(__name__)
        
        html = """<!DOCTYPE html>
<html>
<head>
    <title>AutoPyPI</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #eee; min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; padding: 40px 0; border-bottom: 1px solid #333; margin-bottom: 30px; }
        .header h1 { font-size: 3em; background: linear-gradient(90deg, #00d4ff, #7b2ff7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }
        .header p { color: #888; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); transition: transform 0.3s, box-shadow 0.3s; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 10px 40px rgba(0,0,0,0.3); }
        .card h3 { color: #00d4ff; margin-bottom: 15px; }
        .btn { display: inline-block; padding: 12px 24px; background: linear-gradient(90deg, #00d4ff, #7b2ff7); color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; transition: opacity 0.3s; margin: 5px; }
        .btn:hover { opacity: 0.8; }
        .btn-secondary { background: #444; }
        .output { background: #0d1117; border-radius: 8px; padding: 15px; margin-top: 20px; font-family: 'Monaco', 'Consolas', monospace; font-size: 13px; overflow-x: auto; max-height: 400px; overflow-y: auto; }
        .success { color: #4ade80; }
        .error { color: #f87171; }
        .warning { color: #fbbf24; }
        .info { color: #60a5fa; }
        input, select { width: 100%; padding: 12px; margin: 8px 0; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; color: white; font-size: 14px; }
        input:focus, select:focus { outline: none; border-color: #00d4ff; }
        label { display: block; margin-top: 15px; color: #888; font-size: 12px; text-transform: uppercase; }
        .status { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
        .status-dot { width: 10px; height: 10px; border-radius: 50%; }
        .status-dot.online { background: #4ade80; }
        .version-info { background: rgba(0,212,255,0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AutoPyPI</h1>
            <p>Python Package Publishing Made Easy</p>
            <div class="status"><div class="status-dot online"></div><span>Server Running</span></div>
        </div>
        <div class="version-info" id="projectInfo">Loading project info...</div>
        <div class="grid">
            <div class="card">
                <h3>Build Package</h3>
                <p>Build source distribution and wheel files.</p>
                <label><input type="checkbox" id="buildSdist" checked> Source Distribution</label>
                <label><input type="checkbox" id="buildWheel" checked> Wheel</label>
                <label><input type="checkbox" id="cleanBefore" checked> Clean Before Build</label>
                <br><br>
                <button class="btn" onclick="build()">Build Package</button>
            </div>
            <div class="card">
                <h3>Check Package</h3>
                <p>Verify package before uploading.</p>
                <button class="btn" onclick="check()">Run Checks</button>
            </div>
            <div class="card">
                <h3>Upload Package</h3>
                <p>Upload to PyPI or TestPyPI.</p>
                <label>Repository</label>
                <select id="uploadRepo">
                    <option value="pypi">PyPI (Production)</option>
                    <option value="testpypi">TestPyPI (Testing)</option>
                </select>
                <label>API Token</label>
                <input type="password" id="uploadToken" placeholder="pypi-...">
                <br><br>
                <button class="btn" onclick="upload()">Upload Package</button>
            </div>
            <div class="card">
                <h3>Release</h3>
                <p>Build, check, and upload in one step.</p>
                <label>Version Bump</label>
                <select id="versionBump">
                    <option value="none">No Version Change</option>
                    <option value="patch">Patch (x.x.X)</option>
                    <option value="minor">Minor (x.X.0)</option>
                    <option value="major">Major (X.0.0)</option>
                </select>
                <label><input type="checkbox" id="createTag"> Create Git Tag</label>
                <br><br>
                <button class="btn" onclick="release()">Release</button>
            </div>
            <div class="card">
                <h3>Version Manager</h3>
                <p>Update package version.</p>
                <label>New Version</label>
                <input type="text" id="newVersion" placeholder="1.0.0">
                <br><br>
                <button class="btn" onclick="setVersion()">Set Version</button>
                <button class="btn btn-secondary" onclick="showVersions()">Show Options</button>
            </div>
            <div class="card">
                <h3>CI/CD</h3>
                <p>Generate CI configuration files.</p>
                <button class="btn" onclick="generateCI('github')">GitHub Actions</button>
                <button class="btn btn-secondary" onclick="generateCI('gitlab')">GitLab CI</button>
            </div>
        </div>
        <div class="card" style="margin-top: 20px;">
            <h3>Output</h3>
            <div class="output" id="output">Ready...</div>
        </div>
    </div>
    <script>
        const output = document.getElementById('output');
        function log(msg, type = 'info') { const line = document.createElement('div'); line.className = type; line.textContent = msg; output.appendChild(line); output.scrollTop = output.scrollHeight; }
        function clear() { output.innerHTML = ''; }
        async function api(endpoint, data = {}) {
            clear(); log('Processing...', 'info');
            try {
                const res = await fetch('/api/' + endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
                const json = await res.json(); clear();
                if (json.success) { log('Operation completed successfully!', 'success'); } else { log('Operation failed', 'error'); }
                if (json.message) log(json.message, json.success ? 'success' : 'error');
                if (json.output) log(json.output, 'info');
                if (json.warnings) json.warnings.forEach(w => log(w, 'warning'));
                if (json.errors) json.errors.forEach(e => log(e, 'error'));
                return json;
            } catch (e) { clear(); log('Error: ' + e.message, 'error'); }
        }
        async function loadProjectInfo() { const res = await fetch('/api/info'); const data = await res.json(); document.getElementById('projectInfo').innerHTML = '<strong>' + (data.name || 'Unknown') + '</strong> v' + (data.version || '?') + ' | Python ' + (data.python || '?'); }
        function build() { api('build', { sdist: document.getElementById('buildSdist').checked, wheel: document.getElementById('buildWheel').checked, clean: document.getElementById('cleanBefore').checked }); }
        function check() { api('check'); }
        function upload() { api('upload', { test: document.getElementById('uploadRepo').value === 'testpypi', token: document.getElementById('uploadToken').value }); }
        function release() { api('release', { bump: document.getElementById('versionBump').value, tag: document.getElementById('createTag').checked, token: document.getElementById('uploadToken').value, test: document.getElementById('uploadRepo').value === 'testpypi' }); }
        function setVersion() { api('version/set', { version: document.getElementById('newVersion').value }); }
        function showVersions() { api('version/options'); }
        function generateCI(platform) { api('ci/' + platform); }
        loadProjectInfo();
    </script>
</body>
</html>"""
        
        @app.route("/")
        def index():
            return render_template_string(html)
        
        @app.route("/api/info")
        def get_info():
            cfg = Config(self.path)
            prj = cfg.get_project_config()
            return jsonify({"name": prj.get("name") if prj else None, "version": prj.get("version") if prj else None, "python": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"})
        
        @app.route("/api/build", methods=["POST"])
        def api_build():
            data = request.get_json() or {}
            b = bld(self.path)
            r = b.run(src=data.get("sdist", True), whl=data.get("wheel", True), cln=data.get("clean", True))
            return jsonify({"success": bool(r and (r.get("sdist") or r.get("wheel"))), "message": "Build completed" if r else "Build failed", "sdist": r.get("sdist") if r else None, "wheel": r.get("wheel") if r else None})
        
        @app.route("/api/check", methods=["POST"])
        def api_check():
            c = chk(self.path)
            ok = c.run()
            return jsonify({"success": ok, "message": "All checks passed" if ok else "Check failed", "warnings": c.warns, "errors": c.issues})
        
        @app.route("/api/upload", methods=["POST"])
        def api_upload():
            data = request.get_json() or {}
            u = upl(self.path)
            ok = u.run(tok=data.get("token"), test=data.get("test", False))
            return jsonify({"success": ok, "message": "Upload successful" if ok else "Upload failed"})
        
        @app.route("/api/release", methods=["POST"])
        def api_release():
            data = request.get_json() or {}
            if data.get("bump") and data["bump"] != "none":
                v = ver(self.path)
                v.bump_set(data["bump"])
            b = bld(self.path)
            br = b.run()
            if not br or not (br.get("sdist") or br.get("wheel")):
                return jsonify({"success": False, "message": "Build failed"})
            c = chk(self.path)
            if not c.run():
                return jsonify({"success": False, "message": "Check failed", "errors": c.issues})
            u = upl(self.path)
            ok = u.run(tok=data.get("token"), test=data.get("test", False))
            if ok and data.get("tag"):
                cfg = Config(self.path)
                prj = cfg.get_project_config()
                if prj and prj.get("version"):
                    g = git(self.path)
                    g.release(prj["version"])
            return jsonify({"success": ok, "message": "Release successful" if ok else "Release failed"})
        
        @app.route("/api/version/set", methods=["POST"])
        def api_version_set():
            data = request.get_json() or {}
            v = ver(self.path)
            ok = v.set(data.get("version", ""))
            return jsonify({"success": ok, "message": f"Version set to {data.get('version')}" if ok else "Failed to set version"})
        
        @app.route("/api/version/options", methods=["POST"])
        def api_version_options():
            v = ver(self.path)
            opts = v.next()
            cur = v.get()
            return jsonify({"success": True, "current": cur, "options": opts, "output": f"Current: {cur}\n" + "\n".join(f"{k}: {val}" for k, val in opts.items())})
        
        @app.route("/api/ci/<platform>", methods=["POST"])
        def api_ci(platform):
            c = ci(self.path)
            if platform == "github":
                p = c.github()
            elif platform == "gitlab":
                p = c.gitlab()
            else:
                return jsonify({"success": False, "message": "Unknown platform"})
            return jsonify({"success": True, "message": f"Created {p}"})
        
        self.app = app
        return app
    
    def run(self, debug=False):
        self.log.logo()
        self.log.inf(f"Starting server at http://{self.host}:{self.port}")
        app = self.create()
        if app:
            app.run(host=self.host, port=self.port, debug=debug)
    
    def background(self):
        app = self.create()
        if app:
            t = threading.Thread(target=lambda: app.run(host=self.host, port=self.port), daemon=True)
            t.start()
            return t
        return None
