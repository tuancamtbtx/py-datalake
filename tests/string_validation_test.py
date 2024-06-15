import pytest
from pydata.validation.string import StringValidation

string_validation = StringValidation()


is_check_empty = string_validation.is_empty_string("Hello World")
print(is_check_empty)
is_check_special = string_validation.exist_special_characters("Hello World")
print(is_check_special)