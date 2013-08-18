from flask import Flask,render_template,request,redirect,session
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import reqparse, abort, Api, Resource
from models.todo import Todo
from shared import app,db
import requests
import lib.auth as auth
import json
app_id='526770004048893'
app_secret="2808bb138b8ccd707fdea5b892627a8a"
app.secret_key = "0219"
import json
import flask

@app.route("/todos/<int:id>",methods=["GET","POST"])
def todo(id):
    data = request.form
    todo = db.session.query(Todo).filter_by(id = id).first()
    if request.method == "GET":
        return render_template("edit.html",todo = todo)
    elif request.method == "PUT":
        todo.task = data["task"]
        db.session.commit()
        return redirect("/")

    elif request.method == "DELETE":
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")



@app.before_request
def before_request():
    method = request.form.get('_method', '').upper()
    print(method)
    if method == "DELETE":
        request.environ['REQUEST_METHOD'] = method
        ctx = flask._request_ctx_stack.top
        ctx.url_adapter.default_method = method
        assert request.method == method
    elif method == "PUT":
        request.environ['REQUEST_METHOD'] = method
        ctx = flask._request_ctx_stack.top
        ctx.url_adapter.default_method = method
        assert request.method == method


@app.route("/")
def indexView():
    todos = db.session.query(Todo).all()
    name = session.get("current_user")
    return render_template('index.html',todos=todos,name = name)

@app.route("/new_todo")
def new_todo():
    return render_template("new_todo.html")

@app.route("/login")
def connect():
    return auth.connect()

@app.route("/posted")
def posted():
    code = request.args.get("code")
    data = {}
    data["client_id"] = app_id
    data["redirect_uri"] = "http://localhost:5000/posted"
    data["client_secret"] = app_secret
    data["code"] = code.strip(" ")
    url = "https://graph.facebook.com/oauth/access_token"
    d = requests.get(url,params=data)
    res = requests.get("https://graph.facebook.com/me?"+d.text)
    data = json.loads(res.text)
    session["current_user"] = data["username"]


    return redirect("/")





@app.route("/todos",methods=["GET","POST","DELETE","PUT"])
def todos():
    data = request.form
    if request.method == "POST":
        todo = Todo(data["task"])
        db.session.add(todo)
        print("create new record")
        db.session.commit()
        return redirect("/")
    elif request.method == "PUT":
        id = data["todo_id"]
        t = db.session.query(Todo).filter_by(id == id).first()
        t.task = "fooo"
        db.session.add(t)
        db.session.commit()
    elif request.method == "DELETE":
        return "hello"

    return "a"







if __name__ == '__main__':
    with open("config.json") as f:
        print(f)

    db.create_all()
    app.run(host="0.0.0.0",debug=True)
