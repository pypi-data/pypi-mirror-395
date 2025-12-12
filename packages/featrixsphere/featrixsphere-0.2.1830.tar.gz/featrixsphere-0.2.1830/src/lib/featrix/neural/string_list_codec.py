"""
String List Codec - encodes lists of strings by averaging individual string embeddings.

This codec handles various list formats:
- Python lists: ['apple', 'banana', 'cherry']
- JSON arrays: ["red", "blue", "green"]
- Delimited strings: "cat,dog,bird" or "item1|item2|item3"

Strategy: Use the string encoder on each list element, then average the resulting vectors.
This preserves semantic meaning while handling variable-length lists efficiently.
"""

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from featrix.training.model_config import ColumnType
from featrix.utils.featrix_token import Token, TokenStatus
from featrix.codecs.string_codec import StringCodec


class StringListCodec(nn.Module):
    """
    Codec for lists of strings using averaged string embeddings.
    
    Process:
    1. Parse each value into a list of strings 
    2. Use StringCodec to encode each string element
    3. Average the embeddings to get a fixed-size representation
    4. Handle variable-length lists gracefully
    """
    
    def __init__(self, detector, enc_dim: int = 64, string_cache=None):
        super().__init__()
        
        if not hasattr(detector, 'string_elements'):
            raise ValueError(f"Detector must have string_elements for StringListCodec. Got detector type: {type(detector)}, detector name: {getattr(detector, '_debugColName', 'unknown')}")
        
        if not detector.string_elements:
            # Provide a default single empty string element if string_elements is empty
            detector.string_elements = {""}
        
        self.detector = detector
        self.enc_dim = enc_dim
        self.string_cache = string_cache
        
        # Create a StringCodec for encoding individual string elements
        # Use all unique string elements found during detection
        string_elements_list = list(detector.string_elements) if detector.string_elements else [""]
        
        # Create a fake DataFrame column with our string elements for the StringCodec
        string_series = pd.Series(string_elements_list)
        
        self.string_codec = StringCodec(
            enc_dim=enc_dim,
            debugName=f"{detector._debugColName}_string_list",
            initial_values=string_elements_list,
            string_cache=string_cache
        )
        
        # Linear projection from string embedding dim to target enc_dim
        string_embedding_dim = self.string_codec.d_string_model  # 384
        self.embedding_projection = nn.Linear(string_embedding_dim, enc_dim)
        
        # Linear decoder from averaged embedding back to... well, we can't really decode lists
        # But we need this for the codec interface
        self.decoder = nn.Linear(enc_dim, 1)
        self.loss_fn = nn.MSELoss()
        
        # Initialize layers
        nn.init.xavier_uniform_(self.embedding_projection.weight, gain=0.1)
        nn.init.zeros_(self.embedding_projection.bias)
        nn.init.xavier_uniform_(self.decoder.weight, gain=0.1)
        nn.init.zeros_(self.decoder.bias)

    def get_codec_name(self):
        return ColumnType.STRING_LIST

    def get_codec_info(self):
        return {
            "list_format": getattr(self.detector, 'list_format', 'unknown'),
            "delimiter": getattr(self.detector, 'delimiter', None),
            "unique_string_elements": len(self.detector.string_elements) if self.detector.string_elements else 0,
            "enc_dim": self.enc_dim
        }

    def get_not_present_token(self):
        return Token(
            value=np.zeros(self.enc_dim, dtype=np.float32),
            status=TokenStatus.NOT_PRESENT,
        )

    def get_marginal_token(self):
        """Return a token representing a masked/marginal value for reconstruction testing."""
        return Token(
            value=np.zeros(self.enc_dim, dtype=np.float32),
            status=TokenStatus.MARGINAL,
        )

    def parse_list_value(self, value):
        """Parse a single value into a list of strings using the detector's logic"""
        if hasattr(self.detector, 'parse_list_value'):
            return self.detector.parse_list_value(value)
        else:
            # Fallback parsing
            if pd.isna(value) or value is None:
                return []
            
            str_val = str(value).strip()
            
            # Try JSON array
            try:
                import json
                if str_val.startswith('[') and str_val.endswith(']'):
                    parsed = json.loads(str_val)
                    if isinstance(parsed, list):
                        return [str(item) for item in parsed]
            except:
                pass
            
            # Try Python list
            try:
                import ast
                if str_val.startswith('[') and str_val.endswith(']'):
                    parsed = ast.literal_eval(str_val)
                    if isinstance(parsed, list):
                        return [str(item) for item in parsed]
            except:
                pass
            
            # Try common delimiters
            for delimiter in [',', ';', '|', '/', '-']:
                if delimiter in str_val:
                    parts = [part.strip() for part in str_val.split(delimiter)]
                    if len(parts) >= 2:
                        return [p for p in parts if p]
            
            return []

    def tokenize(self, value):
        """Convert a single list value to averaged string embeddings"""
        if pd.isna(value) or value is None:
            return self.get_not_present_token()
        
        # Parse value into list of strings
        string_list = self.parse_list_value(value)
        
        if not string_list:
            # Empty list - use zero vector
            return Token(
                value=np.zeros(self.enc_dim, dtype=np.float32),
                status=TokenStatus.NOT_PRESENT,
            )
        
        # Encode each string in the list
        string_embeddings = []
        for string_item in string_list:
            if string_item:  # Skip empty strings
                # Use the string codec to get embedding for this string
                string_token = self.string_codec.tokenize(string_item)
                if string_token and hasattr(string_token, 'value'):
                    # Get the embedding (this might need adjustment based on StringCodec interface)
                    embedding = string_token.value
                    if isinstance(embedding, torch.Tensor):
                        embedding = embedding.detach().cpu().numpy()
                    string_embeddings.append(embedding)
        
        if string_embeddings:
            # Average all string embeddings
            averaged_embedding = np.mean(string_embeddings, axis=0)
            
            # Project to target dimension
            averaged_tensor = torch.from_numpy(averaged_embedding).unsqueeze(0)  # Add batch dim
            projected_embedding = self.embedding_projection(averaged_tensor).squeeze(0)  # Remove batch dim
            
            return Token(
                value=projected_embedding.detach().numpy().astype(np.float32),
                status=TokenStatus.OK,
            )
        else:
            # No valid strings found
            return Token(
                value=np.zeros(self.enc_dim, dtype=np.float32),
                status=TokenStatus.UNKNOWN,
            )

    def detokenize(self, embeddings):
        """
        Can't really detokenize averaged embeddings back to original lists,
        but we can return a placeholder representation
        """
        results = []
        batch_size = embeddings.shape[0] if len(embeddings.shape) > 1 else 1
        
        for i in range(batch_size):
            # Just return a placeholder - we can't meaningfully reconstruct lists
            results.append("[reconstructed_list]")
        
        return results

    def compute_loss(self, embeddings, target_tokens):
        """
        Compute loss for string list embeddings.
        Since we're dealing with averaged embeddings, we'll use a simple reconstruction loss.
        """
        # Extract target embeddings
        target_embeddings = []
        for token in target_tokens:
            if token.status == TokenStatus.OK:
                if isinstance(token.value, np.ndarray):
                    target_embeddings.append(torch.from_numpy(token.value))
                else:
                    target_embeddings.append(token.value)
            else:
                target_embeddings.append(torch.zeros(self.enc_dim))
        
        target_tensor = torch.stack(target_embeddings).to(embeddings.device)
        
        # Simple MSE loss between embeddings
        loss = self.loss_fn(embeddings, target_tensor)
        
        return loss

    def forward(self, x):
        """Forward pass - embeddings are already computed in tokenize"""
        return x

    def save(self):
        """Save codec state"""
        return {
            "type": "StringListCodec",
            "enc_dim": self.enc_dim,
            "detector_info": {
                "list_format": getattr(self.detector, 'list_format', 'unknown'),
                "delimiter": getattr(self.detector, 'delimiter', None),
                "string_elements": list(self.detector.string_elements) if self.detector.string_elements else []
            },
            "string_codec_state": self.string_codec.save() if hasattr(self.string_codec, 'save') else None,
            "state_dict": self.state_dict()
        }

    def load(self, data):
        """Load codec state"""
        self.enc_dim = data["enc_dim"]
        
        # Recreate detector info
        detector_info = data.get("detector_info", {})
        if hasattr(self.detector, 'list_format'):
            self.detector.list_format = detector_info.get("list_format", "unknown")
        if hasattr(self.detector, 'delimiter'):
            self.detector.delimiter = detector_info.get("delimiter")
        if hasattr(self.detector, 'string_elements'):
            self.detector.string_elements = set(detector_info.get("string_elements", []))
        
        # Load string codec if available
        if "string_codec_state" in data and data["string_codec_state"]:
            if hasattr(self.string_codec, 'load'):
                self.string_codec.load(data["string_codec_state"])
        
        if "state_dict" in data:
            self.load_state_dict(data["state_dict"])


def create_string_list_codec(detector, embed_dim: int = 64, string_cache=None):
    """Create string list codec from detector"""
    return StringListCodec(detector, embed_dim, string_cache) 