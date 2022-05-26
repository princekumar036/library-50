from flask import Flask, render_template, redirect, request, flash
import json
import requests
import os

from epub import process_epub
from url import process_url
from doc import process_docx
from txt import process_txt

app = Flask(__name__)
app.secret_key = "open access library"
app.config['UPLOAD_FOLDER'] = '.'
ALLOWED_EXT = {'.txt', '.docx', '.epub'}

port = int(os.environ.ge('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=True)

@app.route('/')
def index():
    index_data = json.load(open('templates/bookshelf/index.json'))['index']
    return render_template('index.html', index_data=index_data)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/processing', methods=['GET', 'POST'])
def processing():
    if request.method == 'GET':
        return redirect('/upload')

    url = request.form['url']
    file = request.files['file']

    # Ensure both not empty
    if not (url or file):
        flash('Provide either URL or File. None provided.')
        return redirect('/upload')

    # Ensure not both
    if url and file:
        flash('Provide either URL or File. Both provided.')
        return redirect('/upload')

    # Process URLs
    if url:
        try:
            process_url(url)
        except:
            return redirect('/error')

    # Process Files
    if file:
        filename = file.filename

        if os.path.splitext(filename)[-1] not in ALLOWED_EXT:
            flash('File type not supported.')
            return redirect('/upload')
        
        file.save(filename)

        # Process txt files
        if os.path.splitext(filename)[-1] == '.txt':
            try:
                process_txt(filename)
            except:
                return redirect('/error')

        # Process docx files
        if os.path.splitext(filename)[-1] == '.docx':
            try:
                process_docx(filename)
            except:
                return redirect('/error')

        # Process epub files
        if os.path.splitext(filename)[-1] == '.epub':
            try:
                process_epub(filename)
                flash('File upload successful.')
                return redirect('/')
            except:
                return redirect('/error')

        os.remove(filename)

    flash('File upload successful.')
    return redirect('/')

@app.route('/reader') 
def reader():
    
    # Get document's metadata
    doc_id = request.args.get('doc_id')
    index_data = json.load(open('templates/bookshelf/index.json'))['index']
    doc_reqstd = ''
    for doc in index_data:
        if doc['doc_id'] == doc_id:
            doc_reqstd = doc
    
    return render_template('reader.html', doc_id=doc_id, title=doc_reqstd['title'], top_image=doc_reqstd['top_image'], url=doc_reqstd['url'])

@app.route('/error')
def error():
    return render_template('error.html')