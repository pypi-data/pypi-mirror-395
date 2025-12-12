from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LimitCls:
	"""Limit commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("limit", core, parent)

	@property
	def imax(self):
		"""imax commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_imax'):
			from .Imax import ImaxCls
			self._imax = ImaxCls(self._core, self._cmd_group)
		return self._imax

	@property
	def vmax(self):
		"""vmax commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vmax'):
			from .Vmax import VmaxCls
			self._vmax = VmaxCls(self._core, self._cmd_group)
		return self._vmax

	@property
	def pmax(self):
		"""pmax commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pmax'):
			from .Pmax import PmaxCls
			self._pmax = PmaxCls(self._core, self._cmd_group)
		return self._pmax

	@property
	def apply(self):
		"""apply commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apply'):
			from .Apply import ApplyCls
			self._apply = ApplyCls(self._core, self._cmd_group)
		return self._apply

	def clone(self) -> 'LimitCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = LimitCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
