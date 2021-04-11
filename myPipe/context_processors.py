from myPipe.models import Account
def account_data(request):
    account = Account.info()
    channels = Account.channels()

    #TODO Change this to the normal call of the model, now just on one account
    account = {
        'username': 'RedBear',
        'email': 'redbear@none.com',
        'avatar': 'redbear.png'
    }

    channels = [
        {
            'name': "PIDARAS TV",
            'subscribers': 2,
            'videos': 0,
            'owner': 'RedBear',
            'avatar': 'empty.jpg'
        },
        {
            'name': "UEBOK TV",
            'subscribers': 30,
            'videos': 3,
            'owner': 'RedBear',
            'avatar': 'empty.jpg'
        }
    ]
    return {"account": account, "channels": channels}