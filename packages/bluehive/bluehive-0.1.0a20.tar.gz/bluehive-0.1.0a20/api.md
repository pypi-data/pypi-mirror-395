# Health

Types:

```python
from bluehive.types import HealthCheckResponse
```

Methods:

- <code title="get /v1/health">client.health.<a href="./src/bluehive/resources/health.py">check</a>() -> <a href="./src/bluehive/types/health_check_response.py">HealthCheckResponse</a></code>

# Version

Types:

```python
from bluehive.types import VersionRetrieveResponse
```

Methods:

- <code title="get /v1/version">client.version.<a href="./src/bluehive/resources/version.py">retrieve</a>() -> <a href="./src/bluehive/types/version_retrieve_response.py">VersionRetrieveResponse</a></code>

# Providers

Types:

```python
from bluehive.types import ProviderLookupResponse
```

Methods:

- <code title="get /v1/providers/lookup">client.providers.<a href="./src/bluehive/resources/providers.py">lookup</a>(\*\*<a href="src/bluehive/types/provider_lookup_params.py">params</a>) -> <a href="./src/bluehive/types/provider_lookup_response.py">ProviderLookupResponse</a></code>

# Database

Types:

```python
from bluehive.types import DatabaseCheckHealthResponse
```

Methods:

- <code title="get /v1/database/health">client.database.<a href="./src/bluehive/resources/database.py">check_health</a>() -> <a href="./src/bluehive/types/database_check_health_response.py">DatabaseCheckHealthResponse</a></code>

# Fax

Types:

```python
from bluehive.types import FaxListProvidersResponse, FaxRetrieveStatusResponse, FaxSendResponse
```

Methods:

- <code title="get /v1/fax/providers">client.fax.<a href="./src/bluehive/resources/fax.py">list_providers</a>() -> <a href="./src/bluehive/types/fax_list_providers_response.py">FaxListProvidersResponse</a></code>
- <code title="get /v1/fax/status/{id}">client.fax.<a href="./src/bluehive/resources/fax.py">retrieve_status</a>(id) -> <a href="./src/bluehive/types/fax_retrieve_status_response.py">FaxRetrieveStatusResponse</a></code>
- <code title="post /v1/fax/send">client.fax.<a href="./src/bluehive/resources/fax.py">send</a>(\*\*<a href="src/bluehive/types/fax_send_params.py">params</a>) -> <a href="./src/bluehive/types/fax_send_response.py">FaxSendResponse</a></code>

# Employers

Types:

```python
from bluehive.types import EmployerCreateResponse, EmployerRetrieveResponse, EmployerListResponse
```

Methods:

- <code title="post /v1/employers">client.employers.<a href="./src/bluehive/resources/employers/employers.py">create</a>(\*\*<a href="src/bluehive/types/employer_create_params.py">params</a>) -> <a href="./src/bluehive/types/employer_create_response.py">EmployerCreateResponse</a></code>
- <code title="get /v1/employers/{employerId}">client.employers.<a href="./src/bluehive/resources/employers/employers.py">retrieve</a>(employer_id) -> <a href="./src/bluehive/types/employer_retrieve_response.py">EmployerRetrieveResponse</a></code>
- <code title="get /v1/employers/list">client.employers.<a href="./src/bluehive/resources/employers/employers.py">list</a>() -> <a href="./src/bluehive/types/employer_list_response.py">EmployerListResponse</a></code>

## ServiceBundles

Types:

```python
from bluehive.types.employers import (
    ServiceBundleCreateResponse,
    ServiceBundleRetrieveResponse,
    ServiceBundleUpdateResponse,
    ServiceBundleListResponse,
)
```

Methods:

- <code title="post /v1/employers/{employerId}/service-bundles">client.employers.service_bundles.<a href="./src/bluehive/resources/employers/service_bundles.py">create</a>(employer_id, \*\*<a href="src/bluehive/types/employers/service_bundle_create_params.py">params</a>) -> <a href="./src/bluehive/types/employers/service_bundle_create_response.py">ServiceBundleCreateResponse</a></code>
- <code title="get /v1/employers/{employerId}/service-bundles/{id}">client.employers.service_bundles.<a href="./src/bluehive/resources/employers/service_bundles.py">retrieve</a>(id, \*, employer_id) -> <a href="./src/bluehive/types/employers/service_bundle_retrieve_response.py">ServiceBundleRetrieveResponse</a></code>
- <code title="put /v1/employers/{employerId}/service-bundles/{id}">client.employers.service_bundles.<a href="./src/bluehive/resources/employers/service_bundles.py">update</a>(id, \*, employer_id, \*\*<a href="src/bluehive/types/employers/service_bundle_update_params.py">params</a>) -> <a href="./src/bluehive/types/employers/service_bundle_update_response.py">ServiceBundleUpdateResponse</a></code>
- <code title="get /v1/employers/{employerId}/service-bundles">client.employers.service_bundles.<a href="./src/bluehive/resources/employers/service_bundles.py">list</a>(employer_id) -> <a href="./src/bluehive/types/employers/service_bundle_list_response.py">ServiceBundleListResponse</a></code>
- <code title="delete /v1/employers/{employerId}/service-bundles/{id}">client.employers.service_bundles.<a href="./src/bluehive/resources/employers/service_bundles.py">delete</a>(id, \*, employer_id) -> None</code>

# Hl7

Types:

```python
from bluehive.types import Hl7SendResultsResponse
```

Methods:

- <code title="post /v1/hl7/results">client.hl7.<a href="./src/bluehive/resources/hl7.py">send_results</a>(\*\*<a href="src/bluehive/types/hl7_send_results_params.py">params</a>) -> str</code>

# Orders

Types:

```python
from bluehive.types import (
    OrderCreateResponse,
    OrderRetrieveResponse,
    OrderUpdateResponse,
    OrderRetrieveResultsResponse,
    OrderScheduleAppointmentResponse,
    OrderSendForEmployeeResponse,
    OrderUpdateStatusResponse,
    OrderUploadResultsResponse,
)
```

Methods:

- <code title="post /v1/orders">client.orders.<a href="./src/bluehive/resources/orders.py">create</a>(\*\*<a href="src/bluehive/types/order_create_params.py">params</a>) -> <a href="./src/bluehive/types/order_create_response.py">OrderCreateResponse</a></code>
- <code title="get /v1/orders/{orderId}">client.orders.<a href="./src/bluehive/resources/orders.py">retrieve</a>(order_id) -> <a href="./src/bluehive/types/order_retrieve_response.py">OrderRetrieveResponse</a></code>
- <code title="post /v1/orders/{orderId}">client.orders.<a href="./src/bluehive/resources/orders.py">update</a>(order_id, \*\*<a href="src/bluehive/types/order_update_params.py">params</a>) -> <a href="./src/bluehive/types/order_update_response.py">OrderUpdateResponse</a></code>
- <code title="get /v1/orders/{orderId}/results">client.orders.<a href="./src/bluehive/resources/orders.py">retrieve_results</a>(order_id, \*\*<a href="src/bluehive/types/order_retrieve_results_params.py">params</a>) -> <a href="./src/bluehive/types/order_retrieve_results_response.py">OrderRetrieveResultsResponse</a></code>
- <code title="post /v1/orders/{orderId}/schedule-appointment">client.orders.<a href="./src/bluehive/resources/orders.py">schedule_appointment</a>(order_id, \*\*<a href="src/bluehive/types/order_schedule_appointment_params.py">params</a>) -> <a href="./src/bluehive/types/order_schedule_appointment_response.py">OrderScheduleAppointmentResponse</a></code>
- <code title="post /v1/orders/send">client.orders.<a href="./src/bluehive/resources/orders.py">send_for_employee</a>(\*\*<a href="src/bluehive/types/order_send_for_employee_params.py">params</a>) -> <a href="./src/bluehive/types/order_send_for_employee_response.py">OrderSendForEmployeeResponse</a></code>
- <code title="put /v1/orders/{orderId}/status">client.orders.<a href="./src/bluehive/resources/orders.py">update_status</a>(order_id, \*\*<a href="src/bluehive/types/order_update_status_params.py">params</a>) -> <a href="./src/bluehive/types/order_update_status_response.py">OrderUpdateStatusResponse</a></code>
- <code title="post /v1/orders/{orderId}/upload-results">client.orders.<a href="./src/bluehive/resources/orders.py">upload_results</a>(order_id, \*\*<a href="src/bluehive/types/order_upload_results_params.py">params</a>) -> <a href="./src/bluehive/types/order_upload_results_response.py">OrderUploadResultsResponse</a></code>

# Employees

Types:

```python
from bluehive.types import (
    EmployeeCreateResponse,
    EmployeeRetrieveResponse,
    EmployeeUpdateResponse,
    EmployeeListResponse,
    EmployeeDeleteResponse,
    EmployeeLinkUserResponse,
    EmployeeUnlinkUserResponse,
)
```

Methods:

- <code title="post /v1/employees">client.employees.<a href="./src/bluehive/resources/employees.py">create</a>(\*\*<a href="src/bluehive/types/employee_create_params.py">params</a>) -> <a href="./src/bluehive/types/employee_create_response.py">EmployeeCreateResponse</a></code>
- <code title="get /v1/employees/{employeeId}">client.employees.<a href="./src/bluehive/resources/employees.py">retrieve</a>(employee_id) -> <a href="./src/bluehive/types/employee_retrieve_response.py">EmployeeRetrieveResponse</a></code>
- <code title="put /v1/employees">client.employees.<a href="./src/bluehive/resources/employees.py">update</a>(\*\*<a href="src/bluehive/types/employee_update_params.py">params</a>) -> <a href="./src/bluehive/types/employee_update_response.py">EmployeeUpdateResponse</a></code>
- <code title="get /v1/employees">client.employees.<a href="./src/bluehive/resources/employees.py">list</a>(\*\*<a href="src/bluehive/types/employee_list_params.py">params</a>) -> <a href="./src/bluehive/types/employee_list_response.py">EmployeeListResponse</a></code>
- <code title="delete /v1/employees/{employeeId}">client.employees.<a href="./src/bluehive/resources/employees.py">delete</a>(employee_id) -> <a href="./src/bluehive/types/employee_delete_response.py">EmployeeDeleteResponse</a></code>
- <code title="post /v1/employees/link-user">client.employees.<a href="./src/bluehive/resources/employees.py">link_user</a>(\*\*<a href="src/bluehive/types/employee_link_user_params.py">params</a>) -> <a href="./src/bluehive/types/employee_link_user_response.py">EmployeeLinkUserResponse</a></code>
- <code title="delete /v1/employees/unlink-user">client.employees.<a href="./src/bluehive/resources/employees.py">unlink_user</a>(\*\*<a href="src/bluehive/types/employee_unlink_user_params.py">params</a>) -> <a href="./src/bluehive/types/employee_unlink_user_response.py">EmployeeUnlinkUserResponse</a></code>

# Integrations

Types:

```python
from bluehive.types import IntegrationListResponse, IntegrationCheckActiveResponse
```

Methods:

- <code title="get /v1/integrations">client.integrations.<a href="./src/bluehive/resources/integrations.py">list</a>() -> <a href="./src/bluehive/types/integration_list_response.py">IntegrationListResponse</a></code>
- <code title="get /v1/integrations/{name}">client.integrations.<a href="./src/bluehive/resources/integrations.py">check_active</a>(name) -> <a href="./src/bluehive/types/integration_check_active_response.py">IntegrationCheckActiveResponse</a></code>
