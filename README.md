# sota-backend
This is SoTA backend repository

## What is Sota?
SoTA or **S**ystem of **T**ournamental **A**thleticism is the software from IOC (Skill isuue? Group) which is part of Software Process and Project Management course.

## How to run
Firstly, install the required packages using:
```
pip install -r requirements.txt
```
Then, to run the app use:
```
uvicorn main:app
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