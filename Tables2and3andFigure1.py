import sys
import subprocess
import math
import re
import matplotlib.pyplot as plt
import numpy as np

def lognormal_moment(k, mu, sigma):
    return math.exp((k*mu)+(k*k*sigma*sigma/2))

def lognormal_analytic_moment(k, mu1, sigma1, mu2, sigma2):
    return (lognormal_moment(k, mu1, sigma1)+lognormal_moment(k, mu2, sigma2))/2.

def kern(x, mu, sigma):
    return math.exp(-(math.log(x)-mu)**2/(2*sigma**2))/(x*sigma*math.sqrt(2*math.pi))

def f(x, mu1, sigma1, mu2, sigma2):
    return (kern(x, mu1, sigma1)+kern(x, mu2, sigma2))/2.

def f_num(x, node_definitions):
    value = 0
    for i in range(0,node_definitions['n']):
        value += node_definitions[i]['w']*kern(x, node_definitions[i]['ab'], node_definitions['sig'])
    return value

def f_num_single(x, node_definitions, i):
    return node_definitions[i]['w']*kern(x, node_definitions[i]['ab'], node_definitions['sig'])

def integrate(f_func, p_func, xmin, xmax, N):
    dx = (xmax-xmin)/N
    summation = 0.
    for i in range(0, N):
        x = xmin+(dx*i)
        summation += (f_func(x)-p_func(x))**2

    summation = math.sqrt(summation*dx)
    return summation

## Case variables

case_vars = {1: [3., 0.6, 3., 0.6],
             2: [1.2, 0.6, 3., 0.6],
             3: [3., 0.6, 5., 0.5],
             4: [3., 0.6, 1., 0.8]}

case_range = {1: [60, 60, 0.05],
              2: [60, 60, 0.15],
              3: [500, 450, 0.02],
              4: [60, 60, 0.2]}

case_analytic_moments = {}
case_numerical_nodes = {}
case_numerical_moments = {}

Node_nums = [2, 3, 4]

sigma_re = re.compile("Sigma = (\d*\.\d*)")
node_re = re.compile("Primary node (\d*)")
weight_re = re.compile("Primary weight = (\d*\.\d*)")
absicca_re = re.compile("Primary abscissa = (\d*\.\d*)")

for case in case_vars:
    # Build analytic moments for the case.
    analytic_moments = []
    for k in range(0, 2*Node_nums[-1]+1):
        analytic_moments.append(lognormal_analytic_moment(k, case_vars[case][0], case_vars[case][1], case_vars[case][2], case_vars[case][3]))
    case_analytic_moments[case] = analytic_moments

    # Calculate numerical moments for each set of node numbers
    numerical_nodes = {}
    numerical_moments = {}

    for node_num in Node_nums:
        node_definitions = {'n': node_num}

        # Build command
        command = ["Test-ExtendedMomentInversion", str(2*node_num+1)]
        for i in range(0, 2*node_num+1):
            command.append(str(analytic_moments[i]))

        # Run command
        output_lines = subprocess.check_output(command)
        found_sigma = False
        for line in output_lines.splitlines():
            str_line = line.decode("utf-8")
            sigma_match = sigma_re.match(str_line)
            if sigma_match:
                node_definitions['sig'] = float(sigma_match.group(1))
                found_sigma = True
        if not found_sigma:
            print("Couldn't get sigma!!")
            sys.exit(-1)

        # Extract weight, and abscissae information 
        with open('secondaryQuadrature', 'r') as quad_file:
            quadrature_lines = quad_file.readlines()

        # split lines by node
        current_node = -1
        temp_info = {}
        for line in quadrature_lines:
            node_match = node_re.match(line)
            if node_match:
                if current_node != -1:
                    node_definitions[current_node] = temp_info
                current_node = int(node_match.group(1))
                temp_info = {}
            weight_match = weight_re.match(line)
            if weight_match:
                temp_info['w'] = float(weight_match.group(1))
            absicca_match = absicca_re.match(line)
            if absicca_match:
                temp_info['ab'] = math.log(float(absicca_match.group(1)))
        if current_node != -1:
            node_definitions[current_node] = temp_info

        # Calculate numerical moments
        num_moments = []
        for k in range(0, 2*node_num+1):
            moment = 0
            for n in range(0, node_num):
                moment += node_definitions[n]['w']*lognormal_moment(k, node_definitions[n]['ab'], node_definitions['sig'])
            num_moments.append(moment)

        numerical_nodes[node_num] = node_definitions
        numerical_moments[node_num] = num_moments

    case_numerical_nodes[case] = numerical_nodes
    case_numerical_moments[case] = numerical_moments

# Calculate values in Table2
print("Table 2")
print("Case\tN=2\tN=3\tN=4")
for case in case_analytic_moments:
    for k in range(0, 2*Node_nums[-1]+1):
        report_string = ""
        if k == 0:
            report_string += "%i\t" % case
        else:
            report_string += " \t"

        for num in case_numerical_moments[case]:
            if k >= 2*case_numerical_nodes[case][num]['n']+1:
                report_string += "            \t"
            else:
                mom_err = abs(case_analytic_moments[case][k]-case_numerical_moments[case][num][k])/case_analytic_moments[case][k]
                report_string += "E_%i %.2e\t" % (k, mom_err)
        print(report_string)
    print()


# Calculate values in Table3
# We will numerically integrate the expression.

Title_line = ["Case"]
for num_nodes in case_numerical_nodes[1]:
    Title_line.append("N={}".format(num_nodes))
case_lines = [Title_line]
for case in case_vars:
    case_line = [case]
    for num_nodes in case_numerical_nodes[case]:
        node_definitions = case_numerical_nodes[case][2]
        F = lambda x: f(x, case_vars[case][0], case_vars[case][1], case_vars[case][2], case_vars[case][3])
        P = lambda x: f_num(x, node_definitions)

        d = integrate(F, P, 1e-12, 500, 5000)/case_analytic_moments[case][0]
        case_line.append(d)
    case_lines.append(case_line)

print("Table 3")
for line in case_lines:
    if type(line[0]) is str:
        print("%s\t%s\t%s\t%s" % (line[0], line[1], line[2], line[3]))
    else:
        print("%i\t%e\t%e\t%e" % (line[0], line[1], line[2], line[3]))

# Produce Figures 1a-d
plt.figure(1, figsize=(12,8), dpi=80)

Num_smooth = 1000
Num_point = 40
for case in case_vars:
    plt.subplot(220+int(case))

    plt.plot([], color="#0A246A", linestyle="-", label="Analytical solution")
    plt.plot([], color="#007F00", linestyle="--", label="EQMOM each nodes")
    plt.plot([], color="#D82900", marker="o", markerfacecolor="white", linestyle="None", label="Approximation Distribution")

    x = np.linspace(1e-12,case_range[case][1], Num_smooth)
    y = np.array([f(x, case_vars[case][0], case_vars[case][1], case_vars[case][2], case_vars[case][3]) for x in x])
    plt.plot(x, y, color="#0A246A", linestyle="-")

    for i in range(0,4):
        node_definition = case_numerical_nodes[case][4][i]
        y = np.array([f_num_single(x, case_numerical_nodes[case][4], i) for x in x])
        plt.plot(x, y, color="#007F00", linestyle="--")


    x = np.linspace(1e-12, case_range[case][1], Num_point)
    y = np.array([f_num(x, case_numerical_nodes[case][4]) for x in x])
    plt.plot(x, y, color="#D82900", marker="o", markerfacecolor="white", linestyle="None")

    plt.legend()
    plt.ylabel(r"$n(\xi)$")
    plt.xlabel(r"$\xi$")
    plt.xlim(0,case_range[case][0])
    plt.ylim(0,case_range[case][2])

plt.subplots_adjust(left=0.11, right = 0.98, bottom=0.1, top=0.95, wspace=0.2, hspace = 0.15)

plt.savefig("Figure1.png")
