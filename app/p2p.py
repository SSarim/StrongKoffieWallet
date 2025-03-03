from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print("Hash for password1:", pwd_context.hash("password1"))
print("Hash for password2:", pwd_context.hash("password2"))
