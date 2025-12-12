from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TreferenceCls:
	"""Treference commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("treference", core, parent)

	def set(self, tim_ref: float, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:TREFerence \n
		Snippet: driver.eye.treference.set(tim_ref = 1.0, eye = repcap.Eye.Default) \n
		Selects the gate, which restricts the contributing slices in horizontal direction. Only the timestamps within the defined
		horizontal interval qualify for eye generation. \n
			:param tim_ref: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.decimal_value_to_str(tim_ref)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:TREFerence {param}')

	def get(self, eye=repcap.Eye.Default) -> float:
		"""EYE<*>:TREFerence \n
		Snippet: value: float = driver.eye.treference.get(eye = repcap.Eye.Default) \n
		Selects the gate, which restricts the contributing slices in horizontal direction. Only the timestamps within the defined
		horizontal interval qualify for eye generation. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: tim_ref: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:TREFerence?')
		return Conversions.str_to_float(response)
