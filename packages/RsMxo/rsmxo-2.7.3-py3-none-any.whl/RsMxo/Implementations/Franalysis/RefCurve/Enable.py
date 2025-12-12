from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnableCls:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, state: bool, refCurve=repcap.RefCurve.Default) -> None:
		"""FRANalysis:REFCurve<*>:ENABle \n
		Snippet: driver.franalysis.refCurve.enable.set(state = False, refCurve = repcap.RefCurve.Default) \n
		Enables the display of the reference waveform in the diagram. Before you can display it, create the reference waveform. \n
			:param state: No help available
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
		"""
		param = Conversions.bool_to_str(state)
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		self._core.io.write(f'FRANalysis:REFCurve{refCurve_cmd_val}:ENABle {param}')

	def get(self, refCurve=repcap.RefCurve.Default) -> bool:
		"""FRANalysis:REFCurve<*>:ENABle \n
		Snippet: value: bool = driver.franalysis.refCurve.enable.get(refCurve = repcap.RefCurve.Default) \n
		Enables the display of the reference waveform in the diagram. Before you can display it, create the reference waveform. \n
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
			:return: state: No help available"""
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		response = self._core.io.query_str(f'FRANalysis:REFCurve{refCurve_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
