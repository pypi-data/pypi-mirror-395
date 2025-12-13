import os

import pytest
from pymongo import MongoClient
from pymongo.database import Database

from pytest_scenarios.scenario import ScenarioBuilder
from pytest_scenarios.template_loader import load_templates_from_path


def _option_to_env_var_name(name: str) -> str:
    return name.upper().replace("-", "_")


def _get_option(
    request: pytest.FixtureRequest, name: str, default: str | None = None
) -> str | None:
    """Resolve configuration value from CLI, environment, pytest.ini, or default."""
    value = request.config.getoption(
        f"--{name}",
        default=request.config.getini(name),
    )

    print(f"Using {name}={value}")
    return value


def _register_options(group: pytest.OptionGroup, name: str, default: str, help: str) -> None:
    env_var_name = _option_to_env_var_name(name)
    default_from_env = os.getenv(env_var_name, default=default)
    group.addoption(
        f"--{name}",
        action="store",
        dest=env_var_name.lower(),
        default=default_from_env,
        help=help,
    )
    group.parser.addini(
        name=name,
        help=help,
        default=default_from_env,
        type="string",
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register pytest-scenarios custom command line and ini options."""

    group = parser.getgroup("pytest-scenarios")
    _register_options(
        group,
        name="templates-path",
        default="tests/templates",
        help="Directory containing template modules for pytest-scenarios",
    )
    _register_options(
        group,
        name="db-name",
        default="test_db",
        help="Database name used by pytest-scenarios fixtures",
    )
    _register_options(
        group,
        name="db-url",
        default="mongodb://127.0.0.1:27017",
        help="MongoDB connection string used by pytest-scenarios fixtures",
    )


@pytest.fixture(scope="session")
def templates_path(request: pytest.FixtureRequest):
    return _get_option(request, "templates-path", default="tests/templates")


@pytest.fixture(scope="session")
def mongo_client(request: pytest.FixtureRequest):
    db_url = _get_option(request, "db-url", default="mongodb://127.0.0.1:27017")
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
