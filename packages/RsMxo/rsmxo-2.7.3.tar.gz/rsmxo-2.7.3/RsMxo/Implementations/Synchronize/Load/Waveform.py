from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class WaveformCls:
	"""Waveform commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("waveform", core, parent)

	def set(self) -> None:
		"""SYNChronize:LOAD[:WAVeform] \n
		Snippet: driver.synchronize.load.waveform.set() \n
		Retrieves the waveforms of the latest acquisition from the connected oscilloscope. All selected analog channel waveforms
		are transferred. Digital channels and reference waveforms are not transferred. \n
		"""
		self._core.io.write(f'SYNChronize:LOAD:WAVeform')

	def set_and_wait(self, opc_timeout_ms: int = -1) -> None:
		"""SYNChronize:LOAD[:WAVeform] \n
		Snippet: driver.synchronize.load.waveform.set_and_wait() \n
		Retrieves the waveforms of the latest acquisition from the connected oscilloscope. All selected analog channel waveforms
		are transferred. Digital channels and reference waveforms are not transferred. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsMxo.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYNChronize:LOAD:WAVeform', opc_timeout_ms)
