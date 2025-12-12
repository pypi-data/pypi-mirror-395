from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StypeCls:
	"""Stype commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stype", core, parent)

	# noinspection PyTypeChecker
	def get(self, refCurve=repcap.RefCurve.Default) -> enums.SignalType:
		"""REFCurve<*>:DATA:STYPe \n
		Snippet: value: enums.SignalType = driver.refCurve.data.stype.get(refCurve = repcap.RefCurve.Default) \n
		No command help available \n
			:param refCurve: optional repeated capability selector. Default value: Nr1 (settable in the interface 'RefCurve')
			:return: signal_type: No help available"""
		refCurve_cmd_val = self._cmd_group.get_repcap_cmd_value(refCurve, repcap.RefCurve)
		response = self._core.io.query_str(f'REFCurve{refCurve_cmd_val}:DATA:STYPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalType)
