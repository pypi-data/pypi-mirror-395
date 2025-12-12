from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ImExportCls:
	"""ImExport commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("imExport", core, parent)

	@property
	def name(self):
		"""name commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_name'):
			from .Name import NameCls
			self._name = NameCls(self._core, self._cmd_group)
		return self._name

	@property
	def save(self):
		"""save commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_save'):
			from .Save import SaveCls
			self._save = SaveCls(self._core, self._cmd_group)
		return self._save

	@property
	def open(self):
		"""open commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_open'):
			from .Open import OpenCls
			self._open = OpenCls(self._core, self._cmd_group)
		return self._open

	def clone(self) -> 'ImExportCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ImExportCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
