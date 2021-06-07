#!/bin/bash

# Exit when any command fails
set -e

# Install required dependencies
pip install -r requirements.txt
echo "Successfully installed required packages"

# Check that the script is basically working and creating the same results
python main.py
test -f boxplot.png
test -f combined_histogram.png
test -f female_humans_in_space.png
test -f humans_in_space.png
test -f male_humans_in_space.png
echo "Successfully created the plots"
