import sys
import os
import zipimport
from datetime import datetime
import json
import pickle
from config import info

TOKEN = pickle.load(open(".ok_refresh", "rb"))['access_token']
COURSE = '61a'
#ASSIGNMENT = 'hog'
ASSIGNMENT = 'hog'

import requests
import json
import subprocess, threading

BASE = 'https://ok-server.appspot.com'
#BASE = 'http://localhost:8080'
QUEUE_ENDPOINT = BASE + '/api/v1/queue'
COURSE_ENDPOINT = BASE + '/api/v1/course'
ASSIGN_ENDPOINT = BASE + '/api/v1/assignment'
GROUP_ENDPOINT = BASE + '/api/v1/group'
USER_ENDPOINT = BASE + '/api/v1/user'
SUBM_ENDPOINT = BASE + '/api/v1/submission'
GAE_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

params = {'access_token': TOKEN}

def get_all_students(course):
    raw_data = requests.get(COURSE_ENDPOINT + "/" + str(course) + "/get_students?fields={\"user\":true, \"id\":true}", params=params).json()['data']
    students = [(x['user']['email'], x['id']) for x in raw_data]
    return students

def get_all_backups(student):
    num_backups = 1000
    while True:
        response = requests.get(USER_ENDPOINT + "/" + str(student[0]) + "/get_backups?assignment=" + str(info[ASSIGNMENT]['key']) \
                                   + "&quantity=" + str(num_backups), params=params)
        print(response)
        all_backups = response.json()['data']
        if len(all_backups) < num_backups:
            return all_backups
        else:
            num_backups += 1000

def scrub_backup (backup):
    if type(backup) == type({}):
        if 'email' in backup:
            del backup['email']
        for key in backup:
            scrub_backup(backup[key])
    if type(backup) == type([]):
        for item in backup:
            scrub_backup(item)
    
def main():
    subprocess.call(['mkdir', ASSIGNMENT])

    try:
        all_students = pickle.load(open("student_cache.pkl", "rb"))
    except Exception as e:
        all_students = get_all_students(info[COURSE])
        pickle.dump(all_students, open("student_cache.pkl", "wb"))

    try:
        processed_students = pickle.load(open(ASSIGNMENT+"processed_cache.pkl", "rb"))
    except Exception as e:
        processed_students = []
    
    new_processed = []
    for student, sid in all_students:
        if student in processed_students:
            processed_students.remove(student)
            new_processed.append(student)
            print("Removed from cache")
            continue

        new_processed.append(student)
        backups = get_all_backups(student)
        scrub_backup (backups)
        subprocess.call(['mkdir', ASSIGNMENT + "/" + str(sid)])
  
        with open(ASSIGNMENT + "/" + str(sid) + "/backups.pkl", "wb") as f:
            pickle.dump(backups, f)
            f.flush()
            os.fsync(f.fileno())

        print("Processed {0} out of {1}".format(len(new_processed), len(all_students)))
        pickle.dump(new_processed, open(ASSIGNMENT+"processed_cache.pkl", "wb"))

if __name__ == "__main__":
    main()
