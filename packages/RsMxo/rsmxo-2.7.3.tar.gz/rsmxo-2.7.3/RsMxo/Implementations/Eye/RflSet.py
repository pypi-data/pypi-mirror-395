from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RflSetCls:
	"""RflSet commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rflSet", core, parent)

	def set(self, ref_lev_set: float, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:RFLSet \n
		Snippet: driver.eye.rflSet.set(ref_lev_set = 1.0, eye = repcap.Eye.Default) \n
		Selects the reference level set that defines the timestamps for slicing the data waveform. Define the reference level set
		before you use it. \n
			:param ref_lev_set: Number of the reference level set
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.decimal_value_to_str(ref_lev_set)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:RFLSet {param}')

	def get(self, eye=repcap.Eye.Default) -> float:
		"""EYE<*>:RFLSet \n
		Snippet: value: float = driver.eye.rflSet.get(eye = repcap.Eye.Default) \n
		Selects the reference level set that defines the timestamps for slicing the data waveform. Define the reference level set
		before you use it. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: ref_lev_set: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:RFLSet?')
		return Conversions.str_to_float(response)
