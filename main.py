from flask import Flask, flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource,reqparse,abort,fields,marshal_with
""""

            video api code

"""


# create api with flask
app = Flask(__name__)
api = Api(app)
app.secret_key="me"
# database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# თუ ტემპის ფაილი გვინდა 'sqlite:///tmp/database.db'
db = SQLAlchemy(app)





# video parser for getting values and help for get values
# for updating video
videos_parser = reqparse.RequestParser() #auto parse reques as guidline
# guides
videos_parser.add_argument("name", type=str, help="give me name ! it's required",required=True) #help is erro msg
videos_parser.add_argument("views", type=int, help="give me views ! it's required",required=True) #help is erro msg
videos_parser.add_argument("likes", type=int, help="give me likes ! it's required",required=True) #help is erro msg

#  update with id without required
videos_parser_update = reqparse.RequestParser()
# guides
videos_parser_update.add_argument("name", type=str, help="give me name ! it's required") #help is erro msg
videos_parser_update.add_argument("views", type=int, help="give me views ! it's required") #help is erro msg
videos_parser_update.add_argument("likes", type=int, help="give me likes ! it's required") #help is erro msg


# model  instance for videos storing
class VideoModel(db.Model):
    # this id is equal to resource field id 
    id = db.Column(db.Integer, primary_key=True) #  any id wil be changed 
    #nullable it should have characters # 1000  characters is allowed only 
    name = db.Column(db.String(100), nullable = False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    # represent video values by id
    def __repr__(self):
        return f"Video (name = {name}, views = {views}, likes = {likes}"

db.create_all()

# resource fields for user to add something in VideoModel
# serializing object json format
resource_fields = {
    "id":fields.Integer,
    "name":fields.String,
    "views":fields.Integer,
    "likes":fields.Integer
}



# resource instance for API
class Videos(Resource):
    @marshal_with(resource_fields) # get return value and serialize it with resource_fields (make it as json format)
    def get(self,video_id):  
        # abort_id_err(video_id)
        result = VideoModel.query.filter_by(id = video_id).first() # everything with id and first of objects
        if not result:
            abort(404,message="video id not found")
        return result 

    @marshal_with(resource_fields) # return json formated
    def put(self,video_id):

        # შეამოწმე აიდი თუ უკვე ბაზაშია
        result = VideoModel.query.filter_by(id = video_id).first()
        if result:
            abort(409,message="video id taken")
        args = videos_parser.parse_args() # გაპარსე ყველა მონაცემი და არგში ჩასვი
        # create obj in database
        # ამოიღე გაპარსული და გაუგზავნე ბაზის მოდელს
        video = VideoModel(id = video_id, name = args["name"],views = args["views"] ,likes = args["likes"])
        db.session.add(video) # add
        db.session.commit() 
        return video, 201 
       

    # if someone want to change model
    # http method for updating
    @marshal_with(resource_fields) 
    def patch(self,video_id):      
        args = videos_parser.parse_args() # გაპარსე ყველა მონაცემი და არგში ჩასვი
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:            
            abort(404,message="video not exist can't be updated")
        # check if exist and not none so its updating only if it wants change
        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]: 
            result.likes = args["likes"]
        db.session.commit() # commit change
        return result 
        

    def delete(self,video_id):
        result = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404,message=f"video id '{video_id}' has already deleted  or not existed")
        VideoModel.query.filter_by(id = video_id).delete()
        db.session.commit()
        return  f'video id: "{result.id}"\nname: "{result.name}" has been deleted succesfully'

        
api.add_resource(Videos,"/videos/<int:video_id>")

if __name__== "__main__":
    app.run(debug=True)
