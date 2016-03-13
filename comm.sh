#!/bin/bash

if [ $# -ne 2 ]; then
  exit 2;
fi

comm <(sort $1) <(sort $2)
