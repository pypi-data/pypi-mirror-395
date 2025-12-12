from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UnitCls:
	"""Unit commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("unit", core, parent)

	def set(self, horizontal_unit: enums.HorizontalUnit, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:HORizontal:UNIT \n
		Snippet: driver.eye.horizontal.unit.set(horizontal_unit = enums.HorizontalUnit.ATIMe, eye = repcap.Eye.Default) \n
		Sets the method to define the horizontal scale of the eye diagram: as absolute time, or in unit intervals. \n
			:param horizontal_unit: UI = UINTerval
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.enum_scalar_to_str(horizontal_unit, enums.HorizontalUnit)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:HORizontal:UNIT {param}')

	# noinspection PyTypeChecker
	def get(self, eye=repcap.Eye.Default) -> enums.HorizontalUnit:
		"""EYE<*>:HORizontal:UNIT \n
		Snippet: value: enums.HorizontalUnit = driver.eye.horizontal.unit.get(eye = repcap.Eye.Default) \n
		Sets the method to define the horizontal scale of the eye diagram: as absolute time, or in unit intervals. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: horizontal_unit: UI = UINTerval"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:HORizontal:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.HorizontalUnit)
