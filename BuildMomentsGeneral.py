import math
import argparse

def lognormal_moment(k, mu, sigma):
    return math.exp((k*mu)+(k*k*sigma*sigma/2))

parser = argparse.ArgumentParser("Program to calculate the analytic moments of Cases 1-4")
parser.add_argument("--node", required=True, action='append', nargs=3, metavar=('weight', 'abscissa', 'sigma'), type=float)
parser.add_argument("-N", default=5, help="Number of nodes to calculate", type=int)

args = parser.parse_args()

nodes = []
for node in args.node:
    nodes.append([node[0],math.log(node[1]), node[2]])

for k in range(0,args.N):
    moment = 0.
    for node in nodes:
        moment += node[0]*lognormal_moment(k, node[1], node[2])
    print("M_%i = %.17f" % (k, moment))
