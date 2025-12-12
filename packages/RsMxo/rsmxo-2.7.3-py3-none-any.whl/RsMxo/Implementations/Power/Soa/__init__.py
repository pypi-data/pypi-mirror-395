from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SoaCls:
	"""Soa commands group definition. 28 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("soa", core, parent)

	@property
	def source(self):
		"""source commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_source'):
			from .Source import SourceCls
			self._source = SourceCls(self._core, self._cmd_group)
		return self._source

	@property
	def limit(self):
		"""limit commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	@property
	def mtest(self):
		"""mtest commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_mtest'):
			from .Mtest import MtestCls
			self._mtest = MtestCls(self._core, self._cmd_group)
		return self._mtest

	@property
	def result(self):
		"""result commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_result'):
			from .Result import ResultCls
			self._result = ResultCls(self._core, self._cmd_group)
		return self._result

	def clone(self) -> 'SoaCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SoaCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
