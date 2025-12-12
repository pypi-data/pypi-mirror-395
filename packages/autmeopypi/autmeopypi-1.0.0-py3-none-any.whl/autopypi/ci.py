import os
from autopypi.utl import Utils
from autopypi.log import Logger

class ci:
    
    gh = """name: Publish to PyPI

on:
  release:
    types: [published]
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      test_pypi:
        description: 'Upload to TestPyPI'
        required: false
        default: 'false'
        type: boolean

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install build twine autopypi
      
      - name: Build package
        run: autopypi build
      
      - name: Check package
        run: autopypi check
      
      - name: Upload to TestPyPI
        if: github.event.inputs.test_pypi == 'true'
        env:
          PYPI_TOKEN: ${{ secrets.TEST_PYPI_TOKEN }}
        run: autopypi upload --test --token $PYPI_TOKEN
      
      - name: Upload to PyPI
        if: github.event.inputs.test_pypi != 'true'
        env:
          PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
        run: autopypi upload --token $PYPI_TOKEN

  notify:
    needs: build
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Build Status
        run: |
          if [ "${{ needs.build.result }}" == "success" ]; then
            echo "Package published successfully"
          else
            echo "Package publishing failed"
            exit 1
          fi
"""
    
    gl = """.pypi-publish:
  image: python:3.11
  stage: deploy
  before_script:
    - pip install build twine autopypi
  script:
    - autopypi build
    - autopypi check
    - autopypi upload --token $PYPI_TOKEN
  only:
    - tags
  
publish-test:
  extends: .pypi-publish
  script:
    - autopypi build
    - autopypi check
    - autopypi upload --test --token $TEST_PYPI_TOKEN
  only:
    - develop
  when: manual

publish-prod:
  extends: .pypi-publish
  only:
    - tags
  when: manual
"""
    
    def __init__(self, path=None, log=None):
        self.path = path or os.getcwd()
        self.log = log or Logger()
    
    def github(self, out=None):
        self.log.hdr("GitHub Workflow")
        
        if not out:
            out = os.path.join(self.path, ".github", "workflows", "publish.yml")
        
        Utils.ensure_dir(os.path.dirname(out))
        Utils.write_file(out, self.gh)
        
        self.log.ok(f"Created: {out}")
        self.log.inf("")
        self.log.inf("Secrets needed:")
        self.log.inf("  - PYPI_TOKEN")
        self.log.inf("  - TEST_PYPI_TOKEN (optional)")
        
        return out
    
    def gitlab(self, out=None):
        self.log.hdr("GitLab CI")
        
        if not out:
            out = os.path.join(self.path, ".gitlab-ci.yml")
        
        Utils.write_file(out, self.gl)
        
        self.log.ok(f"Created: {out}")
        self.log.inf("")
        self.log.inf("Variables needed:")
        self.log.inf("  - PYPI_TOKEN")
        self.log.inf("  - TEST_PYPI_TOKEN (optional)")
        
        return out
    
    def detect(self):
        gh = os.path.exists(os.path.join(self.path, ".github"))
        gl = os.path.exists(os.path.join(self.path, ".gitlab-ci.yml"))
        
        env = {
            "gh": os.environ.get("GITHUB_ACTIONS") == "true",
            "gl": os.environ.get("GITLAB_CI") == "true",
            "tr": os.environ.get("TRAVIS") == "true",
            "cc": os.environ.get("CIRCLECI") == "true",
            "jk": os.environ.get("JENKINS_URL") is not None
        }
        
        return {
            "has_gh": gh,
            "has_gl": gl,
            "in": {k: v for k, v in env.items() if v}
        }
    
    def is_ci(self):
        vars = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "TRAVIS", "CIRCLECI", "JENKINS_URL", "BUILDKITE"]
        return any(os.environ.get(v) for v in vars)
    
    def info(self):
        if os.environ.get("GITHUB_ACTIONS"):
            return {
                "plat": "gh",
                "repo": os.environ.get("GITHUB_REPOSITORY"),
                "br": os.environ.get("GITHUB_REF_NAME"),
                "sha": os.environ.get("GITHUB_SHA"),
                "run": os.environ.get("GITHUB_RUN_ID"),
                "usr": os.environ.get("GITHUB_ACTOR")
            }
        
        if os.environ.get("GITLAB_CI"):
            return {
                "plat": "gl",
                "repo": os.environ.get("CI_PROJECT_PATH"),
                "br": os.environ.get("CI_COMMIT_REF_NAME"),
                "sha": os.environ.get("CI_COMMIT_SHA"),
                "pipe": os.environ.get("CI_PIPELINE_ID"),
                "usr": os.environ.get("GITLAB_USER_LOGIN")
            }
        
        return None
    
    def all(self):
        gh = self.github()
        gl = self.gitlab()
        return {"gh": gh, "gl": gl}
    
    def valid_token(self, tok):
        if not tok:
            return False
        if tok.startswith("pypi-"):
            return len(tok) > 50
        return len(tok) > 10
