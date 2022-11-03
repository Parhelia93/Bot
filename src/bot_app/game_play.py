from .data_struct import ServerRandomWord, CheckAnswer
from .messages import *
from .local_settings import CNT_TRAINT_STEP
from .data_fetcher import put_answer, put_answers
from .utils import prepare_list_dict


async def check_user_answer(user_answer: str, server_word: ServerRandomWord) -> CheckAnswer:
    check_answer = None
    if user_answer in server_word.translate:
        if server_word.choose_language == EN_RUS:
            index_answer = server_word.translate.index(user_answer)
        else:
            index_answer = server_word.all_answer.index(server_word.word)
        true_pk = server_word.all_pk[index_answer]
        await put_answer({'pk': true_pk, 'answer': 'True'})

    if user_answer in DONT_KNOW_CMD:
        res = prepare_list_dict(server_word.all_pk, 'False')
        await put_answers(res)
        server_word.step += 1
        check_answer = CheckAnswer(server_word=server_word,
                                   status=DONT_KNOW_MSG)

    if user_answer in server_word.translate:
        server_word.step += 1
        check_answer = CheckAnswer(server_word=server_word,
                                   status=NEW_MESSAGE)

    if user_answer not in server_word.translate and user_answer not in DONT_KNOW_CMD:
        res = prepare_list_dict(server_word.all_pk, 'False')
        await put_answers(res)
        check_answer = CheckAnswer(server_word=server_word,
                                   status=WRONG_ANSWER)

    if server_word.step > CNT_TRAINT_STEP:
        check_answer = CheckAnswer(server_word=server_word,
                                   status=FINISH)
    return check_answer

