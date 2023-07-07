class User():
    def __init__(self, username, password, active=True):
        self.id = id
        self.username = username
        self.active = active
        self.password = password

    def is_active(self):
        return self.active 
    
    def is_authenticated(self):
        return True

    def get_id(self):
        return self.username

USERS = {
    "admin": User("admin", "12345678")
}

def confirmUserLogin(login, password):
    if USERS.get(login):
        user = USERS.get(login)
        if user.password == password:
            response = {"status":True, "message":"Login Successfull!"}
            return response
        else:
            response = {"status":False, "message":"Wrong password, please try again."}
            return response
    else:
        response = {"status":False, "message":"User does not exist, please try again."}
        return response