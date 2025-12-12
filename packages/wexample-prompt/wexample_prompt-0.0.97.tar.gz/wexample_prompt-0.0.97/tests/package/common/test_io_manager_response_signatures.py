from __future__ import annotations

import inspect


def test_io_manager_response_signatures_align_with_factories() -> None:
    from wexample_prompt.common.io_manager import IoManager

    io = IoManager()

    for response_cls in io.get_response_types():
        method_name = response_cls.get_snake_short_class_name()

        io_method = getattr(io, method_name, None)
        assert io_method is not None, f"{io.__class__.__name__}.{method_name} missing"

        factory_name = f"create_{method_name}"
        factory = getattr(response_cls, factory_name, None)
        assert factory is not None, f"{response_cls.__name__}.{factory_name} missing"

        io_required, io_optional, _ = _summarize_parameters(
            inspect.signature(io_method), {"self"}
        )
        factory_required, factory_optional, _ = _summarize_parameters(
            inspect.signature(factory), {"cls"}
        )

        missing_required = sorted(
            name
            for name in factory_required
            if name not in io_required and name not in io_optional
        )
        missing_optional = sorted(
            name
            for name in factory_optional
            if name not in io_required and name not in io_optional
        )

        assert not missing_required, (
            f"{io.__class__.__name__}.{method_name} missing required arguments from "
            f"{response_cls.__name__}: {missing_required}"
        )
        assert not missing_optional, (
            f"{io.__class__.__name__}.{method_name} missing optional arguments from "
            f"{response_cls.__name__}: {missing_optional}"
        )


def _summarize_parameters(signature: inspect.Signature, skip: set[str]):
    required: set[str] = set()
    optional: set[str] = set()
    has_var_kwargs = False

    for parameter in signature.parameters.values():
        if parameter.name in skip:
            continue

        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
            has_var_kwargs = True
            continue

        if parameter.default is inspect.Parameter.empty and parameter.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        ):
            required.add(parameter.name)
        else:
            optional.add(parameter.name)

    return required, optional, has_var_kwargs
