# Set up path for local development (remove if PyHUBO is installed via pip)
parent_directory = "/Users/frederikkoch/Nextcloud/Pyhubo"
import sys
sys.path.append(parent_directory)


import unittest
from src.pyhubo.HuboHamiltonian import HuboHamiltonian
from src.pyhubo.VariableDictionary import VariableDictionary
from src.pyhubo.VariableAssignment import VariableAssignment

class TestHuboHamiltonian(unittest.TestCase):

    def test_valid_inputs(self):
        variable_dict = VariableDictionary({"x": [0, 1], "y": [0, 1]})
        variable_assignment = VariableAssignment("x", 0) * VariableAssignment("y", 1)
        hamiltonian = HuboHamiltonian(variable_assignment, variable_dict)
        self.assertIsInstance(hamiltonian, HuboHamiltonian)

    def test_invalid_variable(self):
        variable_dict = VariableDictionary({"x": [0, 1]})
        variable_assignment = VariableAssignment("z", 0)
        with self.assertRaises(ValueError):
            HuboHamiltonian(variable_assignment, variable_dict)

    def test_qubit_structure_creation(self):
        variable_dict = VariableDictionary({"x": [0, 1, 2]})
        variable_assignment = VariableAssignment()
        hamiltonian = HuboHamiltonian(variable_assignment, variable_dict)
        qubit_structure = hamiltonian._build_qubit_structure()
        self.assertIn("x", qubit_structure)
        self.assertEqual(len(qubit_structure["x"]), 2)  # 2 bits for domain size 3

    def test_hamiltonian_coefficients(self):
        variable_dict = VariableDictionary({"x": [0, 1], "y": [0, 1]})
        variable_assignment = VariableAssignment("x", 0)* VariableAssignment("y", 1)
        hamiltonian = HuboHamiltonian(variable_assignment, variable_dict)
        coeffs = hamiltonian.get_hamiltonian()
        self.assertGreater(len(coeffs), 0)

    def test_export_functionality(self):
        variable_dict = VariableDictionary({"x": [0, 1]})
        variable_assignment = VariableAssignment("x", 0)
        hamiltonian = HuboHamiltonian(variable_assignment, variable_dict)
        export = hamiltonian.export_dict()
        self.assertIsInstance(export, dict)
        self.assertTrue(all(isinstance(k, frozenset) for k in export.keys()))

    def test_string_representation(self):
        variable_dict = VariableDictionary({"x": [0, 1]})
        variable_assignment = VariableAssignment()
        hamiltonian = HuboHamiltonian(variable_assignment, variable_dict)
        self.assertIn("HuboHamiltonian", repr(hamiltonian))
        self.assertIn("coefficients not yet computed", str(hamiltonian))

if __name__ == "__main__":
    unittest.main()