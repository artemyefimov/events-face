import requests
from requests.adapters import HTTPAdapter, Retry


class NotificationClient:
    def __init__(self, api_url, access_token, owner_id):
        self._api_url = api_url
        self._owner_id = owner_id
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

    def send_notification(self, id, message, email):
        response = self._session.post(
            self._api_url,
            json={
                "id": id,
                "message": message,
                "email": email,
                "owner_id": self._owner_id,
            },
            timeout=self._timeout,
        )
        response.raise_for_status()
        return response.json()
