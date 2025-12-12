from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExportCls:
	"""Export commands group definition. 26 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("export", core, parent)

	@property
	def result(self):
		"""result commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_result'):
			from .Result import ResultCls
			self._result = ResultCls(self._core, self._cmd_group)
		return self._result

	@property
	def waveform(self):
		"""waveform commands group. 2 Sub-classes, 9 commands."""
		if not hasattr(self, '_waveform'):
			from .Waveform import WaveformCls
			self._waveform = WaveformCls(self._core, self._cmd_group)
		return self._waveform

	@property
	def histogram(self):
		"""histogram commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_histogram'):
			from .Histogram import HistogramCls
			self._histogram = HistogramCls(self._core, self._cmd_group)
		return self._histogram

	def clone(self) -> 'ExportCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExportCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
