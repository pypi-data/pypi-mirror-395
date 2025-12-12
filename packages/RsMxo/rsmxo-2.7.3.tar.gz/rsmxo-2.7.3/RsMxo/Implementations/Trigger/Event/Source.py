from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, source_detailed: enums.TriggerSource, evnt=repcap.Evnt.Default) -> None:
		"""TRIGger:EVENt<*>:SOURce \n
		Snippet: driver.trigger.event.source.set(source_detailed = enums.TriggerSource.C1, evnt = repcap.Evnt.Default) \n
		Selects the source of the trigger signal for the selected trigger event. The trigger source works even if it is not
		displayed in a diagram. Available sources depend on the trigger sequence setting. If you trigger on a single event, all
		inputs can be used as trigger source. If you trigger on a sequence, only analog channels can be set as trigger source for
		A, B, and R-events. \n
			:param source_detailed:
				- C1 | C2 | ... | C8: Available for single event, and A, B and R-events in a trigger sequence
				- EXTernanalog | LINE |: Available for single event (suffix 1)
				- D0 | D1 | D2 | ... | D14 | D15: Digital channels, require MSO option. Available for single event (suffix 1)
				- SBUS1 | SBUS2 | SBUS3 | SBUS4: Available if one or more serial protocol options are installed. If the hardware trigger is supported for a protocol, triggering on single event is possible with hardware trigger settings. For all protocols, the software trigger is supported in a A → Serial bus (event 2) .
			:param evnt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Event')"""
		param = Conversions.enum_scalar_to_str(source_detailed, enums.TriggerSource)
		evnt_cmd_val = self._cmd_group.get_repcap_cmd_value(evnt, repcap.Evnt)
		self._core.io.write(f'TRIGger:EVENt{evnt_cmd_val}:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, evnt=repcap.Evnt.Default) -> enums.TriggerSource:
		"""TRIGger:EVENt<*>:SOURce \n
		Snippet: value: enums.TriggerSource = driver.trigger.event.source.get(evnt = repcap.Evnt.Default) \n
		Selects the source of the trigger signal for the selected trigger event. The trigger source works even if it is not
		displayed in a diagram. Available sources depend on the trigger sequence setting. If you trigger on a single event, all
		inputs can be used as trigger source. If you trigger on a sequence, only analog channels can be set as trigger source for
		A, B, and R-events. \n
			:param evnt: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Event')
			:return: source_detailed:
				- C1 | C2 | ... | C8: Available for single event, and A, B and R-events in a trigger sequence
				- EXTernanalog | LINE |: Available for single event (suffix 1)
				- D0 | D1 | D2 | ... | D14 | D15: Digital channels, require MSO option. Available for single event (suffix 1)
				- SBUS1 | SBUS2 | SBUS3 | SBUS4: Available if one or more serial protocol options are installed. If the hardware trigger is supported for a protocol, triggering on single event is possible with hardware trigger settings. For all protocols, the software trigger is supported in a A → Serial bus (event 2) ."""
		evnt_cmd_val = self._cmd_group.get_repcap_cmd_value(evnt, repcap.Evnt)
		response = self._core.io.query_str(f'TRIGger:EVENt{evnt_cmd_val}:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSource)
