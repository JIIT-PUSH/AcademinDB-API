from cloudant.client import Cloudant

def create_user_database(user):
    client = Cloudant('869a3a9a-8356-4ae9-8dbf-06e2f727e1ba-bluemix', '76147209959e786263adc8636eb25e3e61edeb63e68d1b7aa0bd183690f2808f', url='https://869a3a9a-8356-4ae9-8dbf-06e2f727e1ba-bluemix.cloudant.com', connect=True, auto_renew=True)
    session = client.session()
    if user['user_type'] == 'school':
        school_database = client.create_database(user['username'])
        user["_id"] = "root:profile"
        school_profile = school_database.create_document(user)

    if user['user_type'] == 'teacher':
        user["_id"] = "teacher:" + user["username"]
        teacher_database = client[user["data"]["school_code"]]
        teacher_profile = teacher_database.create_document(user)

    client.disconnect()