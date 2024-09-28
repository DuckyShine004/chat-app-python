from src.common.utilities.security import Security

psw = "asd"
hpsw = Security.get_hashed_password(psw)
print(psw)
print(Security.check_password(psw, hpsw))
