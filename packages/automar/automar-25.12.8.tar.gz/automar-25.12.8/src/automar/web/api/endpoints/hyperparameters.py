"""
Hyperparameter Management Endpoints
Handles TOML hyperparameter file creation, validation, and management
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from typing import Dict, Any, Optional

router = APIRouter(prefix="/hyperparameters", tags=["hyperparameters"])


@router.get("/template/{model_type}")
async def get_hyperparameter_template(model_type: str):
    """Get default hyperparameter template for a model"""
    try:
        from automar.shared.services.hyperparameter_manager import get_default_template
        import tomli_w

        # Normalize model type
        model_lower = model_type.lower()
        if model_lower == "log-reg":
            model_lower = "logreg"

        # Get template as dict
        template_dict = get_default_template(model_lower)

        if not template_dict:
            raise HTTPException(
                status_code=404,
                detail=f"No default template found for model type: {model_type}",
            )

        # Convert to TOML string
        template_toml = tomli_w.dumps(template_dict)

        return {
            "model_type": model_lower,
            "template_toml": template_toml,
            "template_object": template_dict,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting template: {str(e)}")


@router.post("/validate")
async def validate_hyperparameters_endpoint(request: Dict[str, Any]):
    """Validate hyperparameter TOML without saving"""
    try:
        from automar.shared.services.hyperparameter_manager import (
            validate_hyperparameters,
        )

        model_type = request.get("model_type")
        toml_content = request.get("toml_content")

        if not model_type or not toml_content:
            raise HTTPException(
                status_code=400, detail="model_type and toml_content are required"
            )

        # Normalize model type
        model_lower = model_type.lower()
        if model_lower == "log-reg":
            model_lower = "logreg"

        is_valid, errors, parsed_config = validate_hyperparameters(
            model_lower, toml_content
        )

        return {"is_valid": is_valid, "errors": errors, "parsed_config": parsed_config}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error validating hyperparameters: {str(e)}"
        )


@router.put("/update")
async def update_hyperparameters_endpoint(request: Dict[str, Any]):
    """Update existing hyperparameter file (overwrite)"""
    try:
        from automar.shared.services.hyperparameter_manager import (
            validate_hyperparameters,
        )

        file_path = request.get("file_path")
        toml_content = request.get("toml_content")
        model_type = request.get("model_type")

        if not file_path or not toml_content or not model_type:
            raise HTTPException(
                status_code=400,
                detail="file_path, toml_content, and model_type are required",
            )

        # Convert to absolute path
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        abs_file_path = project_root / file_path

        # Security check: ensure file is in allowed directories
        allowed_dirs = [
            project_root / "out" / "hyper" / "manual",
            project_root / "out" / "hyper",
        ]

        try:
            if not any(abs_file_path.is_relative_to(d) for d in allowed_dirs):
                raise ValueError("Invalid path")
        except (ValueError, Exception):
            raise HTTPException(
                status_code=403,
                detail="Can only modify files in out/hyper/ directories",
            )

        # Normalize model type
        model_lower = model_type.lower()
        if model_lower == "log-reg":
            model_lower = "logreg"

        # Validate first
        is_valid, errors, _ = validate_hyperparameters(model_lower, toml_content)

        if not is_valid:
            return {
                "status": "error",
                "message": "Validation failed",
                "validation_errors": errors,
            }

        # If valid, overwrite the file
        abs_file_path.write_text(toml_content)

        return {
            "status": "success",
            "message": "Hyperparameters validated and saved successfully",
            "validation_errors": [],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating hyperparameters: {str(e)}"
        )


@router.post("/save")
async def save_hyperparameters_endpoint(request: Dict[str, Any]):
    """Save manually-defined hyperparameters as TOML file (create new)"""
    try:
        from automar.shared.services.hyperparameter_manager import (
            validate_hyperparameters,
            save_manual_hyperparameters,
        )

        model_type = request.get("model_type")
        toml_content = request.get("toml_content")
        custom_name = request.get("custom_name")

        if not model_type or not toml_content:
            raise HTTPException(
                status_code=400, detail="model_type and toml_content are required"
            )

        # Normalize model type
        model_lower = model_type.lower()
        if model_lower == "log-reg":
            model_lower = "logreg"

        # Validate first
        is_valid, errors, _ = validate_hyperparameters(model_lower, toml_content)

        if not is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid hyperparameters: {', '.join(errors)}",
            )

        # Save to file
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        base_dir = project_root / "out" / "hyper" / "manual"

        file_path = save_manual_hyperparameters(
            model_lower, toml_content, custom_name, base_dir
        )

        return {
            "file_path": str(file_path.relative_to(project_root)),
            "message": "Hyperparameters saved successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving hyperparameters: {str(e)}"
        )


@router.get("/list-manual")
async def list_manual_hyperparameters(model_type: Optional[str] = None):
    """List all manually-created hyperparameter files"""
    try:
        from automar.shared.services.hyperparameter_manager import list_manual_configs

        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        base_dir = project_root / "out" / "hyper" / "manual"

        # Normalize model type if provided
        if model_type:
            model_type = model_type.lower()
            if model_type == "log-reg":
                model_type = "logreg"

        manual_configs = list_manual_configs(model_type, base_dir)

        return {"manual_configs": manual_configs}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error listing manual configs: {str(e)}"
        )


@router.get("/file/{file_path:path}")
async def get_hyperparameter_file(file_path: str):
    """Get hyperparameter file content by path"""
    try:
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        full_path = project_root / file_path

        # Security check: ensure file is within allowed directories
        allowed_dirs = [
            (project_root / "out" / "hyper" / "manual").resolve(),
            (project_root / "out" / "hyper").resolve(),
        ]

        resolved_path = full_path.resolve()
        if not any(
            resolved_path.is_relative_to(allowed_dir) for allowed_dir in allowed_dirs
        ):
            raise HTTPException(
                status_code=403, detail="Access to this file is not allowed"
            )

        if not resolved_path.exists():
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")

        # Read and return file content
        with open(resolved_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Return JSON without charset to avoid browser warnings
        return JSONResponse(content={"content": content}, media_type="application/json")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")


@router.delete("/delete")
async def delete_hyperparameter_file(request: Dict[str, Any]):
    """Delete a hyperparameter configuration file"""
    try:
        file_path = request.get("file_path")

        if not file_path:
            raise HTTPException(status_code=400, detail="file_path is required")

        # Convert to absolute path
        from automar.shared.config.path_resolver import get_project_root

        project_root = get_project_root()
        abs_file_path = project_root / file_path

        # Security check: ensure file is in allowed directories
        allowed_dirs = [
            project_root / "out" / "hyper" / "manual",
            project_root / "out" / "hyper",
        ]

        try:
            if not any(abs_file_path.is_relative_to(d) for d in allowed_dirs):
                raise ValueError("Invalid path")
        except (ValueError, Exception):
            raise HTTPException(
                status_code=403,
                detail="Can only delete files in out/hyper/ directories",
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
            status_code=500, detail=f"Error deleting hyperparameter file: {str(e)}"
        )
