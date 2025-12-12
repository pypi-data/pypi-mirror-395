from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.RepeatedCapability import RepeatedCapability
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EyeCls:
	"""Eye commands group definition. 20 total commands, 10 Subgroups, 0 group commands
	Repeated Capability: Eye, default value after init: Eye.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("eye", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_eye_get', 'repcap_eye_set', repcap.Eye.Nr1)

	def repcap_eye_set(self, eye: repcap.Eye) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Eye.Default.
		Default value after init: Eye.Nr1"""
		self._cmd_group.set_repcap_enum_value(eye)

	def repcap_eye_get(self) -> repcap.Eye:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def source(self):
		"""source commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_source'):
			from .Source import SourceCls
			self._source = SourceCls(self._core, self._cmd_group)
		return self._source

	@property
	def rflSet(self):
		"""rflSet commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rflSet'):
			from .RflSet import RflSetCls
			self._rflSet = RflSetCls(self._core, self._cmd_group)
		return self._rflSet

	@property
	def treference(self):
		"""treference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_treference'):
			from .Treference import TreferenceCls
			self._treference = TreferenceCls(self._core, self._cmd_group)
		return self._treference

	@property
	def samtime(self):
		"""samtime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_samtime'):
			from .Samtime import SamtimeCls
			self._samtime = SamtimeCls(self._core, self._cmd_group)
		return self._samtime

	@property
	def mslices(self):
		"""mslices commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mslices'):
			from .Mslices import MslicesCls
			self._mslices = MslicesCls(self._core, self._cmd_group)
		return self._mslices

	@property
	def horizontal(self):
		"""horizontal commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_horizontal'):
			from .Horizontal import HorizontalCls
			self._horizontal = HorizontalCls(self._core, self._cmd_group)
		return self._horizontal

	@property
	def vertical(self):
		"""vertical commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_vertical'):
			from .Vertical import VerticalCls
			self._vertical = VerticalCls(self._core, self._cmd_group)
		return self._vertical

	@property
	def display(self):
		"""display commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_display'):
			from .Display import DisplayCls
			self._display = DisplayCls(self._core, self._cmd_group)
		return self._display

	@property
	def qualify(self):
		"""qualify commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_qualify'):
			from .Qualify import QualifyCls
			self._qualify = QualifyCls(self._core, self._cmd_group)
		return self._qualify

	def clone(self) -> 'EyeCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = EyeCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
