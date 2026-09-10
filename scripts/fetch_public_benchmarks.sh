#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/external/fukuoka results
base="https://www.mqchallenge.org/toy-example"
for n in 10 15 20; do
  f="ToyExample-type1-n${n}.tar.bz2"
  echo "Downloading $f"
  curl -L --fail --retry 3 "$base/$f" -o "data/external/fukuoka/$f"
  mkdir -p "data/external/fukuoka/n${n}"
  tar -xjf "data/external/fukuoka/$f" -C "data/external/fukuoka/n${n}"
done
find data/external -type f | sort > results/external_inventory.txt
: > results/external_headers.txt
while IFS= read -r f; do
  case "$f" in
    *.bz2|*.gz|*.zip|*.xz|*.tar) continue ;;
  esac
  echo "===== $f =====" >> results/external_headers.txt
  head -n 20 "$f" >> results/external_headers.txt 2>/dev/null || true
  echo >> results/external_headers.txt
done < results/external_inventory.txt
