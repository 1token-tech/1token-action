# create-pull-request (internalized)

[peter-evans/create-pull-request](https://github.com/peter-evans/create-pull-request) 的内部化镜像(MIT)。
在 Actions workspace 里把改动开成一个 PR。

```yaml
- uses: 1token-tech/1token-action/create-pull-request@<sha> # create-pull-request/v8.1.1
  with:
    token: ${{ secrets.GH_AUTO_MERGE_TOKEN }}   # 非默认 token 才能触发下游 CI
    commit-message: "..."
    title: "..."
    branch: "..."
    base: "..."
```

完整 inputs/outputs 见[上游文档](https://github.com/peter-evans/create-pull-request#action-inputs)。

- **Provenance**:vendored from `peter-evans/create-pull-request@v8.1.1`,经 `1token-tech/create-pull-request`
  镜像(commit `5f6978f…`,与上游逐字节一致)。`action.yml` + `dist/` + `LICENSE`(MIT)。见 [`../upstreams.yml`](../upstreams.yml)。
- 升级:见 [`../CONTRIBUTING.md`](../CONTRIBUTING.md)。
