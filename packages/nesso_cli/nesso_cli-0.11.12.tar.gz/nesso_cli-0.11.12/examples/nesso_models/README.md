# nesso_tutorial
## Getting started

### Notice
The project is tested on Ubuntu 22.04 and Python 3.10.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- Python >= 3.9

### Installation
Install with 
```bash
bash install.sh
```
Then, each time you work on the repo, remember to activate the virtual environment with
```bash
source .venv/bin/activate
```
(or use VSCode, which automatically activates the virtual environment).

### Configuration
#### 1. Install dpt deps
`dbt deps`

#### 2. Starting up Jupyter Notebook
`jupyter notebook`
You should now be able to see some logs in your terminal. Within the logs, you should be able to see a URL, such as `http://127.0.0.1:8888/`. Please press and hold the `CTRL` button then click on the URL. This will then open Jupyter Notebook.
Once Jupyter Notebook is up and running, please select `nesso Models Creation Tutorial.ipynb`, after which a new tab that contains the exercises will open.