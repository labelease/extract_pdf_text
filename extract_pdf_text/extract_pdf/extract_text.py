"""

    MICROSSERVICE TO TEXT EXTRACTION FROM PDF AND TXT FILES

    INPUT CAN BE:

        1) DIRECTORY CONTAINING MANY PDFS OR TEXT FILES
        2) PATH ABSOLUTE OF A SIGLE PDF OR TXT FILE
        3) ENCODED FILE IN BASE64 FORMAT

    # Arguments
        dir_file          - Required : File path (Path | String)
        dir_save_txt      - Optional : Path to save the file
                                       with the textual result (String)
        name_save_txt     - Optional : Name to save the file
                                       with the textual result (String)

    # Returns
        text              - Required : Text result (String)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (emersonrafaels) & Naomi Lago (naomilago)"""
__organization__ = "labelease"
__data_atualizacao__ = "29/08/2023"

import io
from os import path
from pathlib import Path
from inspect import stack
from typing import Union

from extract_pdf_text.config_project import config_project

from pydantic import validate_arguments, ValidationError
from loguru import logger

from dynaconf import settings
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from extract_pdf_text.utils.generic_functions import save_text_result


class Extract_PDF_Text:

    """

    MICROSERVIÇO PARA EXTRAÇÃO DE TEXTOS DE PDF'S DO TIPO TEXTO.
    O INPUT PODE SER:

    1) DIRETÓRIO CONTENDO VÁRIOS PDFS
    2) DIRETÓRIO ABSOLUTO DE UM ÚNICO PDF
    3) PDF EM FORMATO BASE64.

    # Arguments
        input_pdf_path              - Required : Caminho do arquivo a ser lido (String)

    # Returns
        text                        - Required : Texto do PDF enviado (String)

    """

    def __init__(self):

        # 1- LIST OF ALL EXTENSIONS TYPES ACCEPTED BY THE MICROSSERVICE
        self.list_file_extensions_accepted = settings.get(
            "EXTRACT_PDF_FEATURE.LIST_FORMAT_ACCEPTED", []
        )

        # 2 - GET THE DEFAULT PATH TO SAVE THE TEXT RESULT
        self.dir_save_default = settings.get(
            "EXTRACT_PDF_FEATURE.DIR_SAVE_RESULT", "extract_text_result"
        )

        # 3 - GET THE DEFAULT NAMEFILE TO SAVE THE TEXT RESULT
        self.name_save_default = settings.get(
            "EXTRACT_PDF_FEATURE.NAME_SAVE_RESULT", "result.txt"
        )

    def validate_file_extension(self, filename):

        """

        VERIFICA SE O ARQUIVO ENVIADO É ACEITO PELA CLASSE.

        RETORNA TRUE CASO O ARQUIVO ENVIADO POSSUA
        EXTENSÃO DENTRE AS EXTENSÕES ACEITAS
        ('self.list_file_formats_accepted').

        # Arguments
            filename            - Required : Caminho do arquivo a
                                             ser verificado (String)

        # Returns
            validador           - Required : Validador de execução
                                             da função (Boolean)

        """

        # INICIANDO O VALIDADOR DA FUNÇÃO
        validador = False
        file_format = None

        try:
            # OBTENDO O FORMATO DO ARQUIVO
            file_format = Path(filename).suffix

            # VERIFICANDO SE O FORMATO DO ARQUIVO É ACEITO
            if file_format in self.list_file_extensions_accepted:

                validador = True

        except Exception as ex:
            print("FUNCTION ERROR {} - {}".format(stack()[0][3], ex))

        return validador, file_format

    def get_path_save_txt(self, path_save_txt_input):

        # VERIFICANDO SE NÃO FOI ENVIADO CAMINHO PARA SAVE DO TXT
        if path_save_txt_input is None:
            path_save_txt = path.join(
                self.path_default, path_save_txt_input.split("\\")[-1] + ".txt"
            )

        elif path_save_txt_input.find(".txt") != -1:
            path_save_txt = path.join(
                self.path_default, path_save_txt_input.split("\\")[-1]
            )

        return path_save_txt


    @staticmethod
    @validate_arguments
    def read_txt(path_txt: Union[Path, str]):

        """

        FUNÇÃO PARA LER ARQUIVO TXT.

        # Arguments
            path_txt                   - Required : Diretório do arquivo .txt (String)

        # Returns
            text                       - Required : Texto obtido do arquivo .txt (String)

        """

        # INIT RETURN VARIABLE
        validator = False
        text = ""

        try:
            with open(str(path_txt), "r", encoding=settings.get("ENCODING_DEFAULT",
                                                                "utf-8")) as text_file:

                text = text_file.read()

                validator = True

        except Exception as ex:
            print("FUNCTION ERROR {} - {}".format(stack()[0][3], ex))

        return validator, text

    @staticmethod
    def convert_pdf_to_text(fname, pages: int = None):

        """

        FUNCTION TO GET TEXT FROM A PDF FILE

        # Arguments
            fname                 - Required : Filename (Path | String)
            pages                 - Required : Init page to get the text (Int)

        # Returns
            text                  - Required : Result text (String)

        """

        # INIT RETURN VARIABLE
        validator = False
        text = ""

        # VERIFICA SE HÁ UMA PÁGINA ESPECÍFICA PARA EXTRAIR
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        try:
            output = io.StringIO()

            # INSTANCE PDF RESOURCE MANAGER
            manager = PDFResourceManager()

            # CONFIGURE THE TEXT CONVERTER
            converter = TextConverter(manager, output, laparams=LAParams())

            # INTERPRET THE PAGE
            interpreter = PDFPageInterpreter(manager, converter)

            # OPENING THE FILE
            infile = open(fname, "rb")

            # ITERATE ON EACH PAGE AND DO THE CONVERSION
            for page in PDFPage.get_pages(infile, pagenums):
                interpreter.process_page(page)

        except Exception as ex:
            print("FUNCTION ERROR {} - {}".format(stack()[0][3], ex))

        finally:
            infile.close()

            converter.close()

        try:
            # STORAGE THE TEXT RESULT
            text = output.getvalue()

            validator = True

        except Exception as ex:
            print("FUNCTION ERROR {} - {}".format(stack()[0][3], ex))

        finally:
            output.close()

        return validator, text

    @validate_arguments
    def orchestra_extract_text(self,
                               dir_file: Union[Path, str],
                               dir_save_txt: str = None,
                               name_save_txt: str = None):

        """

        MAIN FUNCTION - ORCHESTRA THE MICROSERVICE

        # Arguments
            dir_file          - Required: File path (Path | String)
            dir_save_txt      - Optional: Path to save the file
                                          with the textual result (String)
            name_save_txt     - Optional: Name to save the file
                                          with the textual result (String)

        # Returns
            text              - Required: Text result (String)

        """

        # INIT RETURN VALUES
        validator = False
        text = ""

        # VALIDANDO SE O ARQUIVO ENVIADO É UM PDF
        validator, extension = Extract_PDF_Text.validate_file_extension(self,
                                                                        filename=dir_file)

        if validator:

            if extension in ["pdf", ".pdf"]:

                try:
                    # READ: PDF FILE
                    validator, text = Extract_PDF_Text.convert_pdf_to_text(dir_file)
                except PDFTextExtractionNotAllowed:
                    logger.error("NOT WAS POSSIBLE TO EXTRACT - PDFTextExtractionNotAllowed")
                except PDFSyntaxError:
                    logger.error("NOT WAS POSSIBLE TO EXTRACT - PDFSyntaxError")
                except Exception as ex:
                    logger.error("NOT WAS POSSIBLE TO EXTRACT - {}".format(str(ex)))

            elif extension in ["txt", ".txt"]:
                # READ: TXT FILE
                validator, text = Extract_PDF_Text.read_txt(dir_file)

            if validator:

                # SAVE THE RESULT TEXT IN A TXT FILE
                validator = save_text_result(path_save=self.dir_save_default,
                                             name_save=self.name_save_default,
                                             text=text)

        else:
            raise (
                "THE FILE HAVE A EXTENSION NOT ACCEPTED BY THE MICROSSERVICE\nACCEPTED EXTENSIONS ARE: {}".format(
                    self.list_file_extensions_accepted
                )
            )

        return validator, text
