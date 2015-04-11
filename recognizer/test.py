#!/usr/bin/env python2
import sys
import os
import os.path
import time
from pprint import pprint

# from pytect.models import *
import pytect

DEBUG = False

YALEFACES_DIR = "data/yalefaces"

def generate_models_from_yalefaces():
    print "generating yalefaces models..."
    # import IPython; IPython.embed()
    # yalefaces = Group.create_group(group_name="yalefaces")
    yalefaces = pytect.create_group(group_name="yalefaces")
    people = []
    
    for parent_folder, subfolders, files in os.walk(YALEFACES_DIR):
        previous_person = None
        previous_faces = []
        for file_name in files:
            if not file_name.startswith("subject"): 
                continue

            subject_tokens = file_name.split(".")
            subject_name = subject_tokens[0]
            action = subject_tokens[1]
            
            if previous_person == None or not previous_person.person_name == subject_name:
                if previous_person and previous_faces: 
                    previous_person.add_faces(previous_faces)

                print "new person detected: {}".format(subject_name)
                previous_person = pytect.create_person(person_name=subject_name)
                # yalefaces.add_person(previous_person)
                previous_faces = []
                people.append(previous_person)

            image_path = os.path.join(parent_folder, file_name)
            more_faces = pytect.detect_faces(image_path, cache=True)
            previous_faces.extend(more_faces)

        if previous_person and previous_faces: 
            previous_person.add_faces(previous_faces)
        break
            
    yalefaces.add_people(people)
    return yalefaces, people

def test_yalefaces(yalefaces):
    for parent_folder, subfolders, files in os.walk(YALEFACES_DIR):
        previous_person = None
        for file_name in files:
            if not file_name.startswith("subject"): 
                continue

            subject_tokens = file_name.split(".")
            subject_name = subject_tokens[0]
            action = subject_tokens[1]

            if previous_person == None or not previous_person.person_name == subject_name:
                # print "new person detected: {}".format(subject_name)
                # previous_person = Person.get(Person.person_name==subject_name)
                previous_person = pytect.get_person(subject_name)

            image_path = os.path.join(parent_folder, file_name)
            
            candidates, groups, scores = pytect.identify(image_path, yalefaces)
            top_candidate = candidates[0]
            top_score = scores[0]
            
            if top_candidate.person_id == previous_person.person_id:
                print "PASS: Face in image '{}' is identified correctly as {} with confidence {}".format(image_path, previous_person, top_score)
            else:
                print "FAIL: Face in image '{}' should be identified as {}".format(image_path, previous_person)
                
            # resp = api.recognition.identify(group_id=yalefaces.group_id, img=File(image_path))

            # verify(resp, previous_person, image_path)
            
def verify(resp, person, image_path):
    passed = False
    try:
        candidates = resp["face"]
        # import IPython; IPython.embed()
        top_person_candidate = candidates[0]["candidate"][0]
        passed = top_person_candidate["person_id"] == person.person_id
    except Exception, e:
        print e

    # passed_string = "PASS" if passed else "FAIL"
    if passed:
        confidence = top_person_candidate["confidence"]
        print "PASS: Face in image '{}' is identified correctly as {} with confidence {}".format(image_path, person, confidence)
    else:
        print "FAIL: Face in image '{}' should be identified as {}".format(image_path, person)
        pprint(resp)
        
def run():
    print "creating models..."
    yale, people = generate_models_from_yalefaces()

    print "training models (this could take a while)..."
    success = pytect.train_group(yale)
    
    print "testing recognition..."
    test_yalefaces(yale)
    print "test complete"

def main():
    try:
        print "starting test..."
        pytect.clear()

        # run test.
        run()

        if DEBUG: import IPython; IPython.embed()
    finally:
        pytect.clear()
        print "done"

if __name__ == '__main__':
    main()
