def detectUser(user):
    if user.user_type==1:
        return 'vendordashboard'
    elif user.user_type==2:
        return 'customerdashboard'
    else:
        return '/admin'