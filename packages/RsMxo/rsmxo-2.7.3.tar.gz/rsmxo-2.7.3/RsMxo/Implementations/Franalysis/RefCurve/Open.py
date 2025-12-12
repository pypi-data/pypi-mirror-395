from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OpenCls:
	"""Open commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("open", core, parent)

	def set(self, refCurve=repcap.RefCurve.Default) -> None:
		"""FRANalysis:REFCurve<*>:OPEN \n
		Snippet: driver.franalysis.refCurve.open.set(refCurve = repcap.RefCurve.Default) \n
		Loads the reference waveform file selected by method RsMxo.Franalysis.RefCurve.Name.set. \n
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
		"""
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		self._core.io.write(f'FRANalysis:REFCurve{refCurve_cmd_val}:OPEN')

	def set_and_wait(self, refCurve=repcap.RefCurve.Default, opc_timeout_ms: int = -1) -> None:
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		"""FRANalysis:REFCurve<*>:OPEN \n
		Snippet: driver.franalysis.refCurve.open.set_and_wait(refCurve = repcap.RefCurve.Default) \n
		Loads the reference waveform file selected by method RsMxo.Franalysis.RefCurve.Name.set. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsMxo.utilities.opc_timeout_set() to set the timeout value. \n
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'FRANalysis:REFCurve{refCurve_cmd_val}:OPEN', opc_timeout_ms)

	def get(self, refCurve=repcap.RefCurve.Default) -> bool:
		"""FRANalysis:REFCurve<*>:OPEN \n
		Snippet: value: bool = driver.franalysis.refCurve.open.get(refCurve = repcap.RefCurve.Default) \n
		Loads the reference waveform file selected by method RsMxo.Franalysis.RefCurve.Name.set. \n
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
			:return: success: No help available"""
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		response = self._core.io.query_str(f'FRANalysis:REFCurve{refCurve_cmd_val}:OPEN?')
		return Conversions.str_to_bool(response)
