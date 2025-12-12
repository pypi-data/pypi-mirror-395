from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PolarityCls:
	"""Polarity commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("polarity", core, parent)

	def set(self, polarity: enums.NormalInverted, serialBus=repcap.SerialBus.Default) -> None:
		"""SBUS<*>:TBTO:POLarity \n
		Snippet: driver.sbus.tbto.polarity.set(polarity = enums.NormalInverted.INVerted, serialBus = repcap.SerialBus.Default) \n
		Selects the polarity of the data signal. \n
			:param polarity: No help available
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
		"""
		param = Conversions.enum_scalar_to_str(polarity, enums.NormalInverted)
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		self._core.io.write(f'SBUS{serialBus_cmd_val}:TBTO:POLarity {param}')

	# noinspection PyTypeChecker
	def get(self, serialBus=repcap.SerialBus.Default) -> enums.NormalInverted:
		"""SBUS<*>:TBTO:POLarity \n
		Snippet: value: enums.NormalInverted = driver.sbus.tbto.polarity.get(serialBus = repcap.SerialBus.Default) \n
		Selects the polarity of the data signal. \n
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
			:return: polarity: No help available"""
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		response = self._core.io.query_str(f'SBUS{serialBus_cmd_val}:TBTO:POLarity?')
		return Conversions.str_to_scalar_enum(response, enums.NormalInverted)
