coalescence_t = 0.59843625345
condensation_t = 0.622446664404

[t, xi] = var("t xi")

def coalescence_ndf(t, xi):
	return ((exp(-t-2*xi+xi*exp(-t)))/(xi*sqrt(1-exp(-t))))*bessel_I(1, 2*xi*sqrt(1-exp(-t)))

def condensation_ndf(t, xi):
	return ((xi*exp(-t/2))^3*exp(-xi*exp(-t/2)))/(6*exp(t/2))

def coalescence_moment(n):
	return numerical_integral(xi**n*coalescence_ndf(coalescence_t, xi), 0, Infinity)

for i in range(0,15):
	print(coalescence_moment(i))
