from collections.abc import Mapping
from typing import cast

from .module_builder import GlobalConfig, LibConfig
from .safe_proxy import Policies, Rule


def _validate_rule(rule: object, path: str) -> Rule:
    if isinstance(rule, str):
        return rule

    if isinstance(rule, Mapping):
        rule_mapping = cast(Mapping[object, object], rule)
        if len(rule_mapping) != 1:
            raise ValueError(f"Invalid rule at '{path}': expected a single key, got {len(rule_mapping)}")
        key_obj, value = next(iter(rule_mapping.items()))
        key = key_obj if isinstance(key_obj, str) else None
        if not isinstance(key, str):
            raise ValueError(f"Invalid rule name at '{path}': expected str, got {type(key).__name__}")
        return {key: value}

    raise ValueError(f"Invalid rule at '{path}': expected str or mapping, got {type(rule).__name__}")


def _validate_policies(policies_obj: object, path: str) -> Policies:
    if not isinstance(policies_obj, Mapping):
        raise ValueError(f"Invalid policies at '{path}': expected mapping, got {type(policies_obj).__name__}")

    policies_obj = cast(Mapping[object, object], policies_obj)

    policies: Policies = {}
    for func_name_obj, rule_list_obj in policies_obj.items():
        func_name = func_name_obj if isinstance(func_name_obj, str) else None
        if not isinstance(func_name, str):
            raise ValueError(f"Invalid policy key at '{path}': expected str, got {type(func_name_obj).__name__}")
        if not isinstance(rule_list_obj, list):
            raise ValueError(f"Invalid rule list at '{path}.{func_name}': expected list, got {type(rule_list_obj).__name__}")

        rule_list = cast(list[object], rule_list_obj)

        validated_rules: list[Rule] = []
        for idx, rule in enumerate(rule_list):
            validated_rules.append(_validate_rule(rule, f"{path}.{func_name}[{idx}]") )

        policies[func_name] = validated_rules

    return policies


def _validate_lib_config(lib_conf_obj: object, lib_name: str) -> LibConfig:
    if not isinstance(lib_conf_obj, Mapping):
        raise ValueError(f"Invalid config for lib '{lib_name}': expected mapping, got {type(lib_conf_obj).__name__}")

    allowed_keys = {"policies", "target_class"}
    lib_conf_obj = cast(Mapping[object, object], lib_conf_obj)
    for key_obj in lib_conf_obj.keys():
        key = key_obj if isinstance(key_obj, str) else None
        if key not in allowed_keys:
            raise ValueError(f"Invalid key '{key_obj}' in config for lib '{lib_name}'. Allowed keys: {sorted(allowed_keys)}")

    if "policies" not in lib_conf_obj:
        raise ValueError(f"Missing 'policies' in config for lib '{lib_name}'")

    if "target_class" not in lib_conf_obj:
        raise ValueError(f"Missing 'target_class' in config for lib '{lib_name}'")

    policies = _validate_policies(lib_conf_obj["policies"], f"libs.{lib_name}.policies")

    target_class_obj = lib_conf_obj["target_class"]
    if not isinstance(target_class_obj, str):
        raise ValueError(f"Invalid 'target_class' for lib '{lib_name}': expected str, got {type(target_class_obj).__name__}")

    validated: LibConfig = {
        "policies": policies,
        "target_class": target_class_obj,
    }

    return validated


def validate_config(raw_config: object) -> GlobalConfig:
    if not isinstance(raw_config, Mapping):
        raise ValueError(f"Invalid config root: expected mapping with 'libs', got {type(raw_config).__name__}")

    raw_config = cast(Mapping[object, object], raw_config)

    libs_obj = raw_config.get("libs", {})
    if not isinstance(libs_obj, Mapping):
        raise ValueError(f"Invalid 'libs' section: expected mapping, got {type(libs_obj).__name__}")

    libs_obj = cast(Mapping[object, object], libs_obj)

    libs: dict[str, LibConfig] = {}
    for lib_name_obj, lib_conf in libs_obj.items():
        lib_name = lib_name_obj if isinstance(lib_name_obj, str) else None
        if not isinstance(lib_name, str):
            raise ValueError(f"Invalid library name in 'libs': expected str, got {type(lib_name_obj).__name__}")
        libs[lib_name] = _validate_lib_config(lib_conf, lib_name)

    return {"libs": libs}


__all__ = ["validate_config"]
