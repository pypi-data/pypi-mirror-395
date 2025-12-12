import importlib
from typing import Any, Dict
from spx_sdk.registry import register_class
from spx_sdk.actions.action import Action
from spx_sdk.components import SpxComponentState
from spx_sdk.validation.decorators import definition_schema


@register_class(name="function")
@definition_schema({
    "type": "object",
    "required": ["function", "call"],
    "properties": {
        "function": {
            "oneOf": [
                {"type": "string", "pattern": r"^(\$in|\$out|\$attr|\$ext)\([^)]+\)$"},
                {"type": "array", "minItems": 1, "items": {"type": "string", "pattern": r"^(\$in|\$out|\$attr|\$ext)\([^)]+\)$"}}
            ],
            "description": "Target attribute(s): single ref or list of refs to attributes using $in/$out/$attr/$ext."
        },
        "prepare_call": {
            "type": "string",
            "minLength": 1,
            "description": "Optional expression executed during prepare() (e.g., seeding RNG)."
        },
        "call": {
            "oneOf": [
                {"type": "string", "minLength": 1},
                {"type": "number"},
                {"type": "boolean"},
                {"type": "null"},
                {"type": "object"},
                {"type": "array"}
            ],
            "description": "Expression string (or literal) that may reference inputs via $in(...) and other helpers."
        },
        "params": {
            "type": "object",
            "description": "Optional mapping of parameter names to literal values or attribute references.",
            "additionalProperties": True
        },
        "imports": {
            "description": "Optional modules/symbols to expose in the call expression.",
            "oneOf": [
                {"type": "string", "minLength": 1},
                {
                    "type": "array",
                    "items": {"type": "string", "minLength": 1},
                    "minItems": 1
                },
                {
                    "type": "object",
                    "additionalProperties": {"type": "string", "minLength": 1}
                }
            ]
        },
    }
}, validation_scope="parent")
class FunctionAction(Action):
    """
    FunctionAction class for executing a function.
    Inherits from Action to manage action components.
    """

    def _populate(self, definition: dict) -> None:
        self.call = None
        self.last_call_result: Any = None
        self._imports_spec: Dict[str, str] = {}
        self._import_context: Dict[str, Any] = {}
        merged_definition = dict(definition or {})
        imports_block = merged_definition.pop("imports", None)
        self._imports_spec = self._normalize_imports(imports_block)
        params_block = merged_definition.pop("params", None)
        if params_block is not None:
            if not isinstance(params_block, dict):
                raise ValueError("FunctionAction 'params' section must be a mapping of parameter names to values.")
            for key, value in params_block.items():
                if key in ("function", "output", "call", "params"):
                    continue
                merged_definition.setdefault(key, value)
        super()._populate(merged_definition)
        # Expose the normalized spec on the instance for observability/debugging
        self.imports = self._imports_spec
        # Optional prepare-time expression
        self.prepare_call = merged_definition.get("prepare_call")

    def prepare(self, *args, **kwargs) -> bool:
        """
        Prepare parameters and eagerly import requested modules/symbols.
        """
        base_ready = super().prepare(*args, **kwargs)
        if base_ready:
            self._import_context = self._load_imports(self._imports_spec)
            if self.prepare_call is not None:
                self.prepare_call = self._evaluate_call(self.prepare_call)
        return base_ready

    def run(self, *args, **kwargs) -> Any:
        """
        Evaluate the call expression, resolving attribute references,
        and write the result to all output attributes.
        """
        base_result = super().run()
        if base_result is True:
            return True  # Action disabled
        if self.call is None:
            return False  # No call defined, nothing to run
        if not self._import_context and self._imports_spec:
            self._import_context = self._load_imports(self._imports_spec)
        evaluated = self._evaluate_call(self.call)
        self.last_call_result = evaluated
        result = self.write_outputs(evaluated)
        self.state = SpxComponentState.STOPPED
        return result

    def _build_eval_context(self) -> Dict[str, Any]:
        """
        Collect resolved parameter values exposed on the action for expression evaluation.
        """
        context: Dict[str, Any] = {"self": self, **self._import_context}
        for key in self.params.keys():
            if key in ("call", "params"):
                continue
            if hasattr(self, key):
                context[key] = getattr(self, key)
        return context

    def _evaluate_call(self, call_value: Any) -> Any:
        """
        Evaluate the call expression with access to resolved parameters.
        Falls back to the original value if evaluation fails.
        """
        if not isinstance(call_value, str):
            return call_value
        try:
            return eval(call_value, globals(), self._build_eval_context())
        except Exception:
            return call_value

    def _normalize_imports(self, imports_block: Any) -> Dict[str, str]:
        """
        Normalize the 'imports' section to a mapping alias -> import path.
        Accepts:
          - list of strings (alias inferred from last segment)
          - dict of alias -> import path
          - single string
        """
        if imports_block is None:
            return {}
        imports_map: Dict[str, str] = {}
        if isinstance(imports_block, str):
            imports_block = [imports_block]
        if isinstance(imports_block, list):
            for entry in imports_block:
                if not isinstance(entry, str):
                    raise ValueError("FunctionAction 'imports' entries must be strings.")
                alias = entry.split(".")[-1]
                imports_map[alias] = entry
        elif isinstance(imports_block, dict):
            for alias, target in imports_block.items():
                if not isinstance(alias, str) or not isinstance(target, str):
                    raise ValueError("FunctionAction 'imports' mapping must use string keys and values.")
                imports_map[alias] = target
        else:
            raise ValueError("FunctionAction 'imports' must be a string, list of strings, or mapping.")
        return imports_map

    def _load_imports(self, imports_map: Dict[str, str]) -> Dict[str, Any]:
        """
        Import requested modules/symbols and return a context dict.
        """
        context: Dict[str, Any] = {}
        for alias, target in imports_map.items():
            context[alias] = self._import_symbol(target)
        return context

    def _import_symbol(self, target: str) -> Any:
        """
        Import a module or attribute by dotted path.
        Example targets:
          - "random" -> module
          - "random.randint" -> function
          - "numpy.random.default_rng" -> callable
        """
        parts = target.split(".")
        for idx in range(len(parts), 0, -1):
            module_name = ".".join(parts[:idx])
            try:
                module = importlib.import_module(module_name)
            except ImportError:
                if idx == 1:
                    raise
                continue
            obj: Any = module
            for attr in parts[idx:]:
                try:
                    obj = getattr(obj, attr)
                except AttributeError as exc:
                    raise ImportError(f"Cannot resolve '{target}': missing attribute '{attr}' on '{module_name}'") from exc
            return obj
        raise ImportError(f"Unable to import '{target}'")
