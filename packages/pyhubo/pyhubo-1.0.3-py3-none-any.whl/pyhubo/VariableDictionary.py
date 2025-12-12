from typing import Dict, List, Hashable, Tuple
import math
import pyqubo
from .VariableAssignment import VariableAssignment

class VariableDictionary:
    def __init__(self, domains: Dict[Hashable, List[Hashable]]):
        """
        Initialize VariableDictionary with domain definitions.
        
        Args:
            domains: Dictionary mapping variables to their possible values
        
        Raises:
            ValueError: If any domain is empty or contains duplicates
        """
        # Validation
        for var, values in domains.items():
            if not values:
                raise ValueError(f"Domain for variable '{var}' cannot be empty")
            if len(values) != len(set(values)):
                raise ValueError(f"Domain for variable '{var}' contains duplicate values")
        
        # Store immutable domains
        self._domains = {var: tuple(values) for var, values in domains.items()}

        self.nbr_bits = {var: self._compute_required_bits(self.get_domain_size(var)) for var in self.variables()}

        # ToDo: Check if 2**nbr_bits for each variable is equal to domain size, if not, give out warning and create auxiliary values in the domains
        self._aux_vals = {}
        domain_modified = False
        for var in self._domains.keys():
            nbr_empty_indicies = self._nbr_empty_indicies(var)
            if nbr_empty_indicies:
                domain_modified = True
                original_domain = self.get_domain(var)
                additional_domain = tuple([f"aux_{i}" for i in range(nbr_empty_indicies)])
                self._domains[var] = original_domain + additional_domain
                self._aux_vals[var] = tuple([f"aux_{i}" for i in range(nbr_empty_indicies)])
        if domain_modified:
            print("There are unused indicies in your Variable Dictionary, auxiliary values added to Variable Dictionary. " \
            "Consider adding a penalty term from .get_penalty_term() to penalize the unused indicies")
        
        # Build bidirectional mappings per variable
        self._value_to_index = {}  # {var: {val: idx}}
        self._index_to_value = {}  # {var: {idx: val}}
        
        for var, values in self._domains.items():
            self._value_to_index[var] = {val: idx for idx, val in enumerate(values)}
            self._index_to_value[var] = {idx: val for idx, val in enumerate(values)}

    def _compute_required_bits(self, domain_size: int) -> int:
        """
        Compute number of bits required to encode a domain of given size.
        
        Args:
            domain_size: Number of possible values in the domain
            
        Returns:
            Number of bits needed (ceil(log2(domain_size)))
            
        Edge Cases:
            - domain_size = 1: returns 0 (no bits needed)
            - domain_size = 2: returns 1
            - domain_size = 3,4: returns 2
            etc.
        """
        if domain_size <= 1:
            return 0
        return math.ceil(math.log2(domain_size))

    def get_penalty_term(self):
        """
        Create a Variable Assignment Object to get the penalties indicies that don't have a value. 
        
        E.g. consider a Variable Assignment Object VarAss("var1", "val1") + 2 VarAss("var1", "val2") + 3 VarAss("var1", "val3").
        Since "var1" has 3 possible assignments, 2 bits are required. 
        However, this leaves 1 index without an assigned value. In the above example the binary index that has not_defined
        would be the best assignment, since one could rewrite it as VarAss("var1", "val1") + 2 VarAss("var1", "val2") + 3 VarAss("var1", "val3") + 0 * VarAss("var1", "not_defined").
        This function give a penalty term for such cases.
        """
        penalty = []
        for var, aux_vals in self._aux_vals.items():
            penalty += [VariableAssignment(var, aux_val) for aux_val in aux_vals]
        return sum(penalty)

    def _nbr_empty_indicies(self, variable:Hashable):
        return 2**self.nbr_bits[variable] - self.get_domain_size(variable)
    
    def _compute_binary_string(self, index: int, nbr_bits:int):
        b = bin(index)[2:]           # Strip '0b', e.g. '110'
        b = b[::-1]              # Reverse string: '011'
        return b.ljust(nbr_bits, '0')[:nbr_bits]   # Pad right with '0', trim to width
    
    def _compute_decimal_sol(self, binary_string:str):
        bstr = binary_string[::-1]              # Reverse so MSB is leftmost (standard order)
        return int(bstr, 2)            # Convert standard binary string to decimal
        
    def solution_dict_to_string_format(self, solution_dict:dict):
        solution_strings = {}
        for var, val in solution_dict.items():
            index = self.get_index(var, val)
            binary_string = self._compute_binary_string(index, self.nbr_bits[var])
            solution_strings[var] = binary_string
        return solution_strings
    
    def string_format_to_solution_dict(self, solution_strings:dict):
        solution_dict = {}
        for var, solution_string in solution_strings.items():
            decimal_index = self._compute_decimal_sol(solution_string)
            value = self.get_value(var, decimal_index)
            solution_dict[var] = value
        return solution_dict

    def get_total_qubits(self) -> int:
        """Get number of qubits required for COP"""
        return sum(self.nbr_bits.values())

    def get_index(self, variable: Hashable, value: Hashable) -> int:
        """Get index for a variable-value pair."""
        if variable not in self._domains:
            raise KeyError(f"Variable '{variable}' not found in dictionary")
        if value not in self._value_to_index[variable]:
            raise ValueError(f"Value '{value}' not in domain of variable '{variable}'")
        return self._value_to_index[variable][value]
    
    def get_value(self, variable: Hashable, index: int) -> Hashable:
        """Get value for a variable-index pair."""
        if variable not in self._domains:
            raise KeyError(f"Variable '{variable}' not found in dictionary")
        if index not in self._index_to_value[variable]:
            raise IndexError(f"Index {index} out of range for variable '{variable}' (domain size: {len(self._domains[variable])})")
        return self._index_to_value[variable][index]
    
    def get_domain(self, variable: Hashable) -> Tuple[Hashable, ...]:
        """Get domain (all possible values) for a variable."""
        if variable not in self._domains:
            raise KeyError(f"Variable '{variable}' not found in dictionary")
        return self._domains[variable]
    
    def get_domain_size(self, variable: Hashable) -> int:
        """Get size of domain for a variable."""
        if variable not in self._domains:
            raise KeyError(f"Variable '{variable}' not found in dictionary")
        return len(self._domains[variable])
    
    def variables(self) -> Tuple[Hashable, ...]:
        """Get all variables in the dictionary."""
        return tuple(self._domains.keys())
    
    def one_hot_penalty(self, penalty_coefficient: float = 1.0):
        """
        Generate PyQUBO one-hot constraint: sum_{i}(1 - sum_{j} x_{i,j})^2
        
        Args:
            penalty_coefficient: Coefficient for the penalty terms
            
        Returns:
            PyQUBO expression for one-hot constraints
        """
        total_penalty = 0
        
        for variable, domain in self._domains.items():
            # Create binary variables for this variable's domain
            domain_sum = 0
            for value in domain:
                binary_var = pyqubo.Binary(f"{variable}_{value}")
                domain_sum += binary_var
            
            # Add (1 - sum)^2 penalty for this variable
            constraint = (1 - domain_sum) ** 2
            total_penalty += penalty_coefficient * constraint
        
        return total_penalty
    
    def __len__(self) -> int:
        """Return number of variables."""
        return len(self._domains)
    
    def __contains__(self, variable: Hashable) -> bool:
        """Check if variable exists in dictionary."""
        return variable in self._domains
    
    def __repr__(self) -> str:
        """String representation of the dictionary."""
        items = [f"{var}: {list(domain)}" for var, domain in self._domains.items()]
        return f"VariableDictionary({{{', '.join(items)}}})"
    
    def __eq__(self, other) -> bool:
        """Check equality with another VariableDictionary."""
        if not isinstance(other, VariableDictionary):
            return False
        return self._domains == other._domains