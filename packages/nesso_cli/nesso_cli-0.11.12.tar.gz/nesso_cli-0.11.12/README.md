# nesso-cli

![coverage](coverage/coverage-badge.svg)![docs_coverage](coverage/docstring_coverage.svg)

---
**Documentation**: 📚 [dyvenia docs (internal)][mkdocs page]

**Source Code**: 💾 [dyvenia/nesso-cli][github page]

---

<!-- body-begin -->

The [CLI](https://www.w3schools.com/whatis/whatis_cli.asp) interface of the [nesso data platform].

## Features

- [x] simplify and automate data modelling
- [x] simplify and automate metadata generation
- [x] manage nesso project configuration
- [ ] simplify and automate job scheduling (coming soon!)

## Where does nesso-cli fit in?

Currently, nesso-cli contains a single module, `models` (`nesso models`), which is used for the T in ELTC (Extract, Load, Transform, Catalog), sitting between data ingestion (`viadot`) and metadata ingestion (`luma-cli`):

![Where does nesso-cli fit](docs/_static/where_nesso_cli_fits.png)

In the future, nesso-cli will include additional modules to allow interacting with different components of the nesso data platform through a unified interface.

The next planned module is `jobs`, which will allow creating and scheduling EL and ELTC jobs via a simple CLI interface. Currently, this is done by creating jobs manually in Python and then manually scheduling them in Prefect. We hope to replace this tedious and error-prone (though repeatable) process with simple commands, such as `nesso jobs deployment create --job my_job --schedule "0 0 * * *"`, as well as interactive commands which will guide user through a set of limited choices, such as `nesso jobs job create`.

[github page]: https://github.com/dyvenia/nesso-cli
[mkdocs page]: https://nesso-cli.docs.dyvenia.com/
[nesso data platform]: https://nesso.docs.dyvenia.com/

<!-- body-end -->