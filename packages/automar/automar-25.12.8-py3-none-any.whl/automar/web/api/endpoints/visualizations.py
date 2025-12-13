# -*- coding: utf-8 -*-
"""
Visualization endpoints for Automar API

These endpoints provide data for visualizing job results including:
- Confusion matrices
- Cross-validation results
- Training history
- Hyperparameter tuning statistics
- PCA analysis
- Extraction summaries
- Prediction probabilities
- Growing windows analysis
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/visualize", tags=["visualizations"])


@router.get("/available/{job_id}")
async def get_available_visualizations(job_id: str):
    """Get list of available visualizations for a completed job"""
    try:
        from automar.shared.services.visualization_utils import (
            load_job_visualization_data,
        )

        data = load_job_visualization_data(job_id)
        return data

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/confusion-matrix/{job_id}")
async def get_confusion_matrix_visualization(job_id: str):
    """Get confusion matrix data for visualization"""
    try:
        from automar.shared.services.visualization_utils import (
            prepare_confusion_matrix_data,
        )

        data = prepare_confusion_matrix_data(job_id)
        return data

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cross-validation/{job_id}")
async def get_cross_validation_visualization(job_id: str):
    """Get cross-validation results for visualization"""
    try:
        from automar.shared.services.visualization_utils import (
            prepare_cross_validation_data,
        )

        data = prepare_cross_validation_data(job_id)
        return data

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/training-history/{job_id}")
async def get_training_history_visualization(job_id: str):
    """Get training history for visualization"""
    try:
        from automar.shared.services.visualization_utils import (
            prepare_training_history_data,
        )

        data = prepare_training_history_data(job_id)
        return data

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tuning-statistics/{job_id}")
async def get_tuning_statistics_visualization(job_id: str):
    """Get hyperparameter tuning statistics for visualization"""
    try:
        from automar.shared.services.visualization_utils import (
            prepare_tuning_statistics_data,
        )

        data = prepare_tuning_statistics_data(job_id)
        return data

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pca-analysis")
async def get_pca_analysis_visualization(pca_file_path: str = Query(...)):
    """Get PCA analysis data for visualization"""
    try:
        from automar.shared.services.visualization_utils import (
            prepare_pca_analysis_data,
        )

        data = prepare_pca_analysis_data(pca_file_path)
        return data

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/extraction-summary/{job_id}")
async def get_extraction_summary_visualization(job_id: str):
    """Get extraction summary data for visualization"""
    try:
        from automar.shared.services.visualization_utils import (
            prepare_extraction_summary_data,
        )

        data = prepare_extraction_summary_data(job_id)
        return data

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/prediction-probability/{job_id}")
async def get_prediction_probability_visualization(job_id: str):
    """Get prediction probability for next trading day"""
    try:
        from automar.shared.services.visualization_utils import (
            prepare_prediction_probability_data,
        )

        data = prepare_prediction_probability_data(job_id)
        return data

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/growing-windows/{job_id}")
async def get_growing_windows_visualization(job_id: str):
    """Get growing windows data splits visualization"""
    try:
        from automar.shared.services.visualization_utils import (
            prepare_growing_windows_data,
        )

        data = prepare_growing_windows_data(job_id)
        return data

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
