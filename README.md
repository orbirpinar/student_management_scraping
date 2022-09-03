## Students and Teachers Seeder

- Getting teacher's first name and last name by school.
- Getting students information by csv file.

#### Installing / Getting started
- Install dependencies

`pip install -r requirements.txt`

- Run project

`flask --app main run`

#### How to Use
 
 - To get teachers information based on a website

endpoint= "localhost:5000/api/v1/teachers"

method=POST

example curl

```
curl --location --request POST 'http://localhost:5000/api/v1/teachers' \
--header 'Content-Type: application/json' \
--data-raw '{
    "school_name": "name",
    "school_website": "website"
}'
```
change name and website field however you want






