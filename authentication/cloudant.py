from cloudant.client import Cloudant
from cloudant.document import Document


def create_user_database(user):
    client = Cloudant('869a3a9a-8356-4ae9-8dbf-06e2f727e1ba-bluemix', '76147209959e786263adc8636eb25e3e61edeb63e68d1b7aa0bd183690f2808f', url='https://869a3a9a-8356-4ae9-8dbf-06e2f727e1ba-bluemix.cloudant.com', connect=True, auto_renew=True)
    #client = Cloudant('khushi', '1234', url='http://127.0.0.1:5984', connect=True, auto_renew=True)
    session = client.session()

    # SCHOOL
    if user['user_type'] == 'school':
        school_database = client.create_database(user['username'])
        user["_id"] = "root:profile"
        school_profile = school_database.create_document(user)
        class_data ={
            '_id':'root:class_list',
            'class_list':[]
        }
        class_list = school_database.create_document(class_data)
    
        teacher_division_data = {
            '_id':'root:teacherDivision',
            'division':[]
        }
        teacher_division = school_database.create_document(teacher_division_data)

        schools_database = client['schools']
        with Document(schools_database, user["subdistrict"]) as document:
            document['schools'].update({

                "name": user["name"],
                "code": user["schoolcode"]
            })

    # TEACHER
    elif user['user_type'] == 'teacher':
        user["_id"] = "teacher:" + user["username"]
        teacher_database = client[user["schoolcode"]]
        teacher_profile = teacher_database.create_document(user)

    # STUDENT
    elif user['user_type'] == 'student':
        user["_id"] = "student:" + user["username"]
        student_database = client[user["schoolcode"]]
        student_profile = student_database.create_document(user)

    client.disconnect()
