from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_HOST')
db = SQLAlchemy(app)
CORS(app)

class Article(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(80), unique=True, nullable=False)
   content = db.Column(db.String(800))
   image = db.Column(db.String(100))
   category = db.Column(db.String(50), nullable=False)
   
   def toJSON(self):
      return {"id": self.id, "title": self.title , "content": self.content, "image": self.image, "category": self.category}

class Categorey(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   cat = db.Column(db.String(80), unique=True, nullable=False)

   def toJSON(self):
      return {"id": self.id, "cat": self.cat}

@app.route("/api/cat/<pg>", methods=['GET']) #amit
@app.route("/api/", methods=['POST', 'GET'])
@app.route("/api/<id>", methods=['POST', 'GET', 'PUT', 'DELETE'])
def api(id=0, pg=0):
   if request.method == 'GET':
      if pg == 0:
         if id == 0: return jsonify([obj.toJSON() for obj in Article.query.all()])
         else: 
            arc = Article.query.get(id)
            if arc: 
               return jsonify([arc.toJSON()])
            else: return jsonify([])
      else: return jsonify([obj.toJSON() for obj in Article.query.filter(Article.category.ilike(str(pg))).all()])
      
   if (request.method == 'POST' or request.method == 'PUT'):
      data = request.get_json()
      if request.method == 'POST' and id == 0:
         new_article = Article(title=data['title'], content=data['content'], category=data['category'],image=data['image'])
         db.session.add(new_article)
         db.session.commit()
         return jsonify({'message': '1'})
      
      if request.method == 'PUT' and id != 0:
         res = Article.query.get(id)
         if res:
            res.title, res.content, res.image, res.category = data['title'], data['content'], data['image'], data['category'],
            db.session.commit()
            return jsonify({'message': '1'})
   
   if request.method == 'DELETE':
      res = Article.query.get(id)
      if res:
         db.session.delete(res)
         db.session.commit()
         return jsonify({'message': '1', 'cat': res.category})
   return jsonify({'message': '0'})

@app.route("/api/cat", methods=['POST', 'GET', 'PUT', 'DELETE'])
def cat():
   return jsonify([obj.toJSON() for obj in Categorey.query.all()])

def otg(data):
      new_article = Article(title=data['title'], content=data['content'], category=data['category'],image=data['image'])
      db.session.add(new_article)
      db.session.commit()
   

with app.app_context():
   db.create_all()

if __name__ == '__main__':
   app.run(debug=True)