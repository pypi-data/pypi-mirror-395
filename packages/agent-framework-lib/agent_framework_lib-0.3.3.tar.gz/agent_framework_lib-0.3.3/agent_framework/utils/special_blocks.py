import json
import re
from typing import Tuple, List

from agent_framework.core.agent_interface import (
    OptionsBlockOutputPart,
    FormDefinitionOutputPart,
)

def parse_special_blocks_from_text(text: str) -> Tuple[str, List]:
    """
    Parse optionsblock and formDefinition code blocks from text and return cleaned text + parts.

    Returns a tuple of (cleaned_text, parts) where parts contains instances of
    FormDefinitionOutputPart and OptionsBlockOutputPart.
    """
    if not text:
        return text, []

    special_parts = []
    cleaned_text = text

    # Pattern to match ```json blocks with formDefinition
    json_formdefinition_pattern = r"```json\s*\n(.*?)\n```"
    json_matches = re.findall(json_formdefinition_pattern, text, re.DOTALL)

    for match in json_matches:
        try:
            json_data = json.loads(match.strip())
            if isinstance(json_data, dict) and "formDefinition" in json_data:
                form_part = FormDefinitionOutputPart(definition=json_data["formDefinition"])
                special_parts.append(form_part)
            else:
                continue
        except json.JSONDecodeError:
            continue

    # Pattern to match ```optionsblock...``` blocks
    optionsblock_pattern = r"```optionsblock\s*\n(.*?)\n```"
    optionsblock_matches = re.findall(optionsblock_pattern, text, re.DOTALL)

    for match in optionsblock_matches:
        try:
            options_data = json.loads(match.strip())
            options_part = OptionsBlockOutputPart(definition=options_data)
            special_parts.append(options_part)
        except json.JSONDecodeError:
            continue

    # Remove all optionsblock code blocks from the text
    cleaned_text = re.sub(optionsblock_pattern, "", cleaned_text, flags=re.DOTALL)

    # Remove JSON blocks that contain formDefinition
    for match in json_matches:
        try:
            json_data = json.loads(match.strip())
            if isinstance(json_data, dict) and "formDefinition" in json_data:
                block_pattern = r"```json\s*\n" + re.escape(match) + r"\n```"
                cleaned_text = re.sub(block_pattern, "", cleaned_text, flags=re.DOTALL)
        except json.JSONDecodeError:
            continue

    # Clean up extra whitespace
    cleaned_text = re.sub(r"\n\s*\n\s*\n", "\n\n", cleaned_text).strip()

    return cleaned_text, special_parts
