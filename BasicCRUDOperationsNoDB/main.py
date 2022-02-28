from fastapi import FastAPI, HTTPException,Response
from fastapi.params import Body
from pydantic import BaseModel
import random
app = FastAPI()
class Post (BaseModel):
    title: str
    content: str
    published: bool = True

myPosts = [
    {"id" : 1, "title" : "Post 1", "content" : "Content for Post 1", "published" : "True"},
    {"id" : 2, "title" : "Post 2", "content" : "Content for Post 2", "published" : "True"},
    {"id" : 3, "title" : "Post 3", "content" : "Content for Post 3", "published" : "True"},
    {"id" : 4, "title" : "Post 4", "content" : "Content for Post 4", "published" : "True"},
           ]
@app.get('/posts')
def getPosts():
    return {"data" : myPosts}


@app.post("/posts", status_code=201)
def makePost(post: Post):
    if post.published:
        post_dict = post.dict()
        post_dict['id'] = random.randrange(1, 10000)
        myPosts.append(post_dict)
        return {"data" : myPosts}

    return {"data" : "post not published"}


def findPost(id):
    for p in myPosts:
        if p['id'] == id:
            print (p['id'])
            return p

@app.get("/posts/{id}")
def get_id(id: int, response: Response):
    print(type(id))
    post = findPost(id)
    print(post)
    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")
        #response.status_code = Status.HTTP_404_NOT_FOUND
        #return {"data" : "Post not found"}
    return {"Post data" : post}


@app.delete("/posts/{id}")
def deletePost(id: int):
    post = findPost(id)
    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")
    myPosts.remove(post)
    return HTTPException(status_code=204)

@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    post_dict = post.dict()
    post_dict['id'] = id
    post = findPost(id)
    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")
    myPosts.remove(post)
    myPosts.append(post_dict)
    return {"data" : myPosts}
