import random
from typing import Any, List

from ..exceptions import ConversionError


class LoremIpsumGenerator:
    name = "lorem_ipsum"

    def __init__(self) -> None:
        self.words_pool = (
            "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua "
            "ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis aute irure dolor "
            "in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident "
            "sunt in culpa qui officia deserunt mollit anim id est laborum"
        ).split()

    def _pick_words(self, count: int) -> List[str]:
        if not isinstance(count, int):
            raise ConversionError("Word count must be int")
        if count <= 0:
            raise ConversionError("Word count must be positive")
        return [random.choice(self.words_pool) for _ in range(count)]

    def _make_sentence(self, words_count: int) -> str:
        words = self._pick_words(words_count)
        text = " ".join(words)
        return text.capitalize() + "."

    def _make_paragraph(self, sentences: int, words_per_sentence: int) -> str:
        if not isinstance(sentences, int):
            raise ConversionError("Sentence count must be int")
        if sentences <= 0:
            raise ConversionError("Sentence count must be positive")
        return " ".join(self._make_sentence(words_per_sentence) for _ in range(sentences))

    def generate(self, **kwargs: Any) -> str:
        words = kwargs.get("words")
        sentences = kwargs.get("sentences")
        paragraphs = kwargs.get("paragraphs")
        words_per_sentence = kwargs.get("words_per_sentence", 12)
        sentences_per_paragraph = kwargs.get("sentences_per_paragraph", 4)

        provided = [p is not None for p in (words, sentences, paragraphs)]
        if sum(provided) > 1:
            raise ConversionError("Use only one of words, sentences, or paragraphs")

        if paragraphs is not None:
            if not isinstance(paragraphs, int):
                raise ConversionError("Paragraph count must be int")
            return "\n\n".join(
                self._make_paragraph(sentences_per_paragraph, words_per_sentence) for _ in range(paragraphs)
            )
        if sentences is not None:
            if not isinstance(sentences, int):
                raise ConversionError("Sentence count must be int")
            return " ".join(self._make_sentence(words_per_sentence) for _ in range(sentences))
        if words is not None:
            return " ".join(self._pick_words(words))
        return " ".join(self._pick_words(10))

