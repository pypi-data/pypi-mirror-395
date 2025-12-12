from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScreenshotCls:
	"""Screenshot commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("screenshot", core, parent)

	def set(self, save_screenshot: enums.TriggerAction, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default) -> None:
		"""POWer<*>:SOA:MTESt<*>:ONViolation:SCReenshot \n
		Snippet: driver.power.soa.mtest.onViolation.screenshot.set(save_screenshot = enums.TriggerAction.NOACtion, power = repcap.Power.Default, maskTest = repcap.MaskTest.Default) \n
		Saves the waveform data to file if the command is set to SUCCess or VIOLation. To configure the screenshot settings, use
		the commands described in 'Screenshots'. \n
			:param save_screenshot: No help available
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
		"""
		param = Conversions.enum_scalar_to_str(save_screenshot, enums.TriggerAction)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		self._core.io.write(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:ONViolation:SCReenshot {param}')

	# noinspection PyTypeChecker
	def get(self, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default) -> enums.TriggerAction:
		"""POWer<*>:SOA:MTESt<*>:ONViolation:SCReenshot \n
		Snippet: value: enums.TriggerAction = driver.power.soa.mtest.onViolation.screenshot.get(power = repcap.Power.Default, maskTest = repcap.MaskTest.Default) \n
		Saves the waveform data to file if the command is set to SUCCess or VIOLation. To configure the screenshot settings, use
		the commands described in 'Screenshots'. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:return: save_screenshot: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:ONViolation:SCReenshot?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerAction)
