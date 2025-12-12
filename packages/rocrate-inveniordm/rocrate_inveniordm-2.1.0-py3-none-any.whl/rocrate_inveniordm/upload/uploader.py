"""
    Uploads a record to the repository.
    Used by deposit.py.

    :author: Philipp Beer
    :author: Milan Szente
"""

import json
import os
import sys

import requests
import rocrate_inveniordm.upload.credentials as credentials


def get_headers(content_type: str):
    headers = {
        "Accept": "application/json",
        "Content-Type": content_type,
        "Authorization": f"Bearer {credentials.get_api_key()}",
    }
    return headers


def deposit(metadata, files, publish=False):
    """
    Entry point.
    Uploads and publishes a record to the repository.

    :param metadata: The record's DataCite metadata.
    :param files: The record's files.
    :param publish: Whether to publish the record after uploading.
    """
    record_id = upload(metadata, files)
    if publish:
        publish_record(record_id)
    return record_id


def create_draft_record(metadata):
    """
    Creates a draft record in the repository.
    Exits the program if the request fails.

    :param metadata: The record's metadata.
    :param files: The record's files.
    :returns: The record's id.
    """
    api_url = credentials.get_repository_base_url()
    resp = requests.post(
        f"{api_url}/api/records",
        data=json.dumps(metadata),
        headers=get_headers("application/json"),
    )

    if resp.status_code != 201:
        print(f"Could not create record: {resp.status_code} {resp.text}")
        sys.exit(1)
    return resp.json().get("id")


def start_draft_files_upload(record_id, files):
    """
    Starts the draft file upload.
    This function does NOT upload any files, but initializes the upload process.
    Exits the program if the request fails.

    :param record_id: The record's id.
    :param files: The files to be uploaded.
    """
    payload = []
    for file in files:
        _, filename = os.path.split(file)
        payload.append({"key": filename})

    api_url = credentials.get_repository_base_url()
    resp = requests.post(
        f"{api_url}/api/records/{record_id}/draft/files",
        data=json.dumps(payload),
        headers=get_headers("application/json"),
    )
    if resp.status_code != 201:
        print(f"Could not initiate file upload: {resp.status_code} {resp.text}")
        sys.exit(1)
    return


def upload_file(record_id, file_path):
    """
    Uploads a file to the record.
    Exits the program if the request fails.

    :param record_id: The record's id.
    :param file_path: The path of the file to upload.
    """
    _, file_name = os.path.split(file_path)
    print(file_name)

    # Upload file content
    api_url = credentials.get_repository_base_url()
    upload_url = f"{api_url}/api/records/{record_id}/draft/files/{file_name}/content"

    with open(file_path, "rb") as f:
        resp = requests.put(
            upload_url,
            data=f,
            headers=get_headers("application/octet-stream"),
        )

    if resp.status_code != 200:
        print(f"Could not upload file content: {resp.status_code} {resp.text}")
        sys.exit(1)

    # Complete draft file upload
    resp = requests.post(
        f"{api_url}/api/records/{record_id}/draft/files/{file_name}/commit",
        headers=get_headers("application/json"),
    )
    if resp.status_code != 200:
        print(f"Could not commit file upload: {resp.status_code} {resp.text}")
        sys.exit(1)


def upload(metadata, files):
    """
    Uploads a draft record to the repository.
    Exits the program if the request fails.

    :param metadata: The record's metadata.
    :param files: The record's files.
    :returns: The draft record's id.
    """

    record_id = create_draft_record(metadata)
    print(f"Preparing to upload {len(files)} files...")
    start_draft_files_upload(record_id, files)

    print(f"Uploading {len(files)} files...")
    for file in files:
        upload_file(record_id, file)

    print(f"All {len(files)} files uploaded.")
    return record_id


def publish_record(record_id):
    """
    Publishes a record.
    Exits the program if the request fails.

    :param record_id: The record's id.
    """
    api_url = credentials.get_repository_base_url()
    resp = requests.post(
        f"{api_url}/api/records/{record_id}/draft/actions/publish",
        headers=get_headers("application/json"),
    )
    if resp.status_code != 202:
        print(f"Could not publish record: {resp.status_code} {resp.text}")
        sys.exit(1)
