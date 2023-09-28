from extract_pdf_text.extract_pdf.extract_text import Extract_PDF_Text

# FILE
dir_pdf = "tests/files_test/BO_TEXTO.pdf"

# CALL MICROSERVICE
result = Extract_PDF_Text().orchestra_extract_text(dir_file=dir_pdf)