from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ThupperCls:
	"""Thupper commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("thupper", core, parent)

	def set(self, dat_thres_upp: float, serialBus=repcap.SerialBus.Default) -> None:
		"""SBUS<*>:MANCh:DATA:THUPper \n
		Snippet: driver.sbus.manch.data.thupper.set(dat_thres_upp = 1.0, serialBus = repcap.SerialBus.Default) \n
		Sets the upper threshold for the data channel. \n
			:param dat_thres_upp: No help available
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
		"""
		param = Conversions.decimal_value_to_str(dat_thres_upp)
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		self._core.io.write(f'SBUS{serialBus_cmd_val}:MANCh:DATA:THUPper {param}')

	def get(self, serialBus=repcap.SerialBus.Default) -> float:
		"""SBUS<*>:MANCh:DATA:THUPper \n
		Snippet: value: float = driver.sbus.manch.data.thupper.get(serialBus = repcap.SerialBus.Default) \n
		Sets the upper threshold for the data channel. \n
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
			:return: dat_thres_upp: No help available"""
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		response = self._core.io.query_str(f'SBUS{serialBus_cmd_val}:MANCh:DATA:THUPper?')
		return Conversions.str_to_float(response)
