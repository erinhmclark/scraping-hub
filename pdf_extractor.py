""" Extracts the text from a pdf file, decrypting where possible. """
import PyPDF2


def extract_text_from_pdf(file_path, password=""):
    """Extracts the text from a pdf file and returns it as a string."""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        if pdf_reader.is_encrypted:
            success = pdf_reader.decrypt(password)
            if not success:
                raise ValueError("Invalid password provided for encrypted PDF.")

        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text


if __name__ == '__main__':
    file_name = input('Please enter filepath: ')

    try:
        text = extract_text_from_pdf(file_name)
        print(text)
    except Exception as e:
        print(f"An error occurred while extracting text from the PDF file: {e}")
