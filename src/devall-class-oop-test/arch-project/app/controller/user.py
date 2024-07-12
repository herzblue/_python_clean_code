from app.application.service.user import create_user
def signup():
    user = create_user(user_name='qq')
    return user