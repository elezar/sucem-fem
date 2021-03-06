## Copyright (C) 2011 Stellenbosch University
##
## This file is part of SUCEM.
##
## SUCEM is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## SUCEM is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with SUCEM. If not, see <http://www.gnu.org/licenses/>. 
##
## Contact: cemagga@gmail.com 
from __future__ import division

import sympy as sp
from sympy import sin, cos, exp, pi

import sys
from sucemfem.Consts import mu0, c0

omega, mu, L, beta, r, theta = sp.symbols(
    'omega mu L beta r theta')

I0 = sp.Symbol('I0')

E_theta = 1j*omega*mu*I0*L*exp(-1j*beta*r)/(4*pi*r)*sin(theta)* \
          sin((beta*L/2)*cos(theta))/((beta*L/2)*cos(theta))

def eval_E_theta(freq, L_val, I_val, theta_val, r_val=1):
    return complex(E_theta.evalf(subs={
        omega:2*pi*freq,
        mu:mu0,
        I0:I_val,
        L:L_val,
        beta:2*pi*freq/c0,
        r:r_val,
        theta:theta_val,
        }))
        
if __name__ == '__main__':
    import numpy as np
    import pylab
    thetas = np.deg2rad(np.linspace(0,180, 181))
    freq = 1e9; L_val = 1; I_val = 1
    vals = [eval_E_theta(freq, L_val, I_val, th) for th in thetas]
    pylab.plot(np.rad2deg(thetas), np.abs(vals))
    pylab.show()
