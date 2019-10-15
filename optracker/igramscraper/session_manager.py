import os


class CookieSessionManager:
    def __init__(self, session_folder, filename):
        self.session_folder = session_folder
        self.filename = filename

    def get_saved_cookies(self):
        try:
            f = open(self.session_folder + self.filename, 'r') 
            return f.read()
        except FileNotFoundError:
            return None

    def set_saved_cookies(self, cookie_string):
        if not os.path.exists(self.session_folder):
            os.makedirs(self.session_folder)

        with open(self.session_folder + self.filename,"w+") as f:
            f.write(cookie_string)

    def empty_saved_cookies(self):
        try:
            os.remove(self.session_folder + self.filename)
        except FileNotFoundError:
            pass
