from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ThlowerCls:
	"""Thlower commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("thlower", core, parent)

	def set(self, dat_thres_low: float, serialBus=repcap.SerialBus.Default) -> None:
		"""SBUS<*>:MANCh:DATA:THLower \n
		Snippet: driver.sbus.manch.data.thlower.set(dat_thres_low = 1.0, serialBus = repcap.SerialBus.Default) \n
		Sets the lower threshold for the data channel. \n
			:param dat_thres_low: No help available
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
		"""
		param = Conversions.decimal_value_to_str(dat_thres_low)
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		self._core.io.write(f'SBUS{serialBus_cmd_val}:MANCh:DATA:THLower {param}')

	def get(self, serialBus=repcap.SerialBus.Default) -> float:
		"""SBUS<*>:MANCh:DATA:THLower \n
		Snippet: value: float = driver.sbus.manch.data.thlower.get(serialBus = repcap.SerialBus.Default) \n
		Sets the lower threshold for the data channel. \n
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
			:return: dat_thres_low: No help available"""
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		response = self._core.io.query_str(f'SBUS{serialBus_cmd_val}:MANCh:DATA:THLower?')
		return Conversions.str_to_float(response)
