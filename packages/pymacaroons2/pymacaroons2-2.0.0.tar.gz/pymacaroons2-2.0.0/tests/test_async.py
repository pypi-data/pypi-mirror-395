import pytest
import asyncio
from pymacaroons22 import Macaroon
from pymacaroons22.async_verifier import AsyncVerifier

@pytest.mark.asyncio
async def test_basic_async_verify():
    m = Macaroon(location="test", identifier=b"id", key=b"secret")
    v = AsyncVerifier()
    await v.verify_async(m, b"secret")  # Should not raise
