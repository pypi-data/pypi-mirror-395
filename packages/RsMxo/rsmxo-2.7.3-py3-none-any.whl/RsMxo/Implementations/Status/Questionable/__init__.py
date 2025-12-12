from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class QuestionableCls:
	"""Questionable commands group definition. 51 total commands, 10 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("questionable", core, parent)

	@property
	def goverload(self):
		"""goverload commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_goverload'):
			from .Goverload import GoverloadCls
			self._goverload = GoverloadCls(self._core, self._cmd_group)
		return self._goverload

	@property
	def ppSupply(self):
		"""ppSupply commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_ppSupply'):
			from .PpSupply import PpSupplyCls
			self._ppSupply = PpSupplyCls(self._core, self._cmd_group)
		return self._ppSupply

	@property
	def coverload(self):
		"""coverload commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_coverload'):
			from .Coverload import CoverloadCls
			self._coverload = CoverloadCls(self._core, self._cmd_group)
		return self._coverload

	@property
	def adcState(self):
		"""adcState commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_adcState'):
			from .AdcState import AdcStateCls
			self._adcState = AdcStateCls(self._core, self._cmd_group)
		return self._adcState

	@property
	def limit(self):
		"""limit commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import LimitCls
			self._limit = LimitCls(self._core, self._cmd_group)
		return self._limit

	@property
	def margin(self):
		"""margin commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_margin'):
			from .Margin import MarginCls
			self._margin = MarginCls(self._core, self._cmd_group)
		return self._margin

	@property
	def imprecise(self):
		"""imprecise commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_imprecise'):
			from .Imprecise import ImpreciseCls
			self._imprecise = ImpreciseCls(self._core, self._cmd_group)
		return self._imprecise

	@property
	def mask(self):
		"""mask commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_mask'):
			from .Mask import MaskCls
			self._mask = MaskCls(self._core, self._cmd_group)
		return self._mask

	@property
	def pll(self):
		"""pll commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_pll'):
			from .Pll import PllCls
			self._pll = PllCls(self._core, self._cmd_group)
		return self._pll

	@property
	def temperature(self):
		"""temperature commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_temperature'):
			from .Temperature import TemperatureCls
			self._temperature = TemperatureCls(self._core, self._cmd_group)
		return self._temperature

	def clone(self) -> 'QuestionableCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = QuestionableCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
