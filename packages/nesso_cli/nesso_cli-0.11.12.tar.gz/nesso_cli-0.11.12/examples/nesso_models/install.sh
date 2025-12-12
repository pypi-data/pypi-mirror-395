#!/usr/bin/bash
set -e

sudo apt install -q python3-venv &&
  # Python dependencies.
  rm -rf .venv &&
  python3 -m venv .venv &&
  source .venv/bin/activate &&
  pip3 install -qr "requirements.txt" &&
  # Allow JupyterLab to use bash as a kernel
  python -m bash_kernel.install
