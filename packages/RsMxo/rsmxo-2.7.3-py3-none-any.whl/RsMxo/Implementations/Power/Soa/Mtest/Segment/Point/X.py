from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class XCls:
	"""X commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("x", core, parent)

	def set(self, x: float, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default, segment=repcap.Segment.Default, point=repcap.Point.Default) -> None:
		"""POWer<*>:SOA:MTESt<*>:SEGMent<*>:POINt<*>:X \n
		Snippet: driver.power.soa.mtest.segment.point.x.set(x = 1.0, power = repcap.Power.Default, maskTest = repcap.MaskTest.Default, segment = repcap.Segment.Default, point = repcap.Point.Default) \n
		Sets the horizontal position of the selected point. \n
			:param x: No help available
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param point: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Point')
		"""
		param = Conversions.decimal_value_to_str(x)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		segment_cmd_val = self._cmd_group.get_repcap_cmd_value(segment, repcap.Segment)
		point_cmd_val = self._cmd_group.get_repcap_cmd_value(point, repcap.Point)
		self._core.io.write(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:SEGMent{segment_cmd_val}:POINt{point_cmd_val}:X {param}')

	def get(self, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default, segment=repcap.Segment.Default, point=repcap.Point.Default) -> float:
		"""POWer<*>:SOA:MTESt<*>:SEGMent<*>:POINt<*>:X \n
		Snippet: value: float = driver.power.soa.mtest.segment.point.x.get(power = repcap.Power.Default, maskTest = repcap.MaskTest.Default, segment = repcap.Segment.Default, point = repcap.Point.Default) \n
		Sets the horizontal position of the selected point. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param point: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Point')
			:return: x: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		segment_cmd_val = self._cmd_group.get_repcap_cmd_value(segment, repcap.Segment)
		point_cmd_val = self._cmd_group.get_repcap_cmd_value(point, repcap.Point)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:SEGMent{segment_cmd_val}:POINt{point_cmd_val}:X?')
		return Conversions.str_to_float(response)
