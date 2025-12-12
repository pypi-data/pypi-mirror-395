from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WindowCls:
	"""Window commands group definition. 19 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("window", core, parent)

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import EnableCls
			self._enable = EnableCls(self._core, self._cmd_group)
		return self._enable

	@property
	def horizontal(self):
		"""horizontal commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_horizontal'):
			from .Horizontal import HorizontalCls
			self._horizontal = HorizontalCls(self._core, self._cmd_group)
		return self._horizontal

	@property
	def vertical(self):
		"""vertical commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_vertical'):
			from .Vertical import VerticalCls
			self._vertical = VerticalCls(self._core, self._cmd_group)
		return self._vertical

	def clone(self) -> 'WindowCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = WindowCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
