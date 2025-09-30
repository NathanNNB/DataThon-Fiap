"""Module responsible for preprocessing methods."""

import re
from typing import List
from unidecode import unidecode

import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk import word_tokenize






class TextPreprocessing:
    """class responsible for TextPreprocessing methods."""

    def preprocess_text(
        self,
        texts: List[str],
        apply_lower: bool = False,
        remove_ponctuation: bool = False,
        remove_numbers: bool = False,
        clean_html: bool = False,
        apply_unidecode: bool = False,
        remove_stopwords: bool = False,
        remove_duplicates: bool = False,
    ) -> str:
        """Preprocess text.

        Args:
            text (str): Text.
            apply_lower (bool, optional): Lowercase the text or not. Defaults to False.
            remove_ponctuation (bool, optional): Remove ponctuation or not. Defaults to False.
            remove_numbers (bool, optional): Remove numbers or not. Defaults to False.
            clean_html (bool, optional): Clean html or not. Defaults to False.
            apply_unidecode (bool, optional): Apply unidecode or not. Defaults to False.
            remove_stopwords (bool, optional): Remove stopwords or not. Defaults to False.
            remove_duplicates (bool, optional): Remove duplicate words or not. Defaults to False.

        Returns:
            str: Text preprocessed.
        """
        text = self.unify_text(texts) if len(texts) > 1 else texts[0]
        text = text.lower() if apply_lower else text
        text = re.sub(r"[^\w\s]", " ", text) if remove_ponctuation else text
        text = re.sub(r"[0-9]+", "", text) if remove_numbers else text
        text = re.sub(r"<.*?>", "", text) if clean_html else text
        text = unidecode(text) if apply_unidecode else text
        text = self.remove_stopwords(text) if remove_stopwords else text
        text = self.remove_duplicates(text) if remove_duplicates else text
        return text
    
    def unify_text(self, texts: List[str]) -> str:
        """Unify a list of texts into a single text.

        Args:
            texts (List[str]): List of texts.

        Returns:
            str: Unified text.
        """
        return "\n\n".join(texts)


    def remove_duplicates(self, text: str) -> str:
        """Remove duplicate words.

        Args:
            text (str): Text.

        Returns:
            str: Text without duplicate words.
        """
        tokens = text.split()
        seen = set()
        unique_tokens = []
        for token in tokens:
            if token not in seen:
                seen.add(token)
                unique_tokens.append(token)
        return " ".join(unique_tokens)

    def get_stopwords(self) -> List[str]:
        """Get stopwords and add custom stopwords.

        Returns:
            List[str]: List of stopwords.
        """
        words = stopwords.words("portuguese")

        stopwords_list = ['nenhum', 'etc', 'ter',' sobre']
        words.extend(stopwords_list)
        return words

    def remove_stopwords(self, text: str) -> str:
        """Remove stopwords.

        Args:
            text (str): Text.

        Returns:
            str: Text without stopwords.
        """
        stop_words = set(self.get_stopwords())
        tokens = word_tokenize(text)
        valid_tokens = [token for token in tokens if token not in stop_words]
        return " ".join(valid_tokens)