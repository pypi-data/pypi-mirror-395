"""Platonic Solids Model module for generating NERDSS molecule types and reactions, and corresponding files for specified platonic solid type.

This module defines the `PlantonicSolidsModel` class, inheriting from the `Model` class, which is used to generate NERDSS molecule types and reactions, and corresponding files for platonic solid.
"""

from .model import Model

class PlantonicSolidsModel(Model):
    """"A class for generating NERDSS molecule types and reactions, and corresponding files for platonic solid.
    
    Attributes:
        pdb_file (str): The path to the PDB structure file.
        solid_type (str): The platonic solid type.
        binding_site_position (str): The binding site position.
    """

    def __init__(self, path, solid_type, binding_site_position):
        super().__init__(path)
        self.solid_type = solid_type
        self.binding_site_position = binding_site_position
