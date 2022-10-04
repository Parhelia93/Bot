import random

def get_random_word_detail(lst: list):
    random_word_detail = random.choice(lst)
    return random_word_detail.get('translate'), random_word_detail.get('example'), random_word_detail.get('word_stat').get('pk')

def get_all_translate(lst: list) -> list:
    return [n.get('translate') for n in lst]