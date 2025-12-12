# Set up path for local development (remove if PyHUBO is installed via pip)
parent_directory = "/Users/frederikkoch/Nextcloud/Pyhubo"
import sys
sys.path.append(parent_directory)

# Import PyHUBO core classes
from src.pyhubo.VariableAssignment import VariableAssignment  # Represents x_i = v_j assignments
from src.pyhubo.VariableDictionary import VariableDictionary    # Maps variables to binary representations
from src.pyhubo.HuboHamiltonian import HuboHamiltonian        # Generates HUBO coefficients

import unittest

class TestVariableAssignment(unittest.TestCase):
    def test_placeholder(self):
        """Placeholder test to verify setup."""
        self.assertTrue(True)

    def test_empty_initialization(self):
        """Test creating an empty VariableAssignment."""
        va = VariableAssignment()
        self.assertEqual(va.terms, {}, "Empty VariableAssignment should have no terms.")

    def test_single_variable_initialization(self):
        """Test creating a VariableAssignment with a single variable-value pair."""
        va = VariableAssignment("x", 1)
        expected_terms = {frozenset({("x", 1)}): 1.0}
        self.assertEqual(va.terms, expected_terms, "Single variable initialization failed.")

    def test_invalid_initialization_non_hashable(self):
        """Test creating a VariableAssignment with non-hashable inputs."""
        with self.assertRaises(ValueError):
            VariableAssignment(["x"], 1)
        with self.assertRaises(ValueError):
            VariableAssignment("x", {1: 2})

    def test_invalid_initialization_partial_inputs(self):
        """Test creating a VariableAssignment with partial inputs."""
        with self.assertRaises(ValueError):
            VariableAssignment("x")
        with self.assertRaises(ValueError):
            VariableAssignment(value=1)

    def test_addition_non_overlapping_terms(self):
        """Test adding two VariableAssignment objects with non-overlapping terms."""
        va1 = VariableAssignment("x", 1)
        va2 = VariableAssignment("y", 2)
        result = va1 + va2
        expected_terms = {
            frozenset({("x", 1)}): 1.0,
            frozenset({("y", 2)}): 1.0
        }
        self.assertEqual(result.terms, expected_terms, "Addition with non-overlapping terms failed.")

    def test_addition_overlapping_terms(self):
        """Test adding two VariableAssignment objects with overlapping terms."""
        va1 = VariableAssignment("x", 1)
        va2 = VariableAssignment("x", 1)
        result = va1 + va2
        expected_terms = {
            frozenset({("x", 1)}): 2.0
        }
        self.assertEqual(result.terms, expected_terms, "Addition with overlapping terms failed.")

    def test_addition_with_constant(self):
        """Test adding a constant to a VariableAssignment."""
        va = VariableAssignment("x", 1)
        result = va + 5
        expected_terms = {
            frozenset({("x", 1)}): 1.0,
            frozenset(): 5.0
        }
        self.assertEqual(result.terms, expected_terms, "Addition with constant failed.")

    def test_addition_with_zero(self):
        """Test adding zero to a VariableAssignment."""
        va = VariableAssignment("x", 1)
        result = va + 0
        self.assertEqual(result.terms, va.terms, "Addition with zero should not change the VariableAssignment.")

    def test_addition_to_itself(self):
        """Test adding a VariableAssignment to itself."""
        va = VariableAssignment("x", 1)
        result = va + va
        expected_terms = {
            frozenset({("x", 1)}): 2.0
        }
        self.assertEqual(result.terms, expected_terms, "Addition to itself failed.")

    def test_subtraction_non_overlapping_terms(self):
        """Test subtracting two VariableAssignment objects with non-overlapping terms."""
        va1 = VariableAssignment("x", 1)
        va2 = VariableAssignment("y", 2)
        result = va1 - va2
        expected_terms = {
            frozenset({("x", 1)}): 1.0,
            frozenset({("y", 2)}): -1.0
        }
        self.assertEqual(result.terms, expected_terms, "Subtraction with non-overlapping terms failed.")

    def test_subtraction_overlapping_terms(self):
        """Test subtracting two VariableAssignment objects with overlapping terms."""
        va1 = VariableAssignment("x", 1)
        va2 = VariableAssignment("x", 1)
        result = va1 - va2
        expected_terms = {}
        self.assertEqual(result.terms, expected_terms, "Subtraction with overlapping terms failed.")

    def test_subtraction_with_constant(self):
        """Test subtracting a constant from a VariableAssignment."""
        va = VariableAssignment("x", 1)
        result = va - 5
        expected_terms = {
            frozenset({("x", 1)}): 1.0,
            frozenset(): -5.0
        }
        self.assertEqual(result.terms, expected_terms, "Subtraction with constant failed.")

    def test_subtraction_with_zero(self):
        """Test subtracting zero from a VariableAssignment."""
        va = VariableAssignment("x", 1)
        result = va - 0
        self.assertEqual(result.terms, va.terms, "Subtraction with zero should not change the VariableAssignment.")

    def test_subtraction_from_itself(self):
        """Test subtracting a VariableAssignment from itself."""
        va = VariableAssignment("x", 1)
        result = va - va
        expected_terms = {}
        self.assertEqual(result.terms, expected_terms, "Subtraction from itself failed.")

    def test_multiplication_by_scalar(self):
        """Test multiplying a VariableAssignment by a scalar."""
        va = VariableAssignment("x", 1)
        result = va * 3
        expected_terms = {
            frozenset({("x", 1)}): 3.0
        }
        self.assertEqual(result.terms, expected_terms, "Multiplication by scalar failed.")

    def test_multiplication_by_zero(self):
        """Test multiplying a VariableAssignment by zero."""
        va = VariableAssignment("x", 1)
        result = va * 0
        expected_terms = {}
        self.assertEqual(result.terms, expected_terms, "Multiplication by zero failed.")

    def test_multiplication_by_negative_scalar(self):
        """Test multiplying a VariableAssignment by a negative scalar."""
        va = VariableAssignment("x", 1)
        result = va * -2
        expected_terms = {
            frozenset({("x", 1)}): -2.0
        }
        self.assertEqual(result.terms, expected_terms, "Multiplication by negative scalar failed.")

    def test_multiplication_with_non_conflicting_terms(self):
        """Test multiplying two VariableAssignment objects with non-conflicting terms."""
        va1 = VariableAssignment("x", 1)
        va2 = VariableAssignment("y", 2)
        result = va1 * va2
        expected_terms = {
            frozenset({("x", 1), ("y", 2)}): 1.0
        }
        self.assertEqual(result.terms, expected_terms, "Multiplication with non-conflicting terms failed.")

    def test_multiplication_with_conflicting_terms(self):
        """Test multiplying two VariableAssignment objects with conflicting terms."""
        va1 = VariableAssignment("x", 1)
        va2 = VariableAssignment("x", 2)
        with self.assertRaises(NotImplementedError):
            result = va1 * va2

    def test_multiplication_by_itself(self):
        """Test multiplying a VariableAssignment by itself."""
        va = VariableAssignment("x", 1)
        result = va * va
        expected_terms = {
            frozenset({("x", 1)}): 1.0
        }
        self.assertEqual(result.terms, expected_terms, "Multiplication by itself failed.")

    def test_conflicting_variable_assignments(self):
        """Test that conflicting variable assignments result in zero."""
        va1 = VariableAssignment("x", "a")
        va2 = VariableAssignment("x", "b")
        with self.assertRaises(NotImplementedError):
            result = va1 * va2


    def test_consistent_variable_assignments(self):
        """Test that consistent variable assignments are preserved."""
        va1 = VariableAssignment("x", "a")
        va2 = VariableAssignment("x", "a")
        result = va1 * va2
        expected_terms = {
            frozenset({("x", "a")}): 1.0
        }
        self.assertEqual(result.terms, expected_terms, "Consistent variable assignments should be preserved.")

    def test_get_coefficient(self):
        """Test retrieving coefficients for specific variable-value pairs."""
        va = VariableAssignment("x", 1)
        self.assertEqual(va.get_coefficient(("x", 1)), 1.0, "Coefficient retrieval failed.")
        self.assertEqual(va.get_coefficient(("y", 2)), 0.0, "Non-existent coefficient should return 0.")

    def test_get_constant(self):
        """Test retrieving the constant term."""
        va = VariableAssignment()
        self.assertEqual(va.get_constant(), 0.0, "Default constant term should be 0.")
        va = VariableAssignment() + 5
        self.assertEqual(va.get_constant(), 5.0, "Constant term retrieval failed.")

    def test_zero_coefficient_removal(self):
        """Test that zero coefficients are automatically removed."""
        va = VariableAssignment("x", 1) - VariableAssignment("x", 1)
        self.assertEqual(va.terms, {}, "Zero coefficients should be removed.")

    def test_string_representation(self):
        """Test the human-readable string representation."""
        va = VariableAssignment("x", 1) + 5
        self.assertEqual(str(va), "5 + Var(x,1)", "String representation failed.")

    def test_debug_representation(self):
        """Test the debug representation (__repr__)."""
        va = VariableAssignment("x", 1)
        expected_repr = "VariableAssignment({frozenset({('x', 1)}): 1.0})"
        self.assertEqual(repr(va), expected_repr, "Debug representation failed.")

    def test_equality_identical_objects(self):
        """Test equality between two identical VariableAssignment objects."""
        va1 = VariableAssignment("x", 1)
        va2 = VariableAssignment("x", 1)
        self.assertEqual(va1, va2, "Identical VariableAssignment objects should be equal.")

    def test_equality_with_constant(self):
        """Test equality between a VariableAssignment and a constant."""
        va = VariableAssignment() + 5
        self.assertEqual(va, 5, "VariableAssignment with constant should equal the constant.")

    def test_hash_consistency(self):
        """Test that hash values are consistent for identical VariableAssignment objects."""
        va1 = VariableAssignment("x", 1)
        va2 = VariableAssignment("x", 1)
        self.assertEqual(hash(va1), hash(va2), "Hash values for identical VariableAssignment objects should be consistent.")

    def test_boolean_conversion_empty(self):
        """Test that an empty VariableAssignment evaluates to False."""
        va = VariableAssignment()
        self.assertFalse(bool(va), "Empty VariableAssignment should evaluate to False.")

    def test_boolean_conversion_non_empty(self):
        """Test that a non-empty VariableAssignment evaluates to True."""
        va = VariableAssignment("x", 1)
        self.assertTrue(bool(va), "Non-empty VariableAssignment should evaluate to True.")

    def test_unary_negation(self):
        """Test negating a VariableAssignment."""
        va = VariableAssignment("x", 1)
        result = -va
        expected_terms = {
            frozenset({("x", 1)}): -1.0
        }
        self.assertEqual(result.terms, expected_terms, "Unary negation failed.")

    def test_unary_plus(self):
        """Test applying unary plus to a VariableAssignment."""
        va = VariableAssignment("x", 1)
        result = +va
        self.assertEqual(result.terms, va.terms, "Unary plus should return a copy of the VariableAssignment.")

    def test_copy_method(self):
        """Test the copy method to ensure it creates a deep copy."""
        va = VariableAssignment("x", 1) + 5
        va_copy = va.copy()
        self.assertEqual(va.terms, va_copy.terms, "Copy method failed to create an identical copy.")
        self.assertIsNot(va, va_copy, "Copy method should create a new instance.")

    def test_to_pyqubo(self):
        """Test the to_pyqubo method for converting to PyQUBO expressions."""
        """
        try:
            from pyqubo import Binary
        except ImportError:
            self.skipTest("PyQUBO is not installed.")

        va = VariableAssignment("x", 1)
        pyqubo_expr = va.to_pyqubo()
        expected_expr = Binary("x_1")
        self.assertEqual(str(pyqubo_expr), str(expected_expr), "to_pyqubo conversion failed.")
        """

    def test_get_binary_variables(self):
        """Test the get_binary_variables method."""
        va = VariableAssignment("x", 1) + VariableAssignment("y", 2)
        binary_vars = va.get_binary_variables()
        expected_vars = {"x_1", "y_2"}
        self.assertEqual(binary_vars, expected_vars, "get_binary_variables failed.")

    def test_validate_invariants_zero_coefficient(self):
        """Test that zero coefficients are caught by _validate_invariants."""
        va = VariableAssignment("x", 1)
        va.terms[frozenset({("x", 1)})] = 0  # Manually introduce invalid state
        with self.assertRaises(AssertionError):
            va._validate_invariants()

    def test_validate_invariants_non_hashable_variable(self):
        """Test that non-hashable variables are caught by _validate_invariants."""
        va = VariableAssignment()
        with self.assertRaises(TypeError):
            va.terms[frozenset({(["x"], 1)})] = 1  # Manually introduce invalid state
            va._validate_invariants()

    def test_large_variable_assignment(self):
        """Test operations on a large VariableAssignment object."""
        va = VariableAssignment()
        for i in range(1000):
            va += VariableAssignment(f"x{i}", i)
        self.assertEqual(len(va.terms), 1000, "Large VariableAssignment should have 1000 terms.")

    def test_extreme_coefficients(self):
        """Test operations with very large and very small coefficients."""
        va = VariableAssignment("x", 1) * 1e100
        self.assertEqual(va.get_coefficient(("x", 1)), 1e100, "Large coefficient failed.")
        va = VariableAssignment("x", 1) * 1e-100
        self.assertEqual(va.get_coefficient(("x", 1)), 1e-100, "Small coefficient failed.")

    def test_overlapping_and_conflicting_variables(self):
        """Test operations involving overlapping and conflicting variables."""
        va1 = VariableAssignment("x", 1) + VariableAssignment("y", 2)
        va2 = VariableAssignment("x", 1) + VariableAssignment("y", 3)

        # Test conflicting multiplication
        with self.assertRaises(NotImplementedError):
            _ = va1 * va2

        # Test conflicting multiplication for single variable
        va3 = VariableAssignment("x", 1)
        va4 = VariableAssignment("x", 2)
        with self.assertRaises(NotImplementedError):
            _ = va3 * va4

if __name__ == "__main__":
    unittest.main()
