"""Text Data Loader."""

import pandas as pd
from typing import Union, List


class TextLoader:
    """Load and preprocess text data."""
    
    def load(self, data: Union[str, List[str]]) -> pd.DataFrame:
        """Load text data."""
        if isinstance(data, str):
            # File path
            with open(data, 'r', encoding='utf-8') as f:
                texts = f.readlines()
        else:
            texts = data
        
        return pd.DataFrame({'text': texts})
