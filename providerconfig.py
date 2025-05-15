##stuff inside schemas.py
##########################
class ProviderConfig(BaseModel):
    class ConfigItem(BaseModel):
        parameter: ProviderConfigItem
        value: Any

    config_updates: List[ConfigItem]

    @model_validator(mode="after")
    def validate_input_types(self):
        for config_update in self.config_updates:
            if config_update.parameter == ProviderConfigItem.SPECIALITY__STR and not isinstance(config_update.value, str):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.LOGO__STR and not isinstance(config_update.value, str):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.ASSETS__SIGNUP_QR_CODE__STR and not isinstance(config_update.value, str):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.ASSETS__BROCHURE__STR and not isinstance(config_update.value, str):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__SOAP__SUPPRESS_SERVICE_DATE__BOOL and not isinstance(config_update.value, bool):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__PANEL_CONFIG__DICT and not isinstance(config_update.value, dict):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__KEY_VITALS__APC__LIST and not isinstance(config_update.value, list):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__KEY_VITALS__AMA__LIST and not isinstance(config_update.value, list):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__AUTH_CALLBACK_URLS__FAILURE__STR and not isinstance(config_update.value, str):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__AUTH_CALLBACK_URLS__SUCCESS__STR and not isinstance(config_update.value, str):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__EMAILS__SUPPRESS_MEMBER_SEND__BOOL and not isinstance(config_update.value, bool):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__EMAILS__CC_FOR_MEMBER_COMMUNICATION__LIST and not isinstance(config_update.value, list):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__EMAILS__BCC_FOR_MEMBER_COMMUNICATION__LIST and not isinstance(config_update.value, list):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__NOTIFICATION_FREQUENCIES__DEFAULT__PUSH__INT and not isinstance(config_update.value, int):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__NOTIFICATION_FREQUENCIES__DEFAULT__INAPP__INT and not isinstance(config_update.value, int):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__NOTIFICATION_FREQUENCIES__DEFAULT__EMAIL__INT and not isinstance(config_update.value, int):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__NOTIFICATION_FREQUENCIES__IOS_APPLEHEALTH_NOTIFICATION__PUSH__INT and not isinstance(config_update.value, int):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__NOTIFICATION_FREQUENCIES__IOS_APPLEHEALTH_NOTIFICATION__INAPP__INT and not isinstance(config_update.value, int):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__NOTIFICATION_FREQUENCIES__IOS_APPLEHEALTH_NOTIFICATION__EMAIL__INT and not isinstance(config_update.value, int):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__NOTIFICATION_FREQUENCIES__DISCONNECTED_SOURCES__PUSH__INT and not isinstance(config_update.value, int):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__NOTIFICATION_FREQUENCIES__DISCONNECTED_SOURCES__INAPP__INT and not isinstance(config_update.value, int):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
            elif config_update.parameter == ProviderConfigItem.OPERATING_PARAMETERS__COMMUNICATION_PARAMETERS__NOTIFICATION_FREQUENCIES__DISCONNECTED_SOURCES__EMAIL__INT and not isinstance(config_update.value, int):
                raise ValueError(f"{config_update.parameter} type cannot be {type(config_update.value)}")
        return self

# -----------------------------
# # Routes
# -----------------------------
@router.post("/v1/apc/provider/config_update", status_code=200)
async def provider_config_update(
    config: ProviderConfig,
    pid: str = Depends(token_auth)
):
    return api_provider_config_update(pid, config)
# -----------------------------
# # API Logic
# -----------------------------
def api_provider_config_update(pid: str, config: ProviderConfig):
    provider_record = ALYF_PROVIDER_OPS.get(pid)
    if not provider_record:
        raise HTTPException(status_code=404, detail=f"Provider not found for id: {pid}")
    updated_config = getattr(provider_record, 'config', {}).copy()
    for item in config.config_updates:
        updated_config[item.parameter.value] = item.value
    ALYF_PROVIDER_OPS.set_config(pid, updated_config)
    return {"status": "success", "updated_config": updated_config}