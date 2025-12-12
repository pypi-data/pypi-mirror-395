"""
***utils/u_struct.py***
Object type utilities module, contains the necessary classes for directory module.

Features:
- NumericCondition: A simple structure for creating ranges of numbers as objects
                    for comparison purposes.
- EMPTY & EMPTY_TYPE: Explicit reference to an empty data structure, mainly used
                      for visual identification.
- NOT_FOUND & NOT_FOUND_TYPE: Used as a default return instead of None in visualized
                              results, represents an unexpected argument result.
- Numeric & NumericTrue: Static types for integer, float, and digital string values.
"""
from __future__ import annotations
import re
from typing import Iterable, List, Literal, Tuple, Union



__all__ = ["EMPTY",
           "NOT_FOUND",
           "NumericCondition",
           "Numeric",
           "NumericTrue"]

Numeric = Union[int, float, str]
NumericTrue = Union[int, float]

class EMPTY_TYPE:
    """
    Object type representing an empty data structure.
    """
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return "EMPTY"

    def __bool__(self):
        return False

    def __len__(self):
        return 0

    def __eq__(self, other)->bool:
        if isinstance(other, EMPTY_TYPE):
            return True
        elif isinstance(other, Iterable):
            return not bool(other)
        raise NotImplementedError

class NOT_FOUND_TYPE:
    """
    Representation of an absent result, or a default return when failing to search for an object.
    """
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return "NOT FOUND"

    def __bool__(self):
        return False

    def __eq__(self, other)->bool:
        if isinstance(other, NOT_FOUND_TYPE):
            return True
        elif isinstance(other, Iterable):
            return not bool(other)
        raise NotImplementedError

#####################
NOT_FOUND = NOT_FOUND_TYPE()
EMPTY = EMPTY_TYPE()
#####################

class NumericCondition:
    """
    Creates a numeric comparison condition checked using **in** keyword.

    Example:
        >>> #Condition: value must be greater than 0 AND less than or equal to 10
        >>> condition = NumericCondition('>0', '<=10')
        >>> 5 in condition
        True
        >>> 10 in condition
        True
        >>> 0 in condition
        False
    
    Args:
        first_condition: The first numeric value or string condition.
        second_condition: The second value or condition.

    Raises:
        ValueError: If a string condition cannot be parsed.
        TypeError: If a condition value is not a supported type.
    """
    CONDITIONS = Literal["equal", "inferior", "inferior or equal", "greater", "greater or equal", "not equal"]

    #Mapping from string operators to internal condition names
    _OPERATOR_MAP = {
        '>': "greater",
        '>=': "greater or equal",
        '<': "inferior",
        '<=': "inferior or equal",
        '!=': "not equal"
    }

    def __init__(self, first_condition: Numeric, second_condition: Numeric = None):
        """
        Creates a condition object, arguments can be an int, float or a parsable digital string
        for more specific condtions, allowed condition keys are:
            '>'
            '>='
            '<'
            '<='
            '!='
            (Note: must always be written first)
        
        Use **in** to compare between a number and the created condition.
        """
        self.__checks: List[Tuple[NumericCondition.CONDITIONS, float]] = []
        self.__or_cond : bool = False

        num1, cond1 = self.__decode_condition(first_condition)

        if second_condition is not None:
            num2, cond2 = self.__decode_condition(second_condition)
            
            #Default case for two numbers: treat as an inclusive range
            if cond1 == "equal" and cond2 == "equal":
                min_val = min(num1, num2)
                max_val = max(num1, num2)
                self.__checks.append(("greater or equal", min_val))
                self.__checks.append(("inferior or equal", max_val))
            else:
                self.__checks.append((cond1, num1))
                self.__checks.append((cond2, num2))
                #Detect impossible conditions
                #and switch to an OR condition
                if (num1 > num2 and "greater" in cond1 and ("inferior" in cond2 or "equal" in cond2)) or \
                   (num1 > num2 and "inferior" in cond2 and ("greater" in cond1 or "equal" in cond1)) or \
                   (num1 < num2 and "greater" in cond2 and ("inferior" in cond1 or "equal" in cond1)) or \
                   (num1 < num2 and "inferior" in cond1 and ("greater" in cond2 or "equal" in cond2)):
                   
                    self.__or_cond = True
        else:
            #A single condition
            self.__checks.append((cond1, num1))

    def __decode_condition(self, value: Numeric) -> Tuple[float, CONDITIONS]:
        """
        Parses a numeric or string value into a condition tuple.
        """
        if isinstance(value, (int, float)):
            return float(value), "equal"

        if isinstance(value, str):
            match = re.match(r'^\s*([<>]=?|!=)\s*(-?\d+\.?\d*)\s*$', value)
            if match:
                operator, num_str = match.groups()
                condition = self._OPERATOR_MAP.get(operator)

                if condition is None:
                    raise ValueError(f"Invalid operator in string: '{value}'")
                return float(num_str), condition
            
            try:
                #Fallback for strings that are just numbers
                return float(value), "equal"
            except ValueError:
                raise ValueError(f"Could not parse numeric value from string: '{value}'")
        
        raise TypeError(f"Unsupported type for range value: {type(value)}")

    def __contains__(self, value: Union[int, float])->bool:
        """
        Checks if the given numeric value satisfies the defined conditions.

        Args:
            value (Union[int, float]): The number to check.

        Returns:
            bool: True if the value meets the condition(s), False otherwise.
            
        Raises:
            TypeError: If the input value is not an int or float.
        """
        if value is None:
            return False
        if not isinstance(value, (int, float)):
            raise TypeError(f"Comparison value must be an integer or float, not {type(value)}.")
        
        checks : List[bool] = [True] * len(self.__checks)
        for i, (condition, num) in enumerate(self.__checks):
            if condition == "greater" and not (value > num):
                checks[i] = False
            elif condition == "greater or equal" and not (value >= num):
                checks[i] = False
            elif condition == "inferior" and not (value < num):
                checks[i] = False
            elif condition == "inferior or equal" and not (value <= num):
                checks[i] = False
            elif condition == "equal" and not (value == num):
                checks[i] = False
            elif condition == "not equal" and (value == num):
                checks[i] = False
        
        return all(checks) if not self.__or_cond else any(checks)

    def __repr__(self) -> str:
        return f"NumericCondition(conditions={self.__checks})"

if __name__ == '__main__':
    print(__doc__)