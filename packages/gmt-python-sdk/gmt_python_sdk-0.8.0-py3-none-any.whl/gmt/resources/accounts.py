# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import account_list_params, account_list_countries_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncPageNumber, AsyncPageNumber
from .._base_client import AsyncPaginator, make_request_options
from ..types.account_list_response import AccountListResponse
from ..types.account_retrieve_response import AccountRetrieveResponse
from ..types.account_list_countries_response import AccountListCountriesResponse

__all__ = ["AccountsResource", "AsyncAccountsResource"]


class AccountsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cameo6/gmt-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cameo6/gmt-python-sdk#with_streaming_response
        """
        return AccountsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        country_code: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AccountRetrieveResponse:
        """
        Returns detailed information about account for specific country including
        pricing and discount information.

        Args:
          country_code: ISO 3166-1 alpha-2 country code (e.g., US, RU, GB).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not country_code:
            raise ValueError(f"Expected a non-empty value for `country_code` but received {country_code!r}")
        return self._get(
            f"/v1/accounts/{country_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrieveResponse,
        )

    def list(
        self,
        *,
        page: int,
        page_size: int,
        sort: Literal["price_asc", "price_desc", "name_asc", "name_desc"],
        country_codes: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageNumber[AccountListResponse]:
        """
        Returns paginated list of accounts with filtering and sorting options.

        Args:
          page: Page number.

          page_size: Number of items per page.

          sort: Sort order for accounts.

          country_codes: Filter by country codes. Comma-separated list of ISO 3166-1 alpha-2 codes (e.g.,
              'US,RU,GB').

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/accounts/",
            page=SyncPageNumber[AccountListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "sort": sort,
                        "country_codes": country_codes,
                    },
                    account_list_params.AccountListParams,
                ),
            ),
            model=AccountListResponse,
        )

    def list_countries(
        self,
        *,
        page: int,
        page_size: int,
        sort: Literal["price_asc", "price_desc", "name_asc", "name_desc"],
        country_codes: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageNumber[AccountListCountriesResponse]:
        """
        Returns a list of all available countries from providers with prices and
        availability. No authentication required.

        Args:
          page: Page number.

          page_size: Number of items per page.

          sort: Sort order for accounts.

          country_codes: Filter by country codes. Comma-separated list of ISO 3166-1 alpha-2 codes (e.g.,
              'US,RU,GB').

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/accounts/countries",
            page=SyncPageNumber[AccountListCountriesResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "sort": sort,
                        "country_codes": country_codes,
                    },
                    account_list_countries_params.AccountListCountriesParams,
                ),
            ),
            model=AccountListCountriesResponse,
        )


class AsyncAccountsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAccountsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cameo6/gmt-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAccountsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cameo6/gmt-python-sdk#with_streaming_response
        """
        return AsyncAccountsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        country_code: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AccountRetrieveResponse:
        """
        Returns detailed information about account for specific country including
        pricing and discount information.

        Args:
          country_code: ISO 3166-1 alpha-2 country code (e.g., US, RU, GB).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not country_code:
            raise ValueError(f"Expected a non-empty value for `country_code` but received {country_code!r}")
        return await self._get(
            f"/v1/accounts/{country_code}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AccountRetrieveResponse,
        )

    def list(
        self,
        *,
        page: int,
        page_size: int,
        sort: Literal["price_asc", "price_desc", "name_asc", "name_desc"],
        country_codes: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[AccountListResponse, AsyncPageNumber[AccountListResponse]]:
        """
        Returns paginated list of accounts with filtering and sorting options.

        Args:
          page: Page number.

          page_size: Number of items per page.

          sort: Sort order for accounts.

          country_codes: Filter by country codes. Comma-separated list of ISO 3166-1 alpha-2 codes (e.g.,
              'US,RU,GB').

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/accounts/",
            page=AsyncPageNumber[AccountListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "sort": sort,
                        "country_codes": country_codes,
                    },
                    account_list_params.AccountListParams,
                ),
            ),
            model=AccountListResponse,
        )

    def list_countries(
        self,
        *,
        page: int,
        page_size: int,
        sort: Literal["price_asc", "price_desc", "name_asc", "name_desc"],
        country_codes: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[AccountListCountriesResponse, AsyncPageNumber[AccountListCountriesResponse]]:
        """
        Returns a list of all available countries from providers with prices and
        availability. No authentication required.

        Args:
          page: Page number.

          page_size: Number of items per page.

          sort: Sort order for accounts.

          country_codes: Filter by country codes. Comma-separated list of ISO 3166-1 alpha-2 codes (e.g.,
              'US,RU,GB').

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/accounts/countries",
            page=AsyncPageNumber[AccountListCountriesResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "sort": sort,
                        "country_codes": country_codes,
                    },
                    account_list_countries_params.AccountListCountriesParams,
                ),
            ),
            model=AccountListCountriesResponse,
        )


class AccountsResourceWithRawResponse:
    def __init__(self, accounts: AccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = to_raw_response_wrapper(
            accounts.retrieve,
        )
        self.list = to_raw_response_wrapper(
            accounts.list,
        )
        self.list_countries = to_raw_response_wrapper(
            accounts.list_countries,
        )


class AsyncAccountsResourceWithRawResponse:
    def __init__(self, accounts: AsyncAccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = async_to_raw_response_wrapper(
            accounts.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            accounts.list,
        )
        self.list_countries = async_to_raw_response_wrapper(
            accounts.list_countries,
        )


class AccountsResourceWithStreamingResponse:
    def __init__(self, accounts: AccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = to_streamed_response_wrapper(
            accounts.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            accounts.list,
        )
        self.list_countries = to_streamed_response_wrapper(
            accounts.list_countries,
        )


class AsyncAccountsResourceWithStreamingResponse:
    def __init__(self, accounts: AsyncAccountsResource) -> None:
        self._accounts = accounts

        self.retrieve = async_to_streamed_response_wrapper(
            accounts.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            accounts.list,
        )
        self.list_countries = async_to_streamed_response_wrapper(
            accounts.list_countries,
        )
