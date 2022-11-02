from dataclasses import dataclass

"""
struct random word from server
{
    'word': 'word',
    'word_detail': [
        {
            'translate': 'translate',
            'example': 'example',
            'word_stat': {'pk': 7}
        }
    ]
}
"""


@dataclass
class ServerRandomWord:
    word: str
    translate: list[str]
    example: str
    all_pk: list[int]
    all_answer: list[str]
    choose_language: str
    step: int
    telegram_id: str


@dataclass
class CheckAnswer:
    server_word: ServerRandomWord
    status: str
