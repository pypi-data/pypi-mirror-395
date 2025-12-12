from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, signal_keys: List[enums.SignalSource], layout=repcap.Layout.Default, diagram=repcap.Diagram.Default) -> None:
		"""LAYout<*>:DIAGram<*>:SOURce \n
		Snippet: driver.layout.diagram.source.set(signal_keys = [SignalSource.C1, SignalSource.XY4], layout = repcap.Layout.Default, diagram = repcap.Diagram.Default) \n
		Assigns the waveforms to a diagram. \n
			:param signal_keys: String with a comma-separated list of waveforms, e.g. 'C1, C2, M1'
			:param layout: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layout')
			:param diagram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Diagram')
		"""
		param = Conversions.enum_list_to_str(signal_keys, enums.SignalSource)
		layout_cmd_val = self._cmd_group.get_repcap_cmd_value(layout, repcap.Layout)
		diagram_cmd_val = self._cmd_group.get_repcap_cmd_value(diagram, repcap.Diagram)
		self._core.io.write(f'LAYout{layout_cmd_val}:DIAGram{diagram_cmd_val}:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, layout=repcap.Layout.Default, diagram=repcap.Diagram.Default) -> List[enums.SignalSource]:
		"""LAYout<*>:DIAGram<*>:SOURce \n
		Snippet: value: List[enums.SignalSource] = driver.layout.diagram.source.get(layout = repcap.Layout.Default, diagram = repcap.Diagram.Default) \n
		Assigns the waveforms to a diagram. \n
			:param layout: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Layout')
			:param diagram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Diagram')
			:return: signal_keys: String with a comma-separated list of waveforms, e.g. 'C1, C2, M1'"""
		layout_cmd_val = self._cmd_group.get_repcap_cmd_value(layout, repcap.Layout)
		diagram_cmd_val = self._cmd_group.get_repcap_cmd_value(diagram, repcap.Diagram)
		response = self._core.io.query_str(f'LAYout{layout_cmd_val}:DIAGram{diagram_cmd_val}:SOURce?')
		return Conversions.str_to_list_enum(response, enums.SignalSource)
