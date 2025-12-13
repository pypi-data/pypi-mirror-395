"""
Pydantic models and response schemas for the API.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class ExtractResponse(BaseModel):
    status: str
    message: str
    rows: Optional[int] = None
    columns: Optional[int] = None
    file_path: Optional[str] = None
    operation_id: Optional[str] = None


class PCAResponse(BaseModel):
    status: str
    message: str
    n_components: Optional[int] = None
    explained_variance: Optional[List[float]] = None
    file_paths: Optional[Dict[str, str]] = None


class TuningResponse(BaseModel):
    status: str
    message: str
    best_params: Optional[Dict[str, Any]] = None
    best_score: Optional[float] = None
    config_path: Optional[str] = None


class TrainingResponse(BaseModel):
    status: str
    message: str
    mdl_path: Optional[str] = None
    metrics: Optional[Dict[str, float]] = None


class CrossvalidateResponse(BaseModel):
    status: str
    message: str
    results_path: Optional[str] = None
    cv_scores: Optional[List[float]] = None
    mean_score: Optional[float] = None
    std_score: Optional[float] = None


class PredictionResponse(BaseModel):
    status: str
    message: str
    job_id: str
    check_status_at: str


class TuningProgress(BaseModel):
    total_trials: int = 0
    completed_trials: int = 0
    running_trials: int = 0
    best_score: Optional[float] = None
    best_params: Optional[Dict[str, Any]] = None
    current_trial_params: Optional[Dict[str, Any]] = None
    trial_history: List[Dict[str, Any]] = []
    estimated_time_remaining: Optional[int] = None  # seconds
    start_time: Optional[str] = None
    last_update: Optional[str] = None


class JobStatus(BaseModel):
    job_id: str
    status: str  # "pending", "running", "completed", "failed", "cancelled"
    type: Optional[str] = (
        None  # "extract", "pca", "tuning", "training", "crossvalidate"
    )
    model: Optional[str] = None  # Model type for tuning/training jobs
    result: Optional[Any] = None
    error: Optional[str] = None
    progress: Optional[TuningProgress] = None
    inputs: Optional[Dict[str, Any]] = None  # Store input parameters
    timing: Optional[Dict[str, Any]] = None  # Store timing information
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    context: Optional[Dict[str, Any]] = None  # Job context (with_pca, industry, etc.)


class TuningProgressCallback:
    """Ray Tune callback for real-time progress tracking."""

    def __init__(self, job_id: str, cfg):
        self.job_id = job_id
        self.cfg = cfg
        self.start_time = datetime.now()
        self.completed_trials = set()  # Track unique completed trials
        self.running_trials = set()  # Track unique running trials

    # Required Ray Tune callback methods (all must be present)
    def setup(self, *args, **kwargs):
        pass

    def on_step_begin(self, *args, **kwargs):
        pass

    def on_step_end(self, *args, **kwargs):
        pass

    def on_experiment_end(self, *args, **kwargs):
        pass

    def on_trial_complete(self, *args, **kwargs):
        pass

    def on_trial_error(self, *args, **kwargs):
        pass

    def on_trial_recover(self, *args, **kwargs):
        pass

    def on_trial_restore(self, *args, **kwargs):
        pass

    def on_trial_save(self, *args, **kwargs):
        pass

    def on_checkpoint(self, *args, **kwargs):
        pass

    def get_state(self):
        return {}

    def set_state(self, state):
        pass

    def is_cancelled(self):
        """Check if job has been cancelled"""
        # Import here to avoid circular dependency
        from automar.web.api.jobs import get_job_store

        job_store = get_job_store()
        return job_store.is_cancelled(self.job_id)

    def on_trial_start(self, iteration, trials, trial, **info):
        """Called when a trial starts"""
        # Import here to avoid circular dependency
        from automar.web.api.jobs import get_job, update_job

        if self.is_cancelled():
            raise KeyboardInterrupt("Job cancelled by user")

        job = get_job(self.job_id)
        if job and job.progress:
            progress = job.progress
            self.running_trials.add(trial.trial_id)
            progress.running_trials = len(self.running_trials)
            progress.last_update = datetime.now().isoformat()
            update_job(self.job_id, {"progress": progress})

    def on_trial_result(self, iteration, trials, trial, result, **info):
        """Called when a trial reports a result"""
        # Import here to avoid circular dependency
        from automar.web.api.jobs import get_job, update_job

        job = get_job(self.job_id)
        if job and job.progress:
            progress = job.progress
            if progress:
                trial_id = trial.trial_id
                if trial_id not in self.completed_trials:
                    self.completed_trials.add(trial_id)

                self.running_trials.discard(trial_id)

                progress.completed_trials = len(self.completed_trials)
                progress.running_trials = len(self.running_trials)
                progress.last_update = datetime.now().isoformat()

                score = result.get(
                    "AUROC", result.get("score", result.get("accuracy", 0))
                )

                if progress.best_score is None or score > progress.best_score:
                    progress.best_score = score
                    progress.best_params = trial.config
                    progress.current_trial_params = trial.config

                current_time = datetime.now()
                elapsed_time = (current_time - self.start_time).total_seconds()

                if progress.completed_trials > 0:
                    avg_time_per_trial = elapsed_time / progress.completed_trials
                    remaining_trials = max(
                        0, self.cfg.tune.num_samples - progress.completed_trials
                    )
                    progress.estimated_time_remaining = max(
                        0, int(avg_time_per_trial * remaining_trials)
                    )
                else:
                    progress.estimated_time_remaining = None

                trial_result = {
                    "trial_id": trial_id,
                    "score": score,
                    "params": trial.config,
                    "timestamp": progress.last_update,
                }

                if (
                    not hasattr(progress, "trial_history")
                    or progress.trial_history is None
                ):
                    progress.trial_history = []

                progress.trial_history.append(trial_result)
                if len(progress.trial_history) > 10:
                    progress.trial_history = progress.trial_history[-10:]

                update_job(self.job_id, {"progress": progress})
