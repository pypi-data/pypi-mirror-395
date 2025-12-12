# Set up path for local development (remove if PyHUBO is installed via pip)
parent_directory = "/Users/frederikkoch/Nextcloud/Pyhubo"
import sys
sys.path.append(parent_directory)

import unittest
from src.pyhubo.HuboHamiltonian import PauliZ

class TestPauliZ(unittest.TestCase):

    def test_identity_operator(self):
        z = PauliZ()
        self.assertEqual(len(z), 0)
        self.assertEqual(str(z), "I")

    def test_non_identity_operator(self):
        z = PauliZ([("a", 0)])
        self.assertEqual(len(z), 1)
        self.assertIn(("a", 0), z)
        self.assertEqual(str(z), "Z_{a,0}")

    def test_multiplication_identity(self):
        z1 = PauliZ([("a", 0)])
        identity = PauliZ()
        self.assertEqual(z1 * identity, z1)

    def test_multiplication_symmetric_difference(self):
        z1 = PauliZ([("a", 0)])
        z2 = PauliZ([("a", 1)])
        result = z1 * z2
        self.assertEqual(len(result), 2)
        self.assertIn(("a", 0), result)
        self.assertIn(("a", 1), result)

    def test_multiplication_commutativity(self):
        z1 = PauliZ([("a", 0)])
        z2 = PauliZ([("b", 1)])
        self.assertEqual(z1 * z2, z2 * z1)

    def test_hash_and_equality(self):
        z1 = PauliZ([("a", 0)])
        z2 = PauliZ([("a", 0)])
        z3 = PauliZ([("b", 1)])
        self.assertEqual(z1, z2)
        self.assertNotEqual(z1, z3)
        self.assertEqual(hash(z1), hash(z2))

    def test_frozenset_behavior(self):
        z = PauliZ([("a", 0), ("b", 1)])
        self.assertEqual(len(z), 2)
        self.assertIn(("a", 0), z)
        self.assertIn(("b", 1), z)
        self.assertNotIn(("c", 2), z)

    def test_string_representation(self):
        z = PauliZ([("a", 0), ("b", 1)])
        self.assertEqual(repr(z), "PauliZ([('a', 0), ('b', 1)])")
        self.assertEqual(str(z), "Z_{a,0} * Z_{b,1}")

    def test_invalid_multiplication(self):
        z = PauliZ([("a", 0)])
        with self.assertRaises(TypeError):
            z * "invalid"

if __name__ == "__main__":
    unittest.main()