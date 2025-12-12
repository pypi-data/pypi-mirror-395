#
# BSD 3-Clause License
#
# Copyright (c) 2022, California Institute of Technology and
# Max Planck Institute for Gravitational Physics (Albert Einstein Institute)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# This software may be subject to U.S. export control laws. By accepting this
# software, the user agrees to comply with all applicable U.S. export laws and
# regulations. User has the responsibility to obtain export licenses, or other
# export authority as may be required before exporting such information to
# foreign countries or providing access to foreign persons.
#
"""
Script to upload and publish a new version on Zenodo.

Prior to running this script run `python -m build` to build a distribution archive for
the package that is meant to be uploaded to Zenodo.
"""

import argparse
import json
import logging
import os
from datetime import datetime

import requests

logger = logging.getLogger(__name__)


def upload_and_publish(recid, token, version, publish, path, sandbox):
    """Upload and publish a new version on Zenodo.

    Args:
        recid (int): Zenodo ID of the first version
        token (str): Zenodo access token
        version (str): new deposition version
        publish (bool): whether new record should be published
        path (str): path to archive to be uploaded
        sandbox (bool): use Zenodo sandbox
    """
    # pylint: disable=too-many-statements
    params = {"access_token": token}
    headers = {"Content-Type": "application/json"}

    publication_date = datetime.today().strftime("%Y-%m-%d")

    url = "https://sandbox.zenodo.org" if sandbox else "https://zenodo.org"

    # Retrieve latest deposition and read out its id
    try:
        req = requests.get(
            f"{url}/api/deposit/depositions/{recid}", params=params, timeout=20
        )
        req.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise RuntimeError("Retrieval of latest deposition failed") from error
    logger.info("Request to deposition '%d' successful", recid)

    try:
        req = requests.get(req.json()["links"]["latest"], timeout=20)
        req.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise RuntimeError("Retrieval of latest deposition ID failed") from error
    latest_id = req.json()["id"]
    logger.info("Obtained latest deposition ID '%d'", latest_id)

    # Create new version
    try:
        req = requests.post(
            f"{url}/api/deposit/depositions/{latest_id}/actions/newversion",
            params=params,
            timeout=20,
        )
        req.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise RuntimeError("Creation of new version failed") from error
    draft_url = req.json()["links"]["latest_draft"]
    logger.info("Created new draft version at '%s'", draft_url)

    def _write_metadata(path):
        """Write metadata of the draft deposition."""
        try:
            with open(path, encoding="utf-8") as file:
                metadata = json.load(file)

            metadata["version"] = version
            metadata["publication_date"] = publication_date
            data = {"metadata": metadata}

            req = requests.put(
                draft_url,
                params=params,
                data=json.dumps(data),
                headers=headers,
                timeout=20,
            )
            req.raise_for_status()
        except (FileNotFoundError, requests.exceptions.HTTPError) as error:
            raise RuntimeError(
                "Writing of metadata failed, "
                "consider removing new draft version manually online"
            ) from error

    # Write metadata
    if sandbox:
        # reduced set of metadata since communities are not available on Zenodo sandbox
        _write_metadata(".zenodo_sandbox.json")
    else:
        _write_metadata(".zenodo.json")
    logger.info("Wrote metadata to draft")

    # Delete all files
    try:
        req = requests.get(draft_url + "/files", params=params, timeout=20)
        for file in req.json():
            file_url = file["links"]["self"]
            req = requests.delete(file_url, params=params, timeout=20)
        req.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            "Deletion of files failed, consider "
            "removing new draft version manually online"
        ) from error
    logger.info("Deleted old files from draft")

    # Upload new files
    try:
        with open(path, "rb") as file:
            data = {"name": os.path.basename(path)}
            files = {"file": file}
            req = requests.post(
                draft_url + "/files", params=params, data=data, files=files, timeout=20
            )
            req.raise_for_status()
    except (FileNotFoundError, requests.exceptions.HTTPError) as error:
        raise RuntimeError("File upload failed") from error
    logger.info("Upload files to draft")

    # Publish new version
    if publish:
        try:
            req = requests.post(
                draft_url + "/actions/publish", params=params, timeout=20
            )
        except requests.exceptions.HTTPError as error:
            raise RuntimeError(
                "Publication failed, consider removing new draft "
                "version manually online"
            ) from error
        logger.info("Published draft")


def main():
    """Parse command-line arguments and upload and publish."""
    parser = argparse.ArgumentParser(description="Upload and publish to Zenodo.")
    parser.add_argument("--project", type=int, help="Zenodo ID")
    parser.add_argument("--token", help="Zenodo access token")
    parser.add_argument("--version", help="version of the new deposition")
    parser.add_argument(
        "--publish", action="store_true", help="whether new record should be published"
    )
    parser.add_argument(
        "--sandbox", action="store_true", help="use Zenodo sandbox for testing"
    )
    parser.add_argument("path", help="path to archive")

    args = parser.parse_args()

    upload_and_publish(
        args.project, args.token, args.version, args.publish, args.path, args.sandbox
    )


if __name__ == "__main__":
    main()
