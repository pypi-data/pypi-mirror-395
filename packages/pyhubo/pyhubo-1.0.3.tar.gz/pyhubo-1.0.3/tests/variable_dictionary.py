# Set up path for local development (remove if PyHUBO is installed via pip)
parent_directory = "/Users/frederikkoch/Nextcloud/Pyhubo"
import sys
sys.path.append(parent_directory)

# Import PyHUBO core classes
from src.pyhubo.VariableAssignment import VariableAssignment  # Represents x_i = v_j assignments
from src.pyhubo.VariableDictionary import VariableDictionary    # Maps variables to binary representations
from src.pyhubo.HuboHamiltonian import HuboHamiltonian        # Generates HUBO coefficients
import unittest
from src.pyhubo.VariableDictionary import VariableDictionary
from src.pyhubo.VariableAssignment import VariableAssignment

class TestVariableDictionary(unittest.TestCase):

    def test_domain_initialization_and_validation(self):
        # Test non-empty domains
        with self.assertRaises(ValueError):
            VariableDictionary({"var1": []})

        # Test no duplicate values
        with self.assertRaises(ValueError):
            VariableDictionary({"var1": ["a", "a"]})

        # Test immutability of stored domains
        domains = {"var1": ["a", "b"]}
        vd = VariableDictionary(domains)
        domains["var1"].append("c")
        self.assertNotIn("c", vd.get_domain("var1"))

        # Test mixed data types
        vd = VariableDictionary({"var1": [1, "a", (1, 2), frozenset({3})]})
        self.assertEqual(len(vd.get_domain("var1")), 4)

    def test_bidirectional_mapping(self):
        vd = VariableDictionary({"var1": ["a", "b", "c"]})

        # Test valid mappings
        self.assertEqual(vd.get_index("var1", "a"), 0)
        self.assertEqual(vd.get_value("var1", 1), "b")

        # Test invalid mappings
        with self.assertRaises(KeyError):
            vd.get_index("var2", "a")
        with self.assertRaises(ValueError):
            vd.get_index("var1", "d")
        with self.assertRaises(IndexError):
            vd.get_value("var1", 4)

    def test_domain_retrieval(self):
        vd = VariableDictionary({"var1": ["a", "b", "c"]})

        # Test valid domain retrieval
        self.assertEqual(vd.get_domain("var1"), ("a", "b", "c", "aux_0"))
        self.assertEqual(vd.get_domain_size("var1"), 4)

        # Test invalid domain retrieval
        with self.assertRaises(KeyError):
            vd.get_domain("var2")

    def test_variable_management(self):
        vd = VariableDictionary({"var1": ["a", "b"], "var2": [1, 2, 3]})

        # Test variables method
        self.assertEqual(set(vd.variables()), {"var1", "var2"})

        # Test __contains__
        self.assertIn("var1", vd)
        self.assertNotIn("var3", vd)

        # Test __len__
        self.assertEqual(len(vd), 2)

    def test_one_hot_penalty(self):
        vd = VariableDictionary({"var1": ["a", "b"]})

        # Test penalty generation
        penalty = vd.one_hot_penalty()
        self.assertIsNotNone(penalty)

    def test_equality_and_representation(self):
        vd1 = VariableDictionary({"var1": ["a", "b"]})
        vd2 = VariableDictionary({"var1": ["a", "b"]})
        vd3 = VariableDictionary({"var1": ["a", "c"]})

        # Test equality
        self.assertEqual(vd1, vd2)
        self.assertNotEqual(vd1, vd3)

        # Test representation
        self.assertEqual(repr(vd1), "VariableDictionary({var1: ['a', 'b']})")

    def test_immutability(self):
        domains = {"var1": ["a", "b"]}
        vd = VariableDictionary(domains)

        # Modify input dictionary
        domains["var1"].append("c")
        self.assertNotIn("c", vd.get_domain("var1"))

        # Test immutability of returned domains
        with self.assertRaises(TypeError):
            vd.get_domain("var1")[0] = "x"

    def test_edge_cases(self):
        # Test with no variables
        vd = VariableDictionary({})
        self.assertEqual(len(vd), 0)

        # Test with large domains
        large_domain = list(range(1000))
        vd = VariableDictionary({"var1": large_domain})
        import math
        domain_size_with_aux_vars = 2**math.ceil(math.log2(1000))
        self.assertEqual(vd.get_domain_size("var1"), domain_size_with_aux_vars)

    def test_error_handling(self):
        vd = VariableDictionary({"var1": ["a", "b"]})

        # Test descriptive error messages
        with self.assertRaises(KeyError):
            vd.get_index("var2", "a")
        with self.assertRaises(ValueError):
            vd.get_index("var1", "c")
        with self.assertRaises(IndexError):
            vd.get_value("var1", 3)

if __name__ == "__main__":
    unittest.main()
