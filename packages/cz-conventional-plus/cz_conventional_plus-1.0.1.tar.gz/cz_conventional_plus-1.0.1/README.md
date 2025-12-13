# `commitizen` Extended Conventional Commits

**`cz-conventional-plus`** is a [commitizen](https://github.com/commitizen-tools/commitizen) plugin subclassing the `cz_conventional_commits` configuration. It extends it by adding 'chore' and 'revert' to the possible commit types.

## Installation

```sh
pip install cz-conventional-plus
cz init
```

## Configuration samples

`pyproject.toml`

```toml
[tool.commitizen]
name = "cz_conventional_plus"
```

`.cz.yaml`

```yaml
commitizen:
    name: cz_conventional_plus
```

`.cz.json`

```json
{
    "commitizen": {
        "name": "cz_conventional_plus",
    }
}
```
