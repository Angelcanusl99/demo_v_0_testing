import jwt
import datetime

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"


def create_token(user_name: str):
    payload = {
        "sub": user_name,
        "rol": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }

    token_encripted = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_encripted


def verify_token(token_recivided: str):
    try:
        payload_decoded = jwt.decode(
            token_recivided, SECRET_KEY, algorithms=[ALGORITHM])
        return payload_decoded

    except jwt.ExpiredSignatureError:
        return "ERROR: The token has expired. You need to log in again."

    except jwt.InvalidTokenError:
        return "ERROR: ¡Intruder Alert! This Token is false or has been altered."


if __name__ == "__main__":
    print("--- INITIATING SECURITY PROTOCOL ---")

    my_new_token = create_token("Angel_Admin")
    print(f"\n1. Token Generaded:\n{my_new_token}\n")

    result_verify = verify_token(my_new_token)
    print(f"2. Token Verify (Info inside):\n{result_verify}\n")

    token_false = my_new_token + "x"
    resultaded_hack = verify_token(token_false)
    print(f"3. Hackibg attempt:\n{resultaded_hack}\n")
