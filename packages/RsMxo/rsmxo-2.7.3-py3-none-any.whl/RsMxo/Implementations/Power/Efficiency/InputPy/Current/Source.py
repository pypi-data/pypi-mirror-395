from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, source_current: enums.SignalSource, power=repcap.Power.Default) -> None:
		"""POWer<*>:EFFiciency:INPut:CURRent[:SOURce] \n
		Snippet: driver.power.efficiency.inputPy.current.source.set(source_current = enums.SignalSource.C1, power = repcap.Power.Default) \n
		Selects the current source waveform of the input line. \n
			:param source_current: No help available
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.enum_scalar_to_str(source_current, enums.SignalSource)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		self._core.io.write(f'POWer{power_cmd_val}:EFFiciency:INPut:CURRent:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, power=repcap.Power.Default) -> enums.SignalSource:
		"""POWer<*>:EFFiciency:INPut:CURRent[:SOURce] \n
		Snippet: value: enums.SignalSource = driver.power.efficiency.inputPy.current.source.get(power = repcap.Power.Default) \n
		Selects the current source waveform of the input line. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: source_current: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:EFFiciency:INPut:CURRent:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSource)
