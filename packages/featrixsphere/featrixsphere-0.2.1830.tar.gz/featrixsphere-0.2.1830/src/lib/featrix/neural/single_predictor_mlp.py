#!/usr/bin/env python3
"""
Simplified SinglePredictorMLP class that wraps the entire single predictor training workflow.
"""
import pickle
from pathlib import Path
from typing import Optional

from featrix.neural.embedded_space import EmbeddingSpace
from featrix.neural.single_predictor import FeatrixSinglePredictor
from featrix.neural.simple_mlp import SimpleMLP
from featrix.neural.model_config import SimpleMLPConfig
from featrix.neural.input_data_file import FeatrixInputDataFile


class SinglePredictorMLP:
    """
    Simplified wrapper for training single predictors with automatic architecture selection.
    
    This class provides a streamlined interface for training neural network predictors on top
    of pre-trained embedding spaces. It features:
    
    🔬 AUTOMATIC DATASET COMPLEXITY ANALYSIS:
    ----------------------------------------
    When n_hidden_layers=None (default), the system automatically analyzes your dataset before
    training to determine optimal architecture. The analysis examines:
    
    1. **Feature-Target Correlations** (Mutual Information):
       - Weak correlations (MI < 0.15) → suggests nonlinear patterns → deeper network
       - Strong correlations (MI > 0.4) → suggests linear patterns → shallower network
    
    2. **Nonlinearity Detection**:
       - Tests if Random Forest significantly outperforms Linear Model
       - Strong nonlinearity (gain > 0.15) → deeper network recommended
    
    3. **Class Imbalance** (classification):
       - Detects severe imbalance and recommends proper weighting
       - Note: Handled via loss weighting, not architecture
    
    4. **Chi-Square Tests** (categorical targets):
       - Tests statistical independence between features and target
    
    🏗️ AUTOMATIC ARCHITECTURE SELECTION:
    -------------------------------------
    Based on analysis, selects 2-4 hidden layers with clear reasoning:
    
    - Simple linear problem: 2 layers
    - Moderate complexity: 2-3 layers
    - Complex nonlinear: 3-4 layers
    - Small dataset (<2k rows): capped at 2 layers
    
    The analysis takes 2-10 seconds but significantly improves model performance.
    
    Example usage:
    
    ```python
    # Load existing embedding space
    es = load_embedding_space("embedded_space.pickle")
    
    # Create predictor with AUTOMATIC architecture detection
    sp = SinglePredictorMLP(
        embedding_space=es,
        target_column="class",
        target_column_type="set",
        positive_label="good",
        n_hidden_layers=None  # Let system analyze and decide
    )
    
    # Train - analysis happens automatically before architecture is created
    sp.train(
        data_file="credit.csv",
        n_epochs=50,
        batch_size=128,
        use_class_weights=True  # Recommended for imbalanced data
    )
    
    # System will log:
    # 📊 DATASET COMPLEXITY ANALYSIS
    # 🔍 Feature-Target Relationship Analysis:
    #    • Mutual Information: 0.0425 (weak)
    # 🏗️ ARCHITECTURE DECISION: 3 hidden layers
    #    → Reasoning: Weak correlations suggest nonlinear patterns
    
    # Make predictions
    result = sp.predict({"age": 25, "income": 50000})
    ```
    
    Alternative: Specify architecture manually
    ```python
    # Skip analysis and use fixed architecture
    sp = SinglePredictorMLP(
        embedding_space=es,
        target_column="class",
        target_column_type="set",
        n_hidden_layers=3  # Fixed architecture
    )
    sp.train(data_file="credit.csv")
    ```
    
    Handling imbalanced datasets:
    ```python
    sp = SinglePredictorMLP(
        embedding_space=es,
        target_column="approved",
        target_column_type="set",
        positive_label="rejected"
    )
    
    # Production has 97% approved, 3% rejected
    # But training data is balanced 50/50
    sp.train(
        data_file="loans.csv",
        use_class_weights=True,
        class_imbalance={"approved": 0.97, "rejected": 0.03}
    )
    ```
    
    Args:
        embedding_space: Pre-trained EmbeddingSpace
        target_column: Name of target column to predict
        target_column_type: "set" (classification) or "scalar" (regression)
        positive_label: Positive label for binary classification (optional)
        d_hidden: Hidden layer dimension (default: 256)
        n_hidden_layers: Number of hidden layers (None = auto-detect from data, or 2-4)
        dropout: Dropout rate (default: 0.1)
    
    What you get:
        - Automatic complexity analysis (when n_hidden_layers=None)
        - Optimal architecture matched to your problem
        - Clear explanations of architectural decisions
        - Better performance than one-size-fits-all
        - Transparent logging of all decisions
    """
    
    def __init__(
        self,
        embedding_space: EmbeddingSpace,
        target_column: str,
        target_column_type: str,  # "set" or "scalar"
        positive_label: Optional[str] = None,
        d_hidden: int = 256,
        n_hidden_layers: int = None,  # None = auto-detect
        dropout: float = 0.3,  # Increased from 0.1 to prevent overfitting on imbalanced data
        name: Optional[str] = None,
    ):
        """
        Initialize SinglePredictorMLP.
        
        Args:
            embedding_space: Pre-trained EmbeddingSpace
            target_column: Name of target column to predict
            target_column_type: "set" (classification) or "scalar" (regression)
            positive_label: Positive label for binary classification (optional)
            d_hidden: Hidden layer dimension
            n_hidden_layers: Number of hidden layers (None = auto-detect from data)
            dropout: Dropout rate
            name: Name for the predictor (optional, auto-generated if not provided)
        """
        self.es = embedding_space
        self.target_column = target_column
        self.target_column_type = target_column_type
        self.positive_label = positive_label
        self.d_hidden = d_hidden
        self.dropout = dropout
        self.name = name or f"{target_column}_predictor"
        
        # Defer predictor creation until train() if n_hidden_layers is None
        # This allows us to analyze the data first
        if n_hidden_layers is not None:
            self._create_predictor(n_hidden_layers)
        else:
            self.fsp = None  # Will be created in train()
        
        self.trained = False
        self.training_data_file = None
    
    def _create_predictor(self, n_hidden_layers: int):
        """Create the predictor MLP with specified architecture."""
        d_model = self.es.d_model
        config = SimpleMLPConfig(
            d_in=d_model,
            d_out=2,  # Will be set by prep_for_training
            d_hidden=self.d_hidden,
            n_hidden_layers=n_hidden_layers,
            dropout=self.dropout,
            normalize=False,
            residual=True,
            use_batch_norm=True,
        )
        predictor = SimpleMLP(config)
        
        # Create FeatrixSinglePredictor with name
        self.fsp = FeatrixSinglePredictor(self.es, predictor, name=self.name)
        
    def train(
        self,
        data_file: str,
        n_epochs: int = 50,
        batch_size: int = 0,  # 0 = auto
        learning_rate: float = 0.0001,
        fine_tune: bool = False,
        use_class_weights: bool = False,
        class_imbalance: dict = None,
    ):
        """
        Train the single predictor.
        
        Args:
            data_file: Path to training data CSV file
            n_epochs: Number of training epochs
            batch_size: Training batch size (0 = auto)
            learning_rate: Learning rate
            fine_tune: Whether to fine-tune the embedding space
            use_class_weights: Whether to use class weighting for imbalanced data
            class_imbalance: Optional dict with expected class ratios/counts from real world
                           (for set codec only, when data has been sampled down)
            
        Returns:
            Training results dict
        """
        # Load data
        input_file = FeatrixInputDataFile(data_file)
        train_df = input_file.df
        self.training_data_file = data_file
        
        # If predictor not created yet, analyze data and create optimal architecture
        if self.fsp is None:
            from featrix.neural.utils import analyze_dataset_complexity, ideal_single_predictor_hidden_layers
            
            print("=" * 80)
            print("🔍 ANALYZING DATASET TO DETERMINE OPTIMAL ARCHITECTURE")
            print("=" * 80)
            
            # Analyze complexity
            complexity_analysis = analyze_dataset_complexity(
                train_df=train_df,
                target_column=self.target_column,
                target_column_type=self.target_column_type
            )
            
            # Determine optimal architecture
            n_hidden_layers = ideal_single_predictor_hidden_layers(
                n_rows=len(train_df),
                n_cols=len(train_df.columns),
                d_model=self.es.d_model,
                fine_tune=fine_tune,
                complexity_analysis=complexity_analysis
            )
            
            print(f"\n✅ Creating predictor with {n_hidden_layers} hidden layers")
            print("=" * 80)
            
            # Now create the predictor
            self._create_predictor(n_hidden_layers)
        
        # Prep for training
        self.fsp.prep_for_training(
            train_df=train_df,
            target_col_name=self.target_column,
            target_col_type=self.target_column_type,
            use_class_weights=use_class_weights,
            class_imbalance=class_imbalance
        )
        
        # Train
        training_results = self.fsp.train(
            train_df=train_df,
            n_epochs=n_epochs,
            batch_size=batch_size,
            learning_rate=learning_rate,
            positive_label=self.positive_label,
            fine_tune=fine_tune,
        )
        
        self.trained = True
        return training_results
    
    def predict(self, record: dict):
        """
        Make a prediction on a single record.
        
        Args:
            record: Dictionary with feature values
            
        Returns:
            Prediction result
        """
        if not self.trained:
            raise RuntimeError("Model not trained yet. Call train() first.")
        
        return self.fsp.predict(record)
    
    def save(self, path: str):
        """Save the trained predictor to disk."""
        if not self.trained:
            raise RuntimeError("Model not trained yet. Call train() first.")
        
        with open(path, 'wb') as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load(path: str):
        """Load a trained predictor from disk."""
        with open(path, 'rb') as f:
            return pickle.load(f)


def load_embedding_space(path: str) -> EmbeddingSpace:
    """Load a pickled embedding space from disk."""
    with open(path, 'rb') as f:
        return pickle.load(f)

