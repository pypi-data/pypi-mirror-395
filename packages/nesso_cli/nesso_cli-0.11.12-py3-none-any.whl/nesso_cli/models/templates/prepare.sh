#!/usr/bin/bash
set -e

GREEN="\e[32m"
GREY="\e[90m"
ENDCOLOR="\e[0m"

script_dir=`dirname $0`
cd $script_dir

sudo apt-get -qq update && sudo apt-get -qq -y upgrade \
  # Linux depenencies.
  sudo apt-get install -qq python3-venv && \
  {% if db_type == "sqlserver" -%}
  curl -s https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc > /dev/null  && \
  curl -s https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list > /dev/null  && \
  sudo apt-get -qq update && \
  ACCEPT_EULA=Y sudo apt-get -qq install -y msodbcsql18 && \
  {% endif -%}
  # Python dependencies.
  rm -rf .venv && \
  python3 -m venv .venv

export GIT_TERMINAL_PROMPT=0

# Verify the token
set +e

token_verified=false
while [ "$token_verified" = false ]; do
    read -s -p "Please provide your GitHub Personal Access Token: " token

    git clone -q https://${token}@github.com/dyvenia/nesso-cli.git --depth=1 > /dev/null 2>&1

    if test -d ./nesso-cli
    then
    echo -e "Token has been verified ${GREEN}succsessfully${ENDCOLOR}."
    rm -rf ./nesso-cli
    token_verified=true
    else
    echo -e "Token verification ${RED}failed${ENDCOLOR}. Please retry."
    fi
done

echo "export DBT_ENV_SECRET_GITHUB_TOKEN=${token}" >> ~/.bashrc
echo ""
echo -e "${GREEN}All set!${ENDCOLOR}"
echo -e "You can now activate your virtual environment by running ${GREY}. .venv/bin/activate${ENDCOLOR}"

exec /usr/bin/bash -i