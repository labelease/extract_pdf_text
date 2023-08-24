from os import path, makedirs
from inspect import stack


def create_path(dir):

    """

    FUNÇÃO PARA CRIAR UM PATH;

    # Arguments
            dir                      - Required : Diretório a ser criado (String)

    # Returns
            validador                - Required : Validador de execução da função (Boolean)

    """

    # INICIANDO O VALIDADOR DA FUNÇÃO
    validador = False

    try:
        makedirs(dir)
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

    return validador


def verify_path(dir):

    """

    FUNÇÃO PARA VERIFICAR SE UM DIRETÓRIO (PATH) EXISTE.

    # Arguments
            dir                      - Required : Diretório a ser verificado (String)

    # Returns
            validador                - Required : Validador de execução da função (Boolean)

    """

    # INICIANDO O VALIDADOR DA FUNÇÃO
    validador = False

    try:
        validador = path.exists(dir)
    except Exception as ex:
        print("ERRO NA FUNÇÃO {} - {}".format(stack()[0][3], ex))

    return validador
