from __future__ import annotations
from typing import Self
from .util import logger


class AQLQuery:
    """A convenience class for working with the AQL language in JSM Asset.

    The implementation keeps network calls on the session object and lazily
    imports :class:`AssetObject` to avoid circular imports.
    """

    def __init__(self, jsm_asset_instance, query: str, start_index: int = 0,
                 results_per_page: int = 25, include_attributes: bool = True) -> Self:
        """Create an AQLQuery wrapper.

        Args:
            jsm_asset_instance (AssetSession): The active session to execute
                queries against.
            query (str): The AQL query string.
            start_index (int): The starting offset for results pagination.
            results_per_page (int): Number of results to request per page.
            include_attributes (bool): Whether to request attribute values.

        Attributes:
            session: The session object provided.
            query: The AQL query string.
            start_index: Pagination start index.
            results_per_page: Page size for AQL results.
            include_attributes: Whether attribute values are included in results.
        """
        self.session = jsm_asset_instance
        self.query = query
        self.start_index = start_index
        self.results_per_page = results_per_page
        self.include_attributes = include_attributes

        # cached
        self._results = None
        self._total_count = None

    def __str__(self):
        return str(self.query)

    def __repr__(self):
        return f'<AQLQuery: {self.query}>'

    @property
    def results(self):
        """Generator that yields :class:`AssetObject` instances matching the query.

        The property returns a generator which pages through the AQL results
        using the session's API. Each yielded item is an :class:`AssetObject`.

        Yields:
            AssetObject: The next matching object from the query results.
        """
        params = {
            'startAt': self.start_index,
            'maxResults': self.results_per_page,
            'includeAttributes': self.include_attributes,
        }
        while True:
            response = self.session.api_request(method="POST", path='/object/aql', data={'qlQuery': self.query}, params=params)
            if response.status_code != 200:
                logger.error('AQL query failed with status code %s', response.status_code)
                break
            data = response.json()
            # lazy import to avoid cycles
            from .object import AssetObject
            for item in data.get('values', []):
                yield AssetObject(self.session.schemas[item['objectType']['objectSchemaId']], item['objectType']['id'], object_data=item)
            if data.get('isLast') is False:
                params['startAt'] += self.results_per_page
            else:
                break

    @property
    def total_count(self):
        """Return total number of results for this query.

        The count is fetched from the API and cached on first access.

        Returns:
            int: The total number of matching objects, or ``None`` if the
                request failed.
        """
        if self._total_count is None:
            response = self.session.api_request(method='POST', path=f'/object/aql/totalcount', data={'qlQuery': self.query})
            if response.status_code != 200:
                logger.error('Failed to retrieve object count for query %s', self.query)
            else:
                self._total_count = response.json()['totalCount']
        return self._total_count
