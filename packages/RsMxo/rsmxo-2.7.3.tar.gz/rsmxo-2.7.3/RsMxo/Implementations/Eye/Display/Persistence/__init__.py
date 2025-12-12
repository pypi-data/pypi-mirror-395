from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PersistenceCls:
	"""Persistence commands group definition. 4 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("persistence", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import StateCls
			self._state = StateCls(self._core, self._cmd_group)
		return self._state

	@property
	def infinite(self):
		"""infinite commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_infinite'):
			from .Infinite import InfiniteCls
			self._infinite = InfiniteCls(self._core, self._cmd_group)
		return self._infinite

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_time'):
			from .Time import TimeCls
			self._time = TimeCls(self._core, self._cmd_group)
		return self._time

	def reset(self, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:DISPlay:PERSistence:RESet \n
		Snippet: driver.eye.display.persistence.reset(eye = repcap.Eye.Default) \n
		Resets the display, removing all waveform points. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:DISPlay:PERSistence:RESet')

	def reset_and_wait(self, eye=repcap.Eye.Default, opc_timeout_ms: int = -1) -> None:
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		"""EYE<*>:DISPlay:PERSistence:RESet \n
		Snippet: driver.eye.display.persistence.reset_and_wait(eye = repcap.Eye.Default) \n
		Resets the display, removing all waveform points. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsMxo.utilities.opc_timeout_set() to set the timeout value. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'EYE{eye_cmd_val}:DISPlay:PERSistence:RESet', opc_timeout_ms)

	def clone(self) -> 'PersistenceCls':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = PersistenceCls(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
