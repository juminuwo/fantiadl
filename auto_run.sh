#!/bin/zsh

cd "$(dirname "$0")"
source ~/.zshrc
conda activate fantia-dler && python ./auto.py
