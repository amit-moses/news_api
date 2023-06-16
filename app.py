from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
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
         else: return jsonify([obj.toJSON() for obj in Article.query.filter(Article.id.ilike(id)).all()])
      else: return jsonify([obj.toJSON() for obj in Article.query.filter(Article.category.ilike(pg)).all()])
      
   if (request.method == 'POST' or request.method == 'PUT'):
      data = request.get_json()
      if request.method == 'POST' and id == 0:
         new_article = Article(title=data['title'], content=data['content'], category=data['category'],image=data['image'])
         db.session.add(new_article)
         db.session.commit()
         print('888')
         return jsonify({'message': '1'})
      
      if request.method == 'PUT' and id != 0:
         res = Article.query.filter(Article.id.ilike(id)).all()
         if len(res)>0:
            print(res[0].toJSON())
            res[0].title, res[0].content, res[0].image, res[0].category = data['title'], data['content'], data['image'], data['category'],
            print(res[0].toJSON())
            db.session.commit()
            return jsonify({'message': '1'})
   
   if request.method == 'DELETE':
      res = Article.query.filter(Article.id.ilike(id)).all()
      if len(res)>0:
         db.session.delete(res[0])
         db.session.commit()
         return jsonify({'message': '1', 'cat': res[0].category})
   return jsonify({'message': '0'})

@app.route("/api/cat", methods=['POST', 'GET', 'PUT', 'DELETE'])
def cat():
   return jsonify([obj.toJSON() for obj in Categorey.query.all()])

   

with app.app_context():
   db.create_all()

if __name__ == '__main__':
   app.run(debug=True)