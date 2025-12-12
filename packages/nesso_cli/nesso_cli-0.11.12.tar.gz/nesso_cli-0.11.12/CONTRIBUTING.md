# Contributing to `nesso` CLI

## Local installation

1. Clone the repo

    ```bash
    git clone https://github.com/dyvenia/nesso-cli.git
    ```

2. Go into the repo directory

    ```bash
    cd nesso-cli
    ```

3. Initialize the environment

    ```bash
    python -m venv .venv && \
        source .venv/bin/activate && \
        pip install .[test]
    ```

Note that due to a [bug](https://github.com/dbt-labs/dbt-utils/issues/627) in `dbt_utils`, [this fix](https://github.com/dbt-labs/dbt-utils/issues/627#issuecomment-1576624016) is required after finishing this step (the file can be found in `src/nesso_cli/models/tests/dbt_projects/postgres/dbt_packages`).

## Running tests

First, spin up a local Postgres database:

```bash
cd src/nesso_cli/models/tests && \
    docker compose up -d
```

Then, run the tests:

```bash
cd src/nesso_cli && \
    pytest tests/
```

We utilize fixtures in specific test files, as well as global fixtures, such as `setup_and_teardown()`, in `conftest.py`.

In the tests, we pre-create two test tables in Postgres, `test_table_contact` and `test_table_account`. All tests should assume these tables exist.

## Test coverage

### Code coverage

Run below to generate a coverage badge (per module)

```bash
coverage run -m pytest <module>/tests/ # eg. src/nesso_cli/models/tests/
coverage xml -o coverage/coverage.xml
coverage html -d coverage/report
genbadge coverage -i coverage/coverage.xml
```

You can instal the VSCode "Live Preview" extension to view the HTML reports generated in `coverage/report`.

### Docstring coverage

TODO (use `interrogate`)

### Static code analysis

On each PR to `main`, static analysis of the code is performed using `flake8` .

## Building docs

To run the docs locally, make sure to install nesso CLI with the `test` extra (`pip install .[test]` or `pip install .[all]`), and then run:

```bash
mkdocs serve
```

## Releasing

The process of creating a new release is quite straightforward.

### Bump package version in `pyproject.toml`

Either do this as part of the last PR in the release, or as a separate PR:

```bash
rye version x.y.z
git add pyproject.toml
git commit -m "🔖 Release x.y.z"
git push
```

### Merge the release PR

Merge the PR into `main`.

### Create and push a new version tag

Releases are made from the `main` branch. To release a version, publish a version tag:

```bash
nesso_cli_version=v0.10.0
git checkout main && git pull
git tag -a $nesso_cli_version -m "Release $nesso_cli_version"
git push origin $nesso_cli_version
```

The push of the tag will trigger a CI action that bumps the package version and creates a new release.

## Adding support for a new database

### Add the model in `models/models.py`

- add the pydantic model
- register the model in `dbt_config_map`

### Add dependencies

- add dependency in `pyproject.toml`

### (optional) Add support for PII column hashing

- if required, add database-specific hashing algorithm in `nesso_cli/models/macros/hash_column.sql` to be able to use PII column hashing

## Adding GitHub Actions

To run actions locally, follow the steps below.

1. Install [Nektos Act](https://github.com/nektos/act) and pull the large run image

2. Build a `postgres` container database

    Pull the PostgreSQL Docker image from Docker Hub.

    ```bash
    docker pull postgres:16.4
    ```

    Start the PostgreSQL container with the following command.

    ```bash
    docker run -d \
    --name postgres-test-container \
    -p 5432:5432 \
    -e POSTGRES_USER=user \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=db \
    postgres:16.4
    ```

3. Add an `act` secret with your GitHub credentials

    Create a `.secrets` file containing the necessary credentials.

    **The following script should be executed in the project root directory**

    ``` bash
    cp .github/.secrets.example .github/.secrets
    ```

    Add your credentials in the generated `.github/.secrets`.

4. Run Act

    Run `act`, pointing to the generated `.secret` file.

    ```bash
    act pull_request --secret-file .github/.secrets
    ```

5. Run select jobs with act

    Running the `act` command triggers all GitHub actions. If you want to run only one job locally, use the command below:

    ```bash
    act -j your_job
    ```

    To see a list of all available jobs in the repository, run:

    ```
    act -l
    ```

## Install `nesso-cli` macros as a dbt package

nesso-cli provides a dbt package named `nesso_macros`, and nesso projects include this package as a dependency by default. The way this is done is that the `nesso-models init --project` command adds the `nesso_macros` dbt package into the project's `packages.yml` file.

`nesso_macros` is available through this repo only, and not through dbt's official package repository. As such, the method for importing this package as a dependency in dbt is slightly different from other packages.
