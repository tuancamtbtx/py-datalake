
# Importing required modules
from pydata.logger.logger_mixing import LoggerMixing

class StringValidation(LoggerMixing):
    def __init__(self) -> None:
        super().__init__()

    def is_empty_string(self, input_string: str) -> bool:
        """
        This function checks if the input string is empty or not.
        Args:
        input_string : str : Input string to be checked
        Returns:
        bool : True if the input string is empty, False otherwise
        """
        if not input_string:
            self.logger.error("Input string is empty")
            return True
        return False
    
    def exist_special_characters(self, input_string: str) -> bool:
        """
        This function checks if the input string contains special characters or not.
        Args:
        input_string : str : Input string to be checked
        Returns:
        bool : True if the input string contains special characters, False otherwise
        """
        special_characters = "!@#$%^&*()-+?_=,<>/"
        for character in input_string:
            if character in special_characters:
                self.logger.error("Input string contains special characters")
                return True
        return False