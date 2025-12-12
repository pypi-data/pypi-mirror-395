from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Y1PositionCls:
	"""Y1Position commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("y1Position", core, parent)

	def set(self, signal_or_val: float=None, cursor=repcap.Cursor.Default) -> None:
		"""CURSor<*>:Y1Position \n
		Snippet: driver.cursor.y1Position.set(signal_or_val = 1.0, cursor = repcap.Cursor.Default) \n
		The command usage depends on the setting of method RsMxo.Cursor.Smode.set. In single source and second source mode. the
		command sets or queries the position of the lower horizontal cursor line. The <Signal> parameter is irrelevant. If method
		RsMxo.Cursor.Tracking.State.set is enabled, the Y-positions are set automatically, and the query returns the measurement
		result. In multiple source mode, tracking is always on. The command is used as query only, and you specify the signal for
		which you want to get the value. \n
			:param signal_or_val: No help available
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
		"""
		param = ''
		if signal_or_val:
			param = Conversions.decimal_value_to_str(signal_or_val)
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		self._core.io.write(f'CURSor{cursor_cmd_val}:Y1Position {param}'.strip())

	def get(self, cursor=repcap.Cursor.Default) -> float:
		"""CURSor<*>:Y1Position \n
		Snippet: value: float = driver.cursor.y1Position.get(cursor = repcap.Cursor.Default) \n
		The command usage depends on the setting of method RsMxo.Cursor.Smode.set. In single source and second source mode. the
		command sets or queries the position of the lower horizontal cursor line. The <Signal> parameter is irrelevant. If method
		RsMxo.Cursor.Tracking.State.set is enabled, the Y-positions are set automatically, and the query returns the measurement
		result. In multiple source mode, tracking is always on. The command is used as query only, and you specify the signal for
		which you want to get the value. \n
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
			:return: value: Y-position of the first horizontal cursor line."""
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		response = self._core.io.query_str(f'CURSor{cursor_cmd_val}:Y1Position?')
		return Conversions.str_to_float(response)
