from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TotalCls:
	"""Total commands group definition. 16 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("total", core, parent)

	@property
	def opower(self):
		"""opower commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_opower'):
			from .Opower import OpowerCls
			self._opower = OpowerCls(self._core, self._cmd_group)
		return self._opower

	@property
	def efficiency(self):
		"""efficiency commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_efficiency'):
			from .Efficiency import EfficiencyCls
			self._efficiency = EfficiencyCls(self._core, self._cmd_group)
		return self._efficiency

	def clone(self) -> 'TotalCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = TotalCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
