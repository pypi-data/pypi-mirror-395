from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MtestCls:
	"""Mtest commands group definition. 17 total commands, 3 Subgroups, 0 group commands
	Repeated Capability: MaskTest, default value after init: MaskTest.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mtest", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_maskTest_get', 'repcap_maskTest_set', repcap.MaskTest.Nr1)

	def repcap_maskTest_set(self, maskTest: repcap.MaskTest) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to MaskTest.Default.
		Default value after init: MaskTest.Nr1"""
		self._cmd_group.set_repcap_enum_value(maskTest)

	def repcap_maskTest_get(self) -> repcap.MaskTest:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def imExport(self):
		"""imExport commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_imExport'):
			from .ImExport import ImExportCls
			self._imExport = ImExportCls(self._core, self._cmd_group)
		return self._imExport

	@property
	def onViolation(self):
		"""onViolation commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_onViolation'):
			from .OnViolation import OnViolationCls
			self._onViolation = OnViolationCls(self._core, self._cmd_group)
		return self._onViolation

	@property
	def segment(self):
		"""segment commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_segment'):
			from .Segment import SegmentCls
			self._segment = SegmentCls(self._core, self._cmd_group)
		return self._segment

	def clone(self) -> 'MtestCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MtestCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
