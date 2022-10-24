import random

def get_random_word_detail(lst: list):
    random_word_detail = random.choice(lst)
    return random_word_detail.get('example'), random_word_detail.get('word_stat').get('pk')

def get_all_translate(lst: list) -> list:
    return [n.get('translate') for n in lst]

def get_all_pk(lst: list) -> list:
    return [n.get('word_stat').get('pk') for n in lst]

def prepare_dict(dct: dict, choose_str: str) -> dict:
    word_detail_list = dct.get('words_detail')
    random_word_detail_exaple, random_word_detail_pk = get_random_word_detail(word_detail_list)
    if choose_str == "En-Rus":
        return dict(word=dct.get('word'), translate_list=get_all_translate(word_detail_list), example=random_word_detail_exaple, stat_id=random_word_detail_pk, all_pk=get_all_pk(word_detail_list), all_msg=word_detail_list)
    else:
        return dict(word=get_all_translate(word_detail_list), translate_list=[dct.get('word')], example=random_word_detail_exaple, stat_id=random_word_detail_pk, all_pk=get_all_pk(word_detail_list), all_msg=word_detail_list)

def prepare_list_dict(lst: list, answer: str) -> list:
    result = []
    for l in lst:
        my_dict = {"pk": l, "answer": answer}
        result.append(my_dict)
    return result

def find_answer(messages: list, answer: str):
    for message in messages:
        if answer == message.get('translate'):
            return message.get('word_stat').get('pk')