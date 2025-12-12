import os
import json
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from .coords import Coords

@dataclass
class MoleculeInterface:
    """Represents an interface of a molecule type.
    
    Attributes:
        name (str): Name of the interface.
        coord (Tuple[float, float, float]): Coordinates of the interface.
    """
    name: str
    coord: Coords

@dataclass
class MoleculeType:
    """Represents a molecule type in the model.
    
    Attributes:
        name (str): Name of the molecule type.
        interfaces (List[MoleculeInterface]): List of interfaces associated with the molecule.
    """
    name: str
    interfaces: List[MoleculeInterface]
    diffusion_translation: float = 0.0
    diffusion_rotation: float = 0.0

@dataclass
class ReactionType:
    """Represents a reaction in the model.
    
    Attributes:
        name (str): Reaction expression.
        binding_radius (float): Binding radius of the reaction.
        binding_angles (Tuple[float, float, float, float, float]): Binding angles.
        norm1 (Tuple[float, float, float]): Normal vector 1.
        norm2 (Tuple[float, float, float]): Normal vector 2.
    """
    name: str
    binding_radius: float
    binding_angles: Tuple[float, float, float, float, float]
    norm1: Tuple[float, float, float]
    norm2: Tuple[float, float, float]
    ka: float = 0.0  # Forward rate constant
    kb: float = 0.0  # Reverse rate constant

@dataclass
class Model:
    """Parent class for all models to generate input files for NERDSS simulations.
    
    Attributes:
        name (str): Name of the model.
        molecule_types (List[MoleculeType]): List of molecule types in the model.
        reactions (List[Reaction]): List of reactions in the model.
    """
    name: str
    molecule_types: List[MoleculeType] = field(default_factory=list)
    reactions: List[ReactionType] = field(default_factory=list)

    def save_model(self, file_path: str) -> None:
        """Saves the model to a specified JSON file.
        
        Args:
            file_path (str): Path to the file where the model should be saved.
        """
        data = {
            "name": self.name,
            "molecule_types": [
                {
                    "name": mol.name,
                    "interfaces": [
                        {"name": iface.name, "coord": iface.coord} for iface in mol.interfaces
                    ],
                    "diffusion_translation": mol.diffusion_translation,
                    "diffusion_rotation": mol.diffusion_rotation,
                }
                for mol in self.molecule_types
            ],
            "reactions": [
                {
                    "name": rxn.name,
                    "binding_radius": rxn.binding_radius,
                    "binding_angles": rxn.binding_angles,
                    "norm1": rxn.norm1,
                    "norm2": rxn.norm2,
                    "ka": rxn.ka,
                    "kb": rxn.kb,
                }
                for rxn in self.reactions
            ],
        }
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4, cls=CustomJSONEncoder)  # Use custom encoder

    @classmethod
    def load_model(cls, file_path: str) -> "Model":
        """Loads a model from a specified JSON file.
        
        Args:
            file_path (str): Path to the JSON file containing the model data.
        
        Returns:
            Model: An instance of the Model class with the loaded data.
        """
        with open(file_path, "r") as file:
            data = json.load(file)

        molecule_types = [
            MoleculeType(
                name=mol["name"],
                interfaces=[MoleculeInterface(name=iface["name"], coord=Coords(**iface["coord"])) for iface in mol["interfaces"]],
                diffusion_translation=mol["diffusion_translation"],
                diffusion_rotation=mol["diffusion_rotation"],
            )
            for mol in data["molecule_types"]
        ]

        reactions = [
            ReactionType(
                name=rxn["name"],
                binding_radius=rxn["binding_radius"],
                binding_angles=tuple(rxn["binding_angles"]),
                norm1=tuple(rxn["norm1"]),
                norm2=tuple(rxn["norm2"]),
                ka=rxn["ka"],
                kb=rxn["kb"],
            )
            for rxn in data["reactions"]
        ]

        return cls(name=data["name"], molecule_types=molecule_types, reactions=reactions)

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Coords serialization and NumPy types."""
    
    def default(self, obj):
        if isinstance(obj, Coords):
            return {"x": obj.x, "y": obj.y, "z": obj.z}  # Convert Coords to dict
        elif isinstance(obj, np.float32):  # Convert numpy float32 to standard float
            return float(obj)
        elif isinstance(obj, np.ndarray):  # Convert numpy array to list
            return obj.tolist()
        return super().default(obj)
