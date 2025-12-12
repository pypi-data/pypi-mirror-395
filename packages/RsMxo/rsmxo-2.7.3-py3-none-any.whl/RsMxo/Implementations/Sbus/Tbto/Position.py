from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PositionCls:
	"""Position commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("position", core, parent)

	def set(self, tbto_position: float, serialBus=repcap.SerialBus.Default) -> None:
		"""SBUS<*>:TBTO:POSition \n
		Snippet: driver.sbus.tbto.position.set(tbto_position = 1.0, serialBus = repcap.SerialBus.Default) \n
		Sets the vertical position of the 1000BASE-T1 signal. \n
			:param tbto_position: No help available
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
		"""
		param = Conversions.decimal_value_to_str(tbto_position)
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		self._core.io.write(f'SBUS{serialBus_cmd_val}:TBTO:POSition {param}')

	def get(self, serialBus=repcap.SerialBus.Default) -> float:
		"""SBUS<*>:TBTO:POSition \n
		Snippet: value: float = driver.sbus.tbto.position.get(serialBus = repcap.SerialBus.Default) \n
		Sets the vertical position of the 1000BASE-T1 signal. \n
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
			:return: tbto_position: No help available"""
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		response = self._core.io.query_str(f'SBUS{serialBus_cmd_val}:TBTO:POSition?')
		return Conversions.str_to_float(response)
