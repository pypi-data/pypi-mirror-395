import pytest

from pymacaroons2 import Macaroon
from pymacaroons2.async_verifier import AsyncVerifier


@pytest.mark.asyncio
async def test_basic_async_verify():
    m = Macaroon(location="test", identifier=b"id", key=b"secret")
    v = AsyncVerifier()
    await v.verify_async(m, b"secret")  # Should not raise
