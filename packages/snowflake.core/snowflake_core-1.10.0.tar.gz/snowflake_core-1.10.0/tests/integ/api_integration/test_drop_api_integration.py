import pytest

from snowflake.core.api_integration import ApiIntegration, GitHook
from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string


def test_drop(api_integrations):
    ai_name = random_string(10, "test_api_integration_drop_")
    ai_def = ApiIntegration(
        name=ai_name,
        api_hook=GitHook(),
        api_allowed_prefixes=["https://github.com"],
        enabled=True,
        comment="created by test_drop",
    )
    ai = api_integrations.create(ai_def)
    ai.drop()
    with pytest.raises(NotFoundError):
        ai.fetch()
    ai.drop(if_exists=True)
