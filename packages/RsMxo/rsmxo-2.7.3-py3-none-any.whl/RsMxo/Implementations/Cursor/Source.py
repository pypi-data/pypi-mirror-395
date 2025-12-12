from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, signal: List[enums.SignalSource]=None, cursor=repcap.Cursor.Default) -> None:
		"""CURSor<*>:SOURce \n
		Snippet: driver.cursor.source.set(signal = [SignalSource.C1, SignalSource.XY4], cursor = repcap.Cursor.Default) \n
		Selects the cursor source or multiple sources, which are the waveforms to be measured. The query returns the waveforms
		sorted by category and number. \n
			:param signal: Comma-separated list of waveforms.
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
		"""
		param = ''
		if signal:
			param = Conversions.enum_list_to_str(signal, enums.SignalSource)
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		self._core.io.write(f'CURSor{cursor_cmd_val}:SOURce {param}'.strip())

	# noinspection PyTypeChecker
	def get(self, cursor=repcap.Cursor.Default) -> List[enums.SignalSource]:
		"""CURSor<*>:SOURce \n
		Snippet: value: List[enums.SignalSource] = driver.cursor.source.get(cursor = repcap.Cursor.Default) \n
		Selects the cursor source or multiple sources, which are the waveforms to be measured. The query returns the waveforms
		sorted by category and number. \n
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
			:return: signal: Comma-separated list of waveforms."""
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		response = self._core.io.query_str(f'CURSor{cursor_cmd_val}:SOURce?')
		return Conversions.str_to_list_enum(response, enums.SignalSource)
