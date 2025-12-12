import json
from typing import Optional, cast
import backoff
import requests

from arcane.core import BaseAccount, BadRequestError
from arcane.datastore import Client as DatastoreClient

from .const import TIKTOK_SERVER_URL
from .exceptions import TikTokAuthError, TikTokApiError
from .lib import get_tiktok_account, get_tikok_user_credentials

class TiktokClient:
    def __init__(
        self,
        gcp_service_account: str,
        base_account: Optional[BaseAccount] = None,
        user_email: Optional[str] = None,
        clients_service_url: Optional[str] = None,
        firebase_api_key: Optional[str] = None,
        gcp_credentials_path: Optional[str] = None,
        datastore_client: Optional[DatastoreClient] = None,
        gcp_project: Optional[str] = None,
        auth_enabled: bool = True
    ) -> None:

        creator_email = None

        if gcp_service_account and (base_account or user_email):
            if user_email:
                creator_email = user_email
            else:
                base_account = cast(BaseAccount, base_account)
                tiktok_account = get_tiktok_account(
                    base_account=base_account,
                    clients_service_url=clients_service_url,
                    firebase_api_key=firebase_api_key,
                    gcp_service_account=gcp_service_account,
                    auth_enabled=auth_enabled
                )

                creator_email = cast(str, tiktok_account['creator_email'])

            if creator_email is None:
                raise BadRequestError('creator_email should not be None while using user access protocol')

            credentials = get_tikok_user_credentials(
                user_email=creator_email,
                gcp_credentials_path=gcp_credentials_path,
                gcp_project=gcp_project,
                datastore_client=datastore_client
            )

            self._access_token = credentials['access_token']
        else:
            raise BadRequestError('gcp_service_account and (base_account or user_email) should be provided to initialize TiktokClient')


    @backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=5)
    def _make_request(self, endpoint: str, method: str, params: Optional[dict] = None, headers: Optional[dict] = None, **kwargs) -> dict:
        """Send a request to TikTok API"""

        default_headers = {"Access-Token": self._access_token}
        if headers:
            default_headers.update(headers)

        response = requests.request(method=method, url=f"{TIKTOK_SERVER_URL}{endpoint}", headers=default_headers, params=params, **kwargs)
        response.raise_for_status()

        response = response.json()
        # tiktok return error codes in 200 HTTP responses
        api_code = response.get('code')
        if api_code != 0:
            if api_code in [40104, 40105, 40106]:
                raise TikTokAuthError(f"{response.get('message')}")
            raise TikTokApiError(f"{response.get('message')}")

        return response.get('data', {})

    def get_advertiser_info(self, advertiser_ids: list[str]) -> dict:
        """Get advertiser info"""
        params = {"advertiser_ids": json.dumps(advertiser_ids)}

        response = self._make_request(
            endpoint="/advertiser/info/",
            method="GET",
            params=params
            )
        return response.get('list', {})

    def get_account_campaigns(self, advertiser_id: str) -> list[dict[str, str]]:
        """Get campaigns for an advertiser account"""
        page = 1
        campaigns = []
        while True:
            params = {
                "advertiser_id": advertiser_id,
                "page_size": 1000,
                "page": page,
                "fields": json.dumps(["campaign_id","campaign_name","operation_status"])
            }

            response = self._make_request(
                endpoint='/campaign/get/',
                method='GET',
                params=params
            )

            current_campaigns = response.get('list', [])
            total_page = response.get('page_info', {}).get('total_page', 1)

            if current_campaigns:
                campaigns.extend(current_campaigns)

            if page >= total_page:
                break
            page += 1

        return [{
            'id': campaign.get('campaign_id'),
            'name': campaign.get('campaign_name'),
            'status': campaign.get('operation_status')
        } for campaign in campaigns]
