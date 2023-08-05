#!/bin/bash

function editable_install() {
  local dir=$1
  cd ${dir}
  pip install -e .[all]
  cd ..
}

editable_install figaro-ai
editable_install figaro-ai-chat
editable_install figaro-ai-tools

# Development
pip install prompt_toolkit
pip install pip-tools
pip install twine
