"""
Search space management utilities for custom search space files.
"""

import ast
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Standard imports that are always required (not editable by users)
STANDARD_IMPORTS = """import ray
from ray.tune.search import optuna
import optuna
"""


def strip_standard_imports(content: str) -> str:
    """
    Remove standard imports and function wrapper from search space content.
    Users only see/edit the dictionary structure.
    """
    lines = content.split("\n")

    # Find the return statement with the dict
    in_return_block = False
    dict_lines = []
    indent_to_remove = None

    for line in lines:
        # Skip imports
        if line.strip().startswith(("import ", "from ")):
            continue

        # Skip function definition line
        if line.strip().startswith("def get_search_space"):
            continue

        # Look for return { or return statement
        if "return {" in line or (line.strip() == "return {"):
            in_return_block = True
            # Extract just the dict part after 'return '
            dict_start = line.find("return ") + len("return ")
            dict_part = line[dict_start:]
            if dict_part.strip():
                dict_lines.append(dict_part)
            continue

        # Once in return block, collect all lines
        if in_return_block:
            # Determine indentation from first line
            if indent_to_remove is None and line.strip():
                indent_to_remove = len(line) - len(line.lstrip())

            # Remove the function body indentation
            if indent_to_remove and line.startswith(" " * indent_to_remove):
                dict_lines.append(line[indent_to_remove:])
            elif line.strip():
                dict_lines.append(line)
            else:
                dict_lines.append("")

    return "\n".join(dict_lines).strip()


def restore_standard_imports(content: str) -> str:
    """
    Add standard imports and function wrapper back to search space content before validation/saving.
    Users edit just the dict, but the file needs the full function structure.
    """
    # Check if already has full structure (imports + function)
    if "import ray" in content and "def get_search_space" in content:
        return content

    # Wrap the user's dict in the function structure
    # Indent the dict content by 4 spaces for function body
    indented_content = "\n".join(
        "    " + line if line.strip() else line for line in content.split("\n")
    )

    full_content = STANDARD_IMPORTS + "\n\n"
    full_content += "def get_search_space(input_dim):\n"
    full_content += "    return " + indented_content.lstrip()

    return full_content


def generate_search_space_filename(
    model_type: str, custom_name: Optional[str] = None
) -> str:
    """Generate filename for custom search space file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if custom_name:
        # Sanitize custom name (remove special chars)
        safe_name = "".join(c for c in custom_name if c.isalnum() or c in "-_")
        return f"{model_type}_{safe_name}_{timestamp}.py"
    return f"{model_type}_custom_{timestamp}.py"


def validate_search_space_file(file_path: str) -> Tuple[bool, List[str]]:
    """
    Validate a search space Python file structure.

    This validates:
    - Python syntax (with accurate line numbers for user-edited content)
    - Presence of get_search_space function
    - Required parameters
    - Required keys based on model type

    Returns:
        (is_valid, error_messages)
    """
    errors = []

    try:
        # Read file content (this has imports restored)
        content = Path(file_path).read_text()

        # For syntax validation, we need to validate the USER-VISIBLE content
        # (without the standard imports wrapper) to get accurate line numbers.
        # Strip imports to get what the user actually edited
        user_content = strip_standard_imports(content)

        # Validate syntax on user content for accurate line numbers
        try:
            ast.parse(user_content)
        except SyntaxError as e:
            # Extract line number and error details
            line_info = f" at line {e.lineno}" if e.lineno else ""
            col_info = f", column {e.offset}" if e.offset else ""
            error_msg = f"Python syntax error{line_info}{col_info}"
            if e.text:
                error_msg += f": {e.text.strip()}"
            if e.msg:
                error_msg += f" ({e.msg})"
            errors.append(error_msg)
            return False, errors

        # Now parse the full content (with imports) for structural validation
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # This shouldn't happen if user content parsed successfully
            errors.append("Unexpected error: Content with imports has syntax issues")
            return False, errors

        # Check for get_search_space function
        has_function = False
        function_has_param = False
        function_returns_dict = False

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "get_search_space":
                has_function = True

                # Check function has at least one parameter (input_dim)
                if len(node.args.args) >= 1:
                    function_has_param = True
                else:
                    errors.append(
                        "get_search_space function must accept at least one parameter (input_dim)"
                    )

                # Check function has a return statement
                for item in ast.walk(node):
                    if isinstance(item, ast.Return):
                        # Check if it returns a dict (simple check for dict literal)
                        if isinstance(item.value, ast.Dict):
                            function_returns_dict = True
                        break

                break

        if not has_function:
            errors.append("Missing required function: get_search_space")
            return False, errors

        if not function_has_param:
            return False, errors

        if not function_returns_dict:
            errors.append(
                "get_search_space should return a dictionary literal (detected simplified check)"
            )
            # This is a warning, not a hard error - function might build dict dynamically

        # Basic structure validation - check for required keys based on model type
        # Detect model type by looking at keys in the dict
        found_keys = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                for key in node.keys:
                    if isinstance(key, ast.Constant):
                        found_keys.add(key.value)

        # Determine if this is a log-reg or neural network (GRU/Transformer) search space
        logreg_keys = {"window_inc", "alphabet_size", "feature_selection"}
        neural_keys = {"model", "optimizer"}

        is_logreg = any(k in found_keys for k in logreg_keys)
        is_neural = any(k in found_keys for k in neural_keys)

        if is_logreg:
            # Validate log-reg structure
            required_logreg_keys = ["window_inc", "alphabet_size", "feature_selection"]
            missing = [k for k in required_logreg_keys if k not in found_keys]
            if missing:
                errors.append(f'Missing required log-reg keys: {", ".join(missing)}')
                return False, errors
        elif is_neural:
            # Validate neural network (GRU/Transformer) structure
            if "model" not in found_keys:
                errors.append(
                    'Missing required key in search space dictionary: "model" (should contain model architecture parameters)'
                )
            if "optimizer" not in found_keys:
                errors.append(
                    'Missing required key in search space dictionary: "optimizer" (should contain optimizer parameters)'
                )

            if "model" not in found_keys or "optimizer" not in found_keys:
                return False, errors
        else:
            # Can't determine type - might be custom structure
            errors.append(
                "Cannot determine search space type. Expected either:\n"
                "  - Log-reg keys: window_inc, alphabet_size, feature_selection\n"
                "  - Neural network keys: model, optimizer"
            )
            return False, errors

        return True, []

    except Exception as e:
        errors.append(f"Validation error: {str(e)}")
        return False, errors


def list_search_space_files(
    search_spaces_dir: Path, model_type: Optional[str] = None
) -> List[Dict]:
    """List all custom search space files."""
    if not search_spaces_dir.exists():
        return []

    pattern = f"{model_type}_*.py" if model_type else "*.py"
    files = sorted(
        search_spaces_dir.glob(pattern),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    # Get absolute search_spaces_dir for consistent path resolution
    abs_search_spaces_dir = search_spaces_dir.resolve()
    # Get project root for consistent path resolution
    from automar.shared.config.path_resolver import get_project_root

    project_root = get_project_root()

    result = []
    for file_path in files:
        # Parse filename: {model}_{name}_{timestamp}.py
        parts = file_path.stem.split("_")
        model = parts[0] if parts else "unknown"

        # Return path relative to project root for consistent resolution
        result.append(
            {
                "file_path": str(file_path.resolve().relative_to(project_root)),
                "model_type": model,
                "filename": file_path.name,
                "created_date": datetime.fromtimestamp(
                    file_path.stat().st_ctime
                ).isoformat(),
                "modified_date": datetime.fromtimestamp(
                    file_path.stat().st_mtime
                ).isoformat(),
                "file_size": file_path.stat().st_size,
            }
        )

    return result
