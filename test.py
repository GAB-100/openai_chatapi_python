import pytest
from main import has_exceeded_max_length
import random
import string

# Run pytest -x test.py to execute tests
def generate_random_string(length):
    # Get all the ASCII letters in lowercase and uppercase
    letters = string.ascii_letters
    # Randomly choose characters from letters for the given length of the string
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def test_prompt_is_within_limit():
    text_within_limit = generate_random_string(200)
    assert has_exceeded_max_length(text_within_limit) is False

def test_prompt_has_exceeded_limit():
    text_beyond_limit = generate_random_string(4200)
    assert has_exceeded_max_length(text_beyond_limit) is True


