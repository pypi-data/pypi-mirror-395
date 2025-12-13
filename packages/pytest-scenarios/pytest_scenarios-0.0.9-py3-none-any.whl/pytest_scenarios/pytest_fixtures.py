import os

import pytest
from pymongo import MongoClient
from pymongo.database import Database

from pytest_scenarios.scenario import ScenarioBuilder
from pytest_scenarios.template_loader import load_templates_from_path


def _get_option(request: pytest.FixtureRequest, name: str, default=None):
    value = request.config.getoption(
        f"--{name}", default=os.environ.get(name.upper().replace("-", "_"), default)
    )
    print(f"Using option {name}={value}")
    return value


@pytest.fixture(scope="session")
def templates_path(request: pytest.FixtureRequest):
    return _get_option(request, "templates-path", default="tests/templates")


@pytest.fixture(scope="session")
def mongo_client(request: pytest.FixtureRequest):
    db_url = _get_option(
        request, "db-url", default="mongodb://127.0.0.1:27017/?directConnection=true"
    )
    with MongoClient(db_url) as client:
        yield client


@pytest.fixture(scope="session")
def db(request: pytest.FixtureRequest, mongo_client: MongoClient):
    db_name = _get_option(request, "db-name", default="test_db")
    yield mongo_client[db_name]


@pytest.fixture(scope="session")
def scenario_builder(db: Database, templates_path: str) -> ScenarioBuilder:
    templates = load_templates_from_path(templates_path)
    return ScenarioBuilder(db, templates)


@pytest.fixture(scope="function", autouse=True)
def cleanup_database(scenario_builder: ScenarioBuilder):
    """Clear all collections in the database before each test function."""
    scenario_builder.cleanup_collections()
