# https://newspaper.readthedocs.io/en/latest/

import lxml
from newspaper import Article, Config
import uuid
import os

from indexing import add_to_index


def process_url(url):
    config = Config()
    config.fetch_images = True
    config.request_timeout = 30
    config.keep_article_html = True
    article = Article(url, config=config)

    article.download()
    article.parse()

    article_html = article.article_html

    html = lxml.html.fromstring(article_html)
    for tag in html.xpath('//*[@class]'):
        tag.attrib.pop('class')

    # Generate id for article
    id = str(uuid.uuid4())

    # Make directory
    dir_path = os.path.join('templates', 'bookshelf', id)
    os.mkdir(dir_path)

    # Generate metadata
    url = url
    title = article.title
    top_image = article.top_image

    # Write article to a file
    article_file = os.path.join(dir_path, 'document.txt')
    with open(article_file, 'w') as f:
        f.write(lxml.html.tostring(html).decode('utf-8'))


    # Add article to index
    add_to_index(id, 'url', url, title, top_image)