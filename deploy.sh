#!/bin/bash

function build_and_upload() {
  local dir=$1
  echo "-> Building ${dir}"
  cd $1
  python -m build
  twine upload -r testpypi dist/*
}

build_and_upload figaro_ai
