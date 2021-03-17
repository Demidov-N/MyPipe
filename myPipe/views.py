from django.shortcuts import render

# Create your views here.

username = ''
def login(request):
    """The main login page, the first page people see"""
    return render(request, 'base.html')

def username_safe(request):
    """Saves a username for the following usage, redirects to the main page"""

def create_account(request):
    """Create account page, creates new account"""
    return render(request,  'create_channel.html')

def account_safe(request):
    """Saves the account in the database, redirects on the main page"""





def main_page(request):
    """The main page of a project"""


def search_video(request):
    """Once tried to search a video, outputs the first 20 values"""

def video_page(request):
    """A single video page, with comments, with an option to leave comments"""

def comment_safe(request):
    """Saves a comment in the database, updates the html page of a video"""



def account_info(request):
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





def video_create(request):
    """Page of video creation form"""

def video_safe(request):
    """Saves the video in the database, redirects to the success_page if everything right"""

def video_edit(request):
    """Edit video form"""

def video_edit_safe(request):
    """Safe edits on the video"""
