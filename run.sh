#!/bin/bash

# Run cases
bash RunCases.sh

# Run script for tables 2 and 3, figure 1
# Also checks that the output for Tables2and3 match
python3 Tables2and3andFigure1.py > actual_Tables2and3.txt
if [[ $(diff Tables2and3.txt actual_Tables2and3.txt) != "" ]]; then
    echo "Tables 2 and 3: FAIL"
else
    echo "Tables 2 and 3: PASS"
fi

# Run script for Figures 12 and 13
python3 Figures12and13.py

# Run script for Figure 14
python3 Figure14.py

# Run the scripts for all the other figures
bash Create_Comparison_Plots.sh
bash Create_Inversion_Plots.sh
