# 1token-action

1token 内部化的 GitHub Actions monorepo。第三方 / 自有 action 各占一个子目录(vendored 进来),
下游统一以 `1token-tech/1token-action/<action>@<sha>` 形式 **SHA-pin** 引用。

## 用法

```yaml
# @ 后面永远是 commit SHA;行尾注释写该 SHA 对应的 <action>/<version> tag
- uses: 1token-tech/1token-action/setup-uv@<sha> # setup-uv/v0.3.0
- uses: 1token-tech/1token-action/create-pull-request@<sha> # create-pull-request/v8.1.1
```

查 tag 对应的 SHA:`git ls-remote https://github.com/1token-tech/1token-action.git 'setup-uv/v0.3.0'`

## Registry

| Action | 类型 | 当前版本 | 上游 | tag |
|---|---|---|---|---|
| [setup-uv](./setup-uv) | composite | v0.3.0 | 1token-tech/setup-uv | `setup-uv/v0.3.0` |
| [create-pull-request](./create-pull-request) | node24 | v8.1.1 | peter-evans/create-pull-request | `create-pull-request/v8.1.1` |
| [pnpm-action-setup](./pnpm-action-setup) | node-js | v5.0.0 | pnpm/action-setup | `pnpm-action-setup/v5.0.0` |
| [setup-flyctl](./setup-flyctl) | node-js | v1.6 | superfly/flyctl-actions/setup-flyctl | `setup-flyctl/v1.6` |
| [setup-just](./setup-just) | composite | v4.0.0 ⚠改写 | extractions/setup-just | `setup-just/v4.0.0` |
| [setup-crate](./setup-crate) | node24 | v2.0.0 | extractions/setup-crate | `setup-crate/v2.0.0` |
| [retry](./retry) | node-js | v4.0.0 | nick-fields/retry | `retry/v4.0.0` |
| [codecov-action](./codecov-action) | composite | v6.0.2 (+v4.6.0) | codecov/codecov-action | `codecov-action/v6.0.2` |
| [reviewdog-action-setup](./reviewdog-action-setup) | composite | v1.5.0 | reviewdog/action-setup | `reviewdog-action-setup/v1.5.0` |
| [reviewdog-action-yamllint](./reviewdog-action-yamllint) | docker | v1.21.0 | reviewdog/action-yamllint | `reviewdog-action-yamllint/v1.21.0` |
| [reviewdog-action-shellcheck](./reviewdog-action-shellcheck) | composite | v1.32.0 ⚠改写 | reviewdog/action-shellcheck | `reviewdog-action-shellcheck/v1.32.0` |
| [reviewdog-action-hadolint](./reviewdog-action-hadolint) | composite | v1.50.5 | reviewdog/action-hadolint | `reviewdog-action-hadolint/v1.50.5` |
| [enable-pull-request-automerge](./enable-pull-request-automerge) | composite | v3.0.0 | peter-evans/enable-pull-request-automerge | `enable-pull-request-automerge/v3.0.0` |
| [actions-gh-pages](./actions-gh-pages) | node-js | v4.1.0 | peaceiris/actions-gh-pages | `actions-gh-pages/v4.1.0` |
| [setup-bun](./setup-bun) | node-js | v2.2.0 | oven-sh/setup-bun | `setup-bun/v2.2.0` |
| [golangci-lint-action](./golangci-lint-action) | node-js | v8.0.0 | golangci/golangci-lint-action | `golangci-lint-action/v8.0.0` |
| [pull-request-stats](./pull-request-stats) | node-js | v2.15.2 | flowwer-dev/pull-request-stats | `pull-request-stats/v2.15.2` |
| [paths-filter](./paths-filter) | node-js | v4.0.1 | dorny/paths-filter | `paths-filter/v4.0.1` |
| [vercel-action](./vercel-action) | node-js | v42.3.0 | amondnet/vercel-action | `vercel-action/v42.3.0` |

> ⚠改写 = 该 action 的 nested `uses:` 被改写为本地 `./` 引用(真内部化),action.yml 非字节一致。
> codecov-action 有 v6.0.2(composite)与 v4.6.0(JS,tag `codecov-action/v4.6.0`)两版并存。
> claude-code-action 经评估**未内部化**(~190 文件、运行时 bun install、高频迭代);其消费方只把 @v1 钉成 SHA。

> provenance(每个 action 的上游 repo / tag / commit)见 [`upstreams.yml`](./upstreams.yml)。

## 约定

- **一个 action 一个子目录**,自包含(`action.yml` + 运行所需文件;JS 带 committed `dist/`)。
- **tag 命名 `<action>/vX.Y.Z`**:git tag 是仓库全局的,所以按 action 前缀命名避免 `v8` 撞车。
  每次新增/升级**一个** action 只打它自己的 tag,不动别的。
- **下游永远 SHA-pin**,`@` 后是 40 位 commit SHA,版本号放行尾注释 `# <action>/vX.Y.Z`。
  真正 pin 住的是 SHA;tag 只是给人查「版本→SHA」用。
- **新增 / 升级 / re-vendor**:见 [`CONTRIBUTING.md`](./CONTRIBUTING.md)。所有 vendored 内容必须与
  上游对应 tag **逐字节一致**(CI 会校验 provenance)。

## 为什么是 monorepo

一个入口、一张 registry 总表、一套分支保护/CODEOWNERS;新增内部化 action 只是加个目录,
不必每个 action 建一个 repo。代价(上游 commit SHA 溯源、体积)用 `upstreams.yml` provenance
清单 + CI byte-identity 校验来兜底。详见 actions repo 的 `1token-action-monorepo-design.md`。
