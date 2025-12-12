from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Y2PositionCls:
	"""Y2Position commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("y2Position", core, parent)

	def set(self, signal_or_val: float=None, cursor=repcap.Cursor.Default) -> None:
		"""CURSor<*>:Y2Position \n
		Snippet: driver.cursor.y2Position.set(signal_or_val = 1.0, cursor = repcap.Cursor.Default) \n
		Defines or queries the position of the upper horizontal cursor line.The command works in the same way as method RsMxo.
		Cursor.Y1Position.set. \n
			:param signal_or_val: No help available
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
		"""
		param = ''
		if signal_or_val:
			param = Conversions.decimal_value_to_str(signal_or_val)
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		self._core.io.write(f'CURSor{cursor_cmd_val}:Y2Position {param}'.strip())

	def get(self, cursor=repcap.Cursor.Default) -> float:
		"""CURSor<*>:Y2Position \n
		Snippet: value: float = driver.cursor.y2Position.get(cursor = repcap.Cursor.Default) \n
		Defines or queries the position of the upper horizontal cursor line.The command works in the same way as method RsMxo.
		Cursor.Y1Position.set. \n
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
			:return: value: Y-position of the second horizontal cursor line."""
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		response = self._core.io.query_str(f'CURSor{cursor_cmd_val}:Y2Position?')
		return Conversions.str_to_float(response)
