# Authors:
# Neilen Marais <nmarais@gmail.com>
# Evan Lezar <mail@evanlezar.com>
from __future__ import division
import dolfin
from FenicsCode.BoundaryConditions import BoundaryCondition


class EssentialBoundaryCondition(BoundaryCondition):
    """Essential boundary condition class

    Sets up Dirichlet type boundary conditions for prescribed boundary
    values. The boundary conditions are applied to the user-specified
    function space self.function_space. If a non-zero BC is required,
    set_boundary_value_expression() needs to be called.

    The boundary region can be specified using a pre-defined mesh
    function (init_with_meshfunction()) or using a SubDomain object
    (init_with_subdomain())

    Also see documentation of the parent class
    """

    def init_with_meshfunction(self, mesh_function, region_number):
        """Initialise using a mesh function to indicate boundary region

        Parameters
        ----------

        mesh_function -- A 'uint' mesh function defined on the facets
            (i.e. of dimension one lower than mesh geometry) of the
            computational mesh

        region_number -- Region number (as defined in mesh_function)
            that this boundary condition should be applied to
        """
        self.set_region_number ( region_number )
        self.set_mesh_function ( mesh_function )

    def set_PEC_expression ( self ):
        """Initialise and set the BC expression to a zero-valued Dolfin Expression 
        with dimension equal to that of the mesh.
        """
        expr = ()
        for i in range(self.function_space.mesh().geometry().dim()):
            expr += ('0.0',)
        
        self.set_boundary_value_expression ( dolfin.Expression(expr, degree=1) )

    def get_essential_application_func(self, function_space=None):
        """Return an essential boundary condition application function.

        See parent class documentation for more details
        """
        if function_space is not None: self.set_function_space ( function_space )
                
        if self.boundary_value_expression is None:
            self.set_PEC_expression()
            
        self._dirichletBC = dolfin.DirichletBC(self.function_space, 
                                               self.boundary_value_expression, 
                                               self.mesh_function, 
                                               self.region_number)
        return self._dirichletBC.apply

class PECWallsBoundaryCondition ( EssentialBoundaryCondition ):
    """A class for an essential boundary condition that models PEC walls
    """
    def init_with_mesh (self, mesh ):
        """initialise the boundary condition using the mesh.
        
        A mesh function is constructed from the mesh and the boundary region is marked.
        
        @param mesh: The mesh on which the boundary condition is to be applied
        """
        mesh_function = dolfin.MeshFunction(
                    'uint', mesh, mesh.topology().dim()-1)
        mesh_function.set_all ( 0 )
        walls = dolfin.DomainBoundary()
        walls.mark(mesh_function, 999)
                
        self.init_with_meshfunction(mesh_function, 999)
