import hashlib
import hmac
from decouple import config
from server.redis import redis_client

def hash_otp(otp):
    secret = config("OTP_SECRET_KEY")
    return hmac.new(
            secret.encode(),
            otp.encode(),
            hashlib.sha256
        ).hexdigest()

def store_otp(user_id, purpose, hash):
    key = f"otp:{purpose}:{user_id}"
    redis_client.set(
        key,
        hash,
        ex=300
    )

def retrieve_otp(user_id, purpose):
    key = f"otp:{purpose}:{user_id}"
    return redis_client.get(key)

def verify_otp(digested, digest):
    return hmac.compare_digest(digested, digest)

def store_reset_token(userid, purpose, token):
    key = f"token:{purpose}:{userid}"

    redis_client.set(
        key,
        token,
        ex=300
    )

def retrieve_reset_token(userid, purpose):
    key = f"token:{purpose}:{userid}"
    token = redis_client.get(key)

    if token:
        redis_client.delete(key)

    return token