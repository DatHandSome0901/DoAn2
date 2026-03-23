import fitz, os

def pdf_folder_to_text(folder, out_file):
    text = ""
    for f in os.listdir(folder):
        if f.endswith('.pdf'):
            path = os.path.join(folder, f)
            doc = fitz.open(path)
            for page in doc:
                text += page.get_text() + "\n"
    with open(out_file, 'w', encoding='utf-8') as fp:
        fp.write(text)

pdf_folder_to_text('data/pdfs', 'data/all_text_raw.txt')
print('DONE PDF -> TEXT')