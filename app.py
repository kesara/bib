from flask import Flask, jsonify
from waitress import serve
import json
import os
import redis


DOC_INDEX = 'idx_doc'
BASE_URL = 'https://devbox.amsl.com'
app = Flask(__name__)
redis_db = redis.from_url(os.environ['REDIS_URL'])


@app.route('/')
def hello_world():
    return 'try /get/<document_id> and /search/<term>'


@app.route('/get/<document_id>')
def get(document_id):
    doc = redis_db.json().get(document_id)
    if doc is not None:
        return doc
    else:
        return jsonify({'error': 'Document not found'}), 404


@app.route('/search/<term>')
def search(term):
    results = redis_db.ft(DOC_INDEX).search(term)
    docs = []
    for doc in results.docs:
        data = json.loads(doc.json)
        docs.append({
            'id': doc.id,
            'title': data['title'],
            'abstract': data['abstract'],
            'json_url': f'{BASE_URL}/get/{doc.id}',
            })
    return jsonify({'documents': docs})


if __name__ == '__main__':
    serve(app, listen='*:80')
