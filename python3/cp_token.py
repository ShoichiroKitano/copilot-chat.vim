class Token:
    def __init__(self, token, expires_at):
        self.token = token
        self.expires_at = expires_at

    def expired(self, time):
        return self.expires_at < time
