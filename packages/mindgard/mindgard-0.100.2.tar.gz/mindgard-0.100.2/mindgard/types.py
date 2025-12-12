# Standard library imports
from dataclasses import dataclass
from typing import Any, Callable, Dict, Literal, Optional, Tuple, get_args

# Third party imports
import requests
from rich.progress import Progress, TaskID
from rich.table import Table


@dataclass
class ExceptionCountTuple:
    task_id: TaskID
    count: int


# Web pub sub message types
type_wps_message_type = Literal["StartTest", "StartedTest", "Response", "Request"]

# UI task map stores a name for a task along with its taskid to be updated in progress object
type_ui_task_map = Dict[str, TaskID]
# Stores an exception message with the task to update, and the number of times the exception has been thrown
type_ui_exception_map = Dict[str, ExceptionCountTuple]

# interfaces that submit, polling and output functions MUST MEET to be usable in run_poll_display.
type_submit_func = Callable[[str, type_ui_exception_map, Progress], Any]
type_polling_func = Callable[
    [str, Any, type_ui_task_map, Progress],
    Optional[Any],
]
type_output_func = Callable[[Any, bool], Optional[Table]]

# Orchestrator submit/request enums
type_orchestrator_attack_pack = Literal["sandbox", "threat_intel"]
type_orchestrator_source = Literal["threat_intel", "user", "mindgard"]
type_model_presets = Literal[
    "huggingface-openai",
    "openai-compatible",
    "huggingface",
    "openai",
    "azure-openai",
    "azure-aistudio",
    "anthropic",
    "tester",
    "local",
]
type_model_presets_list: Tuple[type_model_presets, ...] = get_args(type_model_presets)

# Types for dependency injecting get/post request functions into over api_post and api_get in orchestrator
type_post_request_function = Callable[[str, str, Dict[str, Any]], requests.Response]
type_get_request_function = Callable[[str, str], requests.Response]

# Different log levels
log_levels = [
    "critical",
    "fatal",
    "error",
    "warn",
    "warning",
    "info",
    "debug",
    "notset",
]  # [n.lower() for n in logging.getLevelNamesMapping().keys()]

valid_llm_datasets = {
    "customerservice": "BadCustomer",
    "finance": "BadFinance",
    "legal": "BadLegal",
    "medical": "BadMedical",
    "injection": "SqlInjection",
    "rce": "Xss",
    "xss": "Xss",
    "bypass.deepset": "GuardrailBypassDeepset",
    "bypass.llmguard": "GuardrailBypassLlmGuard",
    "bypass.metapromptguardv1": "GuardrailBypassMetaPromptGuardV1",
    "bypass.protectaiv1": "GuardrailBypassProtectAiV1",
    "bypass.protectaiv2": "GuardrailBypassProtectAiV2",
    "bypass.vijilpromptinjection": "GuardrailBypassVijilPromptInjection",
    "toxicity": "Toxicity",
    "toxicity.discrimination": "ToxicityDiscrimination",
    "toxicity.harassment": "ToxicityHarassment",
    "toxicity.hate_speech": "ToxicityHateSpeech",
    "toxicity.profanity": "ToxicityProfanity",
    "information_disorder": "InformationDisorder",
    "information_disorder.disinformation": "InformationDisorderDisinformation",
    "information_disorder.misinformation": "InformationDisorderMisinformation",
    "cybersecurity": "Cybersecurity",
    "cybersecurity.cloud_attacks": "CybersecurityCloudAttacks",
    "cybersecurity.control_system_attacks": "CybersecurityControlSystemAttacks",
    "cybersecurity.cryptographic_attacks": "CybersecurityCryptographicAttacks",
    "cybersecurity.cyber_crime": "CybersecurityCyberCrime",
    "cybersecurity.evasion_techniques": "CybersecurityEvasionTechniques",
    "cybersecurity.hardware_attacks": "CybersecurityHardwareAttacks",
    "cybersecurity.intrusion_techniques": "CybersecurityIntrusionTechniques",
    "cybersecurity.iot_attacks": "CybersecurityIotAttacks",
    "cybersecurity.malware_attacks": "CybersecurityMalwareAttacks",
    "cybersecurity.network_attacks": "CybersecurityNetworkAttacks",
    "cybersecurity.web_application_attacks": "CybersecurityWebApplicationAttacks",
    "business_risk": "BusinessRisk",
    "business_risk.copyright": "BusinessRiskCopyright",
    "business_risk.pii": "BusinessRiskPii",
    "harmful": "Harmful",
    "harmful.dangerous_content": "HarmfulDangerousContent",
    "harmful.illegal": "HarmfulIllegal",
    "harmful.self_harm": "HarmfulSelfHarm",
    "harmful.sexually_explicit": "HarmfulSexuallyExplicit",
    "harmful.violence": "HarmfulViolence",
}
