"""Design Model module for generating NERDSS molecule types and reactions, and corresponding files from user design.

This module defines the `DesignModel` class, inheriting from the `Model` class, which is used to generate NERDSS molecule types and reactions, and corresponding files by designing.
"""

from .model import Model

class DesignModel(Model):
    """"A class for generating NERDSS molecule types and reactions, and corresponding files by designing.
    
    Attributes:
        pdb_file (str): The path to the PDB structure file.
    """

    def __init__(self, path):
        super().__init__(path)
