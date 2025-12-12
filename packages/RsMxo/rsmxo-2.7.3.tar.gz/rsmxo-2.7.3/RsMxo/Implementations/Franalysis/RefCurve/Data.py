from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DataCls:
	"""Data commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("data", core, parent)

	def get(self, refCurve=repcap.RefCurve.Default) -> List[float]:
		"""FRANalysis:REFCurve<*>:DATA \n
		Snippet: value: List[float] = driver.franalysis.refCurve.data.get(refCurve = repcap.RefCurve.Default) \n
		Returns the data of the specified reference waveform. \n
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
			:return: data: Comma-separated values"""
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		response = self._core.io.query_bin_or_ascii_float_list(f'FRANalysis:REFCurve{refCurve_cmd_val}:DATA?')
		return response
