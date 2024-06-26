import logging
from loguru import logger

class LoggerMixing(object):

	_logger: logging.Logger = None
	@property
	def logger(self) -> logging.Logger:
			"""
			Returns the logger object.

			:return: The logger object.
			:rtype: logging.Logger
			"""
			if self._logger is None:
					self._logger = logger
			return self._logger
