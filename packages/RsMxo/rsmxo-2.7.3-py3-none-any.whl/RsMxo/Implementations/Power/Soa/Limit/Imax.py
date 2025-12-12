from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImaxCls:
	"""Imax commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("imax", core, parent)

	def set(self, current_max: float, power=repcap.Power.Default) -> None:
		"""POWer<*>:SOA:LIMit:IMAX \n
		Snippet: driver.power.soa.limit.imax.set(current_max = 1.0, power = repcap.Power.Default) \n
		Sets the maximum current for the mask. \n
			:param current_max: No help available
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.decimal_value_to_str(current_max)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		self._core.io.write(f'POWer{power_cmd_val}:SOA:LIMit:IMAX {param}')

	def get(self, power=repcap.Power.Default) -> float:
		"""POWer<*>:SOA:LIMit:IMAX \n
		Snippet: value: float = driver.power.soa.limit.imax.get(power = repcap.Power.Default) \n
		Sets the maximum current for the mask. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: current_max: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:SOA:LIMit:IMAX?')
		return Conversions.str_to_float(response)
