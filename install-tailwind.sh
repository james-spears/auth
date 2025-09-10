#!/bin/bash

arch=$(uname -m)
os=$(uname -s)
system="${arch}-${os}"
echo "${system}"

if test -f "./tailwindcss"; then
  echo "Tailwind binary exists in project root, skipping download..."
else
  echo "Tailwind binary not found in project root, downloading..."
  case "$system" in
    "arm64-Darwin")
        curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.7/tailwindcss-macos-arm64
        chmod u+x tailwindcss-macos-arm64
        mv tailwindcss-macos-arm64 tailwindcss
        ;;
    "aarch64-Linux")
        curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.7/tailwindcss-linux-arm64
        chmod u+x tailwindcss-linux-arm64
        mv tailwindcss-linux-arm64 tailwindcss
        ;;
    *)
        echo "Defaulting to linux-x64..."
        curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v4.1.7/tailwindcss-linux-x64
        chmod u+x tailwindcss-linux-x64
        mv tailwindcss-linux-x64 tailwindcss
        ;;
  esac
fi
