from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Mapping, MutableMapping, Optional, TypedDict, Union

AgentInputFieldType = Literal["text", "textarea", "number", "select", "multi-select", "file"]


class AgentInputOption(TypedDict):
    label: str
    value: str


class AgentInputDefinition(TypedDict, total=False):
    id: str
    label: str
    type: AgentInputFieldType
    helperText: str
    required: bool
    placeholder: str
    options: List[Union[AgentInputOption, str]]
    maxFiles: int


class AgentIntegrationRequestPreview(TypedDict, total=False):
    method: str
    url: str
    headers: Dict[str, str]
    body: Dict[str, Any]


class AgentIntegrationWebhookPreview(TypedDict, total=False):
    url: str
    headers: Dict[str, str]
    body: Dict[str, Any]
    instructions: str


class AgentIntegrationFileConfig(TypedDict, total=False):
    maxFiles: int


class AgentIntegrationConfigInput(TypedDict, total=False):
    endpointUrl: str
    secretKey: str
    signatureHeader: str
    inputs: List[AgentInputDefinition]
    files: AgentIntegrationFileConfig
    requestPreview: AgentIntegrationRequestPreview
    webhookUrl: str
    webhook: AgentIntegrationWebhookPreview


class AgentSkillInput(TypedDict):
    name: str
    categoryKey: str


class AgentProfileInput(TypedDict, total=False):
    walletAddress: str
    displayName: str
    title: str
    bio: str
    pricePerTask: float
    currency: str
    responseTime: str
    languages: List[str]
    categoryKeys: List[str]
    skillIds: List[str]
    newSkills: List[AgentSkillInput]
    avatar: str
    location: str
    timezone: str
    availability: Literal["available", "busy", "offline"]
    integration: AgentIntegrationConfigInput


class AgentRecord(TypedDict):
    id: str
    displayName: str
    title: str
    bio: str
    pricePerTask: float
    currency: str
    responseTime: str
    languages: List[str]
    categoryKeys: List[str]
    integration: AgentIntegrationConfigInput


class AgentRegistrationResponse(TypedDict):
    success: bool
    agent: AgentRecord


@dataclass
class CrewRequestMetadata:
    agent_id: str
    session_id: str
    request_timestamp: str
    signature_header: str


@dataclass
class CrewAgentRequest:
    metadata: CrewRequestMetadata
    payload: Mapping[str, Any]


class CrewWebhookResponse(TypedDict, total=False):
    taskId: str
    requestId: str
    status: Literal["completed", "failed", "in-progress"]
    result: Any
    response: Any
    error: Any
    attachments: List[Mapping[str, Any]]
    meta: Optional[MutableMapping[str, Any]]
