# Companies

Types:

```python
from kausate.types import (
    CompanyReport,
    DateInfo,
    LegalForm,
    Person,
    ProductOrderResponse,
    SignatoryRules,
    Status,
    UltimateBeneficialOwner,
    UltimateBeneficialOwnerReport,
    CompanyExtractUboResponse,
)
```

Methods:

- <code title="post /v2/companies/{kausateId}/shareholder-graph">client.companies.<a href="./src/kausate/resources/companies/companies.py">extract_shareholder_graph</a>(kausate_id, \*\*<a href="src/kausate/types/company_extract_shareholder_graph_params.py">params</a>) -> <a href="./src/kausate/types/product_order_response.py">ProductOrderResponse</a></code>
- <code title="post /v2/companies/{kausateId}/ubo">client.companies.<a href="./src/kausate/resources/companies/companies.py">extract_ubo</a>(kausate_id, \*\*<a href="src/kausate/types/company_extract_ubo_params.py">params</a>) -> <a href="./src/kausate/types/company_extract_ubo_response.py">CompanyExtractUboResponse</a></code>

## Search

Types:

```python
from kausate.types.companies import (
    Address,
    CompanySearchResult,
    GermanAdvancedQuery,
    Identifier,
    LiveSearchResponse,
    UkAdvancedQuery,
    SearchAutocompleteResponse,
    SearchIndexResponse,
    SearchRealTimeResponse,
)
```

Methods:

- <code title="get /v2/companies/search/autocomplete">client.companies.search.<a href="./src/kausate/resources/companies/search.py">autocomplete</a>(\*\*<a href="src/kausate/types/companies/search_autocomplete_params.py">params</a>) -> <a href="./src/kausate/types/companies/search_autocomplete_response.py">SearchAutocompleteResponse</a></code>
- <code title="post /v2/companies/search/indexed">client.companies.search.<a href="./src/kausate/resources/companies/search.py">index</a>(\*\*<a href="src/kausate/types/companies/search_index_params.py">params</a>) -> <a href="./src/kausate/types/companies/search_index_response.py">SearchIndexResponse</a></code>
- <code title="post /v2/companies/search/live">client.companies.search.<a href="./src/kausate/resources/companies/search.py">real_time</a>(\*\*<a href="src/kausate/types/companies/search_real_time_params.py">params</a>) -> <a href="./src/kausate/types/companies/search_real_time_response.py">SearchRealTimeResponse</a></code>

## Products

Types:

```python
from kausate.types.companies import DocumentResult, ProductOrderResponse
```

Methods:

- <code title="post /v2/companies/{kausateId}/products/order">client.companies.products.<a href="./src/kausate/resources/companies/products.py">order</a>(kausate_id, \*\*<a href="src/kausate/types/companies/product_order_params.py">params</a>) -> <a href="./src/kausate/types/companies/product_order_response.py">ProductOrderResponse</a></code>

## Report

Types:

```python
from kausate.types.companies import ReportCreateResponse
```

Methods:

- <code title="post /v2/companies/{kausateId}/report">client.companies.report.<a href="./src/kausate/resources/companies/report.py">create</a>(kausate_id, \*\*<a href="src/kausate/types/companies/report_create_params.py">params</a>) -> <a href="./src/kausate/types/companies/report_create_response.py">ReportCreateResponse</a></code>

## Documents

Types:

```python
from kausate.types.companies import DocumentListResponse
```

Methods:

- <code title="post /v2/companies/{kausateId}/documents/list">client.companies.documents.<a href="./src/kausate/resources/companies/documents.py">list</a>(kausate_id, \*\*<a href="src/kausate/types/companies/document_list_params.py">params</a>) -> <a href="./src/kausate/types/companies/document_list_response.py">DocumentListResponse</a></code>

# Orders

Types:

```python
from kausate.types import (
    Currency,
    InterestType,
    PercentageShare,
    Role,
    Shareholder,
    ShareholderReportData,
    OrderRetrieveResponse,
    OrderListResponse,
)
```

Methods:

- <code title="get /v2/orders/{orderId}">client.orders.<a href="./src/kausate/resources/orders.py">retrieve</a>(order_id, \*\*<a href="src/kausate/types/order_retrieve_params.py">params</a>) -> <a href="./src/kausate/types/order_retrieve_response.py">OrderRetrieveResponse</a></code>
- <code title="get /v2/orders">client.orders.<a href="./src/kausate/resources/orders.py">list</a>(\*\*<a href="src/kausate/types/order_list_params.py">params</a>) -> <a href="./src/kausate/types/order_list_response.py">OrderListResponse</a></code>

# Secrets

Types:

```python
from kausate.types import SecretResponsePublic, SecretListResponse
```

Methods:

- <code title="post /v2/secrets">client.secrets.<a href="./src/kausate/resources/secrets.py">create</a>(\*\*<a href="src/kausate/types/secret_create_params.py">params</a>) -> <a href="./src/kausate/types/secret_response_public.py">SecretResponsePublic</a></code>
- <code title="put /v2/secrets/{datasourceSlug}">client.secrets.<a href="./src/kausate/resources/secrets.py">update</a>(datasource_slug, \*\*<a href="src/kausate/types/secret_update_params.py">params</a>) -> <a href="./src/kausate/types/secret_response_public.py">SecretResponsePublic</a></code>
- <code title="get /v2/secrets">client.secrets.<a href="./src/kausate/resources/secrets.py">list</a>(\*\*<a href="src/kausate/types/secret_list_params.py">params</a>) -> <a href="./src/kausate/types/secret_list_response.py">SecretListResponse</a></code>
- <code title="delete /v2/secrets/{datasourceSlug}">client.secrets.<a href="./src/kausate/resources/secrets.py">delete</a>(datasource_slug, \*\*<a href="src/kausate/types/secret_delete_params.py">params</a>) -> object</code>

# Webhooks

Types:

```python
from kausate.types import WebhookResponse, WebhookStatus, WebhookListResponse
```

Methods:

- <code title="post /v2/webhooks">client.webhooks.<a href="./src/kausate/resources/webhooks.py">create</a>(\*\*<a href="src/kausate/types/webhook_create_params.py">params</a>) -> <a href="./src/kausate/types/webhook_response.py">WebhookResponse</a></code>
- <code title="get /v2/webhooks/{webhookId}">client.webhooks.<a href="./src/kausate/resources/webhooks.py">retrieve</a>(webhook_id) -> <a href="./src/kausate/types/webhook_response.py">WebhookResponse</a></code>
- <code title="put /v2/webhooks/{webhookId}">client.webhooks.<a href="./src/kausate/resources/webhooks.py">update</a>(webhook_id, \*\*<a href="src/kausate/types/webhook_update_params.py">params</a>) -> <a href="./src/kausate/types/webhook_response.py">WebhookResponse</a></code>
- <code title="get /v2/webhooks">client.webhooks.<a href="./src/kausate/resources/webhooks.py">list</a>() -> <a href="./src/kausate/types/webhook_list_response.py">WebhookListResponse</a></code>
- <code title="delete /v2/webhooks/{webhookId}">client.webhooks.<a href="./src/kausate/resources/webhooks.py">delete</a>(webhook_id) -> None</code>
