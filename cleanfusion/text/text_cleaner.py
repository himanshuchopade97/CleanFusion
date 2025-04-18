"""
Text cleaning module for preprocessing text data.
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from cleanfusion.utils.logger import Logger

# Download required NLTK resources
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt', quiet=True)


class TextCleaner:
    """
    Class for cleaning and preprocessing text data.
    
    Features:
    - Lowercasing
    - Special character removal
    - Stopword removal
    - Lemmatization
    - Negation handling
    """
    
    def __init__(self, remove_stopwords=True, lemmatize=True, handle_negation=True, preserve_structure=False):
        """
        Initialize the TextCleaner.
        
        Parameters
        ----------
        remove_stopwords : bool, default=True
            Whether to remove stopwords.
        
        lemmatize : bool, default=True
            Whether to apply lemmatization.
        
        handle_negation : bool, default=True
            Whether to handle negation (e.g., "not good" → "not_good").
        
        preserve_structure : bool, default=False
            Whether to preserve paragraph structure (line breaks).
        """
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        self.handle_negation = handle_negation
        self.preserve_structure = preserve_structure
        self.logger = Logger()
        
        # Initialize NLTK components
        self.stopwords = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
    
    def clean_text(self, text):
        """
        Clean and preprocess text.
        
        Parameters
        ----------
        text : str
            The input text to clean.
        
        Returns
        -------
        str
            The cleaned text.
        """
        if text is None:
            return ""
        
        # Convert to string if not already
        text = str(text)
        
        if not text.strip():
            return ""
        
        if self.preserve_structure:
            # Process each paragraph separately
            paragraphs = text.split('\n')
            cleaned_paragraphs = [self._clean_paragraph(p) for p in paragraphs]
            return '\n'.join(cleaned_paragraphs)
        else:
            return self._clean_paragraph(text)
    
    def _clean_paragraph(self, text):
        """Clean a single paragraph of text."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # Handle negation
        if self.handle_negation:
            text = self._handle_negation(text)
        
        # Tokenize
        words = text.split()
        
        # Remove stopwords
        if self.remove_stopwords:
            words = [word for word in words if word not in self.stopwords]
        
        # Lemmatize
        if self.lemmatize:
            words = [self.lemmatizer.lemmatize(word) for word in words]
        
        return ' '.join(words)
    
    def _handle_negation(self, text):
        """Handle negation by preserving 'not' with the next word."""
        words = text.split()
        negation_words = {"not", "no", "never", "n't"}
        cleaned_words = []
        skip_next = False
        
        for i, word in enumerate(words):
            if skip_next:
                skip_next = False
                continue
            if word in negation_words and i + 1 < len(words):
                cleaned_words.append(f"not_{words[i + 1]}")
                skip_next = True
            else:
                cleaned_words.append(word)
        
        return " ".join(cleaned_words)