import os
import json

def add_to_index(id, type, url, title, image):
    # Create a dictionary
    dict = {
            'doc_id'    : id,
            'type'      : type,
            'url'       : url,
            'title'     : title,
            'top_image' : image,
            'dir_path'  : os.path.join('templates', 'bookshelf', id)
        }

    with open('templates/bookshelf/index.json', 'r+') as f:
        existing_data = json.load(f)
        existing_data['index'].append(dict)
        f.seek(0)
        json.dump(existing_data, f, indent = 4)