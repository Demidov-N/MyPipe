# coding: utf-8

import mux_python
import requests
import pafy
# Exercises all direct upload operations.

# Authentication Setup
configuration = mux_python.Configuration()
configuration.username = 'd3e93141-790a-4a2e-8b49-47e284a9777d'
configuration.password = 'Z85xrauScwtj24i0iCEuQgisgDEOm4rqVm0CeWgyjveI0UYbrc/uiroFWpK0Cq/WAWb4iEa9RPm'

# All required apis
uploads_api = mux_python.DirectUploadsApi(mux_python.ApiClient(configuration))
asset_api = mux_python.AssetsApi(mux_python.ApiClient(configuration))
live_api = mux_python.LiveStreamsApi(mux_python.ApiClient(configuration))
playback_ids_api = mux_python.PlaybackIDApi(mux_python.ApiClient(configuration))


def upload(file):
    """Creates a direct upload on the file, and returns the asset id of an upload"""
    create_asset_request = mux_python.CreateAssetRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC])
    create_upload_request = mux_python.CreateUploadRequest(timeout=3600, new_asset_settings=create_asset_request,
                                                           cors_origin="*")
    create_upload_response = uploads_api.create_direct_upload(create_upload_request)
    upload = create_upload_response.data
    requests.put(upload.url, data=open(file.temporary_file_path(), "rb"))

    direct_upload = uploads_api.get_direct_upload(create_upload_response.data.id)


    while (direct_upload.data.status == "waiting"):
        direct_upload = uploads_api.get_direct_upload(create_upload_response.data.id)
    data = direct_upload.data
    return direct_upload.data.asset_id


def makeStream():
    # ========== create-live-stream ==========
    new_asset_settings = mux_python.CreateAssetRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC])
    create_live_stream_request = mux_python.CreateLiveStreamRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC],
                                                                    new_asset_settings=new_asset_settings)
    create_live_stream_response = live_api.create_live_stream(create_live_stream_request)
    live_stream_response = live_api.get_live_stream(create_live_stream_response.data.id)
    data = live_stream_response.data
    return data.id

def stream_key(stream_id):

    live_stream_response = live_api.get_live_stream(stream_id)
    return live_stream_response.data.stream_key

def delete_stream(stream_id):
    live_stream_response = live_api.get_live_stream(stream_id)
    while (live_stream_response.data.status != "idle"):
        live_stream_response = live_api.get_live_stream(stream_id)
    live_api.delete_live_stream(stream_id)

def delete_asset(asset_id):
    live_stream_response = asset_api.delete_asset(asset_id)


def playback_id(asset_id):
    """Creates a playback id for embedding it into the video"""
    return asset_api.get_asset(asset_id).data.playback_ids[0].id


def get_id(url):
    """Gets id of a video on youtube"""
    vid = pafy.new(url)
    return vid.videoid



def youtube_url(id):
    """Gets a url for a video embeding"""
    try:
        vid = pafy.new("https://www.youtube.com/watch?v=" + id)
        stream = vid.getbest()
        return stream.url_https
    except ValueError:
        return False


def get_thumbnails(video):
    if video.get("type") == "youtube":
        return 'https://img.youtube.com/vi/%s/hqdefault.jpg' % (video.get("location"))
    else:
        return 'https://image.mux.com/%s/thumbnail.png?width=1920&height=1080&fit_mode=pad' % (playback_id(video.get("location")))




