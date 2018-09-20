import helpers
import matplotlib.pyplot as plt
import numpy as np
import math
import sys

import scipy.integrate as integrate

num_nodes_list = [1, 2, 3, 5, 6, 7]
max_nodes = max(num_nodes_list)


## Calculate the coalescence moments
t = 0.59843625345 # Found from FindTValues.sage
coalescence_func = lambda x: helpers.coalescence_ndf(t, x)
coalescence_moments = []
for i in range(0,2*max_nodes+1):
    coalescence_moments.append(helpers.extract_analytic_moment(coalescence_func, 1e-10, 5e2, i))

print("Coalescence Moments")
for i in range(0,2*max_nodes+1):
    print("M_{} = {}".format(i, coalescence_moments[i]))

plt.figure(12, figsize=(12,12), dpi=80)

#x = np.linspace(1e-5,250., 200)
#y = [coalescence_func(x) for x in x]
#
#plt.plot(x, y)
#
#plt.yscale('log')
#plt.ylim(1e-15, 1e0)
#plt.xlim(0, 250)


plot_i = 1
for num_nodes in num_nodes_list:
    plt.subplot(320+plot_i)

    x = np.linspace(1e-5, 250., 50)
    y = [coalescence_func(x) for x in x]

    plt.plot([], color="#0A246A", linestyle="-", label="Analytical solution")
    plt.plot([], color="#007F00", linestyle="-.", label="EQMOM each node")
    plt.plot([], color="#D82900", linestyle="None", marker="o", markerfacecolor="None", label="Approximation Distribution")

    plt.plot(x, y, color="#0A246A", linestyle="-")

    # Invert moments
    node_definitions = helpers.perform_moment_inversion(num_nodes, coalescence_moments)
    print(node_definitions)

    # Plot individual nodes
    for n in range(0, num_nodes):
        try:
            y = [helpers.f_num_single_lognormal(x, node_definitions, n) for x in x]
            plt.plot(x, y, color="#007F00", linestyle="-.")
        except:
            pass

    # Plot full solution
    try:
        y = [helpers.f_num_lognormal(x, node_definitions) for x in x]
        plt.plot(x, y, color="#D82900", linestyle="None", marker="o", markerfacecolor="None")
    except:
        pass

    plt.yscale('log')
    plt.ylim(1e-15, 1e0)
    plt.xlim(0, 250)
    plot_i += 1

plt.savefig("Figure12.png")

### Calculate the condensation moments
#t = 0.622446664404 # Found from FindTValues.sage
#condensation_func = lambda x: helpers.condensation_ndf(t, x)
#condensation_moments = []
#for i in range(0,2*max_nodes+1):
#    condensation_moments.append(helpers.extract_analytic_moment(condensation_func, 0, np.inf, i))
#
#print("Condensation Moments")
#for i in range(0,2*max_nodes+1):
#    print("M_{} = {}".format(i, condensation_moments[i]))
#
#plt.figure(13, figsize=(12,12), dpi=80)
#
#plot_i = 1
#for num_nodes in num_nodes_list:
#    plt.subplot(320+plot_i)
#
#    x = np.linspace(1e-5, 80., 50)
#    y = [condensation_func(x) for x in x]
#
#    plt.plot([], color="#0A246A", linestyle="-", label="Analytical solution")
#    plt.plot([], color="#007F00", linestyle="-.", label="EQMOM each node")
#    plt.plot([], color="#D82900", linestyle="None", marker="o", markerfacecolor="None", label="Approximation Distribution")
#
#    plt.plot(x, y, color="#0A246A", linestyle="-")
#
#    # Invert moments
#    node_definitions = helpers.perform_moment_inversion(num_nodes, coalescence_moments)
#    print(node_definitions)
#
#    # Plot individual nodes
#    for n in range(0, num_nodes):
#        try:
#            y = [helpers.f_num_single_lognormal(x, node_definitions, n) for x in x]
#            plt.plot(x, y, color="#007F00", linestyle="-.")
#        except:
#            pass
#
#    # Plot full solution
#    try:
#        y = [helpers.f_num_lognormal(x, node_definitions) for x in x]
#        plt.plot(x, y, color="#D82900", linestyle="None", marker="o", markerfacecolor="None")
#    except:
#        pass
#
#    plt.yscale('log')
#    plt.ylim(1e-20, 1e3)
#    plt.xlim(0, 80)
#    plot_i += 1
#
#plt.savefig("Figure13.png")
