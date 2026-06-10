#!/usr/bin/env python3
"""Validate every vendored action in this monorepo.

For each `<action>/action.yml` (one level under repo root, dotdirs excluded):
- the YAML parses
- `runs.using` is present
- node*: `runs.main` (and pre/post if set) point to files that exist in the action dir
- composite: `runs.steps` is non-empty
- docker: `runs.image` is set, or a Dockerfile exists in the action dir

Also cross-checks that every action with a `<dir>` has an entry in upstreams.yml
and vice-versa. Exits non-zero if anything fails.
"""
import os
import sys

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_actions():
    for name in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, name)
        if name.startswith(".") or not os.path.isdir(d):
            continue
        for fn in ("action.yml", "action.yaml"):
            p = os.path.join(d, fn)
            if os.path.isfile(p):
                yield name, d, p
                break


def validate_action(name, d, p):
    errs = []
    try:
        with open(p) as f:
            spec = yaml.safe_load(f)
    except Exception as e:  # noqa: BLE001
        return [f"YAML parse error: {e}"]
    runs = (spec or {}).get("runs") or {}
    using = runs.get("using")
    if not using:
        errs.append("runs.using missing")
    elif str(using).startswith("node"):
        if not runs.get("main"):
            errs.append("node action missing runs.main")
        for key in ("main", "pre", "post"):
            rel = runs.get(key)
            if rel and not os.path.isfile(os.path.join(d, rel)):
                errs.append(f"runs.{key} -> {rel} not found in {name}/")
    elif using == "composite":
        if not runs.get("steps"):
            errs.append("composite action has no steps")
    elif using == "docker":
        if not (runs.get("image") or os.path.isfile(os.path.join(d, "Dockerfile"))):
            errs.append("docker action missing runs.image and Dockerfile")
    else:
        errs.append(f"unknown runs.using: {using}")
    return errs


def load_manifest():
    p = os.path.join(ROOT, "upstreams.yml")
    if not os.path.isfile(p):
        return None
    with open(p) as f:
        return (yaml.safe_load(f) or {}).get("actions") or {}


def main():
    actions = list(find_actions())
    if not actions:
        print("no actions found", file=sys.stderr)
        return 1
    manifest = load_manifest()
    failures = []
    for name, d, p in actions:
        errs = validate_action(name, d, p)
        if manifest is not None and name not in manifest:
            errs.append("missing entry in upstreams.yml")
        print(f"[{'OK' if not errs else 'FAIL'}] {name} (using={(yaml.safe_load(open(p)) or {}).get('runs', {}).get('using')})")
        for e in errs:
            print(f"        - {e}")
        if errs:
            failures.append(name)
    if manifest is not None:
        names = {n for n, _, _ in actions}
        for m in manifest:
            if m not in names:
                print(f"[FAIL] upstreams.yml lists '{m}' but no {m}/action.yml exists")
                failures.append(m)
    print(f"\n{len(actions)} actions checked, {len(failures)} failing")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
