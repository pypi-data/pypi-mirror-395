from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePyCls:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	def set(self, input_type: enums.PowerCoupling, power=repcap.Power.Default, output=repcap.Output.Default) -> None:
		"""POWer<*>:EFFiciency:OUTPut<*>[:TYPE] \n
		Snippet: driver.power.efficiency.output.typePy.set(input_type = enums.PowerCoupling.AC, power = repcap.Power.Default, output = repcap.Output.Default) \n
		Selects the type of the current flow: AC or DC. \n
			:param input_type: No help available
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
		"""
		param = Conversions.enum_scalar_to_str(input_type, enums.PowerCoupling)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		self._core.io.write(f'POWer{power_cmd_val}:EFFiciency:OUTPut{output_cmd_val}:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, power=repcap.Power.Default, output=repcap.Output.Default) -> enums.PowerCoupling:
		"""POWer<*>:EFFiciency:OUTPut<*>[:TYPE] \n
		Snippet: value: enums.PowerCoupling = driver.power.efficiency.output.typePy.get(power = repcap.Power.Default, output = repcap.Output.Default) \n
		Selects the type of the current flow: AC or DC. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param output: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: input_type: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		output_cmd_val = self._cmd_group.get_repcap_cmd_value(output, repcap.Output)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:EFFiciency:OUTPut{output_cmd_val}:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.PowerCoupling)
