"""Assets that should be PRELOADED into the website on every page"""


from myPipe.models import Accounts
from myPipe.forms import UploadFileForm
def account_data(request):
    ses_acc = request.session.get("account", Accounts("empty"))
    account = ses_acc.info()
    channels = ses_acc.channels()
    subscribed = ses_acc.subscriptions()
    #TODO Change this to the normal call of the model, now just on one account

    return {"account": account, "acc_channels": channels, "subscribed": subscribed,
            "forms": UploadFileForm}