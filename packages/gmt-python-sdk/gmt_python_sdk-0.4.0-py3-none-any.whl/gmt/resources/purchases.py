# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import purchase_list_params, purchase_create_params, purchase_request_verification_code_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
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
from ..types.purchase_list_response import PurchaseListResponse
from ..types.purchase_create_response import PurchaseCreateResponse
from ..types.purchase_retrieve_response import PurchaseRetrieveResponse
from ..types.purchase_request_verification_code_response import PurchaseRequestVerificationCodeResponse

__all__ = ["PurchasesResource", "AsyncPurchasesResource"]


class PurchasesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PurchasesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cameo6/gmt-python-sdk#accessing-raw-response-data-eg-headers
        """
        return PurchasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PurchasesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cameo6/gmt-python-sdk#with_streaming_response
        """
        return PurchasesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        country_code: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PurchaseCreateResponse:
        """Creates a new purchase for specified country.

        Deducts balance immediately and
        returns purchase with `PENDING` status.

        **Purchase Creation Process**

        1. Validates country availability and user balance.
        2. Reserves account from provider.
        3. Atomically deducts balance and creates purchase record.
        4. Returns purchase in `PENDING` status.

        **Next steps.** Call `POST /purchases/:id/request-code` to retrieve login
        credentials.

        **Country availability.** Accounts may become unavailable between checking
        `/accounts` and creating purchase. Always handle availability errors gracefully.

        Args:
          country_code: ISO 3166-1 alpha-2 country code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/purchases/",
            body=maybe_transform({"country_code": country_code}, purchase_create_params.PurchaseCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PurchaseCreateResponse,
        )

    def retrieve(
        self,
        purchase_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PurchaseRetrieveResponse:
        """
        Returns detailed information about specific purchase including verification data
        if available.

        **Security.** Verification data is only visible to the purchase owner.

        Args:
          purchase_id: Unique purchase identifier.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/v1/purchases/{purchase_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PurchaseRetrieveResponse,
        )

    def list(
        self,
        *,
        page: int,
        page_size: int,
        status: Literal["PENDING", "SUCCESS", "ERROR", "REFUND"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageNumber[PurchaseListResponse]:
        """
        Returns paginated list of user's purchases with optional status filtering.

        **Chronological Ordering.** Purchases are always returned **newest first**
        (descending by `created_at`).

        **Pagination behavior**

        - Results are consistent during session (no duplicates or missing items when
          paginating).
        - `has_next: true` indicates more pages available.
        - Maximum `page_size` is 50 items.

        **Filtering.** Combine `status` filter with pagination for subset queries (e.g.,
        all successful purchases).

        Args:
          page: Page number (starts from 1).

          page_size: Number of items per page (max 50).

          status: **Purchase Status Lifecycle.** `PENDING` (initial) → `SUCCESS` (after code
              request) or `ERROR` (provider failure). Any status can transition to `REFUND`
              via admin action.

              **Important.** Status is immutable once set to `SUCCESS`, `ERROR`, or `REFUND`.

              **Filter options**

              - `PENDING` - code not requested.
              - `SUCCESS` - code ready.
              - `ERROR` - provider failed.
              - `REFUND` - money returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/purchases/",
            page=SyncPageNumber[PurchaseListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "status": status,
                    },
                    purchase_list_params.PurchaseListParams,
                ),
            ),
            model=PurchaseListResponse,
        )

    def request_verification_code(
        self,
        purchase_id: int,
        *,
        callback_url: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PurchaseRequestVerificationCodeResponse:
        """Requests verification code and password from provider.

        Updates purchase status
        to SUCCESS.

        **Idempotent Operation.** Safe to retry on network errors - will not generate
        duplicate codes.

        **Behavior.**

        - First call: Fetches code from provider, updates status to `SUCCESS`
        - Subsequent calls: Returns conflict error (use `GET /purchases/:id` to retrieve
          existing code)

        **Provider timeout.** Code retrieval may take 5-30 seconds depending on provider
        availability.

        **Webhook notification.** Optionally provide `callback_url` to receive a POST
        webhook when code is retrieved. See [Webhooks](#tag/webhooks) section for
        payload structure and **Models** section for `WebhookSuccessPayload` /
        `WebhookFailedPayload` schemas.

        Args:
          purchase_id: Unique purchase identifier.

          callback_url: URL to receive webhook notification when code is received. POST request will be
              sent with either `WebhookSuccessPayload` or `WebhookFailedPayload`.

              **Retry policy.** If your endpoint does not return HTTP 200, webhook will be
              retried up to 3 times with delays: immediately, after 10 seconds, after 30
              seconds. Any non-200 response triggers retry.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/v1/purchases/{purchase_id}/request-code",
            body=maybe_transform(
                {"callback_url": callback_url},
                purchase_request_verification_code_params.PurchaseRequestVerificationCodeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PurchaseRequestVerificationCodeResponse,
        )


class AsyncPurchasesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPurchasesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cameo6/gmt-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncPurchasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPurchasesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cameo6/gmt-python-sdk#with_streaming_response
        """
        return AsyncPurchasesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        country_code: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PurchaseCreateResponse:
        """Creates a new purchase for specified country.

        Deducts balance immediately and
        returns purchase with `PENDING` status.

        **Purchase Creation Process**

        1. Validates country availability and user balance.
        2. Reserves account from provider.
        3. Atomically deducts balance and creates purchase record.
        4. Returns purchase in `PENDING` status.

        **Next steps.** Call `POST /purchases/:id/request-code` to retrieve login
        credentials.

        **Country availability.** Accounts may become unavailable between checking
        `/accounts` and creating purchase. Always handle availability errors gracefully.

        Args:
          country_code: ISO 3166-1 alpha-2 country code.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/purchases/",
            body=await async_maybe_transform(
                {"country_code": country_code}, purchase_create_params.PurchaseCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PurchaseCreateResponse,
        )

    async def retrieve(
        self,
        purchase_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PurchaseRetrieveResponse:
        """
        Returns detailed information about specific purchase including verification data
        if available.

        **Security.** Verification data is only visible to the purchase owner.

        Args:
          purchase_id: Unique purchase identifier.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/v1/purchases/{purchase_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PurchaseRetrieveResponse,
        )

    def list(
        self,
        *,
        page: int,
        page_size: int,
        status: Literal["PENDING", "SUCCESS", "ERROR", "REFUND"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[PurchaseListResponse, AsyncPageNumber[PurchaseListResponse]]:
        """
        Returns paginated list of user's purchases with optional status filtering.

        **Chronological Ordering.** Purchases are always returned **newest first**
        (descending by `created_at`).

        **Pagination behavior**

        - Results are consistent during session (no duplicates or missing items when
          paginating).
        - `has_next: true` indicates more pages available.
        - Maximum `page_size` is 50 items.

        **Filtering.** Combine `status` filter with pagination for subset queries (e.g.,
        all successful purchases).

        Args:
          page: Page number (starts from 1).

          page_size: Number of items per page (max 50).

          status: **Purchase Status Lifecycle.** `PENDING` (initial) → `SUCCESS` (after code
              request) or `ERROR` (provider failure). Any status can transition to `REFUND`
              via admin action.

              **Important.** Status is immutable once set to `SUCCESS`, `ERROR`, or `REFUND`.

              **Filter options**

              - `PENDING` - code not requested.
              - `SUCCESS` - code ready.
              - `ERROR` - provider failed.
              - `REFUND` - money returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/purchases/",
            page=AsyncPageNumber[PurchaseListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page": page,
                        "page_size": page_size,
                        "status": status,
                    },
                    purchase_list_params.PurchaseListParams,
                ),
            ),
            model=PurchaseListResponse,
        )

    async def request_verification_code(
        self,
        purchase_id: int,
        *,
        callback_url: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PurchaseRequestVerificationCodeResponse:
        """Requests verification code and password from provider.

        Updates purchase status
        to SUCCESS.

        **Idempotent Operation.** Safe to retry on network errors - will not generate
        duplicate codes.

        **Behavior.**

        - First call: Fetches code from provider, updates status to `SUCCESS`
        - Subsequent calls: Returns conflict error (use `GET /purchases/:id` to retrieve
          existing code)

        **Provider timeout.** Code retrieval may take 5-30 seconds depending on provider
        availability.

        **Webhook notification.** Optionally provide `callback_url` to receive a POST
        webhook when code is retrieved. See [Webhooks](#tag/webhooks) section for
        payload structure and **Models** section for `WebhookSuccessPayload` /
        `WebhookFailedPayload` schemas.

        Args:
          purchase_id: Unique purchase identifier.

          callback_url: URL to receive webhook notification when code is received. POST request will be
              sent with either `WebhookSuccessPayload` or `WebhookFailedPayload`.

              **Retry policy.** If your endpoint does not return HTTP 200, webhook will be
              retried up to 3 times with delays: immediately, after 10 seconds, after 30
              seconds. Any non-200 response triggers retry.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/v1/purchases/{purchase_id}/request-code",
            body=await async_maybe_transform(
                {"callback_url": callback_url},
                purchase_request_verification_code_params.PurchaseRequestVerificationCodeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PurchaseRequestVerificationCodeResponse,
        )


class PurchasesResourceWithRawResponse:
    def __init__(self, purchases: PurchasesResource) -> None:
        self._purchases = purchases

        self.create = to_raw_response_wrapper(
            purchases.create,
        )
        self.retrieve = to_raw_response_wrapper(
            purchases.retrieve,
        )
        self.list = to_raw_response_wrapper(
            purchases.list,
        )
        self.request_verification_code = to_raw_response_wrapper(
            purchases.request_verification_code,
        )


class AsyncPurchasesResourceWithRawResponse:
    def __init__(self, purchases: AsyncPurchasesResource) -> None:
        self._purchases = purchases

        self.create = async_to_raw_response_wrapper(
            purchases.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            purchases.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            purchases.list,
        )
        self.request_verification_code = async_to_raw_response_wrapper(
            purchases.request_verification_code,
        )


class PurchasesResourceWithStreamingResponse:
    def __init__(self, purchases: PurchasesResource) -> None:
        self._purchases = purchases

        self.create = to_streamed_response_wrapper(
            purchases.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            purchases.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            purchases.list,
        )
        self.request_verification_code = to_streamed_response_wrapper(
            purchases.request_verification_code,
        )


class AsyncPurchasesResourceWithStreamingResponse:
    def __init__(self, purchases: AsyncPurchasesResource) -> None:
        self._purchases = purchases

        self.create = async_to_streamed_response_wrapper(
            purchases.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            purchases.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            purchases.list,
        )
        self.request_verification_code = async_to_streamed_response_wrapper(
            purchases.request_verification_code,
        )
