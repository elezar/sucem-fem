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
# Authors:
# Neilen Marais <nmarais@gmail.com>
# Evan Lezar <mail@evanlezar.com>

"""this is a set of test cases for the testing of the linear algebra solvers in FenicsCode/Utilities"""

import sys
import unittest
import numpy as np
import scipy.sparse

sys.path.insert(0, '../')
from sucemfem.Utilities.LinalgSolvers import solve_sparse_system, calculate_residual
del sys.path[0]


class TestSparseSolver ( unittest.TestCase ):
    def test_sparse_identity ( self ):
        N = 1000;
        A = scipy.sparse.eye ( N, N )
        b = np.random.rand ( N )

        try:
            x = solve_sparse_system ( A, b )
        except AttributeError:
            # Deal with older scipy versions that do not have spilu module
            x = solve_sparse_system ( A, b, preconditioner_type='diagonal')
        
        np.testing.assert_array_equal( b, x )
   
class TestOther ( unittest.TestCase ):   
    def _call_function (self, A, x, b ):
        print b.shape
        print x.shape
        assert ( calculate_residual ( A, x, b ) == 0 )
    
    def test_x1d_b1d (self):
        N = 1000;
        A = scipy.sparse.eye ( N, N )
        b = np.random.rand( N )
        x = b.copy()
        self._call_function(A, x, b)
        
    def test_x1d_brow (self):
        N = 1000;
        A = scipy.sparse.eye ( N, N )
        b = np.random.rand( 1, N )
        x = b.copy()[0,:]
        self._call_function(A, x, b)
        
    def test_x1d_bcolumn (self):
        N = 1000;
        A = scipy.sparse.eye ( N, N )
        b = np.random.rand( N, 1 )
        x = b.copy()[:,0]
        self._call_function(A, x, b)
        
    def test_xcol_b1d (self):
        N = 1000;
        A = scipy.sparse.eye ( N, N )
        b = np.random.rand( N )
        x = b.copy().reshape( (N,1) )
        self._call_function(A, x, b)
        
    def test_xcol_brow (self):
        N = 1000;
        A = scipy.sparse.eye ( N, N )
        b = np.random.rand( 1, N )
        x = b.copy().reshape ( (N,1) )
        self._call_function(A, x, b)
        
    def test_xcol_bcol (self):
        N = 1000;
        A = scipy.sparse.eye ( N, N )
        b = np.random.rand( N, 1 )
        x = b.copy()
        self._call_function(A, x, b)
    
    
if __name__ == "__main__":
    unittest.main()
