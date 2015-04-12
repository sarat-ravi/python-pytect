#Overview
overview

##Recognizer
###Overview
This is the component that can detect and recognize faces, and the groups these faces belong to. The `make install` target installs the package in such a way that one can edit the source while developing in a completely random path.

###Install
```
cd recognizer
make install
```
###Uninstall
```
make clean
```

###Test
The test script trains on the `yalefaces` dataset, and tests the code by trying to detect and recognize the same faces it trained on, asserting that the confidence scores are greater than 0.95

```
make test
```

###Basic Usage

```python
import pytect

# create groups
yale = pytect.create_group(group_name="yale")
berkeley = pytect.create_group(group_name="berkeley")

# create people
bob = pytect.create_person(person_name="bob")
alice = pytect.create_person(person_name="alice")
aaron = pytect.create_person(person_name="aaron")

# add people to groups
yale.add_people([bob, alice])
berkeley.add_people([alice, aaron])

# train the images in the groups
pytect.train_group(yale)
pytect.train_group(berkeley)

# identify people and their groups from any image!
candidates, groups, scores = pytect.identify("bob.jpg", yale)
assert candidates[0] == bob and groups[0] == yale and scores[0] >= 0.95

# clear all models and forget everything
pytect.clear()

# clear any cached data as well
pytect.clear_cache()
```
