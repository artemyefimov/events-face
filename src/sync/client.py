from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter, Retry


class EventsProviderClient:
    def __init__(self, api_url, access_token):
        self._api_url = api_url
        self._timeout = 10

        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            }
        )

        retry = Retry(
            total=3,
            status_forcelist=(408, 429, 500, 502, 503, 504),
            raise_on_status=False,
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)

    def _get(self, url, params=None):
        response = self._session.get(url, params=params, timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def _generate_events(self, *, changed_at=None):
        url = self._api_url
        params = {"changed_at": changed_at}

        next_url = url
        next_params = params

        while next_url:
            payload = self._get(next_url, next_params)

            results = payload["results"]
            for item in results:
                yield item

            next_url = payload.get("next")
            next_params = None

    def get_events(self, *, changed_at=None):
        return list(self._generate_events(changed_at=changed_at))
