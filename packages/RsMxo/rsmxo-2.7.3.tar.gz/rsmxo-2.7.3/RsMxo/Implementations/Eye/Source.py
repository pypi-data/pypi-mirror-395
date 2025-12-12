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

	def set(self, source: enums.SignalSource, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:SOURce \n
		Snippet: driver.eye.source.set(source = enums.SignalSource.C1, eye = repcap.Eye.Default) \n
		Selects the waveform from which the eye diagram is generated. \n
			:param source: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SignalSource)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, eye=repcap.Eye.Default) -> enums.SignalSource:
		"""EYE<*>:SOURce \n
		Snippet: value: enums.SignalSource = driver.eye.source.get(eye = repcap.Eye.Default) \n
		Selects the waveform from which the eye diagram is generated. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: source: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSource)
