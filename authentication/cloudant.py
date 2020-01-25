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
          
        try:
            school_database = client['username']
        except:
            raise serializers.ValidationError('School does not exist.')
        #school_database = client.create_database(username)
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
        try:
            school = client[user["schoolcode"]]
        except:
            raise serializers.ValidationError('School does not exist.')
        teacher_search = "teacher:" + teacher_id
        if not teacher_search in school:
            raise serializers.ValidationError('You are not registered in school records. Please contact School Administration')
        else:   
            teacher = school[teacher_search]
            if teacher["name"] == user['name']:
                if teacher["dob"] == user['dob']:
                    if teacher["phone"] == user['phoneNumber']:
                        if teacher["email"] == user['emailAddress']:
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
                    if student["phoneNumber"] == user['phoneNumber']:
                        if student["emailAddress"] == user['emailAddress']:
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

def update_database(user):
    client = Cloudant('869a3a9a-8356-4ae9-8dbf-06e2f727e1ba-bluemix', '76147209959e786263adc8636eb25e3e61edeb63e68d1b7aa0bd183690f2808f', url='https://869a3a9a-8356-4ae9-8dbf-06e2f727e1ba-bluemix.cloudant.com', connect=True, auto_renew=True)
    session = client.session()

    if user['user_type'] == 'school':
        school_database = client("user['username']")
        root_document = school_database['root:profile']

        root_document['phone'] = user['phoneNumber']
        root_document['email'] = user['emailAddress']
        root_document['principal'] = user['principal']
        root_document['teacherCount'] = user['teacherCount']

    if user['user_type'] == 'teacher':
        school_database = client("user['schoolCode']")
        teacher_document = school_database['teacher:username']

        teacher_document['dob'] = user['dob']
        teacher_document['phone'] = user['phoneNumber']
        teacher_document['email'] = user['emailAddress']
        teacher_document['address'] = user['address']
        teacher_document['pincode'] = user['pincode']

    if user['user_type'] == 'student':
        school_database = client("user['schoolCode']")
        student_document = school_database['student:username']

        student_document['dob'] = user['dob']
        student_document['phone'] = user['phoneNumber']
        student_document['email'] = user['emailAddress']
        student_document['address'] = user['address']
        student_document['transport'] = user['transport']
        student_document['father_name'] = user['father_name']
        student_document['mother_name'] = user['mother_name']

    client.disconnect()