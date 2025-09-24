#!/bin/zsh

cd "$(dirname "$0")"
source ~/.zshrc
conda activate fantia-dler && /home/howis/miniconda3/envs/fantia-dler/bin/python /mnt/g/AV/fantiadl/auto.py
