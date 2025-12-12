import typing

# Types related to Elasticsearch data import.
Bucket: typing.TypeAlias = dict[str, dict[typing.Any, typing.Any]]
BundleDict: typing.TypeAlias = dict[str, typing.Any]

Metadata: typing.TypeAlias = dict[str, str | int]

# Types related to random bundle generation.
RandomBiProcessData: typing.TypeAlias = dict[str, str | list[dict[str, str]]]
RandomWetProcessData: typing.TypeAlias = dict[str, str | float]
RandomAnalysisData: typing.TypeAlias = dict[str, str | list[int | str]]
