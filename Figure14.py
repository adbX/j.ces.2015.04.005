import helpers
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import math
import sys

cases = [5, 6, 7, 8, 9]
num_nodes = 2

ylims = { 5:[-1e1,1e1],
          6:[-1e1,1e1],
          7:[-1e1,1e1],
          8:[-1e1,1.5e1],
          9:[-3,3] }

# Produce Figures 2a-d
plt.figure(14, figsize=(12,16), dpi=80)

for case in cases:
    # Load rigorous data
    rig_data = helpers.load_csv_data("Passalaqua2015_Case{}_N_RIG.csv".format(case))
    x = list(rig_data.keys())
    y = list(rig_data.values())

    # Extract moments from distribution
    m = []
    for i in range(0,2*num_nodes+1):
        m.append(helpers.extract_moments_from_data(x, y, i))

    m0 = m[0]
    for i in range(0,2*num_nodes+1):
        m[i] = m[i]/m0

    print("Extracted Moments:")
    for i in range(0, 2*num_nodes+1):
        print("M_{} = {}".format(i, m[i]))

    #print(helpers.perform_moment_inversion(2, m))
    #print(helpers.lognormal_eqmom_invert(m, 2))
    #sys.exit(0)

    # 'target' function
    f = lambda x: m[2]**3*x**8-2*m[1]*m[2]*m[3]*x**6+(m[0]*m[3]**2+m[1]**2*m[4])*x**2-m[0]*m[2]*m[4]

    plt.subplot(5, 3, ((case-5)*3)+1)

    x = np.linspace(0, 1, 200)

    y = [f(math.exp(v**2/2.)) for v in x]
    #y = [f(x) for x in x]

    plt.plot(x, y, linestyle='-', color='k')
    lower_bound = abs(m[2]**3-2*m[1]*m[2]*m[3]+(m[0]*m[3]**2+m[1]**2*m[4])-m[0]*m[2]*m[4])
    plt.ylim(-1.2*lower_bound, 1.2*lower_bound)
    #plt.ylim(ylims[case][0],ylims[case][1])
    #plt.xlim(0., 1.)

plt.savefig("Figure14.png")
