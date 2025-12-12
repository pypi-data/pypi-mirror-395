from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HistogramCls:
	"""Histogram commands group definition. 5 total commands, 4 Subgroups, 0 group commands
	Repeated Capability: Histogram, default value after init: Histogram.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("histogram", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_histogram_get', 'repcap_histogram_set', repcap.Histogram.Nr1)

	def repcap_histogram_set(self, histogram: repcap.Histogram) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Histogram.Default.
		Default value after init: Histogram.Nr1"""
		self._cmd_group.set_repcap_enum_value(histogram)

	def repcap_histogram_get(self) -> repcap.Histogram:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def save(self):
		"""save commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_save'):
			from .Save import SaveCls
			self._save = SaveCls(self._core, self._cmd_group)
		return self._save

	@property
	def normalize(self):
		"""normalize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_normalize'):
			from .Normalize import NormalizeCls
			self._normalize = NormalizeCls(self._core, self._cmd_group)
		return self._normalize

	@property
	def name(self):
		"""name commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_name'):
			from .Name import NameCls
			self._name = NameCls(self._core, self._cmd_group)
		return self._name

	@property
	def data(self):
		"""data commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Data import DataCls
			self._data = DataCls(self._core, self._cmd_group)
		return self._data

	def clone(self) -> 'HistogramCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HistogramCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
