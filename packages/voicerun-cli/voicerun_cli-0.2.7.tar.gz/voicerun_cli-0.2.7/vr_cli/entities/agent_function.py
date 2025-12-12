from .base import BaseEntity, BaseRepository
from ..utils.utils import is_uuid


class AgentFunction(BaseEntity):
    def __init__(
        self,
        id: str = None,
        agent_id: str = None,
        name: str = None,
        display_name: str = None,
        code: str = None,
        code_path: str = None,
        is_multifile: bool = False,
        language: str = "python",
        strategy: str = "cascade",
        test_data: dict = None,
        created_at: str = None,
        updated_at: str = None,
        deleted_at: str = None,
    ):
        self.id = id
        self.agent_id = agent_id
        self.name = name
        self.display_name = display_name
        self.code = code
        self.code_path = code_path
        self.is_multifile = is_multifile
        self.language = language
        self.strategy = strategy
        self.test_data = test_data
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at or None

    def get_display_name(self) -> str:
        """Get the display name for the function (display_name with fallback to name)"""
        return self.display_name or self.name


class AgentFunctionRepository(BaseRepository[AgentFunction]):
    def __init__(self, agent_id: str):
        super().__init__("agent", f"/v1/agents/{agent_id}/functions", AgentFunction)

    def get_by_name_or_id(self, name_or_id: str) -> AgentFunction:
        """
        Override to search by name, display_name, or ID.
        This allows functions to be found by their display name.
        """
        if is_uuid(name_or_id):
            return self.get_by_id(name_or_id)

        entities = self.get()
        for entity in entities:
            # Check both name and display_name fields
            if entity.name == name_or_id or entity.display_name == name_or_id:
                return entity

        return None
