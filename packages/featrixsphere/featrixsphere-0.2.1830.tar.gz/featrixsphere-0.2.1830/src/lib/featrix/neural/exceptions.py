#
#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Custom exceptions for Featrix neural network training.
"""


class FeatrixTrainingAbortedException(Exception):
    """
    Exception raised when training is aborted due to an ABORT file.
    
    This exception is raised when an ABORT file is detected in the job's output directory,
    indicating that training should be stopped immediately. This is different from a
    normal training failure - it's an explicit user/system request to abort.
    
    The ABORT file also prevents job restart after crashes, so this exception should
    be caught and the job should be marked as FAILED with an appropriate error message.
    """
    
    def __init__(self, message, job_id=None, abort_file_path=None):
        """
        Args:
            message: Human-readable description of why training was aborted
            job_id: Optional job ID for logging/debugging
            abort_file_path: Optional path to the ABORT file that triggered this
        """
        super().__init__(message)
        self.job_id = job_id
        self.abort_file_path = abort_file_path
    
    def __str__(self):
        base_msg = super().__str__()
        if self.job_id:
            return f"{base_msg} (job_id: {self.job_id})"
        return base_msg


class FeatrixRestartTrainingException(Exception):
    """
    Exception raised when training needs to be restarted with new parameters.
    
    This is used to signal that training has encountered a problem (e.g., dead gradients)
    and needs to restart from a checkpoint or current state with modified hyperparameters.
    
    The exception carries a RestartConfig object that specifies how to restart training.
    """
    
    def __init__(self, message, restart_config):
        """
        Args:
            message: Human-readable description of why restart is needed
            restart_config: RestartConfig object with restart parameters
        """
        super().__init__(message)
        self.restart_config = restart_config
        
    def __str__(self):
        return f"{super().__str__()} | Restart Config: {self.restart_config}"


class RestartConfig:
    """
    Configuration for restarting training after a failure or intervention.
    
    This object specifies how to modify training parameters when restarting.
    """
    
    def __init__(
        self,
        reason,
        epoch_detected,
        lr_multiplier=5.0,
        max_lr=0.01,
        reset_optimizer_state=True,
        reset_scheduler=False,
        load_best_checkpoint=False,
        additional_epochs=None,
        metadata=None
    ):
        """
        Args:
            reason: String describing why restart is needed (e.g., "DEAD_GRADIENTS")
            epoch_detected: Epoch number where problem was detected
            lr_multiplier: Multiply current LR by this factor (default 5.0)
            max_lr: Cap learning rate at this value (default 0.01)
            reset_optimizer_state: Clear momentum/adaptive terms (default True)
            reset_scheduler: Reset LR scheduler to initial state (default False)
            load_best_checkpoint: Reload best checkpoint before restarting (default False)
            additional_epochs: Add this many epochs to training (default None = no change)
            metadata: Dict of additional info for logging (default None)
        """
        self.reason = reason
        self.epoch_detected = epoch_detected
        self.lr_multiplier = lr_multiplier
        self.max_lr = max_lr
        self.reset_optimizer_state = reset_optimizer_state
        self.reset_scheduler = reset_scheduler
        self.load_best_checkpoint = load_best_checkpoint
        self.additional_epochs = additional_epochs
        self.metadata = metadata or {}
        
    def to_dict(self):
        """Convert to dictionary for JSON logging."""
        return {
            "reason": self.reason,
            "epoch_detected": self.epoch_detected,
            "lr_multiplier": self.lr_multiplier,
            "max_lr": self.max_lr,
            "reset_optimizer_state": self.reset_optimizer_state,
            "reset_scheduler": self.reset_scheduler,
            "load_best_checkpoint": self.load_best_checkpoint,
            "additional_epochs": self.additional_epochs,
            "metadata": self.metadata
        }
        
    def __repr__(self):
        return (
            f"RestartConfig(reason='{self.reason}', epoch={self.epoch_detected}, "
            f"lr_mult={self.lr_multiplier}x, reset_opt={self.reset_optimizer_state})"
        )

