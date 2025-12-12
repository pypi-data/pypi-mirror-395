from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PolarityCls:
	"""Polarity commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("polarity", core, parent)

	def set(self, data_polarity: enums.SbusManchDataPolarity, serialBus=repcap.SerialBus.Default) -> None:
		"""SBUS<*>:MANCh:DATA:POLarity \n
		Snippet: driver.sbus.manch.data.polarity.set(data_polarity = enums.SbusManchDataPolarity.MANC, serialBus = repcap.SerialBus.Default) \n
		Sets the polarity for the data line. \n
			:param data_polarity:
				- MANC: Selects the Manchester data representation convention as per G. E. Thomas: High-to-low transition for logical 1.
				- MANT: Selects the Manchester II (Manchester Two) data representation convention as per IEEE 802.3: Low-to-high transition for logical 1.
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')"""
		param = Conversions.enum_scalar_to_str(data_polarity, enums.SbusManchDataPolarity)
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		self._core.io.write(f'SBUS{serialBus_cmd_val}:MANCh:DATA:POLarity {param}')

	# noinspection PyTypeChecker
	def get(self, serialBus=repcap.SerialBus.Default) -> enums.SbusManchDataPolarity:
		"""SBUS<*>:MANCh:DATA:POLarity \n
		Snippet: value: enums.SbusManchDataPolarity = driver.sbus.manch.data.polarity.get(serialBus = repcap.SerialBus.Default) \n
		Sets the polarity for the data line. \n
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
			:return: data_polarity:
				- MANC: Selects the Manchester data representation convention as per G. E. Thomas: High-to-low transition for logical 1.
				- MANT: Selects the Manchester II (Manchester Two) data representation convention as per IEEE 802.3: Low-to-high transition for logical 1."""
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		response = self._core.io.query_str(f'SBUS{serialBus_cmd_val}:MANCh:DATA:POLarity?')
		return Conversions.str_to_scalar_enum(response, enums.SbusManchDataPolarity)
