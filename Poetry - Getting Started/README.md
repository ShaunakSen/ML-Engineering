### Common commands

`potery add pytest`
`poetry add requests@2.12.1`
`poetry remove requests`

`poetry add requests^2.12.1` - install most recent version following 2.12.1 upltil minor version (it wont go to 3.*.*)

`poetry show [package_name]`

When u already have a pyproject file and just want to install dependencies

`poetry install --no-root` 

`poetry shell` - create virtualenv




### Files

`poetry.lock` - internal file managed by poetry

`poetry.toml` - The pyproject.toml file is what is the most important here. This will orchestrate your project and its dependencies. For now, it looks like this:

### Step by step setup

```
cd Poetry\ -\ Getting\ Started
poetry init
```

This creates:


```
(poetry-test) ➜  Poetry - Getting Started git:(master) ✗ tree                          
.
├── README.md
└── pyproject.toml

1 directory, 2 files

```

If you want to use Poetry only for dependency management but not for packaging, you can use the non-package mode:

```
[tool.poetry]
package-mode = false
```

Add a dependency

`poetry add numpy`

### Virtual envs with poetry

By default, Poetry creates a virtual environment in {cache-dir}/virtualenvs. You can change the cache-dir value by 
editing the Poetry configuration. Additionally, you can use the virtualenvs.in-project configuration variable to 
create virtual environments within your project directory.


```
(base) ➜  virtualenvs pwd
/Users/shaunaksen/Library/Caches/pypoetry/virtualenvs
(base) ➜  virtualenvs ls
nemo-guardrails-service-nkdf2NrA-py3.9 nemo-guardrails-service-uKtOboKb-py3.9
(base) ➜  virtualenvs 
```

> External virtual environment management

> Poetry will detect and respect an existing virtual environment that has been externally activated. This is a powerful mechanism that is intended to be an alternative to Poetry’s built-in, simplified environment management.

> To take advantage of this, simply activate a virtual environment using your preferred method or tooling, before running any Poetry commands that expect to manipulate an environment.