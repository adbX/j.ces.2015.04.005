import math
import csv
import subprocess
import re
import numpy as np
import scipy.integrate as integrate
import scipy.special as special
import scipy.linalg as linalg
from shutil import copyfile

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

def load_csv_data(filepath):
    data_dict = {}
    with open(filepath, "r") as analytic_file:
        csvreader = csv.reader(analytic_file, delimiter=",", quotechar='"')
        for row in csvreader:
            x = float(row[0])
            y = float(row[1])
            data_dict[x] = y
    return data_dict

def lognormal_moment(k, mu, sigma):
    return math.exp((k*mu)+(k*k*sigma*sigma/2))

def gamma_moment(k, mu, sigma):
    Lambda = mu/sigma
    return (math.gamma(Lambda+k)/math.gamma(Lambda))*(mu/Lambda)**k

def lognormal_analytic_moment(k, mu1, sigma1, mu2, sigma2):
    return (lognormal_moment(k, mu1, sigma1)+lognormal_moment(k, mu2, sigma2))/2.

def lognormal_kern(x, mu, sigma):
    return math.exp(-(math.log(x)-mu)**2/(2*sigma**2))/(x*sigma*math.sqrt(2*math.pi))

def gamma_kern(x, mu, sigma):
    Lambda = mu/sigma
    try:
        return (((x**(Lambda-1))*math.exp(-x/sigma))/(math.gamma(Lambda)*(sigma**Lambda)))
    except OverflowError:
        try:
            log_kern = (Lambda-1)*math.log(x)-(x/sigma)-special.loggamma(Lambda)-Lambda*math.log(sigma)
            return math.exp(log_kern)
        except OverflowError as e:
            print("x: ", x)
            print("mu: ", mu)
            print("sigma: ", sigma)
            print("Lambda: ", Lambda)
            raise e


def f_lognormal(x, mu1, sigma1, mu2, sigma2):
    return (lognormal_kern(x, mu1, sigma1)+lognormal_kern(x, mu2, sigma2))/2.

def f_num_lognormal(x, node_definitions):
    value = 0
    for i in range(0,node_definitions['n']):
        value += node_definitions[i]['w']*lognormal_kern(x, node_definitions[i]['ab'], node_definitions['sig'])
    return value

def f_num_gamma(x, node_definitions):
    value = 0
    for i in range(0,node_definitions['n']):
        value += node_definitions[i]['w']*gamma_kern(x, node_definitions[i]['ab'], node_definitions['sig'])
    return value

def f_num_single_lognormal(x, node_definitions, i):
    return node_definitions[i]['w']*lognormal_kern(x, node_definitions[i]['ab'], node_definitions['sig'])

def f_num_single_gamma(x, node_definitions, i):
    return node_definitions[i]['w']*gamma_kern(x, node_definitions[i]['ab'], node_definitions['sig'])

def l2diff(f_func, p_func, xmin, xmax, N):
    dx = (xmax-xmin)/N
    summation = 0.
    for i in range(0, N):
        x = xmin+(dx*i)
        summation += (f_func(x)-p_func(x))**2

    summation = math.sqrt(summation*dx)
    return summation

def log_coalescence_ndf(t, xi, loud=False):
    if loud:
        print(special.iv(1, 2*xi*math.sqrt(1-math.exp(-t))))
    return -t-2*xi+xi*math.exp(-t)-math.log(xi)-(1/2)*(1-math.exp(-t))+math.log(special.iv(1, 2*xi*math.sqrt(1-math.exp(-t))))

def coalescence_ndf(t, xi):
    #return math.exp(log_coalescence_ndf(t,xi))
    return (math.exp(-t-2*xi+xi*math.exp(-t))/(xi*math.sqrt(1-math.exp(-t))))*special.iv(1,2*xi*math.sqrt(1-math.exp(-t)))


def condensation_ndf(t, xi):
    return ((xi*math.exp(-t/2))**3*math.exp(-xi*math.exp(-t/2)))/(6*math.exp(t/2))

def extract_analytic_moment(f, xmin, xmax, N):
    # We are explicitly ignoring error here!!
    return integrate.quad(lambda x: (x**N)*f(x), xmin, xmax)[0]

def extract_moments_from_data(x_list, y_list, N):
    # Extract moments from distribution
    new_moment = 0.
    for j in range(0,len(x_list)-1):
        dx = x_list[j+1]-x_list[j]
        x = (x_list[j+1]+x_list[j])/2.
        y = (y_list[j+1]+y_list[j])/2.
        new_moment += y*(x**N)*dx
    return new_moment

sigma_re = re.compile("Sigma = (\d*\.\d*)")
node_re = re.compile("Primary node (\d*)")
weight_re = re.compile("Primary weight = (\d*\.\d*)")
absicca_re = re.compile("Primary abscissa = (\d*\.\d*)")

def perform_moment_inversion(node_num, analytic_moments, inversion_type='lognormal'):
    # Prepare moment inversion for the appropriate type.    
    copyfile('quadratureProperties.{}'.format(inversion_type), 'quadratureProperties')

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
            if inversion_type == 'lognormal':
                temp_info['ab'] = math.log(float(absicca_match.group(1)))
            else:
                temp_info['ab'] = float(absicca_match.group(1))
    if current_node != -1:
        node_definitions[current_node] = temp_info

    return node_definitions

def lognormal_eqmom_invert(mom, n, tolerance=1e-15):
    x = []
    w = []
    sig = None

    if len(mom) < 2*n+1:
        print("Not enough moments provided!")
        return [x, w, sig]

    if mom[0] < 0:
        print("negative number density in 1-D quadrature!")
        return [x, w]

    #1. Guess sigma
    z = math.exp(1.**2/2.)

    mom_star = []
    for i in range(0, 2*n+1):
        mom_star.append(0.)

    print("1")
    error = np.inf
    while error > tolerance:
        print("2")
        #2. Generate M_star moments
        for i in range(0, 2*n):
            mom_star[i] = mom[i]*z**(-(2*i)**2)

        #3. use the wheeler inversion to obtain weights and abscissae for the mom_star moments
        [chi, weight] = wheeler_invert(mom_star, n)
        print("wheeler result")
        print(chi)
        print(weight)

        x = chi
        w = weight

        #4. Calculate mom_star[2n]
        mom_star[2*n] = 0.
        for i in range(0, n):
            mom_star[2*n] = weight[i]*chi[i]**(2*n)

        #5. J function and error:
        error = abs(m[2*n]-z**((2*n)**2)*ms[2*n])
        if error >= tolerance:
            z = (mom[2*n]/mom_star[2*n])**(-(2*n)**2)

    sig = math.sqrt(2*math.log(z))
    return [ w, chi, sig]
    

def wheeler_invert(mom, n):
    x = []
    w = []
    if len(mom) < 2*n:
        print("Not enough moments provided!")
        return [x, w]

    if mom[0] < 0:
        print("negative number density in 1-D quadrature!")
        return [x, w]
    elif mom[0] == 0:
        w = [0]
        x = [0]
        return [x, w]
    if n == 1:
        w = mom[0]
        x = mom[1]/mom[0]
        nout = 1
        return [ x, w]

    Z = np.zeros((2*n+1,2*n+1))

    alpha = []
    beta = []

    # initialize rows
    for i in range(1,2*n+1):
        Z[1][i] = mom[i-1] 
    alpha = [mom[1]/mom[0]]
    beta = [mom[0]]

    # Calculate recursion coefficients
    for k in range(2,n+1):
        # first calculate row values
        for l in range(k,2*n-k+2):
            Z[k][l] = Z[k-1][l+1] - alpha[k-2]*Z[k-1][l] - beta[k-2]*Z[k-2][l]
        # Calc new alpha/beta values
        alpha.append((Z[k][k+1]/Z[k][k])-(Z[k-1][k]/Z[k-1][k-1]))
        beta.append(Z[k][k]/Z[k-1][k-1])

    for b in beta:
        if b < 0:
            print("Error! Moments not realizable! {}".format(beta))
            return [x, w]

    diagonal_vals = np.array(alpha)
    offdiagonal_vals = np.sqrt(np.array(beta[1:]))

    (w_res, v_res) = linalg.eigh_tridiagonal(diagonal_vals, offdiagonal_vals)

    for i in range(0,n):
        x.append(w_res[i])

    for i in range(0,n):
        v = v_res[:,i]
        mag = 0.
        for j in range(0, n):
            mag += v[j]*v[j]
        w.append(((v[0]*mom[0])**2)/mag)

    return [x, w]
