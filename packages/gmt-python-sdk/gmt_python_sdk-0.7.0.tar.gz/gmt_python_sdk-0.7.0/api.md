# Service

Types:

```python
from gmt.types import ServiceGetServerTimeResponse, ServiceHealthCheckResponse
```

Methods:

- <code title="get /v1/service/time">client.service.<a href="./src/gmt/resources/service.py">get_server_time</a>() -> <a href="./src/gmt/types/service_get_server_time_response.py">ServiceGetServerTimeResponse</a></code>
- <code title="get /v1/service/health">client.service.<a href="./src/gmt/resources/service.py">health_check</a>() -> <a href="./src/gmt/types/service_health_check_response.py">ServiceHealthCheckResponse</a></code>

# Accounts

Types:

```python
from gmt.types import AccountRetrieveResponse, AccountListResponse, AccountListCountriesResponse
```

Methods:

- <code title="get /v1/accounts/{country_code}">client.accounts.<a href="./src/gmt/resources/accounts.py">retrieve</a>(country_code) -> <a href="./src/gmt/types/account_retrieve_response.py">AccountRetrieveResponse</a></code>
- <code title="get /v1/accounts/">client.accounts.<a href="./src/gmt/resources/accounts.py">list</a>(\*\*<a href="src/gmt/types/account_list_params.py">params</a>) -> <a href="./src/gmt/types/account_list_response.py">SyncPageNumber[AccountListResponse]</a></code>
- <code title="get /v1/accounts/countries">client.accounts.<a href="./src/gmt/resources/accounts.py">list_countries</a>(\*\*<a href="src/gmt/types/account_list_countries_params.py">params</a>) -> <a href="./src/gmt/types/account_list_countries_response.py">SyncPageNumber[AccountListCountriesResponse]</a></code>

# Profile

Types:

```python
from gmt.types import ProfileRetrieveResponse
```

Methods:

- <code title="get /v1/profile/">client.profile.<a href="./src/gmt/resources/profile.py">retrieve</a>() -> <a href="./src/gmt/types/profile_retrieve_response.py">ProfileRetrieveResponse</a></code>

# Purchases

Types:

```python
from gmt.types import (
    PurchaseCreateResponse,
    PurchaseRetrieveResponse,
    PurchaseListResponse,
    PurchaseRefundResponse,
    PurchaseRequestVerificationCodeResponse,
)
```

Methods:

- <code title="post /v1/purchases/">client.purchases.<a href="./src/gmt/resources/purchases.py">create</a>(\*\*<a href="src/gmt/types/purchase_create_params.py">params</a>) -> <a href="./src/gmt/types/purchase_create_response.py">PurchaseCreateResponse</a></code>
- <code title="get /v1/purchases/{purchase_id}">client.purchases.<a href="./src/gmt/resources/purchases.py">retrieve</a>(purchase_id) -> <a href="./src/gmt/types/purchase_retrieve_response.py">PurchaseRetrieveResponse</a></code>
- <code title="get /v1/purchases/">client.purchases.<a href="./src/gmt/resources/purchases.py">list</a>(\*\*<a href="src/gmt/types/purchase_list_params.py">params</a>) -> <a href="./src/gmt/types/purchase_list_response.py">SyncPageNumber[PurchaseListResponse]</a></code>
- <code title="post /v1/purchases/{purchase_id}/refund">client.purchases.<a href="./src/gmt/resources/purchases.py">refund</a>(purchase_id) -> <a href="./src/gmt/types/purchase_refund_response.py">PurchaseRefundResponse</a></code>
- <code title="post /v1/purchases/{purchase_id}/request-code">client.purchases.<a href="./src/gmt/resources/purchases.py">request_verification_code</a>(purchase_id, \*\*<a href="src/gmt/types/purchase_request_verification_code_params.py">params</a>) -> <a href="./src/gmt/types/purchase_request_verification_code_response.py">PurchaseRequestVerificationCodeResponse</a></code>

# Webhooks

Types:

```python
from gmt.types import WebhookTestResponse
```

Methods:

- <code title="post /v1/webhooks/test">client.webhooks.<a href="./src/gmt/resources/webhooks.py">test</a>(\*\*<a href="src/gmt/types/webhook_test_params.py">params</a>) -> <a href="./src/gmt/types/webhook_test_response.py">WebhookTestResponse</a></code>
