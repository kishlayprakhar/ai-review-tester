# A sloppy, insecure code snippet for testing:
def login_user(username, password):
    # DANGEROUS: Exposed credentials and vulnerable string formatting
    AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE" 
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return query
