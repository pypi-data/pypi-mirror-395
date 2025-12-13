"""Client session for JSM Assets API interactions."""
from __future__ import annotations
from typing import Self
import requests
from .util import logger


class AssetSession:
    """Client session for a JSM Assets workspace.

    The session encapsulates authentication and provides convenience accessors
    for top-level resources such as object schemas, icons and status types.
    """

    def __init__(self, email: str, api_token: str, jira_site_url: str, api_version: str = "v1") -> Self:
        """Create a new AssetSession and initialize connection parameters.

        Args:
            email (str): Email address used for API authentication.
            api_token (str): API token associated with `email`.
            jira_site_url (str): Base URL of the JSM instance (e.g. https://your.atlassian.net).
            api_version (str): API version to target (defaults to "v1").
        """
        self.email = email
        self.__auth = requests.auth.HTTPBasicAuth(email, api_token)
        self.api_user = self.email
        self.jira_site_url = jira_site_url
        self.workspace = None
        self.http_timeout = 30  # seconds
        try:
            # get_workspace_id is a module-level helper defined below (not a method)
            self.workspace = get_workspace_id(jira_site_url, self.__auth)
        except Exception:
            logger.exception('Failed to retrieve workspace id during session init')
        self.asset_api_url = f"https://api.atlassian.com/jsm/assets/workspace/{self.workspace}/{api_version}"

        # cached properties
        self._schemas = None
        self._icons = None
        self._statustypes = None

    def __str__(self):
        return self.asset_api_url

    def __repr__(self):
        return f'JSMAsset: {self.asset_api_url} ({self.jira_site_url.split(".")})'

    @property
    def schemas(self) -> dict:
        """Return a mapping of schema id -> :class:`AssetSchema`.

        The mapping is lazily loaded from the Assets API on first access.
        """
        if self._schemas is None:
            response = self.api_request('get', '/objectschema/list')
            if response.status_code == 200:
                # import lazily to avoid cycle
                from .schema import AssetSchema
                self._schemas = {x['id']: AssetSchema(self, x['id'], object_data=x) for x in response.json().get('values', [])}
        return self._schemas

    @property
    def icons(self) -> dict:
        """Return cached icon metadata keyed by icon id.

        Icons are fetched from the API on first access and cached on the
        session instance.
        """
        if self._icons is None:
            response = self.api_request('get', '/icon/global')
            if response.status_code == 200:
                self._icons = {x['id']: x for x in response.json()}
        return self._icons

    @property
    def statustypes(self) -> dict:
        """Return status type metadata keyed by id.

        Cached on first access.
        """
        if self._statustypes is None:
            response = self.api_request('get', '/config/statustype')
            if response.status_code == 200:
                self._statustypes = {x['id']: x for x in response.json()}
        return self._statustypes

    def api_request(self, method: str = "get", path: str = "", data: dict = None, params: dict = None) -> requests.Request:
        """Perform an HTTP request against the Assets API.

        Args:
            method (str): HTTP method (GET/POST/PUT/DELETE).
            path (str): API path to append to the session's base URL.
            data (dict, optional): JSON body to send.
            params (dict, optional): Query parameters.

        Returns:
            requests.Response: The HTTP response object.

        Notes:
            This method raises in the case of an HTTP error by calling
            ``raise_for_status`` on the response; callers may catch
            requests exceptions as needed.
        """
        path = f'{self.asset_api_url}' + f'{path}'
        logger.debug('%s, json=%s, params=%s', path, data, params)
        try:
            r = requests.request(method.upper(), path.lower(), json=data, params=params, auth=self.__auth, timeout=self.http_timeout)
            logger.info('API request %s %s returned status code %s', method.upper(), path, r.status_code)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as e:
            logger.error('API request %s %s failed with error: %s', method.upper(), path, e.response.text)
            return r
        except requests.exceptions.JSONDecodeError as e:
            logger.error('API request %s %s failed to decode JSON: %s', method.upper(), path, e.msg)
            return e.msg

    def aql_query(self, query: str):
        """Create an :class:`AQLQuery` builder for the given query string.

        Args:
            query (str): The AQL query string.

        Returns:
            AQLQuery: A query helper bound to this session.
        """
        # lazy import to avoid circular imports
        from .aql import AQLQuery
        return AQLQuery(self, query)

    def create_schema(self, name: str, object_schema_key: str, description: str = None):
        """Create a new Asset schema.

        Args:
            name (str): The human-readable name for the schema.
            object_schema_key (str): The unique schema key.
            description (str, optional): Free-text description.

        Returns:
            AssetSchema: The created schema on success, or ``None`` on failure.
        """
        data = {
            'name': name,
            'objectSchemaKey': object_schema_key,
            'description': description,
        }
        response = self.api_request('post', '/objectschema/create', data=data)
        if response.status_code == 201:
            from .schema import AssetSchema
            data = response.json()
            new_schema = AssetSchema(self, data['id'], object_data=data)
            if self.schemas is None:
                self._schemas = {}
            self.schemas[new_schema.id] = new_schema
            logger.info('Created new AssetSchema %s with id %s', name, new_schema.id)
            return new_schema
        else:
            logger.error('Attempt to create AssetSchema %s failed.', name)
            return None

    def get_object_by_id(self, object_id):
        """Retrieve a single object by id and return an :class:`AssetObject`.

        Args:
            object_id (int|str): The id of the object to retrieve.

        Returns:
            AssetObject: The requested object on success, or ``None`` on
                failure.
        """
        response = self.api_request('get', f'/object/{object_id}')
        if response.status_code == 200:
            data = response.json()
            schema_id = data['objectType']['objectSchemaId']
            type_id = data['objectType']['id']
            from .schema import AssetSchema, AssetObjectType
            from .object import AssetObject
            if schema_id in (self.schemas or {}):
                schema = self.schemas[schema_id]
            else:
                schema = AssetSchema(self, schema_id)
                if self.schemas is None:
                    self._schemas = {}
                self.schemas[schema_id] = schema
            if type_id in schema.object_types:
                obj_type = schema.object_types[type_id]
            else:
                obj_type = AssetObjectType(schema, type_id)
                schema.object_types[type_id] = obj_type
            return AssetObject(schema, type_id, object_id=object_id, object_data=data)
        else:
            logger.error('Attempt to retrieve AssetObject %s failed.', object_id)
            return None


# session-level helper functions (kept here for cohesion)
def get_workspace_id(jira_instance_url, auth):
    """Retrieve the workspace id for a JSM instance.

    Args:
        jira_instance_url (str): The base URL of the JSM instance.
        auth: requests-compatible auth object to use for the request.

    Returns:
        str: The workspace id string returned by the instance.

    Raises:
        requests.exceptions.HTTPError: If the request fails.
    """
    try:
        r = requests.request("get", f'{jira_instance_url}/rest/servicedeskapi/insight/workspace', auth=auth, timeout=30)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error('Attempting to get workspace ID failed with error: %s', e.response.text)
        raise
    return r.json()["values"][0]["workspaceId"]


def get_org_id(jira_instance_url):
    """Return the cloud organization id for the given instance.

    Args:
        jira_instance_url (str): The base JSM URL.

    Returns:
        str: The cloud/organization id.

    Raises:
        requests.exceptions.HTTPError: If the request fails.
    """
    try:
        r = requests.request("get", f'{jira_instance_url}/_edge/tenant_info', timeout=30)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error('Attempting to get org ID failed with error: %s', e.response.text)
        raise
    return r.json()["cloudId"]


def resolve_team_id(jira_session, team_id):
    """Resolve a human-readable team id to the canonical name via the API.

    Args:
        jira_session (AssetSession): Session used to make the request.
        team_id (str): The team identifier to resolve.

    Returns:
        str|None: The resolved team name, or None on error.
    """
    try:
        response = jira_session.api_request("get", f'/rest/api/2/group?groupname={team_id}')
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.error('Attempting to resolve team ID failed with error: %s', e.response.text)
        return None
    return response.json()["name"]
