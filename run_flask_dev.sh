#!/bin/bash

source ./environment.sh

# Run the land-registry-elements build
node build_assets.js

python run_dev.py
