from rich import print


class Sexagesimal:
    """
    A class to represent numbers in a sexagesimal (base-60) format.
    
    This class takes an integer and represents it in a sexagesimal format using
    two internal bases: a quasi base-5 and base-12. Each "register" in the
    sexagesimal representation contains two parts:

    - a part that counts up to 5 (represented with '>') 
    - and another part that counts up to 12 (represented with '|').
    
    Attributes:
    registers (list): A list of dictionaries where each dictionary holds boolean values
                      representing the presence of a symbol in base-5 and base-12 parts.
    
    Methods:
    _parse_sexagesimal(value): Recursively parses an integer into the sexagesimal format and stores it in registers.
    symbols(): Returns a string representation of the sexagesimal number using specific symbols.
    """
    def __init__(self, value=0):
        """
        Initializes the Sexagesimal object, setting up the registers and parsing the input value.

        Args:
        value (int): The integer value to be converted into sexagesimal format.
        """
        self.registers = []
        self._parse_sexagesimal(value)

    def _parse_sexagesimal(self, value):
        """
        Recursively parses an integer into sexagesimal format and stores the
        result in registers.  Each register contains a representation in base-5
        and base-12.

        Args:
        value (int): The integer value to be parsed.
        """
        if value == 0:
            return

        quotient, remainder = divmod(value, 60)

        base_5, base_12 = divmod(remainder, 12)

        register = {
            "base_5": [True if i < base_5 else False for i in range(5)],
            "base_12": [True if i < base_12 else False for i in range(12)],
        }

        self.registers.insert(0, register)

        self._parse_sexagesimal(quotient)


    @property
    def symbols(self):
        """
        Converts the parsed sexagesimal representation in registers into symbols
        for visual representation and returns it as a string.

        Returns:
        str: A string representing the sexagesimal format using symbols.
        """
        symbols = []
        for register in self.registers:
            base_5_symbol = ">" * sum(register["base_5"])
            base_12_symbol = "|" * sum(register["base_12"])
            symbols.append(f"{base_5_symbol:5}{base_12_symbol:12}")

        # Displaying symbols in the reverse order for readability (higher orders first)
        return " ".join(symbols[::-1])


if __name__ == "__main__":
    for value in range(1, 70):
        bab_num = Sexagesimal(value)
        print(f"{value:5} {bab_num.symbols}")
