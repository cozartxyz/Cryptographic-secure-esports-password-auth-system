import bcrypt
# i got this from a more experienced friend of mine after bcrypt was giving me astronomical errors
salt = bcrypt.gensalt()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(password, hashed_password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def hash_ip(ip_address):
    return bcrypt.hashpw(ip_address.encode('utf-8'), salt).decode('utf-8')