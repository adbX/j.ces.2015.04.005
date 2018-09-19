# Figure 12:
xi_intercept = 232 # Extracted from WebPlotDigitizer
f_intercept = 1e-15

[t, xi] = var("t xi")

def coalescence_ndf(t, xi):
	return ((exp(-t-2*xi+xi*exp(-t)))/(xi*sqrt(1-exp(-t))))*bessel_I(1, 2*xi*sqrt(1-exp(-t)))

results = find_root(coalescence_ndf(t, xi_intercept) == f_intercept, 1e-4, 20.)
print("The t value for Figure 12 is: " + str(results))

# Figure 13:
xi_intercept = 76.481 # Extracted from WebPlotDigitizer
f_intercept = 1e-20

def condensation_ndf(t, xi):
	return ((xi*exp(-t/2))^3*exp(-xi*exp(-t/2)))/(6*exp(t/2))

results = find_root(condensation_ndf(t, xi_intercept) == f_intercept, 1e-4, 20.)
print("The t value for Figure 13 is " + str(results))
