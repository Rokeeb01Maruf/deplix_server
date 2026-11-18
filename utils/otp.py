import secrets
import hashlib
import hmac
from decouple import config
from server.redis import redis_client

class GenerateOtp:
    def __init__(self, purpose, user_id):
        self.purpose=purpose
        self.user_id = user_id
        self.secret = config("OTP_SECRET_KEY")

    def generate(self):
        self.otp = f"{secrets.randbelow(1_000_000):06d}"
        return self.otp

    def hash(self):
        digest = hmac.new(
            self.secret.encode(),
            self.otp.encode(),
            hashlib.sha256
        ).hexdigest()

        self.digest = digest

    def store(self):
        self.generate()
        self.hash()
        redis_client.set(
            f"otp:{self.purpose}:{self.user_id}",
            self.digest,
            ex=300
        )

        return self.otp

class VerifyOtp:
    def __init__(self, purpose, user_id, otp):
        self.purpose = purpose
        self.user_id = user_id
        self.otp = otp

    def retrieve(self):
        self.digest = redis_client.get(f"otp:{self.purpose}:{self.user_id}")

    def verify(self):
        if self.digest == None:
            return None

        return hmac.compare_digest(self.otp, self.digest)