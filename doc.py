import uuid
import os
from pydocx import PyDocX
import textract

from indexing import add_to_index


def process_docx(filename):

    # Generate id for article
    id = str(uuid.uuid4())

    # Make directory
    dir_path = os.path.join('templates', 'bookshelf', id)
    os.mkdir(dir_path)

    # Write article to a file
    output = PyDocX.to_html(filename)
    with open(os.path.join(dir_path, 'document.txt'), 'w', encoding="utf-8") as f:
        f.write(output)

    type = 'docx'
    url = ''

    title = ''
    text = textract.process(filename).decode('utf-8')
    for letter in text[:100]:
        if letter == '\n':
            break
        title += str(letter)
    
    top_image = ''


    # Add article to index
    add_to_index(id, type, url, title, top_image)