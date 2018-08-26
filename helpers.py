import math
import csv

def load_probe_data(filepath):
    data_dict = {}
    with open(filepath, "r") as filedata:
        lines = filedata.readlines()
    for line in lines:
        if line[0] == "#":
            continue
        components = line.split()
        try:
            x = float(components[0])
            y = float(components[1])
            data_dict[x] = y
        except:
            pass
    return data_dict

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

def l2diff(f_func, p_func, xmin, xmax, N):
    dx = (xmax-xmin)/N
    summation = 0.
    for i in range(0, N):
        x = xmin+(dx*i)
        summation += (f_func(x)-p_func(x))**2

    summation = math.sqrt(summation*dx)
    return summation
