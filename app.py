from fastapi import FastAPI, HTTPException


from elasticsearch import Elasticsearch

app = FastAPI()


# Password for the 'elastic' user generated by Elasticsearch
ELASTIC_PASSWORD = "NLQOcsuetKM6tWSkZ8pTTloZ"

# Found in the 'Manage Deployment' page
CLOUD_ID = "SIH:YXAtc291dGgtMS5hd3MuZWxhc3RpYy1jbG91ZC5jb206NDQzJDE0Mjc3ODcwNDgwYTQ5NmI5OTc2MDlhODIzN2UwYjY1JGUxOGQ1OTEzNDU3NjQ3OTBhYTY3NzcyNDc1YzgzNDJm"

# Create the client instance
client = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD),
)


@app.get("/search")
def search(q: str):
    result = {}
    try:
        resp = client.search(body={"query": {"query _string": {"query": q}}})
        data = resp["hits"]["hits"]
        result['data'] = data
        result['meta'] = {'total':resp["hits"]["total"]["value"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result
