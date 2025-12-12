from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class VmaxCls:
	"""Vmax commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vmax", core, parent)

	def set(self, voltage_max: float, power=repcap.Power.Default) -> None:
		"""POWer<*>:SOA:LIMit:VMAX \n
		Snippet: driver.power.soa.limit.vmax.set(voltage_max = 1.0, power = repcap.Power.Default) \n
		Sets the maximum voltage for the mask. \n
			:param voltage_max: No help available
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.decimal_value_to_str(voltage_max)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		self._core.io.write(f'POWer{power_cmd_val}:SOA:LIMit:VMAX {param}')

	def get(self, power=repcap.Power.Default) -> float:
		"""POWer<*>:SOA:LIMit:VMAX \n
		Snippet: value: float = driver.power.soa.limit.vmax.get(power = repcap.Power.Default) \n
		Sets the maximum voltage for the mask. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: voltage_max: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:SOA:LIMit:VMAX?')
		return Conversions.str_to_float(response)
