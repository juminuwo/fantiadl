#!/bin/zsh

# Connect to Japan for the script
cd /mnt/c/
/mnt/c/Windows/System32/cmd.exe /c "C:\Program Files\NordVPN\nordvpn.exe" nordvpn -c -g "Japan"

# Run the Python script
cd "$(dirname "$0")"
source ~/.zshrc
conda activate fantia-dler && /home/howis/miniconda3/envs/fantia-dler/bin/python /mnt/g/AV/fantiadl/auto.py

# Disconnect NordVPN when done
cd /mnt/c/
/mnt/c/Windows/System32/cmd.exe /c "C:\Program Files\NordVPN\nordvpn.exe" nordvpn -d
