from django.shortcuts import render, HttpResponseRedirect, Http404
from django.template import RequestContext
from myPipe.models import Accounts, create_user, Channel
from myPipe.context_processors import *
from myPipe.forms import UploadFileForm

from PIL import Image
# Create your views here.

def login(request):
    return render(request, 'login.html')

def username_save(request):
    post = request.POST
    account = Accounts()
    if account.login(post['login'], post['password']):
        request.session['account'] = account
        return HttpResponseRedirect('main')
    else:
        return render(request, 'login.html', {"failed": True})
    """Saves a username for the following usage, redirects to the main page"""



def create_account(request):
    """Create account page, creates new account"""
    form = UploadFileForm()
    return render(request,  'register.html', {'form': form})

def account_safe(request):
    post = request.POST
    avatar = Image.open(request.FILES['file'])
    pass_not_same = post['password'] != post['password_val']
    username = post['username']
    user_info = {
        'username': username,
        'password': post['password'],
        'email': post['email'],
        'phone': post['phone']
    }
    create_user(user_info)
    avatar.save('static/user_data/avatar/' + username + '.png')
    return render(request, 'register.html')
    """Saves the account in the database, redirects on the main page"""






def main_page(request):
    """The main page of a project"""
    return render(request, 'main_page.html')


def search_video(request):
    """Once tried to search a video, outputs the first 20 values"""

def video_page(request):
    """A single video page, with comments, with an option to leave comments. FOR EVERY SESSION THERE IS ONE VIDEO WATCH"""

def comment_safe(request):
    """Saves a comment in the database, updates the html page of a video"""

def channel_views(request):
    return render(request, "acc_channels.html")


def account_info(request, username):
    account = Accounts(username)
    subscriptions = account.subscriptions()
    channels = account.channels()
    if len(channels) == 0:
        channels = False

    return render(request, 'account_page.html',
                  {"acc_now": account.info(),
                   "views": 33333,
                   "subscriptions": 1,
                   "sub_channels": subscriptions[:4],
                   "channels": channels})
    """Info on the account"""

def edit_account(request):
    """Edit account page"""

def edit_acc_safe(request):
    """Saves the changes of the account in the database.
    Outputs success page if successfully saved, back at account edit
    if something is off"""




def create_channel(request):
    """Create channel page, form"""

def channel_safe(request):
    """Saves the changes of the account in the database
    Outputs success page if successfully saved, back at channel edit
    if something is off"""

def channel_page(request):
    """The page of the channel, with channel overview and video creation"""





def video_create(request, channel):
    """Page of video creation form"""
    channel = Channel(channel)
    data = {
        'channel': channel.channel_info(),
        'form': UploadFileForm
    }
    return render(request, 'create_video.html', context=data)

def video_safe(request):
    """Saves the video in the database, redirects to the success_page if everything right"""

def video_edit(request):
    """Edit video form"""

def video_edit_safe(request):
    """Safe edits on the video"""
