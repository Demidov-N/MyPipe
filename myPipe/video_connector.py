# coding: utf-8

import mux_python
import requests
import pafy
# Exercises all direct upload operations.

# Authentication Setup
configuration = mux_python.Configuration()
configuration.username = 'f6ff2b4e-9c13-4e6d-becb-4754b402a5ab'
configuration.password = 'vTTpwx3ktCOm51nutpt1T5BnhKQbJ8jL6NM3r098Cv3qrYm90Hi0JSq8Bj9hV8Wq1lJiTP0DjXC'

# All required apis
uploads_api = mux_python.DirectUploadsApi(mux_python.ApiClient(configuration))
asset_api = mux_python.AssetsApi(mux_python.ApiClient(configuration))


def upload(file):
    """Creates a direct upload on the file, and returns the asset id of an upload"""
    create_asset_request = mux_python.CreateAssetRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC])
    create_upload_request = mux_python.CreateUploadRequest(timeout=3600, new_asset_settings=create_asset_request,
                                                           cors_origin="*")
    create_upload_response = uploads_api.create_direct_upload(create_upload_request)
    upload = create_upload_response.data
    print("uploading")
    print(file.temporary_file_path())

    requests.put(upload.url, data=open(file.temporary_file_path(), "rb"))

    direct_upload = uploads_api.get_direct_upload(create_upload_response.data.id)
    print(direct_upload.data)

    while (direct_upload.data.status == "waiting"):
        direct_upload = uploads_api.get_direct_upload(create_upload_response.data.id)
    return direct_upload.data.asset_id


def playback_id(asset_id):
    """Creates a playback id for embedding it into the video"""
    return asset_api.get_asset(asset_id).data.playback_ids[0].id


def get_id(url):
    """Gets id of a video on youtube"""
    vid = pafy.new(url)
    return vid.videoid

def youtube_url(id):
    """Gets a url for a video embeding"""
    vid = pafy.new("https://www.youtube.com/watch?v=" + id)
    stream = vid.getbest()
    return stream.url_https


def get_thumbnails(video):
    if video.get("type") == "youtube":
        return 'https://img.youtube.com/vi/%s/hqdefault.jpg' % (video.get("location"))
    else:
        return 'https://image.mux.com/%s/thumbnail.png?width=1920&height=1080&fit_mode=pad' % (playback_id(video.get("location")))