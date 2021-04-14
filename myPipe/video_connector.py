# coding: utf-8

import mux_python
import requests
# Exercises all direct upload operations.

# Authentication Setup
configuration = mux_python.Configuration()
configuration.username = 'f02f0b67-d16b-4113-ab1a-47c975884a45'
configuration.password = 'uoZTDZqceaNVBcHuNK48oeXrHx1zGPHtRILtWB4A+OtkYET3MiRRbokXXP8fji7HnJtAIWIjsc7'

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
    requests.put(upload.url, data=file)

    direct_upload = uploads_api.get_direct_upload(create_upload_response.data.id)

    return direct_upload.data.asset_id


def playback_id(asset_id):
    """Creates a playback id for embedding it into the video"""
    return asset_api.get_asset(asset_id).data.playback_ids[0].id


