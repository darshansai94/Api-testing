#!/bin/bash
set -e

pytest --html=index.html
python -m http.server 7000

while true; do sleep 1000; done