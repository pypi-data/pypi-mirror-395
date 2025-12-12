from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelectCls:
	"""Select commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("select", core, parent)

	def set(self, bitrate_select: bool, serialBus=repcap.SerialBus.Default) -> None:
		"""SBUS<*>:MANCh:BITRate:SELect \n
		Snippet: driver.sbus.manch.bitrate.select.set(bitrate_select = False, serialBus = repcap.SerialBus.Default) \n
		Enables setting the bit rate. To set the bit rate, use the command method RsMxo.Sbus.Manch.Bitrate.Width.set. \n
			:param bitrate_select: No help available
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
		"""
		param = Conversions.bool_to_str(bitrate_select)
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		self._core.io.write(f'SBUS{serialBus_cmd_val}:MANCh:BITRate:SELect {param}')

	def get(self, serialBus=repcap.SerialBus.Default) -> bool:
		"""SBUS<*>:MANCh:BITRate:SELect \n
		Snippet: value: bool = driver.sbus.manch.bitrate.select.get(serialBus = repcap.SerialBus.Default) \n
		Enables setting the bit rate. To set the bit rate, use the command method RsMxo.Sbus.Manch.Bitrate.Width.set. \n
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
			:return: bitrate_select: No help available"""
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		response = self._core.io.query_str(f'SBUS{serialBus_cmd_val}:MANCh:BITRate:SELect?')
		return Conversions.str_to_bool(response)
