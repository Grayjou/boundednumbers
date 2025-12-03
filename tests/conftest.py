# conftest.py
import pytest
from ..numbers.bounded import ClampedInt, CyclicInt, BouncedInt, ClampedFloat, CyclicFloat, BouncedFloat
from ..numbers.modulo_int import ModuloInt

@pytest.fixture
def clamp_int():
    return lambda v, mn=0, mx=10: ClampedInt(v, mn, mx)

@pytest.fixture
def cyclic_int():
    return lambda v, mn=0, mx=10: CyclicInt(v, mn, mx)

@pytest.fixture
def bounced_int():
    return lambda v, mn=0, mx=10: BouncedInt(v, mn, mx)

@pytest.fixture
def mod():
    return lambda v, m=10: ModuloInt(v, m)

@pytest.fixture
def clamp_float():
    return lambda v, mn=0.0, mx=1.0: ClampedFloat(v, mn, mx)

@pytest.fixture
def cyclic_float():
    return lambda v, mn=0.0, mx=1.0: CyclicFloat(v, mn, mx)

@pytest.fixture
def bounced_float():
    return lambda v, mn=0.0, mx=1.0: BouncedFloat(v, mn, mx)