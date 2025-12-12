from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, source: enums.SignalSource, refCurve=repcap.RefCurve.Default) -> None:
		"""REFCurve<*>:SOURce \n
		Snippet: driver.refCurve.source.set(source = enums.SignalSource.C1, refCurve = repcap.RefCurve.Default) \n
		Selects the source waveform from the active waveforms, e.g. input channels, math waveforms, or spectrum. \n
			:param source: No help available
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SignalSource)
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		self._core.io.write(f'REFCurve{refCurve_cmd_val}:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, refCurve=repcap.RefCurve.Default) -> enums.SignalSource:
		"""REFCurve<*>:SOURce \n
		Snippet: value: enums.SignalSource = driver.refCurve.source.get(refCurve = repcap.RefCurve.Default) \n
		Selects the source waveform from the active waveforms, e.g. input channels, math waveforms, or spectrum. \n
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
			:return: source: No help available"""
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		response = self._core.io.query_str(f'REFCurve{refCurve_cmd_val}:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSource)
