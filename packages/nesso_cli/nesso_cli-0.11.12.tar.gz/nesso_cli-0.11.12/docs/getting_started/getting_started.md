# Getting Started

## Prerequisites

- Python >= 3.10
- basic familiarity with `dbt` at the level of the [dbt fundamentals](https://courses.getdbt.com/courses/fundamentals) course

## Installation

```bash
python -m venv .venv && \
    . .venv/bin/activate && \
    pip install "nesso-cli[your_database_name]"
```

!!! note "Choosing your database extra"
    Change `your_database_name` to the database you'll be using in your project (see [Supported databases](../reference/supported_dbs.md)).

## Next steps

Follow the [User guide](../user_guide/introduction.md) to learn how to use `nesso models` to create and manage your data models.
