# setup-uv (internalized)

安装并配置 [Astral uv](https://github.com/astral-sh/uv) + 指定 Python 版本,然后 `uv sync --locked`。
自有 composite action(1token IP),纯 inline `run:`,不读任何 sibling 文件。

```yaml
- uses: 1token-tech/1token-action/setup-uv@<sha> # setup-uv/v0.3.0
  with:
    python-version: '3.13.9'   # 可选,默认 3.13.9
```

- **Provenance**:vendored from `1token-tech/setup-uv@v0.3.0`(commit `820443485…`)。见 [`../upstreams.yml`](../upstreams.yml)。
- 升级:bump `1token-tech/setup-uv` → re-vendor `action.yml` → 打 tag `setup-uv/vX.Y.Z`。见 [`../CONTRIBUTING.md`](../CONTRIBUTING.md)。
