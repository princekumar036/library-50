import uuid
import os
import textract
from indexing import add_to_index


def process_txt(filename):

    # Generate id for article
    id = str(uuid.uuid4())

    # Make directory
    dir_path = os.path.join('templates', 'bookshelf', id)
    os.mkdir(dir_path)

    # Write article to a file
    output = textract.process(filename).decode('utf-8')
    with open(os.path.join(dir_path, 'document.txt'), 'w', encoding="utf-8") as f:
        f.write(output)

    # Find a Title
    title = ''
    for letter in output[:100]:
        if letter == '\n':
            break
        title += str(letter)

    # Add article to index
    add_to_index(id, 'txt', '', title, '')