from googleapiclient.discovery import Resource
import logging

def execute_request(service: Resource, site_url: str, request_body: dict) -> dict:
    """
    Executes a Search Analytics API request using the provided service object.

    Args:
        service (Resource): Authenticated GSC API service.
        site_url (str): The URL of the site (e.g. 'sc-domain:example.com').
        request_body (dict): Body of the request with startDate, endDate, dimensions, etc.

    Returns:
        dict: API response containing search analytics data.
    """
    try:
        response = service.searchanalytics().query(
            siteUrl=site_url,
            body=request_body
        ).execute()
        return response
    except Exception as e:
        logging.error(f"❌ GSC API request failed: {e}")
        return {}