class ClearSessionCookie:
    def __init__(self, response, result):
        response.set_cookie("SessionID", "", httponly=True, max_age=0)
