from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RangeCls:
	"""Range commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("range", core, parent)

	def set(self, horiz_rg_ui: float, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:HORizontal:UINTerval:RANGe \n
		Snippet: driver.eye.horizontal.uinterval.range.set(horiz_rg_ui = 1.0, eye = repcap.Eye.Default) \n
		Sets the time range that is covered by the eye diagram in unit intervals. \n
			:param horiz_rg_ui: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.decimal_value_to_str(horiz_rg_ui)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:HORizontal:UINTerval:RANGe {param}')

	def get(self, eye=repcap.Eye.Default) -> float:
		"""EYE<*>:HORizontal:UINTerval:RANGe \n
		Snippet: value: float = driver.eye.horizontal.uinterval.range.get(eye = repcap.Eye.Default) \n
		Sets the time range that is covered by the eye diagram in unit intervals. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: horiz_rg_ui: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:HORizontal:UINTerval:RANGe?')
		return Conversions.str_to_float(response)
