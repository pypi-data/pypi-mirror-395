"""
Search Space Management Endpoints
Handles custom search space file creation, editing, validation, and management
"""

from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import Dict, Any, Optional
import tempfile

router = APIRouter(prefix="/search-space", tags=["search_space"])


@router.get("/template/{model_type}")
async def get_search_space_template(model_type: str):
    """Get default search space template for viewing"""
    try:
        from automar.shared.services.search_space_manager import strip_standard_imports

        # Normalize model type
        model_lower = model_type.lower()
        if model_lower == "log-reg":
            model_lower = "logreg"

        # Path to default template
        assets_dir = (
            Path(__file__).parent.parent.parent.parent
            / "shared"
            / "config"
            / "templates"
            / "hpt_defaults"
        )
        template_path = assets_dir / f"{model_lower}.py"

        if not template_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"No default template found for model type: {model_type}",
            )

        # Read template content and strip standard imports
        template_content = template_path.read_text()
        template_content = strip_standard_imports(template_content)

        return {
            "model_type": model_lower,
            "template_content": template_content,
            "default_path": str(template_path),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading template: {str(e)}")


@router.post("/generate/{model_type}")
async def generate_search_space(model_type: str, request: Dict[str, Any]):
    """Create a new custom search space file based on template"""
    try:
        from automar.shared.services.search_space_manager import (
            generate_search_space_filename,
            strip_standard_imports,
        )

        # Get custom name if provided
        custom_name = request.get("custom_name")

        # Normalize model type
        model_lower = model_type.lower()
        if model_lower == "log-reg":
            model_lower = "logreg"

        # Create output directory
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        search_spaces_dir = project_root / "out" / "search_spaces"
        search_spaces_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename
        filename = generate_search_space_filename(model_lower, custom_name)
        file_path = search_spaces_dir / filename

        # Read default template
        assets_dir = (
            Path(__file__).parent.parent.parent.parent
            / "shared"
            / "config"
            / "templates"
            / "hpt_defaults"
        )
        template_path = assets_dir / f"{model_lower}.py"

        if not template_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"No default template found for model type: {model_type}",
            )

        # Copy template content to new file (full content with imports)
        full_content = template_path.read_text()
        file_path.write_text(full_content)

        # Return stripped content for display (without imports)
        display_content = strip_standard_imports(full_content)

        return {
            "file_path": str(file_path.relative_to(project_root)),
            "content": display_content,
            "message": "Custom search space file created successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating search space: {str(e)}"
        )


@router.put("/update")
async def update_search_space(request: Dict[str, Any]):
    """Save edited search space code with validation"""
    try:
        from automar.shared.services.search_space_manager import (
            validate_search_space_file,
            restore_standard_imports,
        )

        file_path = request.get("file_path")
        content = request.get("content")

        if not file_path or not content:
            raise HTTPException(
                status_code=400, detail="file_path and content are required"
            )

        # Convert to absolute path
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        abs_file_path = project_root / file_path

        # Security check: ensure file is in out/search_spaces directory
        search_spaces_dir = project_root / "out" / "search_spaces"
        try:
            abs_file_path.relative_to(search_spaces_dir)
        except ValueError:
            raise HTTPException(
                status_code=403,
                detail="Can only modify files in out/search_spaces/ directory",
            )

        # Restore standard imports to content before validation/saving
        full_content = restore_standard_imports(content)

        # Write to temporary file for validation
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as tmp_file:
            tmp_file.write(full_content)
            tmp_file_path = tmp_file.name

        try:
            # Validate the temporary file (now with imports)
            is_valid, errors = validate_search_space_file(tmp_file_path)

            if not is_valid:
                return {
                    "status": "error",
                    "message": "Validation failed",
                    "validation_errors": errors,
                }

            # If valid, overwrite the original file with full content (including imports)
            abs_file_path.write_text(full_content)

            return {
                "status": "success",
                "message": "Search space validated and saved successfully",
                "validation_errors": [],
            }

        finally:
            # Clean up temporary file
            Path(tmp_file_path).unlink(missing_ok=True)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating search space: {str(e)}"
        )


@router.get("/file/{file_path:path}")
async def get_search_space_file(file_path: str):
    """Get a custom search space file content (with imports stripped for editing)"""
    try:
        from automar.shared.services.search_space_manager import strip_standard_imports

        # Convert to absolute path
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        abs_file_path = (project_root / file_path).resolve()

        # Security check: ensure file is in out/search_spaces directory
        search_spaces_dir = (project_root / "out" / "search_spaces").resolve()
        try:
            abs_file_path.relative_to(search_spaces_dir)
        except ValueError:
            raise HTTPException(
                status_code=403,
                detail="Can only read files from out/search_spaces/ directory",
            )

        if not abs_file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {file_path}",
            )

        # Read and strip imports
        content = abs_file_path.read_text()
        stripped_content = strip_standard_imports(content)

        return {
            "file_path": file_path,
            "content": stripped_content,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading search space file: {str(e)}"
        )


@router.get("/list")
async def list_search_spaces(model_type: Optional[str] = None):
    """List all custom search space files"""
    try:
        from automar.shared.services.search_space_manager import list_search_space_files

        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        search_spaces_dir = project_root / "out" / "search_spaces"

        # Normalize model type if provided
        if model_type:
            model_type = model_type.lower()
            if model_type == "log-reg":
                model_type = "logreg"

        search_spaces = list_search_space_files(search_spaces_dir, model_type)

        return {"search_spaces": search_spaces}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error listing search spaces: {str(e)}"
        )


@router.delete("/delete")
async def delete_search_space(request: Dict[str, Any]):
    """Delete a custom search space file"""
    try:
        file_path = request.get("file_path")

        if not file_path:
            raise HTTPException(status_code=400, detail="file_path is required")

        # Convert to absolute path
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        abs_file_path = project_root / file_path

        # Security check: ensure file is in out/search_spaces directory
        search_spaces_dir = project_root / "out" / "search_spaces"
        try:
            abs_file_path.relative_to(search_spaces_dir)
        except ValueError:
            raise HTTPException(
                status_code=403,
                detail="Can only delete files in out/search_spaces/ directory",
            )

        # Check file exists
        if not abs_file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        # Delete the file
        abs_file_path.unlink()

        return {
            "status": "success",
            "message": f"Deleted {file_path}",
            "deleted_file": file_path,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting search space: {str(e)}"
        )
