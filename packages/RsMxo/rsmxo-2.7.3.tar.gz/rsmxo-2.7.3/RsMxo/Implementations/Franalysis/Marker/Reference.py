from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ReferenceCls:
	"""Reference commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: Reference, default value after init: Reference.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reference", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_reference_get', 'repcap_reference_set', repcap.Reference.Nr1)

	def repcap_reference_set(self, reference: repcap.Reference) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Reference.Default.
		Default value after init: Reference.Nr1"""
		self._cmd_group.set_repcap_enum_value(reference)

	def repcap_reference_get(self) -> repcap.Reference:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def get(self, marker=repcap.Marker.Default, reference=repcap.Reference.Default) -> float:
		"""FRANalysis:MARKer<*>:REFerence<*> \n
		Snippet: value: float = driver.franalysis.marker.reference.get(marker = repcap.Marker.Default, reference = repcap.Reference.Default) \n
		Returns the vertical value of the reference waveform at the specified marker. \n
			:param marker: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Marker')
			:param reference: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Reference')
			:return: yvalue: No help available"""
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		reference_cmd_val = self._cmd_group.get_repcap_cmd_value(reference, repcap.Reference)
		response = self._core.io.query_str(f'FRANalysis:MARKer{marker_cmd_val}:REFerence{reference_cmd_val}?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'ReferenceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ReferenceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
