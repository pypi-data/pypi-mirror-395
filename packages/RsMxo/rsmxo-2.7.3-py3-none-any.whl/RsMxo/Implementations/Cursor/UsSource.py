from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UsSourceCls:
	"""UsSource commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("usSource", core, parent)

	def set(self, first: bool, cursor=repcap.Cursor.Default) -> None:
		"""CURSor<*>:USSource \n
		Snippet: driver.cursor.usSource.set(first = False, cursor = repcap.Cursor.Default) \n
		Enables the second cursor source. To select the second source, use method RsMxo.Cursor.Ssource.set. The command has the
		same effect as method RsMxo.Cursor.Smode.set. \n
			:param first: No help available
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
		"""
		param = Conversions.bool_to_str(first)
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		self._core.io.write(f'CURSor{cursor_cmd_val}:USSource {param}')

	def get(self, cursor=repcap.Cursor.Default) -> bool:
		"""CURSor<*>:USSource \n
		Snippet: value: bool = driver.cursor.usSource.get(cursor = repcap.Cursor.Default) \n
		Enables the second cursor source. To select the second source, use method RsMxo.Cursor.Ssource.set. The command has the
		same effect as method RsMxo.Cursor.Smode.set. \n
			:param cursor: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cursor')
			:return: first: No help available"""
		cursor_cmd_val = self._cmd_group.get_repcap_cmd_value(cursor, repcap.Cursor)
		response = self._core.io.query_str(f'CURSor{cursor_cmd_val}:USSource?')
		return Conversions.str_to_bool(response)
