from pathlib import Path

import requests

from .model import *


def fail(status_code:int) -> Exception:
    class _(Exception): pass
    _.__name__ = f'E{status_code}'
    return _

class ZenodoClient:

    def __init__(self, host:str, access_token:str, timeout:int = 30):
        self.access_token = access_token
        self.host = host
        self.timeout = timeout

    def _evaluate(self, r:requests.Response):
        if 200 > r.status_code or r.status_code > 299:
            raise fail(r.status_code)(r.content)
        return r.json()

    def list_depositions(self) -> list:
        """Lists all depositions from the user, including draft depostions.

        Returns
        -------
        list of dict
            Depostion data for each deposition
        """
        r = requests.get(
            f'https://{self.host}/api/deposit/depositions',
            params={'access_token':self.access_token},
            timeout=self.timeout
        )
        return self._evaluate(r)

    def new_deposition(self) -> dict:
        """Creates a draft deposition.

        Returns
        -------
        dict
            Depostion data
        """
        r = requests.post(
            f'https://{self.host}/api/deposit/depositions',
            params={'access_token':self.access_token},
            json={},
            timeout=self.timeout
        )
        return self._evaluate(r)

    def file_upload(self, deposition_id:int, path:Path) -> dict:
        """Uploads a file to a draft deposition

        Parameters
        ----------
        deposition_id : int
            Zenodo deposition id
        path : Path
            local path to the file to be uploaded

        Returns
        -------
        dict
            Deposition data
        """
        bucket_url = self.get(deposition_id)['links']['bucket']
        with path.open('rb') as fp:
            r = requests.put(
                f'{bucket_url}/{path.name}',
                params={'access_token':self.access_token},
                data=fp,
                timeout=self.timeout
            )
        return self._evaluate(r)

    def file_delete(self, deposition_id:int, filename:str):
        """Deletes all uploaded files with the given name from a deposition.

        Parameters
        ----------
        deposition_id : int
            Zenodo deposition id
        filename : str
            File name
        """
        urls = [file['links']['self']
                for file in self.get(deposition_id)
                if file['filename'] == filename]
        for url in urls:
            r = requests.delete(
                url,
                params={'access_token':self.access_token},
                timeout=self.timeout
            )
            if r.status_code != 204:
                raise fail(r.status_code)(f"failed to delete {url} ({filename}): {r.content}")

    def set_metadata(self, deposition_id:int, metadata:MetaData) -> dict:
        """Sets metadata on the deposition draft. All at once.

        Parameters
        ----------
        deposition_id : int
            Zenodo deposition id
        metadata : MetaData
            Complete meta data. All current values will be deleted.

        Returns
        -------
        dict
            Updated deposition data
        """
        r = requests.put(
            f"https://{self.host}/api/deposit/depositions/{deposition_id}",
            params={'access_token': self.access_token},
            data=metadata.to_json(),
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        return self._evaluate(r)

    def delete(self, deposition_id:int) -> dict:
        """Deletes a draft deposition.

        Parameters
        ----------
        deposition_id : int
            Zenodo deposition id

        Returns
        -------
        dict
            Depostion data
        """
        depo_url = f'https://{self.host}/api/deposit/depositions/{deposition_id}'
        r = requests.delete(
            depo_url,
            params={'access_token':self.access_token},
            timeout=self.timeout
        )
        if r.status_code != 204:
            raise fail(r.status_code)(f"failed to delete {depo_url}: {r.content}")

    def publish(self, deposition_id:int) -> dict:
        """Publishes a draft deposition. After calling publish it cannot be altered or deleted
        anymore.

        Parameters
        ----------
        deposition_id : int
            Zenodo deposition id

        Returns
        -------
        dict
            Depostion data
        """
        r = requests.post(
            f"https://{self.host}/api/deposit/depositions/{deposition_id}/actions/publish",
            params={'access_token': self.access_token},
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        return self._evaluate(r)

    def discard(self, deposition_id:int) -> dict:
        """Discards a published deposition. After calling discard the deposition has the status
        'discarded' and is hidden from Zenodo users.

        To be confirmed!

        Parameters
        ----------
        deposition_id : int
            Zenodo deposition id

        Returns
        -------
        dict
            Depostion data
        """
        r = requests.post(
            f"https://{self.host}/api/deposit/depositions/{deposition_id}/actions/discard",
            params={'access_token': self.access_token},
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        return self._evaluate(r)

    def get(self, deposition_id:int) -> dict:
        """Zenodo deposition data.

        Parameters
        ----------
        deposition_id : int
            Zenodo deposition id

        Returns
        -------
        dict
            Depostion data
        """
        r = requests.get(
            f"https://{self.host}/api/deposit/depositions/{deposition_id}",
            params={'access_token': self.access_token},
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        return self._evaluate(r)
