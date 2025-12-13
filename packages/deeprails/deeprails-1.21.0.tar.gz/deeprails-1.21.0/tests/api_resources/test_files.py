# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from deeprails import DeepRails, AsyncDeepRails
from tests.utils import assert_matches_type
from deeprails.types import FileResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_upload(self, client: DeepRails) -> None:
        file = client.files.upload(
            files=["string"],
        )
        assert_matches_type(FileResponse, file, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_upload(self, client: DeepRails) -> None:
        response = client.files.with_raw_response.upload(
            files=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileResponse, file, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_upload(self, client: DeepRails) -> None:
        with client.files.with_streaming_response.upload(
            files=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFiles:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_upload(self, async_client: AsyncDeepRails) -> None:
        file = await async_client.files.upload(
            files=["string"],
        )
        assert_matches_type(FileResponse, file, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_upload(self, async_client: AsyncDeepRails) -> None:
        response = await async_client.files.with_raw_response.upload(
            files=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(FileResponse, file, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_upload(self, async_client: AsyncDeepRails) -> None:
        async with async_client.files.with_streaming_response.upload(
            files=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True
