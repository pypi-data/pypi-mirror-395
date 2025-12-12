from .base import BaseEntity, BaseRepository
from ..utils.utils import make_request


class AgentEnvironment(BaseEntity):
    def __init__(
        self,
        id: str = None,
        agent_id: str = None,
        name: str = None,
        function_id: str = None,
        phone_number: str = None,
        stt_model: str = "nova-3",
        stt_endpointing: int = 300,
        stt_language: str = "en",
        stt_prompt: str = "",
        recording_enabled: bool = False,
        redaction_enabled: bool = False,
        is_debug: bool = False,
        created_at: str = None,
        updated_at: str = None,
        deleted_at: str = None,
        # Additional API fields
        audio_input_delay: int = None,
        error_fallback_timeout_seconds: int = None,
        error_fallback_time_window_seconds: int = None,
        error_fallback_occurrence_threshold: int = None,
        error_fallback_type: str = None,
        error_fallback_value: str = None,
        stt_filter: str = None,
        stt_noise_reduction_type: str = None,
        stt_prewarm_model: bool = None,
        stt_auto_switch: bool = None,
        recording_location: str = None,
        eot_threshold: float = None,
        eot_timeout_ms: int = None,
        eager_eot_threshold: float = None,
        startup_audio_interruptible: bool = None,
        startup_audio_url: str = None,
        module_rule: str = None,
        vad_mode: str = None,
        vad_eagerness: str = None,
        ringing_enabled: bool = None,
    ):
        self.id = id
        self.agent_id = agent_id
        self.name = name
        self.function_id = function_id
        self.phone_number = phone_number
        self.stt_model = stt_model
        self.stt_endpointing = stt_endpointing
        self.stt_language = stt_language
        self.stt_prompt = stt_prompt
        self.recording_enabled = recording_enabled
        self.redaction_enabled = redaction_enabled
        self.is_debug = is_debug
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at or None
        # Additional API fields
        self.audio_input_delay = audio_input_delay
        self.error_fallback_timeout_seconds = error_fallback_timeout_seconds
        self.error_fallback_time_window_seconds = error_fallback_time_window_seconds
        self.error_fallback_occurrence_threshold = error_fallback_occurrence_threshold
        self.error_fallback_type = error_fallback_type
        self.error_fallback_value = error_fallback_value
        self.stt_filter = stt_filter
        self.stt_noise_reduction_type = stt_noise_reduction_type
        self.stt_prewarm_model = stt_prewarm_model
        self.stt_auto_switch = stt_auto_switch
        self.recording_location = recording_location
        self.eot_threshold = eot_threshold
        self.eot_timeout_ms = eot_timeout_ms
        self.eager_eot_threshold = eager_eot_threshold
        self.startup_audio_interruptible = startup_audio_interruptible
        self.startup_audio_url = startup_audio_url
        self.module_rule = module_rule
        self.vad_mode = vad_mode
        self.vad_eagerness = vad_eagerness
        self.ringing_enabled = ringing_enabled


class AgentEnvironmentRepository(BaseRepository[AgentEnvironment]):
    def __init__(self, agent_id: str):
        super().__init__(
            "agent", f"/v1/agents/{agent_id}/environments", AgentEnvironment
        )

    def get_debug_environment(self) -> AgentEnvironment:
        response = make_request(f"{self.endpoint}/debug")

        if response and "data" in response:
            return self._create_entity(response["data"])

        return None

    def configure_phone(self, environment_id: str, phone_number: str) -> AgentEnvironment:
        response = make_request(f"{self.endpoint}/{environment_id}/configure-phone", "POST", json={"phoneNumber": phone_number})
        if response and "data" in response:
            return self._create_entity(response["data"])
        return None