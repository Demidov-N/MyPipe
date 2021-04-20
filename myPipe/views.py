from django.shortcuts import render, HttpResponseRedirect, Http404, redirect
from django.template import RequestContext
from myPipe.models import Accounts, Functions, Channel, Content
from myPipe.context_processors import *
from myPipe.forms import UploadFileForm
import myPipe.video_connector as vc
from PIL import Image
# Create your views here.

def login(request):
    """The first login page"""
    request.session.flush()
    request.session['videos'] = []
    request.session['liked'] = []
    return render(request, 'login.html')

def username_save(request):
    """Saves a username for the following usage, if credentials are right, redirects to the main page"""
    post = request.POST
    account = Accounts(post['login'])
    if account.login(post['login'], post['password']):
        request.session['account'] = account
        return HttpResponseRedirect('main')
    else:
        return render(request, 'login.html', {"failed": True})



def create_account(request):
    """Create account page, creates new account"""
    form = UploadFileForm()
    return render(request,  'register.html', {'form': form})

def account_safe(request):
    """Saves the account in the database, redirects on the main page"""
    post = request.POST
    if request.FILES.get('file', False):
        info = request.POST.dict()
        avatar = Image.open(request.FILES['file'])
        info["avatar"] = info["username"] + ".png"
    else:
        info = request.POST.dict()
        avatar = Image.open("static/user_data/avatar/empty.png")
        info["avatar"] = "empty.png"
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


def account_update(request):
    """Update form of the account"""
    return render(request, "change_page.html", context={
        "form": UploadFileForm()
    })

def account_usafe(request, acc):
    """Saves the update of the account"""
    post = request.POST
    if request.FILES.get('file', False):
        info = request.POST.dict()
        avatar = Image.open(request.FILES['file'])
        info["avatar"] = info["username"] + ".png"
    else:
        avatar = Image.open("static/user_data/avatar/" + acc + ".png")
    username = post['username']
    user_info = {
        'username': username,
        'password': post['password'],
        'email': post['email'],
        'avatar': username + ".png",
        'phone': post['phone']
    }
    f = Functions()
    not_exist = f.update_account(user_info, acc)
    if (not_exist):
        request.session['account'] = Accounts(username)
        avatar.save('static/user_data/avatar/' + username + '.png')
        return redirect("account", username)
    else:
        return render(request, 'change_page.html', context= {
            'form' : UploadFileForm(),
            'acc_exist': not not_exist,
        })
    """Updates the account in the database, redirects on the main page"""





def main_page(request):
    """The main page of a project"""
    f = Functions()
    videos = f.get_videos()
    streams = f.get_streams()
    for video in videos:
        video["thumbnail"] = vc.get_thumbnails(video)
    for stream in streams:
        stream["thumbnail"] = vc.stream_thumbnails(stream)
    return render(request, 'main_page.html', context={
        "videos": videos,
        "streams": streams
    })


def video_page(request, id):
    """A single video page, with comments, with an option to leave comments. FOR EVERY SESSION THERE IS ONE VIDEO WATCH"""
    video = Content(id)

    if id not in request.session["videos"]:
        request.session["videos"] += [id]
        video.view_video(request.session.get("account").user)
    info = video.get_info()
    if info.get("type") == "youtube":
        url = vc.youtube_url(info["location"])
    else:
        url = "https://stream.mux.com/" + vc.playback_id(info["location"]) + ".m3u8"
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
        "more": more,
    })

def comment_safe(request, video_id, username, id_replied):
    """Saves a comment in the database, updates the html page of a video"""
    text = request.GET["comment"]
    if id_replied == 0:
        id_replied = None
    video = Content(video_id)
    video.leave_comment(username, text, id_replied)
    return redirect("video", video_id)

def channel_views(request):
    """Gets the page of the account"""
    return render(request, "acc_channels.html")


def account_info(request, username):
    """Info on the account"""
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



def edit_acc_safe(request):
    """Saves the changes of the account in the database.
    Outputs success page if successfully saved, back at account edit
    if something is off"""




def create_channel(request):
    """Create channel page, form"""
    return render(request, "create_channel.html", context={'form': UploadFileForm})

def delete_acc(request, acc):
    """Create channel page, form"""
    ac = Accounts(acc)
    ac.close_account()
    request.session.flush()
    return redirect("login")


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
    acc_now = request.session["account"]
    other = ac.channels()
    videos = ch.videos(6)
    subscribed = acc_now.subscribed(channel)
    streams = ch.streams()
    if len(videos) != 0:
        for video in videos:
            video["thumbnail"] = vc.get_thumbnails(video)
    for stream in streams:
        stream["thumbnail"] = vc.stream_thumbnails(stream)
    return render(request, "channel_page.html", context={
        "channel": info,
        "videos": videos,
        "streams": streams,
        'channels': other,
        'same_acc': ch.channel_info()["name"] == request.session.get("account", ""),
        'if_subscribed': subscribed,
    })


def subscribe(request, channel):
    """Subscribes to the channel"""
    ac = request.session["account"]
    ac.subscribe(channel)
    return redirect("channel", channel)


def unsubscribe(request, channel):
    """Unsubscribes to the channel"""
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
        a_id = vc.upload(video_file)
        vid = {
            "name": post["name"],
            "description": post["description"],
            "location": a_id,
            "channel": channel,
            'type': type
        }
        c = Channel(channel)
        c.create_video(vid)
        return redirect("channel", channel)
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
        return redirect("channel", channel)


def content_update(request, id):
    """Updates the information of the video"""
    vid = Content(id)
    info = vid.get_info()
    ch = Channel(info["channel"])
    c_info = ch.channel_info()
    return render(request, "video_edit.html", context={
        "content": info,
        "channel": c_info
    })
    """Edit video form"""


def stream_update(request, id):
    """Updates the information of the stream"""
    vid = Content(id)
    info = vid.stream_info()
    ch = Channel(info["channel"])
    c_info = ch.channel_info()
    return render(request, "stream_edit.html", context={
        "content": info,
        "channel": c_info
    })


def stream_update_safe(request, id):
    """Saves the updates of the stream in the database"""
    vid = Content(id)
    info = request.POST.dict()
    vid.change_info(info)
    return redirect("stream", id)


def video_edit_safe(request, id):
    """Saves the updates of the video in the database"""
    vid = Content(id)
    info = request.POST.dict()
    vid.change_info(info)
    return redirect("video", id)


def video_delete(request, id, channel):
    """Deletes the video and all its contents"""
    vid = Content(id)
    info = vid.get_info()
    if info["type"] == "direct":
        vc.delete_asset(info["location"])
    vid.delete_video()
    return redirect("channel", channel)

def stream_delete(request, id, channel):
    """Deletes stream and all its contents"""
    vid = Content(id)
    info = vid.stream_info()
    vid.delete_video()
    if info["type"] == "direct":
        vc.delete_stream(info["location"])
    return redirect("channel", channel)


def channel_delete(request, channel):
    """Deletes the channel and all its contents"""
    ch = Channel(channel)
    ch.delete_channel()
    return redirect("my_channels")

def search(request):
    """Searches the contents and gets all that has the text as in search"""
    searching = "%" + request.POST["search"] + "%"
    f = Functions()
    video = f.search_video(searching)
    for vid in video:
        vid["thumbnail"] = vc.get_thumbnails(vid)
    streams = f.search_stream(searching)
    for strem in streams:
        strem["thumbnail"] = vc.stream_thumbnails(strem)

    return render(request, "search_page.html", context={
        "search": search,
        "videos": video,
        "streams": streams
    })

def history(request):
    """Gets the history both videos and streams"""
    acc = request.session["account"]
    videos = acc.history()
    streams = acc.stream_history()
    for vid in videos:
        vid["thumbnail"] = vc.get_thumbnails(vid)
    for stream in streams:
        stream["thumbnail"] = vc.stream_thumbnails(stream)
    return render(request, "history.html", context={
        "videos": videos,
        "streams": streams
    })

def stream(request, id):
    """A single video page, with comments, with an option to leave comments. FOR EVERY SESSION THERE IS ONE VIDEO WATCH"""
    stream = Content(id)
    key = None

    if id not in request.session["videos"]:
        request.session["videos"] += [id]
        stream.view_video(request.session.get("account").user)
    info = stream.stream_info()
    if (info["type"] == "direct"):
        url = "https://stream.mux.com/" + vc.playback_stream(info["location"]) + ".m3u8"
        key = vc.stream_key(info["location"])
    else:
        url = vc.youtube_url(info["location"])
    comments = stream.get_commments()
    replies = stream.get_comment_replies()
    ch = Channel(info["channel"])
    more = ch.videos(4)
    for m in more:
        m["thumbnail"] = vc.get_thumbnails(m)
    return render(request, "stream.html", context={
        "stream": info,
        "comments": comments,
        "replies": replies,
        "url": url,
        "more": more,
        "key": key
    })

def open_stream(request, id):
    """Opens or closes the stream for the public use"""
    strem = Content(id)
    strem.toggle_stream()
    return redirect("stream", id)



def create_stream(request, channel):
    """Page of stream creation form"""
    channel = Channel(channel)
    data = {
        'channel': channel.channel_info(),
    }
    return render(request, 'create_stream.html', context=data)


def stream_safe(request, type, channel):
    """Saves the video in the database, redirects to the success_page if everything right"""
    if type == "direct":
        post = request.POST
        a_id = vc.makeStream()
        strem = {
            "name": post["name"],
            "description": post["description"],
            "location": a_id,
            "channel": channel,
            'type': "direct"
        }
        c = Channel(channel)
        c.create_stream(strem)
        return redirect("channel", channel)
    else:
        post = request.POST.dict()
        strem = {
            "name": post["name"],
            "description": post["description"],
            "location": vc.get_id(post['link']),
            "channel": channel,
            'type': type
        }
        c = Channel(channel)
        c.create_stream(strem)
        return redirect("channel", channel)
