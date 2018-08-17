import math
import argparse

def lognormal_moment(k, mu, sigma):
    return math.exp((k*mu)+(k*k*sigma*sigma/2))

def lognormal_analytic_moment(k, mu1, sigma1, mu2, sigma2):
    return (lognormal_moment(k, mu1, sigma1)+lognormal_moment(k, mu2, sigma2))/2.

parser = argparse.ArgumentParser("Program to calculate the analytic moments of Cases 1-4")
parser.add_argument("--mu1", required=True, type=float)
parser.add_argument("--sigma1", required=True, type=float)
parser.add_argument("--mu2", required=True, type=float)
parser.add_argument("--sigma2", required=True, type=float)
parser.add_argument("-N", default=5, help="Maximum number of moments to calculate", type=int)

args = parser.parse_args()

mu1 = args.mu1
sigma1 = args.sigma1
mu2 = args.mu2
sigma2 = args.sigma2
N = args.N

for k in range(0,N):
    print("M_%i = %.17f" % (k, lognormal_analytic_moment(k, mu1, sigma1, mu2, sigma2)))
