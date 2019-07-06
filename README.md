#### **_Monitors services status from HTML page_**

#### Features

- Parses HTTP response content for services and their status

- Checks each service for status `OK` otherwise returns non 0

- Lists multiple downed services before exit status

- Returns 0 when all services are `OK`

- Validates inputs based on expected content formatting

#### Endpoint response content requirements

- Services must be separated by `<br />`
- Each service and its status must be delimited by `:`

#### Usage
Pass services status endpoint as first argument to the script

```bash
./check_services.py <endpoint>
```
