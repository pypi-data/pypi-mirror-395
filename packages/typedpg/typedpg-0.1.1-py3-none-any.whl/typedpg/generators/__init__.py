"""
Code generators for typedpg.
"""

from typedpg.generators.dataclass_gen import generate_module as generate_dataclass_module
from typedpg.generators.pydantic_gen import generate_module as generate_pydantic_module

__all__ = ["generate_dataclass_module", "generate_pydantic_module"]
