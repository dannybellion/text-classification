"""DistilBERT model for text classification."""
import warnings
from typing import Dict, Optional, Tuple, Union

import torch
import torch.nn as nn
from transformers import AutoModelForSequenceClassification, logging as transformers_logging

# Suppress specific Hugging Face warnings
transformers_logging.set_verbosity_error()
warnings.filterwarnings("ignore", message="Some weights of BertForSequenceClassification were not initialized")
warnings.filterwarnings("ignore", message="Some weights of DistilBertForSequenceClassification were not initialized")


class DistilBERTClassifier(nn.Module):
    """DistilBERT-based classifier for loan default prediction."""
    
    def __init__(
        self, 
        model_name: str = "distilbert/distilbert-base-uncased", num_labels: int = 2
        ):
        """Initialize the transformer classifier.
        
        Args:
            model_name: Name of the pre-trained transformer model
            num_labels: Number of output classes
        """
        super().__init__()
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels
        )
        
    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        labels: Optional[torch.Tensor] = None
    ) -> Union[Dict[str, torch.Tensor], Tuple[torch.Tensor, torch.Tensor]]:
        """Forward pass.
        
        Args:
            input_ids: Token IDs
            attention_mask: Attention mask
            labels: Optional labels for computing loss
            
        Returns:
            If labels are provided, returns (loss, logits)
            Otherwise, returns a dictionary with 'logits'
        """
        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        
        if labels is not None:
            return outputs.loss, outputs.logits
        else:
            return {"logits": outputs.logits}