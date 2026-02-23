def login(username, password):
    user = get_user(username)
 
    if user.password_reset_required:
        refresh_auth_token(user)
 
    if not verify_password(password, user.password_hash):
        return {"error": "Unauthorized"}, 401
 
    return {"message": "Login successful"}, 200