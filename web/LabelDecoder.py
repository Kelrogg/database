name_decoder = {
    0: "Геморрагический инсульт. Внутрижелудочковое кровоизлияние.",
    1: "Геморрагический инсульт. Внутримозговая гематома с вентрикулярным компонентом.",
    2: "Геморрагический инсульт. Внутримозговая гематома в задней черепной ямке.",
    3: "Геморрагический инсульт. Внутримозговая гематома.",
    4: "Геморрагический инсульт. Внутримозговая гематома.",
    5: "Ишемический инсульт.",
    6: "Ишемический инсульт с геморрагической трансформацией.",
    7: "Подозрение на опухоль.",
    8: "Субарахноидальное кровоизлияние",
    9: "Геморрагический инсульт. Внутримозговая гематома с субарахноидальным кровоизлиянием"
}


def decode_label_detail(patology_indexes: list):
    answer = ''

    for i in patology_indexes.all():
        answer += f'{name_decoder[i.value]} и '

    return answer[:-2]

