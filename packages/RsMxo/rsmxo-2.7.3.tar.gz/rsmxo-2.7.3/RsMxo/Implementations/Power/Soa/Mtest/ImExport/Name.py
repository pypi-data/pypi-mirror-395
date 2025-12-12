from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NameCls:
	"""Name commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("name", core, parent)

	def set(self, name: str, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default) -> None:
		"""POWer<*>:SOA:MTESt<*>:IMEXport:NAME \n
		Snippet: driver.power.soa.mtest.imExport.name.set(name = 'abc', power = repcap.Power.Default, maskTest = repcap.MaskTest.Default) \n
		Sets the path, the filename and the file format of the mask file. \n
			:param name: String with path and file name with extension .xml.
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
		"""
		param = Conversions.value_to_quoted_str(name)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		self._core.io.write(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:IMEXport:NAME {param}')

	def get(self, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default) -> str:
		"""POWer<*>:SOA:MTESt<*>:IMEXport:NAME \n
		Snippet: value: str = driver.power.soa.mtest.imExport.name.get(power = repcap.Power.Default, maskTest = repcap.MaskTest.Default) \n
		Sets the path, the filename and the file format of the mask file. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:return: name: String with path and file name with extension .xml."""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:IMEXport:NAME?')
		return trim_str_response(response)
