from inspect import signature, isfunction, isclass
from typing import get_type_hints, get_origin, get_args
from dataclasses import is_dataclass, fields as dataclass_fields


PRIMITIVES = {int, float, str, bool, dict, list, tuple, set}

def get_available_tools_description(tools):
    def format_type(t):
        return str(t).replace("typing.", "")


    def is_primitive(t):
        origin = get_origin(t)
        if origin:  # handle typing e.g. list[int]
            return False
        return t in PRIMITIVES


    def describe_complex_type(t):
        """Return a human-readable description of complex types like Customer"""
        try:
            # Dataclass
            if is_dataclass(t):
                f = dataclass_fields(t)
                details = "\n".join([f"        * {fld.name}: {format_type(fld.type)}" for fld in f])
                return f"\n      Type Structure ({t.__name__}):\n{details}"

            # Pydantic
            if hasattr(t, "__fields__"):
                details = "\n".join([
                    f"        * {name}: {format_type(field.annotation)}"
                    for name, field in t.__fields__.items()
                ])
                return f"\n      Type Structure ({t.__name__}):\n{details}"

            # Regular class with annotations
            if hasattr(t, "__annotations__"):
                ann = t.__annotations__
                details = "\n".join([f"        * {k}: {format_type(v)}" for k, v in ann.items()])
                return f"\n      Type Structure ({t.__name__}):\n{details}"

        except Exception:
            pass

        return ""


    def describe_arg(name, t):
        base = f"    - {name}: {format_type(t)}"
        if not is_primitive(t):
            return base + describe_complex_type(t)
        return base


    def describe_tool(tool):
        description = getattr(tool, "description", "No description")
        func = getattr(tool, "func", None)

        # Determine return type
        return_type = "None"
        return_extra = ""
        if func and isfunction(func):
            hints = get_type_hints(func)
            r = hints.get("return", None)
            if r:
                return_type = format_type(r)
                if not is_primitive(r):
                    return_extra = describe_complex_type(r)

        # Arguments from LangChain args_schema
        params_desc = []
        if hasattr(tool, "args_schema") and tool.args_schema:
            schema = tool.args_schema.model_fields
            for name, field in schema.items():
                t = field.annotation if field.annotation else "Any"
                params_desc.append(describe_arg(name, t))
        else:
            params_desc.append("    - None")

        return (
                f"- {tool.name}:\n"
                f"  Description: {description}\n"
                f"  Arguments:\n" + "\n".join(params_desc) +
                f"\n  Returns: {return_type}" +
                (f"{return_extra}" if return_extra else "")
        )



    available_tools_description = "\n\n".join(describe_tool(tool) for tool in tools)
    return available_tools_description
