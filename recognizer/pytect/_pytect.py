"""
This is the pytect API
"""

from pytect.models import *
import time

def create_group(group_name, people=[]):
    group = Group.create_group(group_name)
    if people:
        group.add_people(people)
    return group

def create_person(person_name, groups=[]):
    person = Person.create_person(person_name=person_name)
    for group in groups:
        group.add_people([person])
        
    return person

def detect_faces(image_path, cache=False):
    faces = Face.detect_and_create_faces(image_path, cache)
    return faces

def get_person(person_name):
    person = Person.get(Person.person_name==person_name)
    return person

def identify(image_path, group):
    people = []
    groups = []
    scores = []

    try:
        response = api.recognition.identify(group_id=group.group_id, img=File(image_path))
        top_candidate = response["face"][0]["candidate"][0]
        candidate_id = top_candidate["person_id"]
        score = top_candidate["confidence"]

        person = Person.get(Person.person_id==candidate_id)
        people.append(person)
        groups.append(group)
        scores.append(score)

    except Exception as e:
        print e

    return people, groups, scores

def train_group(group):
    train_session = api.train.identify(group_id=group.group_id)
    
    while (True):
        time.sleep(0.1)
        resp = api.info.get_session(session_id=train_session["session_id"])
        if resp["status"] == "SUCC":
            if resp["result"]:
                print "training completed successfully"
                return True
            else:
                print "training failed: {}".format(resp)
                return False
            break;
        
def clear():
    delete_models()
    
def clear_cache():
    delete_caches()
