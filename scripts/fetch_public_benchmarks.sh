#!/usr/bin/env bash
set -euo pipefail
mkdir -p data/external/fukuoka
base="https://www.mqchallenge.org/toy-example"
for n in 10 15 20; do
  f="ToyExample-type1-n${n}.tar.bz2"
  echo "Downloading $f"
  curl -L --fail --retry 3 "$base/$f" -o "data/external/fukuoka/$f"
  mkdir -p "data/external/fukuoka/n${n}"
  tar -xjf "data/external/fukuoka/$f" -C "data/external/fukuoka/n${n}"
done
