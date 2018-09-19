import csv
import helpers
import matplotlib.pyplot as plt
import numpy as np
import math
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--case", help="The case number", type=int, required=True)
parser.add_argument("--nodes", help="The number of nodes to use", type=int, required=True)
parser.add_argument("--filename", help="The name to save the image", type=str, required=True)
parser.add_argument("--nylim", help="The max y limit on the ndf plots", type=float, required=True)
parser.add_argument("--dyhigh", help="The max y limit on the d43 plots", type=float, required=True)
parser.add_argument("--tlim", help="The max time on the m0 and d43 plots", type=float, required=True)
parser.add_argument("--dlegendloc", help="The location of the legend on the d43 plot", type=str, required=True)

args = parser.parse_args()

x = np.linspace(1, 10, 300)

case_num = args.case
time_end = args.tlim
node_num = args.nodes

print("Building Comparison Plots for Case {}.".format(case_num))

# Read analytic data from file.
analytic_data = helpers.load_csv_data("Vanni2000_Case{}_N_RIG.csv".format(case_num))
x_analytic = list(analytic_data.keys())
y_analytic = list(analytic_data.values())

# Produce Figures a-d
plt.figure(case_num, figsize=(12,8), dpi=80)

# Produce Figure a
plt.subplot(221)

plt.plot([], color="#007F00", linestyle="-.", label="LnEQMOM N={}, $N_\\alpha$ = 20".format(node_num))
plt.plot([], color="#956363", linestyle="--", label="EQMOM each nodes")
plt.plot([], color="#0A246A", linestyle="-", label="Rigorous solution")

plt.plot(x_analytic, y_analytic, color="#0A246A", linestyle="-")

node_definitions = {'n': node_num}
sigma = None
for i in range(0, node_num):
    node_name = "node%i" % i

    case_dir = "case%iN%i" % (case_num, node_num)

    sigma_data = helpers.load_probe_data("%s/postProcessing/probes/0/sigma.%s.populationBalance" % (case_dir, node_name))
    if sigma is None:
        sigma = sigma_data[time_end]
    else:
        if sigma_data[time_end] != sigma:
            print("ERROR!!! sigma is different!!")
            sys.exit(-1)
        else:
            sigma = sigma_data[time_end]

    abscissa_data = helpers.load_probe_data("%s/postProcessing/probes/0/abscissa.%s.populationBalance" % (case_dir, node_name))
    weight_data = helpers.load_probe_data("%s/postProcessing/probes/0/weight.%s.populationBalance" % (case_dir, node_name))
    node_definitions[i] = {'w': weight_data[time_end], 'ab': math.log(abscissa_data[time_end])}
node_definitions['sig'] = sigma

moment0_data = helpers.load_probe_data("%s/postProcessing/probes/0/moment.0.populationBalance" % case_dir)

for i in range(0, node_num):
    y = [node_definitions[i]['w']*helpers.lognormal_kern(x, node_definitions[i]['ab'], node_definitions['sig'])/moment0_data[time_end] for x in x]

    plt.plot(x, y, color="#956363", linestyle="--")

y = [helpers.f_num_lognormal(x, node_definitions)/moment0_data[time_end] for x in x]

plt.plot(x, y, color="#007F00", linestyle="--")

plt.legend()
plt.ylabel(r"$n(\xi)$")
plt.xlabel(r"$\xi$")
plt.xlim(1., 10.)
plt.ylim(-0.05, args.nylim)

# Produce Figure b

plt.subplot(222)

plt.plot([], color="#FF5252", linestyle="-", label="QMOM nodes")
plt.plot([], color="#0A246A", linestyle="-", label="Rigorous solution")

QMOM_N_data = helpers.load_csv_data("Marchisio2003_Case{}_N_QMOM.csv".format(case_num))

for x_val in QMOM_N_data:
    x = [x_val, x_val]
    y = [0, QMOM_N_data[x_val]]
    plt.plot(x, y, color="#FF5252", linestyle="-")

plt.plot(x_analytic, y_analytic, color="#0A246A", linestyle="-")

plt.legend()
plt.ylabel(r"$n(\xi)$")
plt.xlabel(r"$\xi$")
plt.xlim(1., 10.)
plt.ylim(0., args.nylim)

# Produce Figure c

plt.subplot(223)

plt.plot([], color="#0A246A", linestyle="-", label="Rigorous solution")
plt.plot([], color="#007F00", linestyle="None", marker="o", markerfacecolor="white", label="LnEQMOM N=3, $N_\\alpha$ = 20")
plt.plot([], color="#D82900", linestyle="None", marker="s", markerfacecolor="white", label="QMOM N=3")

M0_data = helpers.load_csv_data("Marchisio2003_Case{}_M0_RIG.csv".format(case_num))

plt.plot(M0_data.keys(), M0_data.values(), color="#0A246A", linestyle="-")

moment0_data = helpers.load_probe_data("%s/postProcessing/probes/0/moment.0.populationBalance" % case_dir)

x_all = sorted(list(moment0_data.keys()))
total_num = len(x_all)
di1 = int((1./1000.)*total_num)
im1 = int((20./1000.)*total_num)
di2 = int((10./1000.)*total_num)
im2 = int((50./1000.)*total_num)
di3 = int((25./1000.)*total_num)
im3 = int((100./1000.)*total_num)
di4 = int((45./1000.)*total_num)

x = []
low = 0
if di1 > 0:
    x = x + [x_all[i] for i in range(low,im1, di1) ]
    low = im1
if di2 > 0:
    x = x + [x_all[i] for i in range(low,im2, di2) ]
    low = im2
if di3 > 0:
    x = x + [x_all[i] for i in range(low,im3, di3) ]
    low = im3
x = x + [x_all[i] for i in range(low,total_num, di4) ]

y = [moment0_data[x] for x in x]

plt.plot(x, y, color="#007F00", linestyle="None", marker="o", markerfacecolor="white")

M0_QMOM_data = helpers.load_csv_data("Marchisio2003_Case{}_M0_QMOM.csv".format(case_num))

plt.plot(M0_QMOM_data.keys(), M0_QMOM_data.values(), color="#D82900", linestyle="None", marker="s", markerfacecolor="white")

plt.legend()
plt.ylabel(r"$M_{0}$")
plt.xlabel(r"$t$")
plt.xlim(0., args.tlim)
plt.ylim(-0.05, 1.)


# Produce Figure d
plt.subplot(224)

plt.plot([], color="#0A246A", linestyle="-", label="Rigorous solution")
plt.plot([], color="#007F00", linestyle="None", marker="o", markerfacecolor="white", label="LnEQMOM N=3, $N_\\alpha$ = 20")
plt.plot([], color="#D82900", linestyle="None", marker="s", markerfacecolor="white", label="QMOM N=3")

d43_data = helpers.load_csv_data("Marchisio2003_Case{}_D43_RIG.csv".format(case_num))

x = d43_data.keys()
y = d43_data.values()

plt.plot(x, y, color="#0A246A", linestyle="-") 

moment3_data = helpers.load_probe_data("%s/postProcessing/probes/0/moment.3.populationBalance" % case_dir)
moment4_data = helpers.load_probe_data("%s/postProcessing/probes/0/moment.4.populationBalance" % case_dir)

# Build set of position values to use
x_all = sorted(list(moment3_data.keys()))
total_num = len(x_all)
di1 = int((1./1000.)*total_num)
im1 = int((20./1000.)*total_num)
di2 = int((10./1000.)*total_num)
im2 = int((50./1000.)*total_num)
di3 = int((25./1000.)*total_num)
im3 = int((100./1000.)*total_num)
di4 = int((45./1000.)*total_num)

x = []
low = 0
if di1 > 0:
    x = x + [x_all[i] for i in range(low,im1, di1) ]
    low = im1
if di2 > 0:
    x = x + [x_all[i] for i in range(low,im2, di2) ]
    low = im2
if di3 > 0:
    x = x + [x_all[i] for i in range(low,im3, di3) ]
    low = im3
x = x + [x_all[i] for i in range(low,total_num, di4) ]

y = [moment4_data[x]/moment3_data[x] for x in x]

plt.plot(x, y, color="#007F00", linestyle="None", marker="o", markerfacecolor="white")

d43_qmom_data = helpers.load_csv_data("Marchisio2003_Case{}_D43_QMOM.csv".format(case_num))
x = list(d43_qmom_data.keys())
y = list(d43_qmom_data.values())

plt.plot(x, y, color="#D82900", linestyle="None", marker="s", markerfacecolor="white")

plt.legend(loc=args.dlegendloc)
plt.ylabel(r"$d_{43}$")
plt.xlabel(r"$t$")
plt.xlim(0., args.tlim)
plt.ylim(1., args.dyhigh)


plt.subplots_adjust(left=0.11, right = 0.98, bottom=0.1, top=0.95, wspace=0.2, hspace = 0.15)

plt.savefig(args.filename)
