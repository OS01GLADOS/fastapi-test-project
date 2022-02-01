from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'Darya'}}


@app.get('/blog')
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    # only 10 published blogs
    if published:
        return {'data': f'{limit} published blogs of db'}
    else:
        return {'data': f'{limit} blogs from db'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def blog(id: int):
    # fetch blog with id = id
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int):
    # fetch comments of blog with id = id
    return {'data': {'1', '2'}}

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f'blog is createdwith title {request.title}'}


# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=9000)