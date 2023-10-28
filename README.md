# sota-backend
This is SoTA backend repository

## What is Sota?
SoTA or **S**ystem of **T**ournamental **A**thleticism is the software from IOC (Skill isuue? Group) which is part of Software Process and Project Management course.

## How to run
1. Firstly, install the required packages using:
```
pip install -r requirements.txt
```
2. Then create a ```.env``` file according to sample.env given.

3. Lastly, to run the app, use:
```
uvicorn sota.main:app
```

## How to create database
1. Create ```dump``` folder in mongodb folder.
2. Copy ```Sota``` folder from ```dump_data``` in the repository to new ```dump``` folder that you create in mongodb folder.
3. Run this command in terminal or docker terminal:
```
mongorestore  dump/
```


## Demo values for collections
### Audient
```
"country_code": "TH",
"sport_id": [1],
"gender": "M",
"age": 21
```
### Medal
```
"country_code": "TH",
"country_name": "Thailand",
"sports": [
   {
    "sport_id": 1,
    "type_id": 1,
    "gold": 0,
    "silver": 0,
    "bronze": 0
   }
]
```
### Sport
```
"sport_id": 1,
"sport_name": "test",
"sport_summary": "test",
"participating_countries": ["TH", "JP"]
```
### Subsport
```
"sport_id": 1,
"type_id": 1,
"type_name": "Men 100m",
"participating_countries": [
"US", "DE", "JP"
]
```