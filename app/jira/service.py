"""Service to operate with Jira"""

import base64
import logging
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.api import request

_LOG = logging.getLogger(__name__)


class JiraService:
    """Jira service with a common set of methods to operate with issues."""

    def __init__(self, url: str, token: str) -> None:
        """
        :param url: Jira base URL
        :param user: Jira user
        :param password: Jira password
        """
        self._url = url
        self._token = token

    def find(
        self, assignee: Optional[str] = None, period: Optional[str] = None
    ) -> Tuple[int, List[str]]:
        """Find all issues defined by criteries.

        :param assignee: issue assignee
        :param period: only issues update in period: month, year, day, week
        :returns: ok? and list of issues
        """
        # Construct params.
        params = {"fields": "key,summary"}
        jql = []
        if assignee:
            jql.append('assignee="%s"' % assignee)
        if period:
            jql.append("updated>=startOf%s()" % period.capitalize())
        if jql:
            params["jql"] = " and ".join(jql)

        max_results = 10
        total = 10 ^ 8
        results = []
        processed = 0
        # Process by batches.
        while processed < total:
            params["startAt"] = processed
            params["maxResults"] = max_results
            response = requests.get(
                **self._request_params(request="search", params=params)
            )
            if response.status_code != 200:
                return False, results
            data = response.json()
            total = data["total"]
            results.extend(
                [
                    "%s: %s" % (item["key"], item["fields"]["summary"])
                    for item in data["issues"]
                ]
            )
            processed = len(results)
            _LOG.debug("Processed %s/%s issues" % (processed, total))
        # Return results.
        return True, results

    def _request_params(
        self,
        request: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Construct dict with request parameters.

        :param request: endpoint
        :param headers: non-trivial headers
        :param params: request params
        :param data: request data
        :returns: dict of request parameters"""
        # Construct headers.
        headers_to_send = {
            "Content-Type": "application/json",
            "Authorization": "Basic %s" % self._token,
        }
        if headers:
            headers_to_send.update(headers)
        # Construct URL.
        url = "%s/%s" % (self._url, request)
        # Construct kwargs.
        kwargs = dict(url=url, headers=headers_to_send, params=params, data=data,)
        return kwargs
