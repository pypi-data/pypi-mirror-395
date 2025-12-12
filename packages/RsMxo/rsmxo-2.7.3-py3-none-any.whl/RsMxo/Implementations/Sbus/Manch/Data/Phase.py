from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PhaseCls:
	"""Phase commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("phase", core, parent)

	def set(self, data_phase: enums.SbusManchDataPhase, serialBus=repcap.SerialBus.Default) -> None:
		"""SBUS<*>:MANCh:DATA:PHASe \n
		Snippet: driver.sbus.manch.data.phase.set(data_phase = enums.SbusManchDataPhase.FEDGe, serialBus = repcap.SerialBus.Default) \n
		Sets the phase for the data line. \n
			:param data_phase:
				- FEDGe: Selects capturing data bits on the clock's first (rising) edge.
				- SEDGe: Selects capturing data bits on the clock's second (falling) edge.
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')"""
		param = Conversions.enum_scalar_to_str(data_phase, enums.SbusManchDataPhase)
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		self._core.io.write(f'SBUS{serialBus_cmd_val}:MANCh:DATA:PHASe {param}')

	# noinspection PyTypeChecker
	def get(self, serialBus=repcap.SerialBus.Default) -> enums.SbusManchDataPhase:
		"""SBUS<*>:MANCh:DATA:PHASe \n
		Snippet: value: enums.SbusManchDataPhase = driver.sbus.manch.data.phase.get(serialBus = repcap.SerialBus.Default) \n
		Sets the phase for the data line. \n
			:param serialBus: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sbus')
			:return: data_phase:
				- FEDGe: Selects capturing data bits on the clock's first (rising) edge.
				- SEDGe: Selects capturing data bits on the clock's second (falling) edge."""
		serialBus_cmd_val = self._cmd_group.get_repcap_cmd_value(serialBus, repcap.SerialBus)
		response = self._core.io.query_str(f'SBUS{serialBus_cmd_val}:MANCh:DATA:PHASe?')
		return Conversions.str_to_scalar_enum(response, enums.SbusManchDataPhase)
