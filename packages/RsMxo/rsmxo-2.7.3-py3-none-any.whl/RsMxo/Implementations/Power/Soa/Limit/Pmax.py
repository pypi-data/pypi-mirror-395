from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PmaxCls:
	"""Pmax commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pmax", core, parent)

	def set(self, power_max: float, power=repcap.Power.Default) -> None:
		"""POWer<*>:SOA:LIMit:PMAX \n
		Snippet: driver.power.soa.limit.pmax.set(power_max = 1.0, power = repcap.Power.Default) \n
		Sets the maximum power for the mask. \n
			:param power_max: No help available
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.decimal_value_to_str(power_max)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		self._core.io.write(f'POWer{power_cmd_val}:SOA:LIMit:PMAX {param}')

	def get(self, power=repcap.Power.Default) -> float:
		"""POWer<*>:SOA:LIMit:PMAX \n
		Snippet: value: float = driver.power.soa.limit.pmax.get(power = repcap.Power.Default) \n
		Sets the maximum power for the mask. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: power_max: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:SOA:LIMit:PMAX?')
		return Conversions.str_to_float(response)
