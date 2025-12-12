import os


class _ClientState:
	def __init__(self, endpoint: str | None = None, api_key: str | None = None, api_version: str | None = None):
		_endpoint = endpoint if endpoint is not None else os.environ.get("DEMAND_AI_ENDPOINT")
		_api_key = api_key if api_key is not None else os.environ.get("DEMAND_AI_API_KEY")
		_api_version = api_version if api_version is not None else os.environ.get("DEMAND_AI_API_VERSION", "v1")

		if _endpoint is None:
			raise ValueError(
				"The endpoint must be provided either a parameter or set using the DEMAND_AI_ENDPOINT environment variable"
			)

		if _api_key is None:
			raise ValueError(
				"The API key must be provided either as a parameter or set using the DEMAND_AI_API_KEY environment variable"
			)

		assert _api_version

		self._endpoint = _endpoint
		self._api_key = _api_key
		self._api_version = _api_version

	def url(self) -> str:
		return f"https://api.{self._endpoint}/{self._api_version}"
