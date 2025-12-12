from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SrcplusCls:
	"""Srcplus commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("srcplus", core, parent)

	def set(self, plus_source: enums.SignalSource, serialBus=repcap.SerialBus.Default) -> None:
		"""SBUS<*>:TBTO:SRCPlus \n
		Snippet: driver.sbus.tbto.srcplus.set(plus_source = enums.SignalSource.C1, serialBus = repcap.SerialBus.Default) \n
		Selects the D+ data source channel for 1000BASE-T1. \n
			:param plus_source: No help available
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
		"""
		param = Conversions.enum_scalar_to_str(plus_source, enums.SignalSource)
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		self._core.io.write(f'SBUS{serialBus_cmd_val}:TBTO:SRCPlus {param}')

	# noinspection PyTypeChecker
	def get(self, serialBus=repcap.SerialBus.Default) -> enums.SignalSource:
		"""SBUS<*>:TBTO:SRCPlus \n
		Snippet: value: enums.SignalSource = driver.sbus.tbto.srcplus.get(serialBus = repcap.SerialBus.Default) \n
		Selects the D+ data source channel for 1000BASE-T1. \n
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
			:return: plus_source: No help available"""
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		response = self._core.io.query_str(f'SBUS{serialBus_cmd_val}:TBTO:SRCPlus?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSource)
