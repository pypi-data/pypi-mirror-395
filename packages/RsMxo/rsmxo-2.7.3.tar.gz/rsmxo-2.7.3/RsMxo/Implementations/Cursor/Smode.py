from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SmodeCls:
	"""Smode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("smode", core, parent)

	def set(self, source_mode: enums.SourceMode, cursor=repcap.Cursor.Default) -> None:
		"""CURSor<*>:SMODe \n
		Snippet: driver.cursor.smode.set(source_mode = enums.SourceMode.MSOurce, cursor = repcap.Cursor.Default) \n
		Selects the number of sources that you want to measure. \n
			:param source_mode:
				- SINGle: The cursor lines are set on one waveform. Select the source with CURSorcu:SOURce.
				- SECond: The cursor lines are set on two waveforms. To set the second souce, use CURSorcu:SSOurce.
				- MSOurce: Multiple waveforms are selected to be measured with one cursor set. Activates CURSorcu:TRACking[:STATe] and sets CURSorcu:FUNCtion to PAIRed. Select the sources with CURSorcu:SOURce.
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')"""
		param = Conversions.enum_scalar_to_str(source_mode, enums.SourceMode)
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		self._core.io.write(f'CURSor{cursor_cmd_val}:SMODe {param}')

	# noinspection PyTypeChecker
	def get(self, cursor=repcap.Cursor.Default) -> enums.SourceMode:
		"""CURSor<*>:SMODe \n
		Snippet: value: enums.SourceMode = driver.cursor.smode.get(cursor = repcap.Cursor.Default) \n
		Selects the number of sources that you want to measure. \n
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
			:return: source_mode:
				- SINGle: The cursor lines are set on one waveform. Select the source with CURSorcu:SOURce.
				- SECond: The cursor lines are set on two waveforms. To set the second souce, use CURSorcu:SSOurce.
				- MSOurce: Multiple waveforms are selected to be measured with one cursor set. Activates CURSorcu:TRACking[:STATe] and sets CURSorcu:FUNCtion to PAIRed. Select the sources with CURSorcu:SOURce."""
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		response = self._core.io.query_str(f'CURSor{cursor_cmd_val}:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.SourceMode)
