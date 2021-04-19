from django.shortcuts import render, HttpResponseRedirect, Http404, redirect
from django.template import RequestContext
from myPipe.database import Accounts, Functions, Channel, Video
from myPipe.context_processors import *
from myPipe.forms import UploadFileForm
import myPipe.video_connector as vc
from PIL import Image
# Create your views here.

def login(request):
    request.session.flush()
    request.session['videos'] = []
    request.session['liked'] = []
    return render(request, 'login.html')

def username_save(request):
    post = request.POST
    account = Accounts(post['login'])
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
    username = post['username']
    user_info = {
        'username': username,
        'password': post['password'],
        'email': post['email'],
        'avatar': username + ".png",
        'phone': post['phone']
    }
    f = Functions()
    not_exist = f.create_account(user_info)
    if (not_exist):
        request.session['account'] = Accounts(username)
        avatar.save('static/user_data/avatar/' + username + '.png')
        return redirect("main")
    else:
        return render(request, 'register.html', context= {
            'form' : UploadFileForm(),
            'acc_exist': not not_exist,
        })
    """Saves the account in the database, redirects on the main page"""






def main_page(request):
    """The main page of a project"""
    f = Functions()
    videos = f.get_videos()
    for video in videos:
        video["thumbnail"] = vc.get_thumbnails(video)
    return render(request, 'main_page.html', context={"videos": videos})


def search_video(request):
    """Once tried to search a video, outputs the first 20 values"""

def video_page(request, id):
    """A single video page, with comments, with an option to leave comments. FOR EVERY SESSION THERE IS ONE VIDEO WATCH"""
    video = Video(id)

    if id not in request.session["videos"]:
        request.session["videos"] += [id]
        video.view_video(request.session.get("account").user)
    info = video.get_info()
    if info.get("type") == "youtube":
        url = vc.youtube_url(info["location"])
    else:
        url = "https://stream.mux.com/" + vc.playback_id(info["location"] + ".m3u8")
    comments = video.get_commments()
    replies = video.get_comment_replies()
    ch = Channel(info["channel"])
    more = ch.videos(4)
    ac = request.session.get("account")
    for m in more:
        m["thumbnail"] = vc.get_thumbnails(m)
    return render(request, "video.html", context= {
        "video": info,
        "comments": comments,
        "replies": replies,
        "url": url,
        "liked": (id not in request.session.get("liked", [])),
        "disliked": (id not in request.session.get("disliked", [])),
        "more": more,
    })

def comment_safe(request, video_id, username, id_replied):
    """Saves a comment in the database, updates the html page of a video"""
    text = request.GET["comment"]
    if id_replied == 0:
        id_replied = None
    video = Video(video_id)
    video.leave_comment(username, text, id_replied)
    return redirect("video", video_id)

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
    return render(request, "create_channel.html", context={'form': UploadFileForm})



def channel_safe(request):
    """Saves the changes of the account in the database
    Outputs success page if successfully saved, back at channel edit
    if something is off"""
    ac = request.session['account']
    if request.FILES.get('file', False):
        info = request.POST.dict()
        avatar = Image.open(request.FILES['file'])
        info["avatar"] = info["name"] + ".png"
        info["owner"] = info["name"] + ".png"
    else:
        info = request.POST.dict()
        avatar = Image.open("static/user_data/channel_avatar/empty.png")
        info["avatar"] = "empty.png"
    response = ac.create_channel(info)
    if response and info['name'] != "":
        avatar.save('static/user_data/channel_avatar/' + info["name"] + '.png')
        return redirect("channel", info['name'])
    else:
        return render(request, "create_channel.html", context=
        {
            'form': UploadFileForm,
            'name_exist': not response,
            'empty_name': info['name'] == ""
        })

def channel_page(request, channel):
    """The page of the channel, with channel overview and video creation"""
    ch = Channel(channel)
    info = ch.channel_info()
    ac = Accounts(info["owner"])
    other = ac.channels()
    videos = ch.videos(6)
    subscribed = ac.subscribed(channel)
    if len(videos) != 0:
        for video in videos:
            video["thumbnail"] = vc.get_thumbnails(video)
    return render(request, "channel_page.html", context={
        "channel": info,
        "videos": videos,
        "streams": [],
        'channels': other,
        'same_acc': ch.channel_info()["name"] == request.session.get("account", ""),
        'if_subscribed': subscribed,
    })


def subscribe(request, channel):
    ac = request.session["account"]
    ac.subscribe(channel)
    return redirect("channel", channel)


def unsubscribe(request, channel):
    ac = request.session["account"]
    ac.unsubscribe(channel)
    return redirect("channel", channel)

def video_create(request, channel):
    """Page of video creation form"""
    channel = Channel(channel)
    data = {
        'channel': channel.channel_info(),
        'form': UploadFileForm
    }
    return render(request, 'create_video.html', context=data)

def video_safe(request, type, channel):
    """Saves the video in the database, redirects to the success_page if everything right"""
    if type == "direct":
        post = request.POST
        files = request.FILES
        video_file = files.get('video')
        vid = {
            "name": post["name"],
            "description": post["description"],
            "location": vc.playback_id(id),
            "channel": channel,
            'type': "direct"
        }
        c = Channel(channel)
        c.create_video(vid)
        return redirect("main")
    else:
        post = request.POST.dict()
        vid = {
            "name": post["name"],
            "description": post["description"],
            "location": vc.get_id(post['link']),
            "channel": channel,
            'type': type
        }
        c = Channel(channel)
        c.create_video(vid)
        return redirect("main")


def video_edit(request):
    """Edit video form"""

def video_edit_safe(request):
    """Safe edits on the video"""


def video_delete(request, video):
    vid = Video(video)
    ch = vid.get_info()["channel"]
    vid.delete_video()
    return redirect("channel", ch)

def channel_delete(request, channel):
    ch = Channel(channel)
    ch.delete_channel()
    return redirect("my_channels")

def search(request):
    searching = request.POST["search"] + "%"
    f = Functions()
    video = f.search_video(searching)
    for vid in video:
        vid["thumbnail"] = vc.get_thumbnails(video)
    streams = f.search_stream(searching)
    for strem in streams:
        strem["thumbnail"] = vc.get_thumbnails(video)

    return render(request, "search_page.html", context={
        "search": search,
        "videos": video,
        "streams": streams
    })
