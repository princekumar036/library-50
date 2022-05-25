import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import epub_meta
import zipfile
import os
import uuid
import re
import base64

from indexing import add_to_index


def process_epub(filename):

    # Generate a unique id for book
    book_id = str(uuid.uuid4())

    # Get books metadata using epub_meta
    # https://github.com/paulocheque/epub-meta
    metadata = epub_meta.get_epub_metadata(filename, read_cover_image=True, read_toc=True)
    
    current_level = 0
    toc_output = ''
    contents_output = ''

    # Make TOC
    for chapter in metadata.toc:

        # Create nested list according to chapter's level
        while chapter['level'] > current_level:
            toc_output += "<ul>"
            current_level += 1
        while chapter['level'] < current_level:
            toc_output += "</ul>"
            current_level -= 1

        # chapter_title = chapter['title']
        # chapter_link = chapter['src']

        # Clean TOC hrefs and append to toc output
        toc_output += f'<li><a href="#{ book_id }/{ chapter["src"] }">{ chapter["title"] }</a></li>'
            

    # Get all the documents with ebooklib
    # https://github.com/aerkalov/ebooklib
    book = epub.read_epub(filename)
    documents = book.get_items_of_type(ebooklib.ITEM_DOCUMENT)

    for document in documents:

        chapter_content = document.get_body_content().decode('utf-8')
        chapter_link = document.get_name()

        chapter_soup = BeautifulSoup(chapter_content, 'html.parser')

        # Clean all 'id' within the chapter
        tags_with_id = chapter_soup.find_all(True, {'id': True})
        for tag in tags_with_id:
            tag['id'] = book_id + '/' + chapter_link + '#' + tag['id']

        # Clean all 'href' within the chapter
        links = chapter_soup.find_all(True, {'href': True})
        for link in links:
            href = link['href']
            if href.startswith('http') or href.startswith('www') or href.startswith('mailto'):
                continue
            link['href'] = '#' + book_id + '/' + href

        # Update all img src within chapter
        imgs = chapter_soup.find_all('img')
        for img in imgs:
            img['src'] = 'static/' + book_id + '/' + img['src']
        images = chapter_soup.find_all('image')
        for image in images:
            image['xlink:href'] = 'static/' + book_id + '/' + image['xlink:href']
        
        # Append to contents output
        contents_output += f'<div id="{book_id}/{chapter_link}">'
        contents_output += chapter_soup.prettify()
        contents_output += f'</div>'
        contents_output += f'<hr class="inserted-hr">'

    # Create a directory called 'id'
    dir_path = os.path.join('templates', 'bookshelf', book_id)
    os.mkdir(dir_path)

    # Write book to a file
    document_file = os.path.join(dir_path, 'document.txt')
    with open(document_file, 'w') as f:
        f.write(contents_output)
        f.write('<ul class="inserted-toc hidden">')
        f.write(toc_output)
        f.write('</ul>')
        
    # Extract images and save to static/id
    with zipfile.ZipFile(filename) as zip:
        for file in zip.infolist():
            if '.jpg' in file.filename:
                file.filename = '/'.join(file.filename.split('/')[1:])
                zip.extract(file, os.path.join('static', book_id))

    # Get book's title
    title = metadata.title
    
    # Get book's cover image
    cover_string = metadata.cover_image_content
    imgdata = base64.b64decode(cover_string)

    cover_ext = metadata.cover_image_extension
    cover_image = os.path.join('static', book_id, 'cover') + cover_ext

    with open(cover_image, 'wb') as f:
        f.write(imgdata)

    # Add book's metadata to index.json
    add_to_index(book_id, 'epub', '', title, cover_image)