import jwt
import datetime
from fastapi import HTTPException


class ApiKey:
    def __init__(self,secret):
        self.key=secret
    def generateKey(self):
        payload = {
            "server":"dns"
        }
        token = jwt.encode(payload,self.key,algorithm="HS256")
        return token
    def verifyToken(self,token):
        try:
            decoded = jwt.decode(token, self.key, algorithms=["HS256"])
            return decoded  # Trả về payload nếu hợp lệ
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")