from collections.abc import Iterable

from bson import ObjectId
from pymongo.database import Database


class ScenarioBuilder:
    def __init__(self, db: Database, templates: dict[str, dict]):
        """Initialize the ScenarioBuilder with a MongoDB database and templates.
        Args:
            db: The MongoDB database instance.
            templates: A dictionary of templates to be used as blueprints for creating documents.
            The keys are collection names and the values are the template documents.
            We also create the collections in the database.
        """
        self._db = db
        self._templates = templates
        self._init_collections()

    def create(
        self, scenario: dict[str, Iterable[dict]], add_scenario_id=False
    ) -> Iterable[tuple[str, list[ObjectId]]]:
        """Create a scenario with the given steps.
        The scenario is a dictionary where keys are collection names
        and values are iterables of documents to insert into those collections."""
        scenario_id = ObjectId()
        scenario_doc = {"scenario_id": scenario_id} if add_scenario_id else {}
        for collection_name, docs in scenario.items():
            collection = self._db[collection_name]
            template = self._templates.get(collection_name, {})
            docs_to_insert = [template | doc | scenario_doc for doc in docs]
            result = collection.insert_many(
                docs_to_insert, comment=f"ScenarioBuilder {scenario_id}"
            )
            if len(result.inserted_ids) != len(docs_to_insert):
                raise ValueError("Failed to insert all documents")

            yield collection_name, result.inserted_ids

    def _init_collections(self) -> Iterable[dict]:
        """Register templates in the database.
        The templates is a dictionary where keys are collection names
        and values are iterables of documents to insert into those collections."""
        for collection_name in self._templates:
            self._db.create_collection(collection_name, check_exists=False)

    @property
    def collections(self) -> Iterable[str]:
        """Return the collection names managed by this ScenarioBuilder."""
        return self._templates.keys()

    def cleanup_collections(self):
        """Clear all collections managed by this ScenarioBuilder."""
        for name in self.collections:
            self._db[name].delete_many({})
