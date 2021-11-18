"""Test Jira service"""
import os

import pytest
from _pytest.fixtures import pytest_fixture_setup

from app.config.service import Config
from app.jira.service import JiraService

TEST_CONFIG = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "config", "config-test.json"
)


@pytest.fixture(scope="function")
def config_e2e() -> Config:
    """Real config located at config-test.json.

    :returns: config
    """
    config_path = TEST_CONFIG
    config = Config.from_file(config_path)
    return config


@pytest.fixture(scope="function")
def jira_e2e_service(config_e2e: Config) -> JiraService:
    """Real Jira service.

    :returns: connectd to Jira service
    """
    service = JiraService(url=config_e2e.jira.url, token=config_e2e.jira.token)
    return service


class TestJiraServiceE2E:
    """Test Jira service."""

    @pytest.mark.skipif(not os.path.exists(TEST_CONFIG), reason="Not test config found")
    def test_find1(self, jira_e2e_service: JiraService) -> None:
        """Test by period."""
        actual = jira_e2e_service.find(period="day")
        assert actual[0]

    @pytest.mark.skipif(not os.path.exists(TEST_CONFIG), reason="Not test config found")
    def test_find2(self, jira_e2e_service: JiraService, config_e2e: Config) -> None:
        """Test by assignee."""
        actual = jira_e2e_service.find(assignee=config_e2e.jira.user, period="Month")
        assert actual[0]
