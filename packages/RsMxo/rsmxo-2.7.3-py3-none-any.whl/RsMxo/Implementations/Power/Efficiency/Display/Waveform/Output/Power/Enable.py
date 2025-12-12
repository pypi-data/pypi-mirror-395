from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnableCls:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, state: bool, power=repcap.Power.Default, output=repcap.Output.Default) -> None:
		"""POWer<*>:EFFiciency:DISPlay:WAVeform:OUTPut<*>:POWer[:ENABle] \n
		Snippet: driver.power.efficiency.display.waveform.output.power.enable.set(state = False, power = repcap.Power.Default, output = repcap.Output.Default) \n
		Displays or hides the specified output power waveform. \n
			:param state: No help available
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
		"""
		param = Conversions.bool_to_str(state)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		self._core.io.write(f'POWer{power_cmd_val}:EFFiciency:DISPlay:WAVeform:OUTPut{output_cmd_val}:POWer:ENABle {param}')

	def get(self, power=repcap.Power.Default, output=repcap.Output.Default) -> bool:
		"""POWer<*>:EFFiciency:DISPlay:WAVeform:OUTPut<*>:POWer[:ENABle] \n
		Snippet: value: bool = driver.power.efficiency.display.waveform.output.power.enable.get(power = repcap.Power.Default, output = repcap.Output.Default) \n
		Displays or hides the specified output power waveform. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: state: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:EFFiciency:DISPlay:WAVeform:OUTPut{output_cmd_val}:POWer:ENABle?')
		return Conversions.str_to_bool(response)
