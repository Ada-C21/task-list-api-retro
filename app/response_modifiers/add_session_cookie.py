class AddSessionCookie:
    def __init__(self, response, result):
        session_bytes = str(result.id)
        response.set_cookie("SessionID", session_bytes, httponly=True, expires=result.expires_at)
