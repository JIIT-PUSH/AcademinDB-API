from cloudant.client import Cloudant

def create_user_database(user):
    client = Cloudant('khushi', '1234', url='http://127.0.0.1:5984', connect=True, auto_renew=True)
    session = client.session()
    if user['user_type'] == 'school':
        school_database = client.create_database(user['username'])
        user["_id"] = "root:profile"
        # temp = user['data']
        # user['data'].pop()
        # for key in temp:
        #     user.add(key,value)
        school_profile = school_database.create_document(user)

    if user['user_type'] == 'teacher':
        user["_id"] = "teacher:" + user["username"]
        teacher_database = client[user["data"]["school_code"]]
        teacher_profile = teacher_database.create_document(user)

    client.disconnect()