from typing import Dict, List, Any
import numpy as np
from functools import reduce
from scipy.linalg import hadamard as hadamard_matrix
from .VariableDictionary import VariableDictionary
from .VariableAssignment import VariableAssignment

class PauliZ:
    """
    Represents a Pauli Z operator as a product of individual Z operators.
    Behaves like a frozenset for HUBO Hamiltonian usage.
    """
    
    def __init__(self, terms=None):
        """
        Initialize a PauliZ operator.
        
        Args:
            terms: Iterable of (variable, bit) tuples. If None, creates identity.
        """
        if terms is None:
            self._terms = frozenset()
        else:
            self._terms = frozenset(terms)

    def __mul__(self, other):
        """
        Multiply two PauliZ operators using Z² = Identity rule.
        
        Args:
            other: Another PauliZ operator
            
        Returns:
            PauliZ: New operator with symmetric difference of terms
        """
        if not isinstance(other, PauliZ):
            return NotImplemented
        
        result_terms = self._terms.symmetric_difference(other._terms)
        return PauliZ(result_terms)
    
    def __hash__(self):
        """
        Hash based on the frozenset of terms for dictionary key usage.
        """
        return hash(self._terms)
    
    def __eq__(self, other):
        """
        Equality based on having the same set of terms.
        """
        if not isinstance(other, PauliZ):
            return False
        return self._terms == other._terms
    
    def __iter__(self):
        """
        Iterate over the terms like a frozenset.
        """
        return iter(self._terms)
    
    def __len__(self):
        """
        Return the number of Z operators in this product.
        """
        return len(self._terms)
    
    def __contains__(self, item):
        """
        Check if a (variable, bit) pair is in this PauliZ operator.
        """
        return item in self._terms
    
    def __repr__(self):
        """
        String representation for debugging.
        """
        if not self._terms:
            return "PauliZ()"
        terms_list = sorted(self._terms)
        return f"PauliZ({terms_list})"
    
    def __str__(self):
        """
        Human-readable string representation.
        """
        if not self._terms:
            return "I"
        terms_list = sorted(self._terms)
        return " * ".join(f"Z_{{{var},{bit}}}" for var, bit in terms_list)

class HuboHamiltonian:
    def __init__(self, variable_assignment: VariableAssignment, variable_dictionary: VariableDictionary):
        """
        Initialize HuboHamiltonian with validation and qubit structure creation.
        
        Args:
            variable_assignment: VariableAssignment object with optimization terms
            variable_dictionary: VariableDictionary defining variable domains
            
        Raises:
            ValueError: If variable_assignment contains variables/values not in variable_dictionary
        """
        # Store inputs
        self._variable_assignment = variable_assignment
        self._variable_dictionary = variable_dictionary
        
        # Validate compatibility
        self._validate_inputs()
        
        # Build qubit structure immediately
        self._single_variable_coefficients = self._build_single_variable_coefficients()
        
        # Hamiltonian coefficients (built lazily)
        self._hamiltonian_coeffs = None
        self._hamiltonian_built = False
        
    def _validate_inputs(self):
        """Validate that all variable-value pairs in assignment exist in dictionary."""
        for coefficient_key in self._variable_assignment.keys():
            for variable, value in coefficient_key:
                # Check if variable exists
                if variable not in self._variable_dictionary:
                    raise ValueError(f"Variable '{variable}' in VariableAssignment not found in VariableDictionary")
                
                # Check if value exists in domain
                try:
                    self._variable_dictionary.get_index(variable, value)
                except ValueError as e:
                    raise ValueError(f"Variable-value pair ({variable}, {value}) not in VariableDictionary domain: {e}")
                
    def _build_qubit_structure(self) -> Dict[Any, List[PauliZ]]:
        """
        Build qubit structure for all variables in the dictionary.
        
        Returns:
            Dictionary mapping variables to lists of PauliZ operators
            Format: {variable: [PauliZ({(variable, 0)}), PauliZ({(variable, 1)}), ...]}
        """
        qubit_structure = {}
        
        for variable in self._variable_dictionary.variables():
            domain_size = self._variable_dictionary.get_domain_size(variable)
            required_bits = self._variable_dictionary._compute_required_bits(domain_size)
            
            # Create list of PauliZ operators for this variable's bits
            pauli_list = []
            for bit_index in range(required_bits):
                pauli_z = PauliZ({(variable, bit_index)})
                pauli_list.append(pauli_z)
            
            qubit_structure[variable] = pauli_list
        
        return qubit_structure
    
    def kronecker_product_set(self, *args):
        return reduce(np.kron, reversed(args))
    
    def _build_single_variable_coefficients(self) -> Dict[Any, List[PauliZ]]:

        # All possible PauliZ coefficients that a single variable
        single_variable_coefficients = {}
        pauli_z_structure = lambda var, bit: np.array([PauliZ({}), PauliZ({(var, bit)})])
        for variable in self._variable_dictionary.variables():
            required_bits = self._variable_dictionary.nbr_bits[variable]
            array_coefficients = [pauli_z_structure(variable, i) for i in range(required_bits)]
            single_variable_coefficients[variable] = self.kronecker_product_set(*array_coefficients)
        return single_variable_coefficients

    def cost_solution(self, solution:dict):
        solutionStrings = self._variable_dictionary.solution_dict_to_string_format(solution)
        return self.subH(solutionStrings)

    def subH(self, solution:dict):
        """
        solution is a dict where the keys are the variables and the values are binary strings, when converted to decimal correspond to an index which is linked to a value
        """
        for var, state_string in solution.items():
            assert len(state_string) == self._variable_dictionary.nbr_bits[var], "The proposed solution must have matching number of bits"
        hamiltonian = self.get_hamiltonian()
        energy = 0
        for coefficients, value in hamiltonian.items():
            product = 1
            for coefficient in coefficients:
                variable = coefficient[0]
                bit = coefficient[1]
                product *= (-1)**(int(solution[variable][bit]))
            energy += product * value
        return energy
    
    def build_hubo_coeff(self):
        """
        Build HUBO Hamiltonian coefficients from VariableAssignment.
        
        This method converts each term in the VariableAssignment to corresponding
        PauliZ operators using binary encoding of variable values.
        
        The conversion process:
        1. For each VariableAssignment term {(var1, val1), (var2, val2), ...}: coeff
        2. Convert each (var, val) to binary representation using VariableDictionary indices
        3. Create PauliZ operators for the binary bits that are set to 1
        4. Store the resulting PauliZ operator as key with coefficient as value
        
        Populates self._hamiltonian_coeffs: Dict[PauliZ, float]
        """
        if self._hamiltonian_built:
            return  # Already built
        
        self._hamiltonian_coeffs = {}

        for coefficient_key, coeff_value in self._variable_assignment.items():
            if len(coefficient_key) == 0:
                # Constant Term only contributes through Identity
                hubo_coefficients = [PauliZ()]
                hubo_vals = [coeff_value]
            else:
                # Create lists of variable and value indicies involved in this coefficient of the objective function
                var_names = [var_val_pair[0] for var_val_pair in coefficient_key]
                val_indicies = [self._variable_dictionary._value_to_index[var_val_pair[0]][var_val_pair[1]] for var_val_pair in coefficient_key]

                # Total number of bits to describe this coefficient is given by the sum of all bits over all variable domains
                total_nbr_bits = sum([self._variable_dictionary.nbr_bits[var] for var in var_names])

                # hubo_vals are the numerical values for the HUBO coefficients. It has 2**total_number_of_bits elements. The i-th value of hubo_vals is the coefficient corresponding to the i-th element in hubo_coefficients
                hadamards = [hadamard_matrix(2**self._variable_dictionary.nbr_bits[var])[val] for var, val in zip(var_names, val_indicies)]
                hubo_vals = coeff_value * 1/(2**total_nbr_bits) * self.kronecker_product_set(*hadamards)

                hubo_coefficient_list = [self._single_variable_coefficients[var] for var in var_names]
                hubo_coefficients = self.kronecker_product_set(*hubo_coefficient_list)

            # Each Coefficient in general gives rise to several HUBO terms, add them to the dictionary
            for hubo_coefficent, hubo_val in zip(hubo_coefficients, hubo_vals):
                if hubo_coefficent in self._hamiltonian_coeffs:
                    self._hamiltonian_coeffs[hubo_coefficent] += float(hubo_val)
                else:
                    self._hamiltonian_coeffs[hubo_coefficent] = float(hubo_val)
        self.simplify_hamiltonian()
        self._hamiltonian_built = True
    
    def get_hamiltonian(self) -> Dict[PauliZ, float]:
        """
        Get the HUBO Hamiltonian coefficients.
        
        Triggers lazy construction if not already built.
        
        Returns:
            Dictionary mapping PauliZ operators to coefficients
        """
        if not self._hamiltonian_built:
            self.build_hubo_coeff()
        
        return self._hamiltonian_coeffs.copy()  # Return copy to prevent external modification
    
    def simplify_hamiltonian(self):
        simplified_hubo_hamiltonian = {coeff: val for coeff, val in self._hamiltonian_coeffs.items() if abs(val)>0}
        self._hamiltonian_coeffs = simplified_hubo_hamiltonian

    
    def export_dict(self, map_coeff_to_str=None, non_standard_definition_pauli_z = False, numerical_tolerance = 10**(-14)) -> Dict[frozenset, float]:
        """
        Export Hamiltonian coefficients with frozenset keys for pickle serialization.
        
        Converts PauliZ objects to their internal frozenset representation
        for saving to pickle files.

        non_standard_definition_pauli_z is a boolean that denotes which definition of PauliZ matricies are used. For example, neal and openjij have the pauli-z operator defined as Z |0> = -1* |0> and Z |1> = |1>, while pennylane uses Z |0> = |0> and Z |1> = -1* |1>

        map_coeff_to_str is a callable function with one argument here called coeffs that maps the tuple elements to a string which denotes qubits, for example in pennylane. For example, I use the notation tuple([coeff[0] + "_" + str(coeff[1]) for coeff in coeffs]), i.e. the variable name is the first part of the string, followed by an underscore, followed by the bit that this qubit denotes

        numerical_tolerance is a float that describes the threshold for which coefficients are discarded. Due to finite numerical accuracy, some coefficients that are supposed to be zero are instead calculated to be slightly above zero, these are discarded here
        
        Returns:
            Dictionary mapping frozensets to coefficients
            Format: {frozenset([(var1, bit1), (var2, bit2)]): coeff, ...}
        """
        if not self._hamiltonian_built:
            self.build_hubo_coeff()
        
        if map_coeff_to_str is None:
            map_coeff_to_str = lambda coeff: coeff
        
        export_dict = {}
        for pauli_z, coefficient in self._hamiltonian_coeffs.items():
            # Convert PauliZ to the specified key format
            if abs(coefficient)<=numerical_tolerance:
                continue
            frozenset_key = map_coeff_to_str(pauli_z._terms)
            prefactor = 1
            if non_standard_definition_pauli_z:
                prefactor = (-1)**(len(frozenset_key))
            export_dict[frozenset_key] = prefactor * coefficient
        
        return export_dict

    def get_variable_assignment(self) -> VariableAssignment:
        """
        Get the original VariableAssignment object.
        
        Returns:
            The VariableAssignment object used to construct this Hamiltonian
        """
        return self._variable_assignment

    def get_variable_dictionary(self) -> VariableDictionary:
        """
        Get the original VariableDictionary object.
        
        Returns:
            The VariableDictionary object used to construct this Hamiltonian
        """
        return self._variable_dictionary

    def is_hamiltonian_built(self) -> bool:
        """
        Check if the Hamiltonian coefficients have been computed.
        
        Returns:
            True if build_hubo_coeff() has been called, False otherwise
        """
        return self._hamiltonian_built
    
    def __repr__(self) -> str:
        """
        Developer-friendly string representation.
        """
        status = "built" if self._hamiltonian_built else "not built"
        num_vars = len(self._variable_dictionary)
        total_bits = self._variable_dictionary.get_total_qubits()
        
        return (f"HuboHamiltonian(variables={num_vars}, "
                f"total_qubits={total_bits}, "
                f"hamiltonian_status='{status}')")

    def __str__(self) -> str:
        """
        User-friendly string representation.
        """
        if not self._hamiltonian_built:
            return "HuboHamiltonian (coefficients not yet computed)"
        
        num_terms = len(self._hamiltonian_coeffs)
        return f"HuboHamiltonian with {num_terms} coefficient terms"