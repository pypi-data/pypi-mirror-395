from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NameCls:
	"""Name commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("name", core, parent)

	def set(self, name: str, refCurve=repcap.RefCurve.Default) -> None:
		"""FRANalysis:REFCurve<*>:NAME \n
		Snippet: driver.franalysis.refCurve.name.set(name = 'abc', refCurve = repcap.RefCurve.Default) \n
		Defines the name of the reference waveform file to be loaded, saved or deleted. \n
			:param name: String with the file path, filename and extension.
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
		"""
		param = Conversions.value_to_quoted_str(name)
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		self._core.io.write(f'FRANalysis:REFCurve{refCurve_cmd_val}:NAME {param}')

	def get(self, refCurve=repcap.RefCurve.Default) -> str:
		"""FRANalysis:REFCurve<*>:NAME \n
		Snippet: value: str = driver.franalysis.refCurve.name.get(refCurve = repcap.RefCurve.Default) \n
		Defines the name of the reference waveform file to be loaded, saved or deleted. \n
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
			:return: name: String with the file path, filename and extension."""
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		response = self._core.io.query_str(f'FRANalysis:REFCurve{refCurve_cmd_val}:NAME?')
		return trim_str_response(response)
