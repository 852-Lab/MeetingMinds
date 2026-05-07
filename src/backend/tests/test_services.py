import pytest
from services.llm import LLMGenerator
import os

def test_llm_generator_init():
    generator = LLMGenerator(model="gemma3:4b")
    assert generator.model == "gemma3:4b"

# More tests could be added here with mocking
