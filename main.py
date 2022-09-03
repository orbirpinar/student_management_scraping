from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import csv
import json
from os.path import exists

app = Flask(__name__)


@app.route("/api/v1/teachers", methods=['POST'])
def get_teachers():
    school_name = request.json['school_name']
    school_website = request.json['school_website']
    school_name = school_name.replace(' ', "_")
    fileName = f"teachers_data/{school_name}_teachers.json"
    if exists(fileName):
        data = get_from_cache(fileName)
        return jsonify(
            {'data': data}
        )

    url = f"{school_website}/teskilat_semasi.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    all_teacher_link_tag = soup.select(".sitemap li a")
    teachers = []
    for i in all_teacher_link_tag:
        name = i.find(text=True)
        nameDict = split_to_firstname_and_lastname(name)
        firstname = nameDict['firstname']
        lastname = nameDict['lastname']
        department = i.get("title", "No department")
        teacherObject = {'firstname': firstname, 'lastname': lastname, 'department': department}
        teachers.append(teacherObject)
    write_json(fileName, teachers)
    return jsonify(
        {'data': teachers}
    )


def split_to_firstname_and_lastname(name):
    nameList = name.split(" ")
    lastname = ""
    firstname = ""
    for i in nameList:
        if i[1].isupper():
            lastname += i + " "
        else:
            firstname += i + " "
    return {"firstname": firstname.strip(), "lastname": lastname.strip()}


@app.route("/api/v1/students")
def get_students():
    filename = 'students.json'
    if exists(filename):
        data = get_from_cache(filename)
        return jsonify(
            {"data": data}
        )
    data = csv_to_json()
    return jsonify(
        {"data": data}
    )


def csv_to_json():
    json_list = []
    with open("students.csv", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            _class = row['class'].split("/")
            row["lastname"] = row['name'].split().pop(-1)
            row["firstname"] = row['name'].rsplit(" ", 1)[0]
            level = _class[0]
            branch = _class[1]
            row['level'] = level.replace(". Sınıf", "").strip()
            row['branch'] = branch.replace("Şubesi", "").strip()
            json_list.append(row)
    write_json("students.json", json_list)
    return json_list


def write_json(file_name, content):
    with open(file_name, 'w+', encoding='utf-8') as jsonf:
        jsonString = json.dumps(content, indent=4)
        print(jsonString)
        jsonf.write(jsonString)


def get_from_cache(file_name):
    with open(file_name, encoding='utf-8') as file:
        return json.load(file)
