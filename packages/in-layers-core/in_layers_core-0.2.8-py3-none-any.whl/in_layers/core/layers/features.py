from __future__ import annotations

import inspect
from collections.abc import Mapping
from typing import Any

from box import Box

from ..globals.libs import extract_cross_layer_props
from ..libs import get_layers_unavailable
from ..protocols import (
    CommonContext,
    CoreNamespace,
    FeaturesContext,
)


def _iter_properties_for_wrap(obj: Any):
    if isinstance(obj, Mapping):
        for k, v in obj.items():
            yield from (k, v)
        return
    for name in dir(obj):
        if name.startswith("_"):
            continue
        try:
            attr = getattr(obj, name)
        except Exception:  # noqa: S112
            continue
        yield name, attr


def _call_with_optional_cross(
    f,
    args_no_cross: list[Any],
    kwargs: dict[str, Any],
    cross: Mapping[str, Any] | None,
):
    if cross is None:
        return f(*args_no_cross, **kwargs)
    sig = inspect.signature(f)
    params = list(sig.parameters.values())
    has_var_positional = any(p.kind is inspect.Parameter.VAR_POSITIONAL for p in params)
    has_var_keyword = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params)
    positional_params = [
        p
        for p in params
        if p.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]
    max_positional = len(positional_params)
    cross_param_names = {"cross", "crossLayerProps", "cross_layer_props"}
    matching_named = [p for p in params if p.name in cross_param_names]
    if matching_named:
        named = matching_named[0]
        if (
            named.kind is inspect.Parameter.KEYWORD_ONLY
            or named.kind is inspect.Parameter.VAR_KEYWORD
            or named.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
        ):
            return f(*args_no_cross, **{**kwargs, named.name: cross})
        # positional-only: must pass positionally
    if has_var_positional:
        return f(*args_no_cross, cross, **kwargs)
    if len(args_no_cross) + 1 <= max_positional:
        return f(*args_no_cross, cross, **kwargs)
    if has_var_keyword:
        name = (
            "crossLayerProps"
            if "crossLayerProps" in {p.name for p in params}
            else "cross"
        )
        return f(*args_no_cross, **{**kwargs, name: cross})
    return f(*args_no_cross, **kwargs)


def _make_passthrough_for_log(f, logger_ids):
    def _inner(log, *args, **kwargs):  # noqa: ARG001

        args_no_cross, cross = extract_cross_layer_props(list(args))
        effective_cross = cross or {"logging": {"ids": logger_ids}}
        return _call_with_optional_cross(
            f, args_no_cross, dict(kwargs), effective_cross
        )

    return _inner


def _should_copy_direct_layer_key(key: str) -> bool:
    return key in (
        "_logging",
        "root_logger",
        "log",
        "constants",
        "config",
        "models",
        "get_models",
        "cruds",
    )


def _wrap_domain_mapping_for_load(
    features: LayersFeatures,
    domain_key: str,
    domain_value: Mapping[str, Any],
    layer_key: str,
    ignore_layer_functions: list[str],
    logger_ids: Any,
) -> Mapping[str, Any]:
    layer_level_key = f"{domain_key}.{layer_key}"
    if _should_ignore_path(ignore_layer_functions, layer_level_key):
        return domain_value
    domain_data: dict[str, Any] = {}
    for property_name, func in domain_value.items():
        if not callable(func):
            domain_data[property_name] = func
            continue
        function_level_key = f"{domain_key}.{layer_key}.{property_name}"
        if _should_ignore_path(ignore_layer_functions, function_level_key):
            domain_data[property_name] = func
            continue
        wrapped_func = features._make_wrapped(func, logger_ids)
        for attr in dir(func):
            try:  # noqa: SIM105
                setattr(wrapped_func, attr, getattr(func, attr))
            except Exception:  # noqa: S110
                pass
        domain_data[property_name] = wrapped_func
    return domain_data


def _build_wrapped_context_for_load(
    features: LayersFeatures,
    ctx: Mapping[str, Any],
    ignore_layer_functions: list[str],
    logger_ids: Any,
) -> Mapping[str, Any]:
    wrapped: dict[str, Any] = {}
    for layer_key, layer_data in ctx.items():
        if _should_copy_direct_layer_key(layer_key) or not isinstance(
            layer_data, Mapping
        ):
            wrapped[layer_key] = layer_data
            continue
        final_layer_data: dict[str, Any] = {}
        for domain_key, domain_value in layer_data.items():
            if not isinstance(domain_value, Mapping):
                final_layer_data[domain_key] = domain_value
                continue
            final_layer_data[domain_key] = _wrap_domain_mapping_for_load(
                features,
                domain_key,
                domain_value,
                layer_key,
                ignore_layer_functions,
                logger_ids,
            )
        wrapped[layer_key] = final_layer_data
    return wrapped


class LayersFeatures:
    def __init__(self, context: FeaturesContext):
        self.context = context

    def _get_layer_context(
        self, common_context: Mapping[str, Any], layer: Mapping[str, Any] | None
    ) -> Mapping[str, Any]:
        if layer:
            merged = Box(common_context)
            return merged + Box(layer)
        return common_context

    def _make_wrapped(self, f, logger_ids):
        def _inner2(*args, **kwargs):
            args_no_cross, cross = extract_cross_layer_props(list(args))
            effective_cross = cross or {"logging": {"ids": logger_ids}}
            return _call_with_optional_cross(
                f, args_no_cross, dict(kwargs), effective_cross
            )

        return _inner2

    def _wrap_layer_functions(
        self,
        loaded_layer: Any,
        layer_logger,
        app_name: str,
        layer: str,
        ignore_layer_functions: list[str],
    ):
        out: dict[str, Any] = {}
        for property_name, func in _iter_properties_for_wrap(loaded_layer):
            if not callable(func):
                out[property_name] = func
                continue
            function_level_key = f"{app_name}.{layer}.{property_name}"
            if _should_ignore_path(ignore_layer_functions, function_level_key):
                out[property_name] = func
                continue
            wrapped = layer_logger._log_wrap(
                property_name, _make_passthrough_for_log(func, layer_logger.get_ids())
            )
            for attr in dir(func):
                try:  # noqa: SIM105
                    setattr(wrapped, attr, getattr(func, attr))
                except Exception:  # noqa: S110
                    pass
            out[property_name] = wrapped
        return out

    async def _load_composite_layer(
        self,
        app: Mapping[str, Any],
        composite_layers,
        common_context: Mapping[str, Any],
        previous_layer: Mapping[str, Any] | None,  # noqa: ARG002
        anti_layers_fn,  # noqa: ARG002
    ):
        result = {}
        for layer in composite_layers:
            layer_logger = (
                self.context.root_logger.get_logger(
                    Box(
                        common_context,
                    )
                )
                .get_app_logger(app.name)
                .get_layer_logger(layer)
            )
            the_context = dict(common_context)
            the_context["log"] = layer_logger
            wrapped_context = the_context
            loaded = self.context.services[CoreNamespace.layers.value].load_layer(
                app,
                layer,
                Box(
                    wrapped_context,
                ),
            )
            if loaded:
                ignore_layer_functions = self.context.config.in_layers_core.logging.get(
                    "ignore_layer_functions", []
                )
                layer_level_key = f"{app.name}.{layer}"
                should_ignore = _should_ignore_path(
                    ignore_layer_functions, layer_level_key
                )
                final_layer = (
                    loaded
                    if should_ignore
                    else self._wrap_layer_functions(
                        loaded, layer_logger, app.name, layer, ignore_layer_functions
                    )
                )
                result = {**result, layer: {app.name: final_layer}}
        return result

    async def _load_layer(
        self,
        app: Mapping[str, Any],
        current_layer: str,
        common_context: Mapping[str, Any],
        previous_layer: Mapping[str, Any] | None,
    ):
        layer_context1 = self._get_layer_context(common_context, previous_layer)
        layer_logger = (
            self.context.root_logger.get_logger(Box(layer_context1))
            .get_app_logger(app.name)
            .get_layer_logger(current_layer)
        )
        layer_context = dict(layer_context1)
        layer_context["log"] = layer_logger

        logger_ids = layer_logger.get_ids()
        ignore_layer_functions = self.context.config.in_layers_core.logging.get(
            "ignore_layer_functions", []
        )
        wrapped_context = _build_wrapped_context_for_load(
            self, layer_context, ignore_layer_functions, logger_ids
        )

        loaded = self.context.services.in_layers_core_layers.load_layer(
            app,
            current_layer,
            Box(wrapped_context),
        )
        if not loaded:
            return {}
        layer_level_key = f"{app.name}.{current_layer}"
        should_ignore = _should_ignore_path(ignore_layer_functions, layer_level_key)
        final_layer = (
            loaded
            if should_ignore
            else self._wrap_layer_functions(
                loaded, layer_logger, app.name, current_layer, ignore_layer_functions
            )
        )
        return {current_layer: {app.name: final_layer}}

    async def load_layers(self):
        layers_in_order = self.context.config.in_layers_core.layer_order
        anti_layers = get_layers_unavailable(layers_in_order)
        core_layers_to_ignore = [
            f"services.{CoreNamespace.layers.value}",
            f"services.{CoreNamespace.globals.value}",
            f"features.{CoreNamespace.layers.value}",
            f"features.{CoreNamespace.globals.value}",
        ]
        starting_context: CommonContext = {k: v for k, v in self.context.items() if k not in core_layers_to_ignore}  # type: ignore[return-value]
        apps = self.context.config.in_layers_core.domains
        existing_layers = starting_context
        for app in apps:
            previous_layer = {}
            for layer in layers_in_order:
                if isinstance(layer, list):
                    layer_instance = await self._load_composite_layer(
                        app,
                        layer,
                        {k: v for k, v in existing_layers.items() if k != "log"},
                        previous_layer,
                        anti_layers,
                    )
                else:
                    layer_instance = await self._load_layer(
                        app,
                        layer,
                        {k: v for k, v in existing_layers.items() if k != "log"},
                        previous_layer,
                    )
                if not layer_instance:
                    previous_layer = {}
                    continue
                new_context = {**existing_layers, **layer_instance}
                if "log" in new_context:
                    new_context = {k: v for k, v in new_context.items() if k != "log"}
                existing_layers = new_context
                previous_layer = layer_instance
        return Box(
            existing_layers,
        )


def create(context: FeaturesContext) -> LayersFeatures:
    return LayersFeatures(context)


def _should_ignore_path(ignore_list: list[str], dotted: str) -> bool:
    if not ignore_list:
        return False
    dotted = dotted.strip().strip(".")
    for pattern in ignore_list:
        if not pattern:
            continue
        pat = str(pattern).strip().strip(".")
        if not pat:
            continue
        if dotted == pat or dotted.startswith(f"{pat}."):
            return True
    return False
