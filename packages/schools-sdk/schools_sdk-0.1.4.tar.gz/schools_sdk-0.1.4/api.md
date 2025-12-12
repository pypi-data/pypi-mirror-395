# Health

Types:

```python
from schools.types import HealthCheckResponse
```

Methods:

- <code title="get /health">client.health.<a href="./src/schools/resources/health.py">check</a>() -> <a href="./src/schools/types/health_check_response.py">HealthCheckResponse</a></code>

# Root

Types:

```python
from schools.types import RootRetrieveResponse
```

Methods:

- <code title="get /">client.root.<a href="./src/schools/resources/root.py">retrieve</a>() -> <a href="./src/schools/types/root_retrieve_response.py">RootRetrieveResponse</a></code>

# Schools

Types:

```python
from schools.types import SchoolRetrieveResponse, SchoolListResponse, SchoolSearchResponse
```

Methods:

- <code title="get /v1/schools/id/{schoolId}">client.schools.<a href="./src/schools/resources/schools.py">retrieve</a>(school_id) -> <a href="./src/schools/types/school_retrieve_response.py">SchoolRetrieveResponse</a></code>
- <code title="get /v1/schools">client.schools.<a href="./src/schools/resources/schools.py">list</a>(\*\*<a href="src/schools/types/school_list_params.py">params</a>) -> <a href="./src/schools/types/school_list_response.py">SchoolListResponse</a></code>
- <code title="get /v1/schools/authority/{authority}">client.schools.<a href="./src/schools/resources/schools.py">by_authority</a>(authority, \*\*<a href="src/schools/types/school_by_authority_params.py">params</a>) -> None</code>
- <code title="get /v1/schools/city/{city}">client.schools.<a href="./src/schools/resources/schools.py">by_city</a>(city, \*\*<a href="src/schools/types/school_by_city_params.py">params</a>) -> None</code>
- <code title="get /v1/schools/status/{status}">client.schools.<a href="./src/schools/resources/schools.py">by_status</a>(status, \*\*<a href="src/schools/types/school_by_status_params.py">params</a>) -> None</code>
- <code title="get /v1/schools/suburb/{suburb}">client.schools.<a href="./src/schools/resources/schools.py">by_suburb</a>(suburb, \*\*<a href="src/schools/types/school_by_suburb_params.py">params</a>) -> None</code>
- <code title="get /v1/schools/search">client.schools.<a href="./src/schools/resources/schools.py">search</a>(\*\*<a href="src/schools/types/school_search_params.py">params</a>) -> <a href="./src/schools/types/school_search_response.py">SchoolSearchResponse</a></code>

# Sync

Types:

```python
from schools.types import SyncGetStatusResponse, SyncTriggerResponse
```

Methods:

- <code title="get /v1/sync/status">client.sync.<a href="./src/schools/resources/sync.py">get_status</a>() -> <a href="./src/schools/types/sync_get_status_response.py">SyncGetStatusResponse</a></code>
- <code title="post /v1/sync">client.sync.<a href="./src/schools/resources/sync.py">trigger</a>() -> <a href="./src/schools/types/sync_trigger_response.py">SyncTriggerResponse</a></code>
