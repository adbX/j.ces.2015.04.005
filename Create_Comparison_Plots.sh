set -e

python3.7 Case_Comparison_Plots.py --case 5 --nodes 3 --filename "Figure3.png" --nylim 0.65 --dyhigh 5.0 --tlim 200.0 --dlegendloc "upper left"
python3.7 Case_Comparison_Plots.py --case 6 --nodes 2 --filename "Figure5.png" --nylim 0.65 --dyhigh 5.5 --tlim 20.0 --dlegendloc "lower right"
python3.7 Case_Comparison_Plots.py --case 7 --nodes 2 --filename "Figure7.png" --nylim 0.65 --dyhigh 7.5 --tlim 10.0 --dlegendloc "lower right"
python3.7 Case_Comparison_Plots.py --case 8 --nodes 2 --filename "Figure9.png" --nylim 0.65 --dyhigh 4.5 --tlim 10.0 --dlegendloc "upper right"
python3.7 Case_Comparison_Plots.py --case 9 --nodes 4 --filename "Figure11.png" --nylim 1.0 --dyhigh 8 --tlim 10.0 --dlegendloc "lower right"
