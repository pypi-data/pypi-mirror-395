from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CoupleCls:
	"""Couple commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("couple", core, parent)

	def set(self, vert_cpl: bool, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:VERTical:COUPle \n
		Snippet: driver.eye.vertical.couple.set(vert_cpl = False, eye = repcap.Eye.Default) \n
		If ON, the vertical position and scale of the source are used. \n
			:param vert_cpl: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.bool_to_str(vert_cpl)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:VERTical:COUPle {param}')

	def get(self, eye=repcap.Eye.Default) -> bool:
		"""EYE<*>:VERTical:COUPle \n
		Snippet: value: bool = driver.eye.vertical.couple.get(eye = repcap.Eye.Default) \n
		If ON, the vertical position and scale of the source are used. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: vert_cpl: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:VERTical:COUPle?')
		return Conversions.str_to_bool(response)
