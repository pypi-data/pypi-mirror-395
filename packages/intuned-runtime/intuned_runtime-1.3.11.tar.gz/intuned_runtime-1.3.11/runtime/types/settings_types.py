import os
import socket
from typing import Any
from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic import Field


def get_intuned_captcha_extension_port():
    if "INTUNED_CAPTCHA_EXTENSION_PORT" in os.environ:
        return int(os.environ["INTUNED_CAPTCHA_EXTENSION_PORT"])
    with socket.socket() as s:
        s.bind(("", 0))
        return s.getsockname()[1]


class CaptchaSettings(BaseModel):
    enabled: bool = Field(default=False)


class CaptchaSolverSolveSettings(BaseModel):
    model_config = {
        "populate_by_name": True,
        "serialize_by_alias": True,
    }
    auto_solve: bool = Field(default=True, alias="autoSolve")
    solve_delay: int = Field(default=2000, alias="solveDelay")
    max_retries: int = Field(default=3, alias="maxRetries")
    timeout: int = Field(default=30000)


class CustomCaptchaSettings(CaptchaSettings):
    model_config = {
        "serialize_by_alias": True,
    }

    image_locators: List[str] = Field(alias="imageLocators", default=[])
    submit_locators: List[str] = Field(alias="submitLocators", default=[])
    input_locators: List[str] = Field(alias="inputLocators", default=[])


class TextCaptchaSettings(CaptchaSettings):
    model_config = {
        "populate_by_name": True,
        "serialize_by_alias": True,
    }
    label_locators: List[str] = Field(alias="labelLocators", default=[])
    submit_locators: List[str] = Field(alias="submitLocators", default=[])
    input_locators: List[str] = Field(alias="inputLocators", default=[])


class CaptchaSolverApiKeyAuthentication(BaseModel):
    model_config = {
        "populate_by_name": True,
        "serialize_by_alias": True,
    }
    type: Literal["apiKey"]
    api_key: str = Field(alias="apiKey")


class CaptchaSolverTokenSettings(BaseModel):
    type: Literal["basic", "bearer"]
    token: str | None


class CaptchaSolverSettings(BaseModel):
    model_config = {
        "populate_by_name": True,
        "serialize_by_alias": True,
    }

    enabled: bool = Field(default=False)
    port: int = Field(default_factory=get_intuned_captcha_extension_port)
    cloudflare: CaptchaSettings = Field(default_factory=CaptchaSettings)
    google_recaptcha_v2: CaptchaSettings = Field(alias="googleRecaptchaV2", default_factory=CaptchaSettings)
    google_recaptcha_v3: CaptchaSettings = Field(alias="googleRecaptchaV3", default_factory=CaptchaSettings)
    awscaptcha: CaptchaSettings = Field(default_factory=CaptchaSettings)
    hcaptcha: CaptchaSettings = Field(default_factory=CaptchaSettings)
    funcaptcha: CaptchaSettings = Field(default_factory=CaptchaSettings)
    geetest: CaptchaSettings = Field(default_factory=CaptchaSettings)
    lemin: CaptchaSettings = Field(default_factory=CaptchaSettings)
    custom_captcha: CustomCaptchaSettings = Field(alias="customCaptcha", default_factory=CustomCaptchaSettings)
    text: TextCaptchaSettings = Field(default_factory=TextCaptchaSettings)
    settings: CaptchaSolverSolveSettings = Field(default_factory=CaptchaSolverSolveSettings)


class IntunedJsonDisabledAuthSessions(BaseModel):
    enabled: Literal[False]


class IntunedJsonEnabledAuthSessions(BaseModel):
    enabled: Literal[True]
    type: Literal["API", "MANUAL"]
    start_url: str | None = Field(default=None, alias="startUrl")
    finish_url: str | None = Field(default=None, alias="finishUrl")


class IntunedMetadata(BaseModel):
    model_config = {"populate_by_name": True}

    default_job_input: dict[str, Any] | None = Field(alias="defaultJobInput", default=None)
    default_run_playground_input: dict[str, Any] | None = Field(
        alias="defaultRunPlaygroundInput",
        default=None,
    )
    test_auth_session_input: dict[str, Any] | None = Field(
        alias="testAuthSessionInput",
        default=None,
    )


class IntunedApiAccessEnabled(BaseModel):
    enabled: Literal[True]


class IntunedApiAccessDisabled(BaseModel):
    enabled: Literal[False]


class IntunedJsonBase(BaseModel):
    model_config = {"populate_by_name": True, "extra": "allow"}

    project_name: str | None = Field(alias="projectName", default=None)
    workspace_id: str | None = Field(alias="workspaceId", default=None)
    captcha_solver: CaptchaSolverSettings | None = Field(alias="captchaSolver", default=None)

    @property
    def metadata(self) -> IntunedMetadata | None:
        if not self.model_extra:
            return None
        if "metadata" not in self.model_extra:
            return None
        try:
            return IntunedMetadata.model_validate(self.model_extra["metadata"])
        except Exception:
            return None


class IntunedJsonApiAccessEnabled(IntunedJsonBase):
    model_config = {"populate_by_name": True, "extra": "allow"}

    api_access: IntunedApiAccessEnabled = Field(alias="apiAccess")
    auth_sessions: IntunedJsonDisabledAuthSessions | IntunedJsonEnabledAuthSessions = Field(alias="authSessions")


class IntunedJsonApiAccessDisabled(IntunedJsonBase):
    model_config = {"populate_by_name": True, "extra": "allow"}

    api_access: IntunedApiAccessDisabled = Field(alias="apiAccess")
    auth_sessions: IntunedJsonDisabledAuthSessions = Field(alias="authSessions")


IntunedJson = IntunedJsonApiAccessEnabled | IntunedJsonApiAccessDisabled
