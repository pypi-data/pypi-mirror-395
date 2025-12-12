from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SlopeCls:
	"""Slope commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("slope", core, parent)

	def set(self, signal_value: enums.SignalSource=None, cursor=repcap.Cursor.Default) -> None:
		"""CURSor<*>:YDELta:SLOPe \n
		Snippet: driver.cursor.ydelta.slope.set(signal_value = enums.SignalSource.C1, cursor = repcap.Cursor.Default) \n
		Returns the inverse value of the voltage difference, the reciprocal of the vertical distance of two horizontal cursor
		lines: 1/ΔV. In multiple source mode, specify the signal for which you want to get the value. \n
			:param signal_value: Only relevant for method RsMxo.Cursor.Smode.set. One of the sources that are specified with method RsMxo.Cursor.Source.set.
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
		"""
		param = ''
		if signal_value:
			param = Conversions.enum_scalar_to_str(signal_value, enums.SignalSource)
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		self._core.io.write(f'CURSor{cursor_cmd_val}:YDELta:SLOPe {param}'.strip())

	def get(self, cursor=repcap.Cursor.Default) -> float:
		"""CURSor<*>:YDELta:SLOPe \n
		Snippet: value: float = driver.cursor.ydelta.slope.get(cursor = repcap.Cursor.Default) \n
		Returns the inverse value of the voltage difference, the reciprocal of the vertical distance of two horizontal cursor
		lines: 1/ΔV. In multiple source mode, specify the signal for which you want to get the value. \n
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
			:return: value: Inverse value of the delta value of the two cursor lines."""
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		response = self._core.io.query_str(f'CURSor{cursor_cmd_val}:YDELta:SLOPe?')
		return Conversions.str_to_float(response)
