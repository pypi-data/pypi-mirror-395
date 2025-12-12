from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MaskCls:
	"""Mask commands group definition. 5 total commands, 0 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mask", core, parent)

	# noinspection PyTypeChecker
	def get_condition(self) -> List[enums.StatusQuestionMask]:
		"""STATus:QUEStionable:MASK:CONDition \n
		Snippet: value: List[enums.StatusQuestionMask] = driver.status.questionable.mask.get_condition() \n
		Returns the contents of the CONDition part of the status register to check for questionable instrument or measurement
		states. This part contains information on the action currently being performed in the instrument. Reading the CONDition
		registers does not delete the contents since it indicates the current hardware status. \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:MASK:CONDition?')
		return Conversions.str_to_list_enum(response, enums.StatusQuestionMask)

	# noinspection PyTypeChecker
	def get_enable(self) -> List[enums.StatusQuestionMask]:
		"""STATus:QUEStionable:MASK:ENABle \n
		Snippet: value: List[enums.StatusQuestionMask] = driver.status.questionable.mask.get_enable() \n
		No command help available \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:MASK:ENABle?')
		return Conversions.str_to_list_enum(response, enums.StatusQuestionMask)

	def set_enable(self, value: List[enums.StatusQuestionMask]) -> None:
		"""STATus:QUEStionable:MASK:ENABle \n
		Snippet: driver.status.questionable.mask.set_enable(value = [StatusQuestionMask.MASK1, StatusQuestionMask.MASK8]) \n
		No command help available \n
			:param value: No help available
		"""
		param = Conversions.enum_list_to_str(value, enums.StatusQuestionMask)
		self._core.io.write(f'STATus:QUEStionable:MASK:ENABle {param}')

	# noinspection PyTypeChecker
	def get_event(self) -> List[enums.StatusQuestionMask]:
		"""STATus:QUEStionable:MASK[:EVENt] \n
		Snippet: value: List[enums.StatusQuestionMask] = driver.status.questionable.mask.get_event() \n
		Returns the contents of the EVENt part of the status register to check if an event has occurred since the last reading.
		Reading an EVENt register deletes its contents. \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:MASK:EVENt?')
		return Conversions.str_to_list_enum(response, enums.StatusQuestionMask)

	# noinspection PyTypeChecker
	def get_ntransition(self) -> List[enums.StatusQuestionMask]:
		"""STATus:QUEStionable:MASK:NTRansition \n
		Snippet: value: List[enums.StatusQuestionMask] = driver.status.questionable.mask.get_ntransition() \n
		No command help available \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:MASK:NTRansition?')
		return Conversions.str_to_list_enum(response, enums.StatusQuestionMask)

	def set_ntransition(self, value: List[enums.StatusQuestionMask]) -> None:
		"""STATus:QUEStionable:MASK:NTRansition \n
		Snippet: driver.status.questionable.mask.set_ntransition(value = [StatusQuestionMask.MASK1, StatusQuestionMask.MASK8]) \n
		No command help available \n
			:param value: No help available
		"""
		param = Conversions.enum_list_to_str(value, enums.StatusQuestionMask)
		self._core.io.write(f'STATus:QUEStionable:MASK:NTRansition {param}')

	# noinspection PyTypeChecker
	def get_ptransition(self) -> List[enums.StatusQuestionMask]:
		"""STATus:QUEStionable:MASK:PTRansition \n
		Snippet: value: List[enums.StatusQuestionMask] = driver.status.questionable.mask.get_ptransition() \n
		No command help available \n
			:return: value: No help available
		"""
		response = self._core.io.query_str('STATus:QUEStionable:MASK:PTRansition?')
		return Conversions.str_to_list_enum(response, enums.StatusQuestionMask)

	def set_ptransition(self, value: List[enums.StatusQuestionMask]) -> None:
		"""STATus:QUEStionable:MASK:PTRansition \n
		Snippet: driver.status.questionable.mask.set_ptransition(value = [StatusQuestionMask.MASK1, StatusQuestionMask.MASK8]) \n
		No command help available \n
			:param value: No help available
		"""
		param = Conversions.enum_list_to_str(value, enums.StatusQuestionMask)
		self._core.io.write(f'STATus:QUEStionable:MASK:PTRansition {param}')
