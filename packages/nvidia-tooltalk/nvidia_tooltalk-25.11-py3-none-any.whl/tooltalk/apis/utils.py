"""
Copyright (c) Microsoft Corporation.
Licensed under the MIT license.
"""
import re
from functools import lru_cache
from typing import Optional

import torch
from transformers import DistilBertModel, DistilBertTokenizer

import numpy as np


def verify_phone_format(phone_number: str) -> bool:
    match = re.match(r"^\d{3}-\d{3}-\d{4}$", phone_number)
    return match is not None


def verify_email_format(email: str) -> bool:
    match = re.match(r"^[\w\-\d\.]+@[\w\-\d\.]+$", email)
    return match is not None

class HFVectorizer:
    def __init__(self, model="distilbert-base-uncased"):
        self.tokenizer = DistilBertTokenizer.from_pretrained(model)
        self.model = DistilBertModel.from_pretrained(model)

    @lru_cache
    def __call__(self, text: str):
        with torch.no_grad():
            encoded_input = self.tokenizer(text, return_tensors='pt')
            output = self.model(**encoded_input)

        return np.array(output.last_hidden_state.squeeze()[0].cpu().numpy())


# TODO this is a hacky way to do this, but it works for now
_vectorize_text: callable = None


def semantic_str_compare(prediction_text: Optional[str], ground_truth_text: str) -> float:
    """
    Compares two strings semantically.
    """
    if prediction_text is None:
        return 0.0

    global _vectorize_text
    if _vectorize_text is None:
        # initialize vectorizer only when needed
        _vectorize_text = HFVectorizer()

    prediction_vec = _vectorize_text(prediction_text)
    ground_truth_vec = _vectorize_text(ground_truth_text)

    cosine_similarity = np.dot(prediction_vec, ground_truth_vec) / (np.linalg.norm(prediction_vec) * np.linalg.norm(ground_truth_vec))

    return cosine_similarity
