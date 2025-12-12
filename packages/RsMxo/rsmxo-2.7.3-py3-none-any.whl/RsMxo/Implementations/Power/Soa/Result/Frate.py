from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FrateCls:
	"""Frate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frate", core, parent)

	def get(self, power=repcap.Power.Default, result=repcap.Result.Default) -> float:
		"""POWer<*>:SOA:RESult<*>:FRATe \n
		Snippet: value: float = driver.power.soa.result.frate.get(power = repcap.Power.Default, result = repcap.Result.Default) \n
		Returns the ratio of failed acquisitions to the number of tested acquisitions. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param result: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Result')
			:return: fail_rate: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		result_cmd_val = self._cmd_group.get_repcap_cmd_value(result, repcap.Result)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:SOA:RESult{result_cmd_val}:FRATe?')
		return Conversions.str_to_float(response)
