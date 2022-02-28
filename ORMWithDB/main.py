from fastapi import FastAPI, HTTPException,Response,Depends
from fastapi.params import Body
from pydantic import BaseModel
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import Base, engine, get_db
from .models import *
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
class Post (BaseModel):
    title: str
    content: str
    published: bool = True

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
def getPosts(db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #print(posts)
    posts = db.query(models.Posts).all()
    return {"data" : posts}

@app.post("/posts", status_code=201)
def makePost(post: Post,db: Session = Depends(get_db)):
    ##staging changes
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    ##commiting changes to Database
    #conn.commit()

    newPost = models.Posts(title=post.title, content=post.content, published=post.published)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return {"data" : newPost}

@app.get("/posts/{id}")
def get_id(id: int, response: Response, db: Session = Depends(get_db)):
    #cursor.execute(""" SELECT * FROM posts WHERE id = (%s) """, (str(id)))
    #post = cursor.fetchone()
    #print(post)
    #if post == None:
    #    raise HTTPException(status_code=404, detail="Post not found")

    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    return {"Post data" : post}


@app.delete("/posts/{id}")
def deletePost(id: int, db: Session = Depends(get_db)):
    #cursor.execute(""" DELETE FROM posts WHERE id = (%s) RETURNING *""", (str(id)))
    #deletedPost = cursor.fetchone()
    #conn.commit()
    #if deletedPost == None:
    #    raise HTTPException(status_code=404, detail="Post not found")

    post = db.query(models.Posts).filter(models.Posts.id == id)
    if post.first() == None:
        HTTPException(status_code=404)
    post.delete(synchronize_session=False)
    db.commit()
    return HTTPException(status_code=204)

@app.put("/posts/{id}")
def updatePost(id: int, post: Post, db: Session = Depends(get_db)):
    #cursor.execute(""" UPDATE posts SET title = (%s), content = (%s), published = (%s) WHERE id = (%s) RETURNING * """, (post.title, post.content, post.published, str(id)))
    #updatedPost = cursor.fetchone()
    #conn.commit()
    updatedPost = db.query(models.Posts).filter(models.Posts.id == id).update({'title': post.title, 'content': post.content, 'published': post.published})
    if updatedPost == None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.commit()
    return {"data" : updatedPost}

