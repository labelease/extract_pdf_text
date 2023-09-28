from os import path, makedirs
from pathlib import Path
from typing import Union
from inspect import stack

from dynaconf import settings
from pydantic import validate_arguments, ValidationError
from loguru import logger

# DEFININDO O DIR ROOT
dir_root = Path(__file__).parent.parent.parent

@validate_arguments
def create_path(dir: Union[Path, str]):

    """

    FUNCTION TO CREATE A PATH

    # Arguments
        dir                      - Required: Directory to create (Path | String)

    # Returns
        validator                - Required: Function validator (Boolean)

    """

    # INICIANDO O VALIDADOR DA FUNÇÃO
    validator = False

    try:
        makedirs(str(dir))

        validator = True
    except Exception as ex:
        print("FUNCTION ERROR {} - {}".format(stack()[0][3], ex))

    return validator


@validate_arguments
def verify_path(dir: Union[Path, str]):

    """

    FUNCTION TO VERIFY IF A DIRECTORY (PATH) EXISTS.

    # Arguments
        dir                      - Required: Directory to verify (Path | String)

    # Returns
        validator                - Required: Function validator (Boolean)

    """

    # INICIANDO O VALIDADOR DA FUNÇÃO
    validator = False

    try:
        validator = path.exists(str(dir))
    except Exception as ex:
        print("FUNCTION ERROR {} - {}".format(stack()[0][3], ex))

    return validator


@validate_arguments
def save_text_result(path_save: Union[Path, str],
                     name_save: str,
                     text: str):

    """

        SAVING THE RESULT TEXT

        # Arguments
            path_save       - Required: Directory to save the file (Path | String)
            name_save       - Required: Name to save the file
                                        with the textual result (String)
            text            - Required: Text result (String)

        # Returns
            validator       - Required: Function validator (Boolean)

    """

    # DIR TO SAVE
    dir_save = str(Path(dir_root, path_save).absolute())
    dir_name_save = str(Path(dir_save, name_save).absolute())

    # VERIFY IF DIR EXISTS
    validator = verify_path(dir=dir_save)

    if not validator:
        validator = create_path(dir=dir_save)

    if validator:

        # REALIZANDO A ABERTURA DO ARQUIVO (MESMO QUE NÃO EXISTENTE)
        with open(dir_name_save, "w", encoding=settings.get("ENCODING_DEFAULT",
                                                            "utf-8")) as text_file:

            try:
                text_file.write(text)

                validator = True

            except Exception as ex:
                print("FUNCTION ERROR {} - {}".format(stack()[0][3], ex))

    else:
        logger.error("ITS NOT POSSIBLE TO CREATE THE DIR: {}".format(dir_save))

    return validator