import importlib.metadata

from demand_ai.client_state import _ClientState
from demand_ai.assets import Assets
from demand_ai.prediction import Prediction


class Client:
	def __init__(self, endpoint: str | None = None, api_key: str | None = None, api_version: str | None = None):
		"""Initialize the Demand-AI client.

		Parameters can be passed directly or read from environment variables.
		If a parameter is `None`, the corresponding environment variable will be evaluated.

		Args:
			endpoint: The endpoint DNS name; if `None`, expects the DEMAND_AI_ENDPOINT environment variable to be set.
			api_key: API key for authentication; if `None`, expects the DEMAND_AI_API_KEY environment variable to be set.
			api_version: API version to use; if `None`, reads the DEMAND_AI_API_VERSION environment variable. Optional, defaults to "v1".

		Raises:
			ValueError: If the endpoint and API key are not provided.

		Example:
			# Using parameters
			client = Client(endpoint="prod.endpoint", api_key="your-key")

			# Using environment variables
			client = Client()
		"""
		self._state = _ClientState(endpoint=endpoint, api_key=api_key, api_version=api_version)

		self.assets = Assets(self._state)
		self.prediction = Prediction(self._state, self.assets)

	def endpoint(self) -> str:
		return self._state._endpoint

	def api_version(self) -> str:
		return self._state._api_version

	def client_version(self) -> str:
		return importlib.metadata.version("demand-ai")

	def client_info(self) -> str:
		"""
		Return a short information line about the client, without connecting to the API.
		The information includes the client version, the endpoint and API version.
		"""
		return f"demand-ai v{self.client_version()} - {self.endpoint()} ({self.api_version()})"
