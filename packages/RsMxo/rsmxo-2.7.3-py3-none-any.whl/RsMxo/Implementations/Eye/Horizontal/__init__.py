from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HorizontalCls:
	"""Horizontal commands group definition. 5 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("horizontal", core, parent)

	@property
	def unit(self):
		"""unit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unit'):
			from .Unit import UnitCls
			self._unit = UnitCls(self._core, self._cmd_group)
		return self._unit

	@property
	def absolute(self):
		"""absolute commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_absolute'):
			from .Absolute import AbsoluteCls
			self._absolute = AbsoluteCls(self._core, self._cmd_group)
		return self._absolute

	@property
	def uinterval(self):
		"""uinterval commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_uinterval'):
			from .Uinterval import UintervalCls
			self._uinterval = UintervalCls(self._core, self._cmd_group)
		return self._uinterval

	def clone(self) -> 'HorizontalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HorizontalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
