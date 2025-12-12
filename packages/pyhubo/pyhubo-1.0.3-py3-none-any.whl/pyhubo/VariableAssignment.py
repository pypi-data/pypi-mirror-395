class VariableAssignment:
    """
    A class representing variable assignments for combinatorial optimization.
    
    Internal structure:
    - self.terms: dict with frozenset keys and numeric values
    - Keys: frozenset of (variable, value) tuples representing coefficients
    - Values: costs associated with those coefficients
    - Empty frozenset() represents constant terms
    """
    
    def __init__(self, variable=None, value=None):
        """
        Initialize a VariableAssignment object.
        
        Args:
            variable: The variable name (can be any hashable type)
            value: The value to assign to the variable (can be any hashable type)
            
        If both variable and value are None, creates an empty VariableAssignment (coefficient 0).
        If variable and value are provided, creates a single variable assignment with coefficient 1.
        """
        self.terms = {}
        
        if variable is not None and value is not None:
            # Validate that variable and value are hashable
            try:
                hash(variable)
                hash(value)
            except TypeError:
                raise ValueError(f"Variable and value must be hashable types, got {type(variable)} and {type(value)}")
            
            # Create a single variable assignment with coefficient 1.0
            coefficient_key = frozenset([(variable, value)])
            self.terms[coefficient_key] = 1.0
        elif variable is None and value is None:
            # Create empty VariableAssignment (represents 0)
            pass
        else:
            raise ValueError("Both variable and value must be provided, or both must be None")
        
        # Validate internal state
        self._validate_invariants()
        
    def __add__(self, other):
        """
        Add two VariableAssignment objects or a VariableAssignment and a number.
        
        Rules:
        - VariableAssignment + Number: Add number as constant term (frozenset(): number)
        - VariableAssignment + VariableAssignment: Merge terms, adding coefficients for same keys
        
        Args:
            other: Another VariableAssignment object or a number
            
        Returns:
            New VariableAssignment object with combined terms
        """
        result = VariableAssignment()  # Start with empty VariableAssignment
        
        # Copy all terms from self
        for key, value in self.terms.items():
            result.terms[key] = value
        
        if isinstance(other, (int, float)):
            # Adding a number: add to constant term
            constant_key = frozenset()
            if constant_key in result.terms:
                result.terms[constant_key] += other
            else:
                result.terms[constant_key] = other
                
            # Remove zero constant terms to keep clean
            if result.terms.get(constant_key, 0) == 0:
                result.terms.pop(constant_key, None)
                
        elif isinstance(other, VariableAssignment):
            # Adding another VariableAssignment: merge terms
            for key, value in other.terms.items():
                if key in result.terms:
                    result.terms[key] += value
                else:
                    result.terms[key] = value
                    
                # Remove zero terms to keep clean
                if result.terms[key] == 0:
                    del result.terms[key]
        else:
            return NotImplemented
            
        # Validate result
        result._validate_invariants()
        return result
    
    def __mul__(self, other):
        """
        Multiply VariableAssignment by a number or another VariableAssignment.
        
        Rules:
        - VariableAssignment * Number: Multiply all coefficients by the number
        - VariableAssignment * VariableAssignment: Distributive multiplication
        - If any variable appears with different values, the product is 0
        - Otherwise, combine the frozensets and multiply coefficients
        
        Args:
            other: A number or another VariableAssignment object
            
        Returns:
            New VariableAssignment object with multiplied terms
        """
        result = VariableAssignment()  # Start with empty
    
        if isinstance(other, (int, float)):
            # Multiply by scalar: multiply all coefficients
            if other == 0:
                return result  # Return empty (zero)
            
            for key, value in self.terms.items():
                new_coefficient = value * other
                if new_coefficient != 0:  # Only keep non-zero terms
                    result.terms[key] = new_coefficient
                    
        elif isinstance(other, VariableAssignment):
            # Multiply two VariableAssignments: distributive law
            for key1, value1 in self.terms.items():
                for key2, value2 in other.terms.items():
                    
                    # Check for conflicts: same variable with different values
                    if self._has_variable_conflict(key1, key2):
                        raise NotImplementedError(f"Multiplication invalid, a variables can't have the same value at once. You tried to assign {key1} both value {value1} and {value2}")
                    
                    # Combine the frozensets (union of variable assignments)
                    combined_key = key1 | key2  # Union of frozensets
                    combined_coefficient = value1 * value2
                    
                    if combined_coefficient != 0:
                        if combined_key in result.terms:
                            result.terms[combined_key] += combined_coefficient
                        else:
                            result.terms[combined_key] = combined_coefficient
                            
                        # Remove if it becomes zero
                        if result.terms[combined_key] == 0:
                            del result.terms[combined_key]
        else:
            return NotImplemented
        
        # Validate result
        result._validate_invariants()
        return result

    def __rmul__(self, other):
        """Right multiplication (for number * VariableAssignment)"""
        return self.__mul__(other)

    def _has_variable_conflict(self, key1, key2):
        """
        Check if two coefficient keys have conflicting variable assignments.
        
        Args:
            key1, key2: frozensets of (variable, value) tuples
            
        Returns:
            True if any variable appears with different values in key1 and key2
        """
        # Extract variables from each key
        vars1 = {var for var, val in key1}
        vars2 = {var for var, val in key2}
        
        # Check for conflicts in common variables
        common_vars = vars1 & vars2
        for var in common_vars:
            # Get values for this variable in both keys
            val1 = next(val for v, val in key1 if v == var)
            val2 = next(val for v, val in key2 if v == var)
            
            if val1 != val2:
                return True  # Conflict found
                
        return False  # No conflicts

    def __radd__(self, other):
        """
        Right addition (for number + VariableAssignment).
        
        Args:
            other: A number to be added to this VariableAssignment
            
        Returns:
            New VariableAssignment object with the number added as constant term
        """
        if isinstance(other, (int, float)):
            return self.__add__(other)
        return NotImplemented

    def __sub__(self, other):
        """
        Subtract another VariableAssignment or number from this one.
        
        Args:
            other: VariableAssignment object or number to subtract
            
        Returns:
            New VariableAssignment object representing the difference
        """
        if isinstance(other, (int, float)):
            return self.__add__(-other)
        elif isinstance(other, VariableAssignment):
            return self.__add__(other * (-1))
        return NotImplemented

    def __rsub__(self, other):
        """
        Right subtraction (for number - VariableAssignment).
        
        Args:
            other: A number from which this VariableAssignment is subtracted
            
        Returns:
            New VariableAssignment object representing other - self
        """
        if isinstance(other, (int, float)):
            return (self * (-1)).__add__(other)
        return NotImplemented

    def __str__(self):
        """
        String representation for user-friendly display.
        
        Returns:
            Human-readable string representation of the VariableAssignment
        """
        if not self.terms:
            return "0"
        
        parts = []
        
        # Sort terms for consistent display (constants first, then by string representation)
        sorted_terms = sorted(self.terms.items(), 
                            key=lambda x: (len(x[0]), str(sorted(x[0]))))
        
        for i, (key, value) in enumerate(sorted_terms):
            if len(key) == 0:  # Constant term
                if i == 0:
                    parts.append(str(value))
                else:
                    parts.append(f" + {value}" if value >= 0 else f" - {abs(value)}")
            else:  # Variable assignment term
                # Format coefficient
                if value == 1:
                    coeff_str = ""
                elif value == -1:
                    coeff_str = "-"
                else:
                    coeff_str = str(value) + "*"
                
                # Format variable assignments
                var_assignments = sorted(key)  # Sort for consistency
                var_str = "*".join([f"Var({var},{val})" for var, val in var_assignments])
                
                term_str = coeff_str + var_str
                
                if i == 0:
                    parts.append(term_str)
                else:
                    if value >= 0:
                        parts.append(f" + {term_str}")
                    else:
                        # Handle negative coefficient
                        if coeff_str == "-":
                            parts.append(f" - {var_str}")
                        else:
                            parts.append(f" - {abs(value)}*{var_str}")
        
        return "".join(parts)

    def __repr__(self):
        """
        Official string representation for debugging.
        
        Returns:
            Detailed string representation showing internal structure
        """
        return f"VariableAssignment({dict(self.terms)})"
    
    def __eq__(self, other):
        """
        Check equality between VariableAssignment objects.
        
        Args:
            other: Another VariableAssignment object or number
            
        Returns:
            True if both represent the same mathematical expression
        """
        if isinstance(other, VariableAssignment):
            return self.terms == other.terms
        elif isinstance(other, (int, float)):
            # Equal to a number only if this is a constant with that value
            if len(self.terms) == 0:
                return other == 0
            elif len(self.terms) == 1 and frozenset() in self.terms:
                return self.terms[frozenset()] == other
            else:
                return False
        return False
    
    def __hash__(self):
        """
        Make VariableAssignment hashable so it can be used in sets and as dict keys.
        
        Returns:
            Hash value based on the terms
        """
        return hash(frozenset(self.terms.items()))
    
    def __bool__(self):
        """
        Boolean conversion: True if non-zero, False if zero.
        
        Returns:
            False if this represents zero (empty terms), True otherwise
        """
        return bool(self.terms)
    
    def __neg__(self):
        """
        Unary negation (-VariableAssignment).
        
        Returns:
            New VariableAssignment with all coefficients negated
        """
        return self * (-1)
    
    def __pos__(self):
        """
        Unary plus (+VariableAssignment).
        
        Returns:
            Copy of this VariableAssignment (no change)
        """
        result = VariableAssignment()
        result.terms = self.terms.copy()
        return result
    
    def items(self):
        """
        Return items from internal terms dictionary.
        
        Returns:
            Dictionary items view of (coefficient_key, value) pairs
        """
        return self.terms.items()
    
    def keys(self):
        """
        Return coefficient keys from internal terms dictionary.
        
        Returns:
            Dictionary keys view of coefficient keys (frozensets)
        """
        return self.terms.keys()
    
    def values(self):
        """
        Return coefficient values from internal terms dictionary.
        
        Returns:
            Dictionary values view of coefficient values
        """
        return self.terms.values()
    
    def get_coefficient(self, *variable_value_pairs):
        """
        Get the coefficient for a specific variable assignment combination.
        
        Args:
            *variable_value_pairs: Variable-value pairs, e.g., ("a", "b"), ("c", "d")
            
        Returns:
            The coefficient for this combination, or 0 if not present
            
        Example:
            obj.get_coefficient(("a", "b"))  # Linear term
            obj.get_coefficient(("a", "b"), ("c", "d"))  # Quadratic term
            obj.get_coefficient()  # Constant term
        """
        key = frozenset(variable_value_pairs)
        return self.terms.get(key, 0)
    
    def get_constant(self):
        """
        Get the constant term (coefficient without any variables).
        
        Returns:
            The constant term value, or 0 if no constant term exists
        """
        return self.terms.get(frozenset(), 0)
    
    def copy(self):
        """
        Create a deep copy of this VariableAssignment.
        
        Returns:
            New VariableAssignment object with same terms
        """
        result = VariableAssignment()
        result.terms = self.terms.copy()
        result._validate_invariants()
        return result
    
    def to_pyqubo(self):
        """
        Convert VariableAssignment to PyQUBO format.
        
        Each (variable, value) coefficient becomes a Binary(f"{variable}_{value}") term.
        
        Returns:
            PyQUBO expression representing this VariableAssignment
            
        Example:
            VariableAssignment("x", 1) → Binary("x_1")
            3 * VariableAssignment("x", 1) → 3 * Binary("x_1")
            VariableAssignment("x", 1) * VariableAssignment("y", 2) → Binary("x_1") * Binary("y_2")
        """
        try:
            from pyqubo import Binary
        except ImportError:
            raise ImportError("PyQUBO is required for this functionality. Install with: pip install pyqubo")
        
        result = 0  # Start with zero
        
        for key, coefficient in self.terms.items():
            if len(key) == 0:
                # Constant term
                result += coefficient
            else:
                # Variable assignment term(s)
                term = coefficient
                for var, val in key:
                    binary_var_name = f"{var}_{val}"
                    term *= Binary(binary_var_name)
                result += term
                
        return result
    
    def get_binary_variables(self):
        """
        Get all binary variable names that would be used in PyQUBO conversion.
        
        Returns:
            Set of binary variable names (strings) in format "variable_value"
        """
        binary_vars = set()
        
        for key in self.terms.keys():
            for var, val in key:
                binary_var_name = f"{var}_{val}"
                binary_vars.add(binary_var_name)
                
        return binary_vars
    
    def evaluate_solution(self, solution:dict):
        """
        Evaluate the cost of this VariableAssignment for a given solution.
        
        Args:
            solution: Dictionary mapping variables to their assigned values
                     Format: {"variable1": "value1", "variable2": "value2", ...}
        
        Returns:
            float: The total cost for the given solution
            
        Raises:
            ValueError: If a variable has multiple different values assigned in the solution
        """
        
        # Check for duplicate variable assignments in solution
        seen_variables = set()
        for variable in solution.keys():
            if variable in seen_variables:
                raise ValueError(f"Variable '{variable}' appears multiple times in solution")
            seen_variables.add(variable)
        
        total_cost = 0.0
        
        # Iterate through all terms in this VariableAssignment
        for key, coefficient in self.terms.items():
            # Check if all variable assignments in this term match the solution
            term_matches = True
            
            for variable, required_value in key:
                if variable not in solution:
                    # Variable not assigned in solution, term doesn't contribute
                    term_matches = False
                    break
                elif solution[variable] != required_value:
                    # Variable assigned to different value, term doesn't contribute
                    term_matches = False
                    break
            
            # If all variables in this term match the solution, add the coefficient to cost
            if term_matches:
                total_cost += coefficient
        
        return total_cost

    def _validate_invariants(self):
        """
        Validate that the object maintains its mathematical invariants.
        
        Raises:
            AssertionError: If any invariant is violated
        """
        assert isinstance(self.terms, dict), "terms must be a dictionary"
        
        for key, value in self.terms.items():
            # Each key must be a frozenset
            assert isinstance(key, frozenset), f"Key must be frozenset, got {type(key)}"
            
            # Each frozenset element must be a tuple of length 2 (variable, value)
            for item in key:
                assert isinstance(item, tuple), f"Key elements must be tuples, got {type(item)}"
                assert len(item) == 2, f"Key elements must be (variable, value) pairs, got {item}"
                var, val = item
                # Variables and values must be hashable
                try:
                    hash(var)
                    hash(val)
                except TypeError:
                    assert False, f"Variables and values must be hashable, got {type(var)} and {type(val)}"
            
            # Coefficients must be numeric and non-zero
            assert isinstance(value, (int, float)), f"Coefficient must be numeric, got {type(value)}"
            assert value != 0, f"Zero coefficients should be removed, found {value} for key {key}"
            assert not (isinstance(value, float) and (value != value)), "Coefficient cannot be NaN"  # NaN check
            assert not (isinstance(value, float) and abs(value) == float('inf')), "Coefficient cannot be infinite"