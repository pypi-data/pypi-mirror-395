# CustomerPortal

Types:

```python
from lark.types import CustomerPortalCreateSessionResponse
```

Methods:

- <code title="post /customer-portal/sessions">client.customer_portal.<a href="./src/lark/resources/customer_portal.py">create_session</a>(\*\*<a href="src/lark/types/customer_portal_create_session_params.py">params</a>) -> <a href="./src/lark/types/customer_portal_create_session_response.py">CustomerPortalCreateSessionResponse</a></code>

# RateCards

Types:

```python
from lark.types import (
    AmountInput,
    FlatPriceInput,
    FlatPriceOutput,
    PackagePriceInput,
    PackagePriceOutput,
    RateCardResource,
    RateCardListResponse,
)
```

Methods:

- <code title="post /rate-cards">client.rate_cards.<a href="./src/lark/resources/rate_cards.py">create</a>(\*\*<a href="src/lark/types/rate_card_create_params.py">params</a>) -> <a href="./src/lark/types/rate_card_resource.py">RateCardResource</a></code>
- <code title="get /rate-cards/{rate_card_id}">client.rate_cards.<a href="./src/lark/resources/rate_cards.py">retrieve</a>(rate_card_id) -> <a href="./src/lark/types/rate_card_resource.py">RateCardResource</a></code>
- <code title="get /rate-cards">client.rate_cards.<a href="./src/lark/resources/rate_cards.py">list</a>(\*\*<a href="src/lark/types/rate_card_list_params.py">params</a>) -> <a href="./src/lark/types/rate_card_list_response.py">RateCardListResponse</a></code>

# UsageEvents

Methods:

- <code title="post /usage-events">client.usage_events.<a href="./src/lark/resources/usage_events.py">create</a>(\*\*<a href="src/lark/types/usage_event_create_params.py">params</a>) -> object</code>

# Subscriptions

Types:

```python
from lark.types import (
    CheckoutCallback,
    SubscriptionResource,
    SubscriptionCreateResponse,
    SubscriptionListResponse,
    SubscriptionChangeRateCardResponse,
)
```

Methods:

- <code title="post /subscriptions">client.subscriptions.<a href="./src/lark/resources/subscriptions.py">create</a>(\*\*<a href="src/lark/types/subscription_create_params.py">params</a>) -> <a href="./src/lark/types/subscription_create_response.py">SubscriptionCreateResponse</a></code>
- <code title="get /subscriptions/{subscription_id}">client.subscriptions.<a href="./src/lark/resources/subscriptions.py">retrieve</a>(subscription_id) -> <a href="./src/lark/types/subscription_resource.py">SubscriptionResource</a></code>
- <code title="get /subscriptions">client.subscriptions.<a href="./src/lark/resources/subscriptions.py">list</a>(\*\*<a href="src/lark/types/subscription_list_params.py">params</a>) -> <a href="./src/lark/types/subscription_list_response.py">SubscriptionListResponse</a></code>
- <code title="post /subscriptions/{subscription_id}/cancel">client.subscriptions.<a href="./src/lark/resources/subscriptions.py">cancel</a>(subscription_id, \*\*<a href="src/lark/types/subscription_cancel_params.py">params</a>) -> <a href="./src/lark/types/subscription_resource.py">SubscriptionResource</a></code>
- <code title="post /subscriptions/{subscription_id}/change-rate-card">client.subscriptions.<a href="./src/lark/resources/subscriptions.py">change_rate_card</a>(subscription_id, \*\*<a href="src/lark/types/subscription_change_rate_card_params.py">params</a>) -> <a href="./src/lark/types/subscription_change_rate_card_response.py">SubscriptionChangeRateCardResponse</a></code>

# Subjects

Types:

```python
from lark.types import SubjectResource, SubjectCreateResponse, SubjectListResponse
```

Methods:

- <code title="post /subjects">client.subjects.<a href="./src/lark/resources/subjects.py">create</a>(\*\*<a href="src/lark/types/subject_create_params.py">params</a>) -> <a href="./src/lark/types/subject_create_response.py">SubjectCreateResponse</a></code>
- <code title="get /subjects/{subject_id}">client.subjects.<a href="./src/lark/resources/subjects.py">retrieve</a>(subject_id) -> <a href="./src/lark/types/subject_resource.py">SubjectResource</a></code>
- <code title="put /subjects/{subject_id}">client.subjects.<a href="./src/lark/resources/subjects.py">update</a>(subject_id, \*\*<a href="src/lark/types/subject_update_params.py">params</a>) -> <a href="./src/lark/types/subject_resource.py">SubjectResource</a></code>
- <code title="get /subjects">client.subjects.<a href="./src/lark/resources/subjects.py">list</a>(\*\*<a href="src/lark/types/subject_list_params.py">params</a>) -> <a href="./src/lark/types/subject_list_response.py">SubjectListResponse</a></code>
- <code title="delete /subjects/{subject_id}">client.subjects.<a href="./src/lark/resources/subjects.py">delete</a>(subject_id) -> object</code>

# PricingMetrics

Types:

```python
from lark.types import (
    Period,
    PricingMetricResource,
    PricingMetricListResponse,
    PricingMetricCreateSummaryResponse,
)
```

Methods:

- <code title="post /pricing-metrics">client.pricing_metrics.<a href="./src/lark/resources/pricing_metrics.py">create</a>(\*\*<a href="src/lark/types/pricing_metric_create_params.py">params</a>) -> <a href="./src/lark/types/pricing_metric_resource.py">PricingMetricResource</a></code>
- <code title="get /pricing-metrics/{pricing_metric_id}">client.pricing_metrics.<a href="./src/lark/resources/pricing_metrics.py">retrieve</a>(pricing_metric_id) -> <a href="./src/lark/types/pricing_metric_resource.py">PricingMetricResource</a></code>
- <code title="get /pricing-metrics">client.pricing_metrics.<a href="./src/lark/resources/pricing_metrics.py">list</a>(\*\*<a href="src/lark/types/pricing_metric_list_params.py">params</a>) -> <a href="./src/lark/types/pricing_metric_list_response.py">PricingMetricListResponse</a></code>
- <code title="post /pricing-metrics/{pricing_metric_id}/summary">client.pricing_metrics.<a href="./src/lark/resources/pricing_metrics.py">create_summary</a>(pricing_metric_id, \*\*<a href="src/lark/types/pricing_metric_create_summary_params.py">params</a>) -> <a href="./src/lark/types/pricing_metric_create_summary_response.py">PricingMetricCreateSummaryResponse</a></code>

# CustomerAccess

Types:

```python
from lark.types import CustomerAccessRetrieveBillingStateResponse
```

Methods:

- <code title="get /customer-access/{subject_id}/billing-state">client.customer_access.<a href="./src/lark/resources/customer_access.py">retrieve_billing_state</a>(subject_id) -> <a href="./src/lark/types/customer_access_retrieve_billing_state_response.py">CustomerAccessRetrieveBillingStateResponse</a></code>

# Invoices

Types:

```python
from lark.types import AmountOutput, InvoiceListResponse
```

Methods:

- <code title="get /invoices">client.invoices.<a href="./src/lark/resources/invoices.py">list</a>(\*\*<a href="src/lark/types/invoice_list_params.py">params</a>) -> <a href="./src/lark/types/invoice_list_response.py">InvoiceListResponse</a></code>
