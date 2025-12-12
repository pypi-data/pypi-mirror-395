#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import logging
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from featrix.neural.single_predictor import FeatrixSinglePredictor

logger = logging.getLogger(__name__)

class TrainingState(Enum):
    TRAIN = 100
    EVAL = 222

class PredictorTrainingContextManager:

    def __init__(self, 
                 fsp: "FeatrixSinglePredictor", 
                 predictor_mode: TrainingState, 
                 encoder_mode: TrainingState, 
                 debugLabel=None):

        # logger.info(f"{debugLabel}: Setting predictor train state: modes = {predictor_mode}, encoder = {encoder_mode}")

        predictor = fsp.predictor
        es_encoder = fsp.embedding_space.encoder
        assert predictor is not None
        assert es_encoder is not None

        self.predictor = predictor
        self.es_encoder = es_encoder

        self.predictor_mode = predictor_mode
        self.encoder_mode = encoder_mode

        self.was_training_predictor = None
        self.was_training_encoder = None

        self._debugLabel = debugLabel or ""


    def __enter__(self):
        self.was_training_predictor = self.predictor.training
        self.was_training_encoder   = self.es_encoder.training
        
        if self.encoder_mode == TrainingState.TRAIN:
            self.es_encoder.train()
        else:
            self.es_encoder.eval()

        if self.predictor_mode == TrainingState.TRAIN:
            self.predictor.train()
        else:
            self.predictor.eval()
        return self
    

    def __exit__(self, exc_type, exc_value, traceback):
        assert self.was_training_predictor is not None
        assert self.was_training_encoder is not None

        if self.was_training_predictor:
            self.predictor.train()
        else:
            self.predictor.eval()

        if self.was_training_encoder:
            self.es_encoder.train()
        else:
            self.es_encoder.eval()

        return False # propogate exceptions


class PredictorEvalModeContextManager(PredictorTrainingContextManager):
    def __init__(self, fsp: "FeatrixSinglePredictor", debugLabel=None):
        super().__init__(
            fsp=fsp,
            predictor_mode=TrainingState.EVAL,
            encoder_mode=TrainingState.EVAL,
            debugLabel=debugLabel
        )
    