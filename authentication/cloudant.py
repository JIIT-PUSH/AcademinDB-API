from cloudant.client import Cloudant
from cloudant.document import Document
from rest_framework import serializers


def create_user_database(user):
    client = Cloudant('869a3a9a-8356-4ae9-8dbf-06e2f727e1ba-bluemix', '76147209959e786263adc8636eb25e3e61edeb63e68d1b7aa0bd183690f2808f', url='https://869a3a9a-8356-4ae9-8dbf-06e2f727e1ba-bluemix.cloudant.com', connect=True, auto_renew=True)
    session = client.session()
    # SCHOOL
    if user['user_type'] == 'school':
        username = user['username']
        user.pop('username')
        school_database = client.create_database(username)
        user["_id"]= "root:profile"
        user["schoolcode"]: username
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
        with Document(schools_database, user['subDistrict']) as document:
            document['schools'].append({
                "name": user["name"],
                "code": username
            })

    # TEACHER
    elif user['user_type'] == 'teacher':
        teacher_id = user['username']
        user.pop('username')
        school = client[user["schoolcode"]]
        teacher_search = "teacher:" + teacher_id
        if not teacher_search in school:
            raise serializers.ValidationError('You are not registered in school records. Please contact School Administration')
        else:   
            teacher = school[teacher_search]
            if teacher["name"] == user['name']:
                if teacher["dob"] == user['dob']:
                    if teacher["phone"] == user['phone']:
                        if teacher["email"] == user['email']:
                            pass
                        else:
                            raise serializers.ValidationError('Email Address does not match')
                    else:
                        raise serializers.ValidationError('Phone Number does not match')  
                else:
                    raise serializers.ValidationError('Date of Birth does not match')   
            else:
                raise serializers.ValidationError('Name does not match') 
 
    # STUDENT
    elif user['user_type'] == 'student':
        student_id = user['username']
        user.pop('username')
        school = client[user["schoolcode"]]
        student_search = "student:" + student_id
        if not student_search in school:
            raise serializers.ValidationError('You are not registered in school records. Please contact School Administration')
        else:           
            student = school[student_search]
            if student["name"] == user['name']:
                if student["dob"] == user['dob']:
                    if student["phone"] == user['phone']:
                        if student["email"] == user['email']:
                            pass
                        else:
                            raise serializers.ValidationError('Email Address does not match')
                    else:
                        raise serializers.ValidationError('Phone Number does not match')  
                else:
                    raise serializers.ValidationError('Date of Birth does not match')   
            else:
                raise serializers.ValidationError('Name does not match') 

    client.disconnect()
