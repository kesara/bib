import os
import redis
import requests
import sys
import yaml

if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} redis_url data_dir')
    sys.exit(1)

redis_url = sys.argv[1]
data_dir = sys.argv[2]
r = redis.from_url(redis_url)

for root, dirs, files in os.walk(data_dir):
    for file in files:
        file_path = os.path.join(root, file)
        with open(file_path, 'r') as f:
            file_contents = f.read()
            data = yaml.safe_load(file_contents)

            doc_id = str(data['id'])
            authors = []
            print(f'loading {doc_id}')
            if not 'contributor' in data.keys():
                print(f'ignoring {doc_id}')
                # ignore these for now
                continue
            for author in data['contributor']:
                if 'person' in author.keys():
                    try:
                        fullname = str(author['person']['name']['completename']['content'])
                    except KeyError:
                        pass
                    try:
                        initials = str(author['person']['name']['given']['formatted_initials']['content'])
                    except KeyError:
                        pass
                    try:
                        surname = str(author['person']['name']['surname']['content'])
                    except KeyError:
                        pass
                    authors.append({
                        'fullname': fullname,
                        'initials': initials,
                        'surname': surname,
                        })
            abstract = None
            try:
                abstract = str(data['abstract'][0]['content'])
            except KeyError:
                pass

            values = {
                'title': str(data['title'][0]['content']),
                'target': str(data['link'][0]['content']),
                'abstract': abstract,
                'date': str(data['date'][0]['value']),
                'authors': authors,
                }

            result = r.json().set(doc_id, '$', values)
            print(f'{result}')
