import pyrebase
import json


class Firebase:
    def __init__(self):
        with open(r"firebase/firebase-client.json") as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.auth = firebase.auth()

    # def sign_up(self, email, name, password):
    #     try:
    #         user = self.auth.create_user_with_email_and_password(email, password)
    #     except Exception as e:
    #         error = list(e.args)
    #         e = json.loads(error[1])
    #         if (
    #             e["error"]["message"]
    #             == "WEAK_PASSWORD : Password should be at least 6 characters"
    #         ):
    #             return "weak"
    #         else:
    #             return -1
    #     if not user:
    #         return False

    #     print(user["localId"])

    #     # create node uid in users node with email and password
    #     self.db.child("users").child(user["localId"]).set(
    #         {"email": email, "name": name, "password": password}
    #     )
    #     return name

    def sign_in(self, email, password):
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
        except Exception as e:
            print(e)
            return -1
        if not user:
            return False
        # return name from db
        return self.db.child("users").child(user["localId"]).child("name").get().val()


# Firebase().sign_up("test10@test.com", "name", "Test@123")
