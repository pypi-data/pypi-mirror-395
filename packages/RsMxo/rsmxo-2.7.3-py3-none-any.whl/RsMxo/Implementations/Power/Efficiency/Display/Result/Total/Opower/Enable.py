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

	def set(self, show_res_total_pow: bool, power=repcap.Power.Default) -> None:
		"""POWer<*>:EFFiciency:DISPlay:RESult:TOTal:OPOWer[:ENABle] \n
		Snippet: driver.power.efficiency.display.result.total.opower.enable.set(show_res_total_pow = False, power = repcap.Power.Default) \n
		The commands enable the total power and efficiency measurements of the selected output line. These measurements require
		an instrument with more than 4 channels. \n
			:param show_res_total_pow: No help available
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.bool_to_str(show_res_total_pow)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		self._core.io.write(f'POWer{power_cmd_val}:EFFiciency:DISPlay:RESult:TOTal:OPOWer:ENABle {param}')

	def get(self, power=repcap.Power.Default) -> bool:
		"""POWer<*>:EFFiciency:DISPlay:RESult:TOTal:OPOWer[:ENABle] \n
		Snippet: value: bool = driver.power.efficiency.display.result.total.opower.enable.get(power = repcap.Power.Default) \n
		The commands enable the total power and efficiency measurements of the selected output line. These measurements require
		an instrument with more than 4 channels. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: show_res_total_pow: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:EFFiciency:DISPlay:RESult:TOTal:OPOWer:ENABle?')
		return Conversions.str_to_bool(response)
