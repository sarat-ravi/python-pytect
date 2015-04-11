import os
import sys
import uuid

from peewee import *
from pytect.facepp import API, File, APIError

DB_NAME = 'pytect.db'
SERVER = 'http://api.us.faceplusplus.com/'
API_KEY = 'a5a46e29bd6f829b9cc2ec3bfab191c6'
API_SECRET = '7oEx2Rcv6sYztPUqedEN_1uJfoU6lfek'
DEBUG_DB = False

db = SqliteDatabase(DB_NAME)
db.connect()

def init():
    from pytect.facepp import API
    return API(API_KEY, API_SECRET, srv=SERVER)

api = init()
del init

class BaseModel(Model):
    class Meta:
        database = db
        
class Group(BaseModel):

    group_id = CharField(primary_key=True)
    group_name = CharField()
    
    @staticmethod
    def delete_groups():
        print "deleting all groups..."
        for group in Group.select():
            group.delete_group()
        
    @staticmethod
    def create_group(group_name):
        group_info = None
        if DEBUG_DB:
            generated_id = str(uuid.uuid4())
            group_info = {"group_id": generated_id}
        else:
            group_info = api.group.create(group_name=group_name)
            
        print "creating group {}".format(group_info)
        group = Group.create(group_id=group_info["group_id"], group_name=group_name)
        return group
    
    def add_people(self, people):
        print "adding people {} to group {}".format(people, self)
        if not DEBUG_DB:
            people_string = ",".join(map(lambda p: p.person_id, people))
            api.group.add_person(group_id=self.group_id, person_id=people_string)
            

    def delete_group(self):

        if not DEBUG_DB:
            try:
                api.group.delete(group_id=self.group_id)
            except APIError:
                pass

        self.delete_instance()
        print "deleted {}".format(self)
        
    def __repr__(self, *args, **kwargs):
        return "Group(group_name={}, group_id={})".format(self.group_name, self.group_id)
    

class Face(BaseModel):
    """
{u'face': [{u'attribute': {u'age': {u'range': 10, u'value': 46},
    u'gender': {u'confidence': 99.9983, u'value': u'Male'},
    u'race': {u'confidence': 99.9892, u'value': u'White'},
    u'smiling': {u'value': 24.7929}},
   u'face_id': u'32d7374fd03bb9e6cc0b5ab2cad296d4',
   u'position': {u'center': {u'x': 58.75, u'y': 61.316872},
    u'eye_left': {u'x': 50.444062, u'y': 49.661317},
    u'eye_right': {u'x': 67.459375, u'y': 50.239095},
    u'height': 51.851852,
    u'mouth_left': {u'x': 50.010937, u'y': 73.930864},
    u'mouth_right': {u'x': 65.039375, u'y': 74.59465},
    u'nose': {u'x': 59.295, u'y': 62.157202},
    u'width': 39.375},
   u'tag': u''}],
 u'img_height': 243,
 u'img_id': u'59db34f15c958a7c09ee322c26eb1d8a',
 u'img_width': 320,
 u'session_id': u'51c2a4ffadd14925b65c8b47c4ea66a4',
 u'url': None}
    """

    face_id = CharField(primary_key=True)
    image = CharField()
    
    @staticmethod
    def delete_faces():
        print "deleting all faces..."
        for face in Face.select():
            face.delete_face()

    @staticmethod
    def detect_and_create_faces(image_path, cache=False):
        print "detecting and creating faces from '{}'".format(image_path)
        assert os.path.exists(image_path)
        
        if cache:
            faces = Face.select().where(Face.image==image_path)
            faces = [f for f in faces]
            if faces:
                print "returning cached results for faces at image path: {}".format(image_path)
                return faces;

        faces_data = None
        if (DEBUG_DB): faces_data = {"face": [{"face_id": 12352}]}
        else: 
            faces_data = api.detection.detect(img=File(image_path))
        
        faces = []
        for face_data in faces_data["face"]:
            face = Face.create(face_id=face_data["face_id"], image=image_path)
            faces.append(face)
            
        return faces
    
    def delete_face(self):
        print "deleting {}".format(self)
        self.delete_instance()
        
    def __repr__(self, *args, **kwargs):
        return "Face(face_id='{}', image='{}')".format(self.face_id, self.image)
            

class Person(BaseModel):
    
    @staticmethod
    def delete_people():
        print "deleting all people..."
        for person in Person.select():
            person.delete_person()
    
    person_id = CharField(primary_key=True)
    person_name = CharField()
    
    # {u'added_face': 0, u'added_group': 0, u'person_id': u'3c3b1248e71b1d352b417432a65a66e0', u'person_name': u'Bob', u'tag': u''}

    @staticmethod
    def create_person(person_name):

        person_info = None;
        if DEBUG_DB:
            generated_id = str(uuid.uuid4())
            person_info = {"person_id": generated_id}
        else:
            person_info = api.person.create(person_name=person_name)

        print "creating person {}".format(person_info)
        person =  Person.create(person_id=person_info["person_id"], person_name=person_name)
        return person
    
    def add_faces(self, faces):
        print "adding {} to {}".format(faces, self)
        if DEBUG_DB: raise Exception("DEBUG_DB not supported")
        faces_string = ",".join(map(lambda f: f.face_id, faces))
        resp = api.person.add_face(person_id=self.person_id, face_id=faces_string)
    
    def delete_person(self):
        print "deleting {}".format(self)

        if not DEBUG_DB:
            api.person.delete(person_id=self.person_id)

        self.delete_instance()
        
    def __repr__(self, *args, **kwargs):
        return "Person(person_name={}, person_id={})".format(self.person_name, self.person_id)

def delete_models():
    print "deleting models..."
    Person.delete_people()
    Group.delete_groups()
    
def delete_caches():
    print "deleting caches..."
    Face.delete_faces()
    
def delete_all_models():
    delete_models()
    delete_caches()

TABLES_TO_CREATE = []
if not Person.table_exists(): TABLES_TO_CREATE.append(Person)
if not Group.table_exists(): TABLES_TO_CREATE.append(Group)
if not Face.table_exists(): TABLES_TO_CREATE.append(Face)
db.create_tables(TABLES_TO_CREATE);
