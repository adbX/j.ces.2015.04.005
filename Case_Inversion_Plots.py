import csv
import helpers
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--case", help="The case number", type=int, required=True)
parser.add_argument("--filename", help="The name to save the image", type=str, required=True)
parser.add_argument("--ylim", help="The max y limit", type=float, required=True)

args = parser.parse_args()

Node_nums = [1, 2, 3, 4]
max_nodes = max(Node_nums)

# Read analytic data from file.
analytic_data = helpers.load_csv_data("Passalaqua2015_Case{}_N_RIG.csv".format(args.case))
x_analytic = list(analytic_data.keys())
y_analytic = list(analytic_data.values())

# Extract moments from distribution
analytic_moments = []
for i in range(0,2*max_nodes+1):
    new_moment = 0.
    for j in range(0,len(x_analytic)-1):
        dx = x_analytic[j+1]-x_analytic[j]
        x = (x_analytic[j+1]+x_analytic[j])/2.
        y = (y_analytic[j+1]+y_analytic[j])/2.
        new_moment += y*(x**i)*dx
    analytic_moments.append(new_moment)


print("Extracted Analytic Moments are: ")
for i in range(0,2*max_nodes+1):
    print("M_%i = %f" % (i, analytic_moments[i]))


x = np.linspace(1, 10, 300)

# Produce Figures 2a-d
plt.figure(2, figsize=(12,8), dpi=80)

for node_num in Node_nums:
    node_definitions_lognormal = helpers.perform_moment_inversion(node_num, analytic_moments, inversion_type='lognormal')
    node_definitions_gamma = helpers.perform_moment_inversion(node_num, analytic_moments, inversion_type='gamma')

    plt.subplot(220+node_num)

    plt.plot([], color="#007F00", linestyle="-.", label="LnEQMOM")
    plt.plot([], color="#D92900", linestyle="--", label="GammaEQMOM")
    plt.plot([], color="#0A246A", linestyle="-", label="Analytical solution")

    plt.plot(x_analytic, y_analytic, color="#0A246A", linestyle="-")

    y = [helpers.f_num_lognormal(x, node_definitions_lognormal)/analytic_moments[0] for x in x]

    plt.plot(x, y, color="#007F00", linestyle="-.")

    y = [helpers.f_num_gamma(x, node_definitions_gamma)/analytic_moments[0] for x in x]
    plt.plot(x, y, color="#D92900", linestyle="--")

    plt.legend()
    plt.ylabel(r"$n(\xi)$")
    plt.xlabel(r"$\xi$")
    plt.xlim(1., 10.)
    plt.ylim(0., args.ylim)

plt.subplots_adjust(left=0.11, right = 0.98, bottom=0.1, top=0.95, wspace=0.2, hspace = 0.15)

plt.savefig(args.filename)
