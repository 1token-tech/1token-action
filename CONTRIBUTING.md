# 贡献 / 维护 1token-action

## 新增一个内部化 action

1. 在上游确定要 vendor 的 **tag**(immutable 版本)。
2. 在仓库根建子目录 `<action>/`,用 `git archive <tag> <paths> | tar -x -C <action>/` 把运行所需文件
   vendored 进去(**逐字节保留**,别手改):
   - **node (JS) action**:`action.yml` + `dist/**` + `LICENSE`(+ 可选 README)。不要带 `src/`、测试、`package*.json`。
   - **composite action**:`action.yml` + 它运行时读的所有 sibling 文件(脚本等)。审计其内部 `uses:`:
     - `uses: ./local` 形式 → 一并 vendor;`uses: owner/repo@sha` 外部依赖 → 记入 provenance,决定是否也内部化。
     - 禁止 repo-**根**相对路径(`uses: ./` 指向仓库根)的 action,monorepo 子目录下会失效。
   - **docker action**:`action.yml` + `Dockerfile` + entrypoint(若 `image: docker://...` 则按需镜像化)。
3. 在 `upstreams.yml` 加 provenance 条目(upstream repo / tag / commit SHA / 日期 / vendored_paths)。
4. 写 `<action>/README.md`(用法 + SHA-pin 片段)与 `<action>/CHANGELOG.md`。
5. `python3 scripts/validate_actions.py` 本地过;在 `.github/CODEOWNERS` 给敏感 action 路径配 owner。
6. 提 PR(必须 CODEOWNER review,见分支保护)。合入后打 tag `<action>/vX.Y.Z`(+ 可选移动 `<action>/vX`)。

## 升级 / re-vendor 已有 action

1. `git archive <new-tag> <paths> | tar -x -C <action>/` 覆盖。
2. 更新 `upstreams.yml` 的 `vendored_version` / `vendored_commit` / `vendored_date`,追加 `CHANGELOG.md`。
3. validate → PR → 合入 → 打新 tag `<action>/v<new>`(移动 `<action>/v<major>` 到新 commit)。
   旧 tag 不动(老消费者仍 pin 老 SHA)。

## 下游怎么引用

**永远 SHA-pin**,版本号放注释:

```yaml
- uses: 1token-tech/1token-action/<action>@<40位commit-sha> # <action>/vX.Y.Z
```

查 tag→SHA:`git ls-remote https://github.com/1token-tech/1token-action.git '<action>/vX.Y.Z'`

## 不变量(CI 会校验)

- 每个 `<action>/action.yml` 合法、`runs.using` 正确、JS 的 `main` 文件在子目录内存在。
- 每个子目录 action 在 `upstreams.yml` 有条目,反之亦然。
- vendored 内容与 `upstreams.yml` 记录的上游 commit 处对应路径**逐字节一致**(provenance 校验)。
