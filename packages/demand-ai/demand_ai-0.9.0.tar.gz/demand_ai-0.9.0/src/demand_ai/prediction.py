import enum
import datetime as dt
import logging
import os
import tempfile
import time

import pandas as pd
import pydantic
import requests

from demand_ai import Model
from demand_ai.client_state import _ClientState
from demand_ai.assets import AssetShortMetadata, Assets

log = logging.getLogger(__name__)


# TODO: see common/src/common/request.py, watcher/main.py, merger/main.py
class RequestStatus(enum.Enum):
	PENDING = "pending"
	"""The request's jobs are awaiting to be run."""

	ACTIVE = "active"
	"""One or more request jobs are actively running."""

	CHUNKS_READY = "chunks-ready"
	"""All request jobs are completed. The chunks are ready to be merged."""

	COMPLETED = "completed"
	"""All chunks have been merged into the final result."""

	FAILED = "failed"
	"""A failure has occurred during the request's lifecycle."""

	@staticmethod
	def parse(value: str) -> "RequestStatus":
		return RequestStatus[value.upper()]


# TODO: controller/main.py
class InferenceParameters(pydantic.BaseModel):
	asset_id: str
	model: Model
	frequency: str
	horizon: int

	model_config = {
		"alias_generator": lambda field_name: field_name.replace("_", "-"),
		"populate_by_name": True,
		"use_enum_values": True,
	}


# TODO: controller/main.py
class InitResponse(pydantic.BaseModel):
	request_id: str

	model_config = {"alias_generator": lambda field_name: field_name.replace("_", "-"), "populate_by_name": True}


# TODO: controller/main.py
class PredictionResult(pydantic.BaseModel):
	url: str


# TODO: controller/main.py
class StatusResponse(pydantic.BaseModel):
	status: RequestStatus
	prediction_result: PredictionResult | None


class Prediction:
	def __init__(self, state: _ClientState, assets: Assets):
		self._state = state
		self._url = f"{self._state.url()}/predict"
		self._assets = assets

	def predict(
		self,
		dataset: str | pd.DataFrame,
		frequency: str,
		horizon: int,
		output_file_path: str | None = None,
		model: Model = Model.I_MOE,
		timeout: int = 1800,
	) -> pd.DataFrame:
		"""
		Run a synchronous (blocking) prediction.

		Args:
			dataset: Either a path to a dataset file (JSON/CSV/Parquet) or a DataFrame. The dataset must have the columns `["unique_id", "ds", "y"]`
			frequency: Pandas-compatible frequency (see https://pandas.pydata.org/docs/user_guide/timeseries.html#dateoffset-objects)
			horizon: Number of future steps to predict (the timespan of a step increment equals the frequency)
			output_file_path: If set, the prediction will be saved to this path, overwriting any existing file
			model: The model used for inference
			timeout: The timeout in seconds
		"""
		file_path: str | None = None
		df: pd.DataFrame | None = None

		if type(dataset) is str:
			if not dataset.endswith((".json", ".csv", ".parquet")):
				raise Exception("Only JSON or CSV is currently supported")
			file_path = dataset
		elif type(dataset) is pd.DataFrame:
			df = dataset
		else:
			raise Exception(f"Invalid dataset parameter type: {type(dataset)}")

		upload_response = self._upload_ds(file_path, df)

		log.debug(f"Initializing inference request (asset ID: {upload_response.id})")

		parameters = InferenceParameters(asset_id=upload_response.id, model=model, frequency=frequency, horizon=horizon)
		init_response = self.init(parameters)

		log.debug(f"Inference request initialized, ID: {init_response.request_id}")

		start = dt.datetime.now(dt.timezone.utc)

		interval = 0.5
		max_interval = 4

		status_response: StatusResponse | None = None
		req_status: RequestStatus | None = None

		while (dt.datetime.now(dt.timezone.utc) - start).total_seconds() < timeout:
			status_response = self.status(init_response.request_id)
			new_status = status_response.status

			if not req_status or req_status != new_status:
				log.debug(f"Request {init_response.request_id} status: {req_status} -> {new_status}")
				req_status = new_status

			if req_status in [RequestStatus.PENDING, RequestStatus.ACTIVE, RequestStatus.CHUNKS_READY]:
				time.sleep(interval)
				if interval < max_interval:
					interval = min(interval * 2, max_interval)
			elif req_status == RequestStatus.COMPLETED:
				break
			elif req_status == RequestStatus.FAILED:
				raise Exception(f"The prediction request (ID: {init_response.request_id}) was marked as failed.")
			else:
				raise Exception(
					f"The prediction request (ID: {init_response.request_id}) is in an unrecognized status: {req_status.value}"
				)

		if req_status != RequestStatus.COMPLETED:
			raise Exception(
				f"Timeout reached while waiting for the prediction result (request ID: {init_response.request_id})"
			)

		assert status_response
		assert status_response.prediction_result

		log.debug("Downloading result")
		with tempfile.TemporaryDirectory() as dir_path:
			file_path = os.path.join(dir_path, f"{init_response.request_id}-result")
			self._assets.download_from(status_response.prediction_result.url, file_path)
			return pd.read_parquet(file_path)

	def _upload_ds(self, file_path: str | None, df: pd.DataFrame | None) -> AssetShortMetadata:
		if not file_path:
			# A dataset was specified: temporarily persist it and upload it
			assert df is not None
			with tempfile.TemporaryDirectory() as dir_path:
				file_path = os.path.join(dir_path, "dataset.json")
				df.to_json(file_path)
				return self._upload_if_new(file_path)
		else:
			# A file path was specified: upload it directly
			return self._upload_if_new(file_path)

	def _upload_if_new(self, file_path: str) -> AssetShortMetadata:
		asset_metadata = self._assets.try_get_by_checksum(self._get_digest(file_path))

		if asset_metadata:
			log.debug(f"Re-using existing asset: {asset_metadata.id}")
		else:
			log.debug("Uploading dataset")
			asset_metadata = self._assets.upload_dataset(file_path)

		return asset_metadata

	def _get_digest(self, file_path: str) -> str:
		hash = self._assets.get_hash()

		buffer_size = 64 * 1024
		with open(file_path, "rb") as file:
			while True:
				data = file.read(buffer_size)
				if not data:
					break
				hash.update(data)

		return hash.hexdigest()

	def _df_from_file_or_df(self, dataset: str | pd.DataFrame) -> pd.DataFrame:
		df: pd.DataFrame

		if type(dataset) is str:
			if dataset.endswith(".json"):
				df = pd.read_json(dataset)
			elif dataset.endswith(".csv"):
				df = pd.read_csv(dataset)
			elif dataset.endswith(".parquet"):
				df = pd.read_parquet(dataset)
			else:
				raise Exception("Only JSON or CSV is currently supported")
		elif type(dataset) is pd.DataFrame:
			df = dataset
		else:
			raise Exception(f"Invalid dataset parameter type: {type(dataset)}")

		return df

	def init(self, parameters: InferenceParameters) -> InitResponse:
		params = parameters.model_dump(by_alias=True)
		response = requests.post(f"{self._url}/init", headers={"x-api-key": self._state._api_key}, json=params)
		response.raise_for_status()
		return InitResponse.model_validate(response.json())

	def status(self, request_id: str) -> StatusResponse:
		response = requests.get(
			f"{self._url}/status", headers={"x-api-key": self._state._api_key, "request-id": request_id}
		)
		response.raise_for_status()
		return StatusResponse.model_validate(response.json())

	def result(self):
		raise Exception("Not implemented")
