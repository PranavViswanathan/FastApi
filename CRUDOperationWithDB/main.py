from fastapi import FastAPI, HTTPException,Response
from fastapi.params import Body
from pydantic import BaseModel
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time

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
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='pranav', user='postgres', password='ganesh99', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection was successfully executed")
        break
    except Exception as e:
        print("DB connection failed")
        print("Error", e)
        time.sleep(5)

@app.get('/posts')
def getPosts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data" : posts}


@app.post("/posts", status_code=201)
def makePost(post: Post):
    #staging changes
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    #commiting changes to Database
    conn.commit()
    return {"data" : "created post"}

@app.get("/posts/{id}")
def get_id(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = (%s) """, (str(id)))
    post = cursor.fetchone()
    print(post)
    if post == None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"Post data" : post}


@app.delete("/posts/{id}")
def deletePost(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = (%s) RETURNING *""", (str(id)))
    deletedPost = cursor.fetchone()
    conn.commit()
    if deletedPost == None:
        raise HTTPException(status_code=404, detail="Post not found")
    return HTTPException(status_code=204)

@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = (%s), content = (%s), published = (%s) WHERE id = (%s) RETURNING * """, (post.title, post.content, post.published, str(id)))
    updatedPost = cursor.fetchone()
    conn.commit()
    if updatedPost == None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"data" : updatedPost}
