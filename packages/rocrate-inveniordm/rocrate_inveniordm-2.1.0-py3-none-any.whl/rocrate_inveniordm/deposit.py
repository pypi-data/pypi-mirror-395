"""
    This script deposits a RO-Crate directory to an InvenioRDM repository.

    :author: Philipp Beer
    :author: Milan Szente
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import sys

import rocrate_inveniordm.mapping.converter as converter
import rocrate_inveniordm.upload.uploader as uploader


def main():
    """
    CLI entrypoint. Passes CLI arguments to deposit().
    """

    parser = argparse.ArgumentParser(
        description="Takes a RO-Crate directory as input and uploads it to an "
        "InvenioRDM repository"
    )

    parser.add_argument(
        "ro_crate_directory",
        help="Path to the RO-Crate directory to upload",
        type=str,
        action="store",
    )
    parser.add_argument(
        "-d",
        "--datacite",
        help="Path to a DataCite metadata file to use for the upload. Skips the "
        "conversion process from RO-Crate metadata to DataCite",
        type=str,
        action="store",
        nargs=1,
    )
    parser.add_argument(
        "--no-upload",
        help="Stop before creating InvenioRDM record and do not upload files. Use this "
        "option to create a DataCite metadata file for manual review",
        action="store_true",
    )
    # included for backwards compatibility
    parser.add_argument(
        "-o",
        "--omit-roc-files",
        help="Omit files named 'ro-crate-metadata.json' and directories/files "
        "containing 'ro-crate-preview' from the upload (not recommended)",
        action="store_true",
    )
    parser.add_argument(
        "-p",
        "--publish",
        help="Publish the record after uploading",
        action="store_true",
    )
    parser.add_argument(
        "-z",
        "--zip",
        help="Instead of uploading all the files within the crate, create and upload a "
        "single zip file containing the whole crate",
        action="store_true",
    )
    args = parser.parse_args()

    crate_dir = args.ro_crate_directory
    datacite_list = args.datacite
    no_upload = args.no_upload
    omit_roc_files = args.omit_roc_files
    publish = args.publish
    use_zip = args.zip

    datacite_file = datacite_list[0] if datacite_list else None

    deposit(
        ro_crate_dir=crate_dir,
        datacite_file=datacite_file,
        no_upload=no_upload,
        omit_roc_files=omit_roc_files,
        publish=publish,
        use_zip=use_zip,
    )


def deposit(
    ro_crate_dir: str,
    datacite_file: str | None = None,
    no_upload: bool = False,
    omit_roc_files: bool = False,
    publish: bool = False,
    use_zip: bool = False,
):
    """
    The main function of the script.
    It takes a RO-Crate directory as input and uploads it to an InvenioRDM repository.

    :param ro_crate_dir: Path to the RO-Crate directory to upload.
    :param datacite_file: Path to a DataCite metadata file which should be used for the
        upload. Skips the conversion process from RO-Crate metadata to DataCite.
        Defaults to None
    :param no_upload: Stop before creating InvenioRDM record and do not upload files.
        Use this option to create a DataCite metadata file for manual review. Defaults
        to False
    :param omit_roc_files: Omit files named 'ro-crate-metadata.json' and
        directories/files containing 'ro-crate-preview' from the upload (not
        recommended). Defaults to False
    :param publish: Publish the record after uploading. Defaults to False
    :param zip: Instead of uploading all the files within the crate, create and upload a
        single zip file containing the whole crate. Defaults to False
    :return: The ID of the created record, or None if no record was created.
    """

    # Get all files in RO-Crate directory and check if it is a RO-Crate directory
    # Exclude RO-Crate metadata, and RO-Crate website files
    all_files = []

    if use_zip:
        crate_name = os.path.basename(ro_crate_dir.strip("/"))
        print(f"Creating zipped crate {crate_name}.zip")
        crate_zip_path = shutil.make_archive(
            crate_name,
            "zip",
            root_dir=ro_crate_dir,
        )
        all_files.append(crate_zip_path)
    else:
        for file in glob.glob(f"{ro_crate_dir}/**", recursive=True):
            if omit_roc_files and (
                "ro-crate-preview" in file or "ro-crate-metadata.json" in file
            ):
                continue
            if os.path.isfile(file):
                all_files.append(file)

    ro_crate_metadata_file = os.path.join(ro_crate_dir, "ro-crate-metadata.json")

    if not os.path.isfile(ro_crate_metadata_file):
        print(
            f"'{ro_crate_dir}' is not a RO-Crate directory: "
            "'ro-crate-metadata.json' not found."
        )
        sys.exit()

    if datacite_file:
        # skip conversion and use the provided file
        print(f"Skipping metadata conversion, loading DataCite file {datacite_file}")
        with open(datacite_file, "r") as f:
            data_cite_metadata = json.load(f)
    else:
        # convert the RO-Crate metadata to DataCite
        with open(ro_crate_metadata_file, "r") as f:
            ro_crate_metadata = json.load(f)

        # if no files to upload, just set the metadata on the record
        metadata_only = False
        if len(all_files) == 0:
            metadata_only = True

        # Convert Metadata
        data_cite_metadata = converter.convert(
            ro_crate_metadata, metadata_only=metadata_only
        )
        # store datacite metadata
        with open("datacite-out.json", "w") as f:
            json.dump(data_cite_metadata, f, indent=4)

    # Upload and publish files, depending on no_upload and publish options
    if no_upload:
        print("Created datacite-out.json, skipping upload.")
        return None
    else:
        record_id = uploader.deposit(data_cite_metadata, all_files, publish=publish)

        print(f"Successfully created record {record_id}")
        return record_id


if __name__ == "__main__":
    main()
