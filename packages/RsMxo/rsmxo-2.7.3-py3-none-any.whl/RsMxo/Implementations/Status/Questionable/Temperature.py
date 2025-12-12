from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TemperatureCls:
	"""Temperature commands group definition. 5 total commands, 0 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("temperature", core, parent)

	# noinspection PyTypeChecker
	def get_condition(self) -> List[enums.StatusQuestionGenerator]:
		"""STATus:QUEStionable:TEMPerature:CONDition \n
		Snippet: value: List[enums.StatusQuestionGenerator] = driver.status.questionable.temperature.get_condition() \n
		Returns the contents of the CONDition part of the status register to check for questionable instrument or measurement
		states. This part contains information on the action currently being performed in the instrument. Reading the CONDition
		registers does not delete the contents since it indicates the current hardware status. \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:TEMPerature:CONDition?')
		return Conversions.str_to_list_enum(response, enums.StatusQuestionGenerator)

	# noinspection PyTypeChecker
	def get_enable(self) -> List[enums.StatusQuestionGenerator]:
		"""STATus:QUEStionable:TEMPerature:ENABle \n
		Snippet: value: List[enums.StatusQuestionGenerator] = driver.status.questionable.temperature.get_enable() \n
		Sets the ENABle part that allows true conditions in the EVENt part to be reported for the summary bit in the status byte.
		These events can be used for a service request. If a bit in the ENABle part is 1, and the corresponding EVENt bit is true,
		a positive transition occurs in the summary bit. This transition is reported to the next higher level. See Table 'Source
		values for STATus:QUEStionable:...:[:EVENt] and STATus:QUEStionable:...:[:ENABLe]' for a list of the return values. \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:TEMPerature:ENABle?')
		return Conversions.str_to_list_enum(response, enums.StatusQuestionGenerator)

	def set_enable(self, value: List[enums.StatusQuestionGenerator]) -> None:
		"""STATus:QUEStionable:TEMPerature:ENABle \n
		Snippet: driver.status.questionable.temperature.set_enable(value = [StatusQuestionGenerator.WGENerator1, StatusQuestionGenerator.WGENerator8]) \n
		Sets the ENABle part that allows true conditions in the EVENt part to be reported for the summary bit in the status byte.
		These events can be used for a service request. If a bit in the ENABle part is 1, and the corresponding EVENt bit is true,
		a positive transition occurs in the summary bit. This transition is reported to the next higher level. See Table 'Source
		values for STATus:QUEStionable:...:[:EVENt] and STATus:QUEStionable:...:[:ENABLe]' for a list of the return values. \n
			:param value: No help available
		"""
		param = Conversions.enum_list_to_str(value, enums.StatusQuestionGenerator)
		self._core.io.write(f'STATus:QUEStionable:TEMPerature:ENABle {param}')

	# noinspection PyTypeChecker
	def get_event(self) -> List[enums.StatusQuestionGenerator]:
		"""STATus:QUEStionable:TEMPerature[:EVENt] \n
		Snippet: value: List[enums.StatusQuestionGenerator] = driver.status.questionable.temperature.get_event() \n
		Returns the contents of the EVENt part of the status register to check if an event has occurred since the last reading.
		Reading an EVENt register deletes its contents. \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:TEMPerature:EVENt?')
		return Conversions.str_to_list_enum(response, enums.StatusQuestionGenerator)

	# noinspection PyTypeChecker
	def get_ntransition(self) -> List[enums.StatusQuestionGenerator]:
		"""STATus:QUEStionable:TEMPerature:NTRansition \n
		Snippet: value: List[enums.StatusQuestionGenerator] = driver.status.questionable.temperature.get_ntransition() \n
		Sets the negative transition filter. If a bit is set, a transition from 1 to 0 in the condition part causes an entry to
		be made in the corresponding bit of the EVENt part of the register. \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:TEMPerature:NTRansition?')
		return Conversions.str_to_list_enum(response, enums.StatusQuestionGenerator)

	def set_ntransition(self, value: List[enums.StatusQuestionGenerator]) -> None:
		"""STATus:QUEStionable:TEMPerature:NTRansition \n
		Snippet: driver.status.questionable.temperature.set_ntransition(value = [StatusQuestionGenerator.WGENerator1, StatusQuestionGenerator.WGENerator8]) \n
		Sets the negative transition filter. If a bit is set, a transition from 1 to 0 in the condition part causes an entry to
		be made in the corresponding bit of the EVENt part of the register. \n
			:param value: No help available
		"""
		param = Conversions.enum_list_to_str(value, enums.StatusQuestionGenerator)
		self._core.io.write(f'STATus:QUEStionable:TEMPerature:NTRansition {param}')

	# noinspection PyTypeChecker
	def get_ptransition(self) -> List[enums.StatusQuestionGenerator]:
		"""STATus:QUEStionable:TEMPerature:PTRansition \n
		Snippet: value: List[enums.StatusQuestionGenerator] = driver.status.questionable.temperature.get_ptransition() \n
		Sets the positive transition filter. If a bit is set, a transition from 0 to 1 in the condition part causes an entry to
		be made in the corresponding bit of the EVENt part of the register. \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:TEMPerature:PTRansition?')
		return Conversions.str_to_list_enum(response, enums.StatusQuestionGenerator)

	def set_ptransition(self, value: List[enums.StatusQuestionGenerator]) -> None:
		"""STATus:QUEStionable:TEMPerature:PTRansition \n
		Snippet: driver.status.questionable.temperature.set_ptransition(value = [StatusQuestionGenerator.WGENerator1, StatusQuestionGenerator.WGENerator8]) \n
		Sets the positive transition filter. If a bit is set, a transition from 0 to 1 in the condition part causes an entry to
		be made in the corresponding bit of the EVENt part of the register. \n
			:param value: No help available
		"""
		param = Conversions.enum_list_to_str(value, enums.StatusQuestionGenerator)
		self._core.io.write(f'STATus:QUEStionable:TEMPerature:PTRansition {param}')
