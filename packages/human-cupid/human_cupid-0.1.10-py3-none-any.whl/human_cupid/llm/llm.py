import logging
import re
from typing import List, Dict, Any, Optional, Type, TypeVar, overload, Union
from pydantic import BaseModel
from litellm.files.main import ModelResponse
from litellm import CustomStreamWrapper, completion
import json

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

def resolve_refs(schema: dict) -> dict:
    defs = schema.pop("$defs", {})

    def _resolve(node):
        if isinstance(node, dict):
            if "$ref" in node:
                ref = node["$ref"].split("/")[-1]
                
                ref_obj = defs.get(ref)

                if isinstance(ref_obj, dict):
                    ref_obj["description"] = node.get("description", ref_obj.get("description"))

                return _resolve(ref_obj)
            return {k: _resolve(v) for k, v in node.items()}
        elif isinstance(node, list):
            return [_resolve(i) for i in node]
        return node

    return _resolve(schema) # type: ignore

def simplify_schema(model: type[BaseModel]) -> Dict[str, Any]:
    raw_schema = model.model_json_schema()
    flat_schema = resolve_refs(raw_schema) 
    return _simplify_props(flat_schema.get("properties", {}), flat_schema.get("required", []))

def _simplify_props(props: Dict[str, Any], required: list[str]) -> Dict[str, Any]:
    result = {}
    for field, details in props.items():
        field_type = details.get("type", "any")
        desc = details.get("description")
        nested = details.get("properties")
        
        if field_type == "array" and "items" in details:
            items = details["items"]
            if "properties" in items:
                result[field] = [_simplify_props(items.get("properties", {}), items.get("required", []))]
            else:
                item_type = items.get("type", "any")
                entry = item_type
                if desc:
                    entry += f" - {desc}"
                if field not in required:
                    entry += " (optional)"
                result[field] = [entry]
        elif field_type == "object" and "additionalProperties" in details:
            addl_props = details["additionalProperties"]
            if "type" in addl_props and addl_props["type"] == "object":
                result[field] = {
                    "<key>": _simplify_props(
                        addl_props.get("properties", {}), 
                        addl_props.get("required", [])
                    )
                }
            else:
                result[field] = f"Dict[string, {addl_props.get('type', 'any')}]"

                if desc:
                    result[field] += f" - {desc}"
                if field not in required:
                    result[field] += " (optional)"
        elif nested: 
            result[field] = _simplify_props(nested, details.get("required", []))
        elif "enum" in details:
            enum_vals = details["enum"]
            entry = ' | '.join(map(str, enum_vals))
            if desc:
                entry += f" - {desc}"
            if field not in required:
                entry += " (optional)"
            result[field] = entry
        else:
            entry = field_type
            if desc:
                entry += f" - {desc}"
            if field not in required:
                entry += " (optional)"
            result[field] = entry
    return result

def extract_json_from_response(text: str) -> str:
    if not isinstance(text, str):
        return text
    
    # Common JSON fence patterns
    fence_patterns = [
        r'```json\s*\n?(.*?)\n?```',  # ```json ... ```
        r'```\s*\n?(.*?)\n?```',      # ``` ... ```
        r'`json\s*\n?(.*?)\n?`',      # `json ... `
        r'`\s*\n?(.*?)\n?`',          # ` ... `
    ]
    
    # Try to extract from fences first
    for pattern in fence_patterns:
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        if matches:
            candidate = matches[0].strip()
            if _looks_like_json(candidate):
                return candidate
    
    # If no fences found, try to find JSON-like content
    # Look for content between first { and last }
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidate = text[first_brace:last_brace + 1].strip()
        if _looks_like_json(candidate):
            return candidate
    
    # Look for content between first [ and last ]
    first_bracket = text.find('[')
    last_bracket = text.rfind(']')
    
    if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
        candidate = text[first_bracket:last_bracket + 1].strip()
        if _looks_like_json(candidate):
            return candidate
    
    return text.strip()

def _looks_like_json(text: str) -> bool:
    """Quick heuristic to check if text looks like JSON."""
    text = text.strip()
    return (
        (text.startswith('{') and text.endswith('}')) or
        (text.startswith('[') and text.endswith(']'))
    ) and len(text) > 2

def parse_json(text: str) -> Any:
    """Parse JSON with multiple fallback strategies."""
    extracted = extract_json_from_response(text)
    
    try:
        return json.loads(extracted)
    except json.JSONDecodeError as e:
        logger.debug(f"Direct JSON parse failed: {e}")
    
    try:
        # Remove trailing commas
        fixed = re.sub(r',(\s*[}\]])', r'\1', extracted)
        # Fix single quotes to double quotes (basic cases)
        fixed = re.sub(r"'([^']*)':", r'"\1":', fixed)
        fixed = re.sub(r":\s*'([^']*)'", r': "\1"', fixed)
        return json.loads(fixed)
    except json.JSONDecodeError as e:
        logger.debug(f"Fixed JSON parse failed: {e}")
    
    try:
        if extracted.strip().startswith(('{', '[')):
            result = eval(extracted, {"__builtins__": {}}, {})
            if isinstance(result, (dict, list)):
                return result
    except Exception as e:
        logger.debug(f"Eval fallback failed: {e}")
    
    raise json.JSONDecodeError(f"Could not parse JSON from: {text[:200]}...", "", 0)

class ErrorResponse(Exception):
    def __init__(self, error: str, details: Optional[str] = None, raw_response: Optional[Any] = None):
        self.error = error
        self.details = details
        self.raw_response = raw_response
        super().__init__(self.__str__())

    def __str__(self):
        base = f"Error: {self.error}"
        if self.details:
            base += f" | Details: {self.details}"
        if self.raw_response:
            base += f" | Raw Response: {self.raw_response}"
        return base

class LLM:
    def __init__(self, model_name: str):
        self.model_name = model_name

    @overload
    def run(self, messages: List[dict], response_format: Type[T], *, stream: bool = False) -> T: ...
    @overload
    def run(self, messages: List[dict], response_format: Dict[str, Any], *, stream: bool = False) -> ModelResponse: ...
    @overload
    def run(self, messages: List[dict], response_format: None = None, *, stream: bool = False) -> ModelResponse: ...
    @overload
    def run(self, messages: List[dict], response_format: Any, *, stream: bool = True) -> CustomStreamWrapper: ...

    def run(
        self,
        messages: Optional[List[dict]] = None,
        response_format: Union[Type[T], Dict[str, Any], None] = None,
        *,
        stream: bool = False,
    ) -> Union[T, ModelResponse, CustomStreamWrapper]:
        if messages is None:
            messages = []

        if isinstance(response_format, type) and issubclass(response_format, BaseModel):
            schema = simplify_schema(response_format)

            schema_message = {
                "role": "system",
                "content": (
                    f"You must respond with valid JSON that matches this schema: {json.dumps(schema, indent=2)}\n\n"
                    "Important guidelines:\n"
                    "- Respond ONLY with the JSON object, no additional text\n"
                    "- Do not wrap the JSON in code fences or markdown\n"
                    "- Ensure all string values are properly quoted\n"
                    "- Do not include trailing commas\n"
                    "- Use double quotes for all strings and property names"
                )
            }
            messages = messages + [schema_message]

        response = completion(
            model=self.model_name,
            messages=messages,
            response_format=response_format if not isinstance(response_format, type) else None,
            stream=stream,
        )

        if isinstance(response, CustomStreamWrapper):
            return response

        if isinstance(response_format, type) and issubclass(response_format, BaseModel):
            raw = response["choices"][0]["message"]["content"]
            
            try:
                if isinstance(raw, str):
                    raw = parse_json(raw)
                return response_format.model_validate(raw)
            except Exception as e:
                raise ErrorResponse(
                    error="Failed to parse model response",
                    details=str(e),
                    raw_response=raw
                )

        return response
