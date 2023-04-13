from flask import Flask, jsonify, request
from waitress import serve
from redis.commands.search.query import Query
import json
import os
import redis


DOC_INDEX = 'idx_doc'
BASE_URL = 'https://devbox.amsl.com'
app = Flask(__name__)
redis_db = redis.from_url(os.environ['REDIS_URL'])


# try to create index if missing
try:
    redis_db.execute_command(f'FT.CREATE {DOC_INDEX} ON JSON SCHEMA $.title AS title TEXT $.abstract AS abstract TEXT $.authors[:][*] AS name TEXT')
except Exception:
    pass



@app.route('/')
def hello_world():
    return 'try /get/<document_id> and /search/<query>'


@app.route('/get/<document_id>')
def get(document_id):
    doc = redis_db.json().get(document_id)
    if doc is not None:
        return doc
    else:
        return jsonify({'error': 'Document not found'}), 404


@app.route('/search/<query>')
def search(query):
    offset = request.values.get('offset', 0)
    limit = request.values.get('limit', 1000)
    results = redis_db.ft(DOC_INDEX).search(Query(query).paging(offset, limit))
    total = results.total
    docs = []
    for doc in results.docs:
        data = json.loads(doc.json)
        docs.append({
            'id': doc.id,
            'title': data['title'],
            'abstract': data['abstract'],
            'json_url': f'{BASE_URL}/get/{doc.id}',
            })
    return jsonify({'total_results': total, 'documents': docs})


if __name__ == '__main__':
    serve(app, listen='*:80')
