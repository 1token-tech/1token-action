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
| [setup-uv](./setup-uv) | composite | v0.3.0 | 自有(装 Astral uv) | `setup-uv/v0.3.0` |
| [create-pull-request](./create-pull-request) | node24 JS | v8.1.1 | peter-evans/create-pull-request (MIT) | `create-pull-request/v8.1.1` |

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
