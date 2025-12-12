import logging
import hashlib
import os

import pydantic
import requests

from demand_ai.client_state import _ClientState

log = logging.getLogger(__name__)


# TODO: asset-management/main.py
class AssetShortMetadata(pydantic.BaseModel):
	id: str = pydantic.Field(..., alias="_id")
	model_config = {"populate_by_name": True}

	@pydantic.field_validator("id", mode="before")
	def parse_object_id(cls, v):
		if isinstance(v, dict) and "$oid" in v:
			return v["$oid"]
		return v


# TODO: unused
class UploadDSResponse(pydantic.BaseModel):
	asset_id: str
	model_config = {"alias_generator": lambda field_name: field_name.replace("_", "-"), "populate_by_name": True}


class Assets:
	def __init__(self, state: _ClientState):
		self._state = state
		self._url = f"{self._state.url()}/assets"

	def upload_dataset(self, file_path: str) -> AssetShortMetadata:
		"""Upload the asset located at the specified file path."""
		response = requests.post(
			f"{self._url}/dataset",
			headers={"x-api-key": self._state._api_key},
			files={"file": (os.path.basename(file_path), open(file_path, "rb"))},
		)
		response.raise_for_status()
		return AssetShortMetadata.model_validate(response.json())

	def download(self, id: str, destination: str, overwrite: bool = True):
		"""Download the asset to the destination file path."""
		self.download_from(f"{self._url}/dataset/{id}", destination, overwrite)

	def download_from(self, url: str, destination: str, overwrite: bool = True):
		"""Reserved for internal use. Please use `download()` instead."""
		if os.path.exists(destination) and not overwrite:
			return

		headers = {"x-api-key": self._state._api_key}
		with requests.get(url, headers=headers, stream=True) as response:
			if response.status_code == 200:
				os.makedirs(os.path.dirname(destination), exist_ok=True)
				with open(destination, "wb") as f:
					for chunk in response.iter_content(chunk_size=8192):
						f.write(chunk)
			else:
				response.raise_for_status()

	def get_by_id(self, id: str) -> AssetShortMetadata:
		response = requests.get(f"{self._url}/meta/{id}", headers={"x-api-key": self._state._api_key})
		response.raise_for_status()
		return AssetShortMetadata.model_validate(response.json())

	def get_by_checksum(self, checksum: str) -> AssetShortMetadata:
		response = requests.get(f"{self._url}/meta/by-checksum/{checksum}", headers={"x-api-key": self._state._api_key})
		response.raise_for_status()
		return AssetShortMetadata.model_validate(response.json())

	def try_get_by_checksum(self, checksum: str) -> AssetShortMetadata | None:
		response = requests.get(f"{self._url}/meta/by-checksum/{checksum}", headers={"x-api-key": self._state._api_key})
		if response.status_code == 404:
			return None
		response.raise_for_status()
		return AssetShortMetadata.model_validate(response.json())

	def get_hash(self):
		return hashlib.sha1()

	def get_digest(self, blob: bytes) -> str:
		hash = hashlib.sha1(blob)
		return hash.hexdigest()
