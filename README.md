# bib
BibXML PoC with redis

## Administration
### Run server
```
docker-compose up --build -d
```

### Create index

```
docker exec -ti bib-redis redis-cli FT.CREATE idx_doc ON JSON SCHEMA $.title AS title TEXT $.abstract AS abstract TEXT $.authors[:][*] AS name TEXT
```

## Load data
```
docker exec -ti bib-python python scripts/load-data.py "redis://redis:6379/0" "/app/relaton-data-rfcs/data"
docker exec -ti bib-python python scripts/load-data.py "redis://redis:6379/0" "/app/relaton-data-ids/data"
```

## Save data
```
docker exec -ti bib-redis redis-cli save
```
