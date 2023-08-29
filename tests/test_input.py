import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).absolute().parent.parent))

from pytest import mark

from extract_pdf_text.extract_pdf.extract_text import Extract_PDF_Text

@mark.test_input
def test_input_pdf_success():

	"""

		CASE: INPUT PDF
		WHEN: CALL MAIN FUNCTION
		THEN: RETURN VALIDATOR TRUE

	"""

	# FILE
	dir_pdf = "files_test/BO_TEXTO.pdf"

	# CALL MICROSERVICE
	result = Extract_PDF_Text().orchestra_extract_text(dir_file=dir_pdf)

	# VALIDATE RESULT
	assert result[0] == True

@mark.test_input
def test_input_txt_success():
	"""

		CASE: INPUT TXT
		WHEN: CALL MAIN FUNCTION
		THEN: RETURN VALIDATOR TRUE

	"""

	# FILE
	dir_txt = "files_test/news_file_i.txt"

	# CALL MICROSERVICE
	result = Extract_PDF_Text().orchestra_extract_text(dir_file=dir_txt)

	# VALIDATE RESULT
	assert result[0] == True

if __name__ == '__main__':
	test_input_txt_success()