from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class QualifyCls:
	"""Qualify commands group definition. 4 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("qualify", core, parent)

	@property
	def logic(self):
		"""logic commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_logic'):
			from .Logic import LogicCls
			self._logic = LogicCls(self._core, self._cmd_group)
		return self._logic

	@property
	def analog(self):
		"""analog commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_analog'):
			from .Analog import AnalogCls
			self._analog = AnalogCls(self._core, self._cmd_group)
		return self._analog

	@property
	def digital(self):
		"""digital commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_digital'):
			from .Digital import DigitalCls
			self._digital = DigitalCls(self._core, self._cmd_group)
		return self._digital

	def clone(self) -> 'QualifyCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = QualifyCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
