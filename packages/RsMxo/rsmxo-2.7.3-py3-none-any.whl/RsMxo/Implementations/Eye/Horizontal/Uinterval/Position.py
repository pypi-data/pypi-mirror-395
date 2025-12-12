from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PositionCls:
	"""Position commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("position", core, parent)

	def set(self, horiz_posi_ui: float, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:HORizontal:UINTerval:POSition \n
		Snippet: driver.eye.horizontal.uinterval.position.set(horiz_posi_ui = 1.0, eye = repcap.Eye.Default) \n
		Defines the position of the zero point in the diagram in unit intervals. The zero point is the alignment point on which
		the slice timestamps are superimposed. \n
			:param horiz_posi_ui: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.decimal_value_to_str(horiz_posi_ui)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:HORizontal:UINTerval:POSition {param}')

	def get(self, eye=repcap.Eye.Default) -> float:
		"""EYE<*>:HORizontal:UINTerval:POSition \n
		Snippet: value: float = driver.eye.horizontal.uinterval.position.get(eye = repcap.Eye.Default) \n
		Defines the position of the zero point in the diagram in unit intervals. The zero point is the alignment point on which
		the slice timestamps are superimposed. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: horiz_posi_ui: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:HORizontal:UINTerval:POSition?')
		return Conversions.str_to_float(response)
