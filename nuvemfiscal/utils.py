
def onlynumber(text) -> str:
    """
    Remove todos os caracteres que não são números
    Informa uma string e retorna somente os números dela

    :param texto: String a ser analisada
    :return: String somente com números
    """
    if not text or not str(text):
        return ''
    return ''.join(filter(str.isdigit, str(text)))
