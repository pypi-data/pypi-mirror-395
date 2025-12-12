from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OffsetCls:
	"""Offset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("offset", core, parent)

	def set(self, vertical_offset: float, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:VERTical:OFFSet \n
		Snippet: driver.eye.vertical.offset.set(vertical_offset = 1.0, eye = repcap.Eye.Default) \n
		Defines the vertical offset in divisions if method RsMxo.Eye.Vertical.Couple.set is OFF. If coupling is ON, the query
		returns the coupled value. \n
			:param vertical_offset: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.decimal_value_to_str(vertical_offset)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:VERTical:OFFSet {param}')

	def get(self, eye=repcap.Eye.Default) -> float:
		"""EYE<*>:VERTical:OFFSet \n
		Snippet: value: float = driver.eye.vertical.offset.get(eye = repcap.Eye.Default) \n
		Defines the vertical offset in divisions if method RsMxo.Eye.Vertical.Couple.set is OFF. If coupling is ON, the query
		returns the coupled value. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: vertical_offset: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:VERTical:OFFSet?')
		return Conversions.str_to_float(response)
