import logging


class Logger:
    LOGGER = logging.getLogger()

    @staticmethod
    def info(message):
        Logger.LOGGER.info(message)

    @staticmethod
    def warn(message):
        Logger.LOGGER.warning(message)

    @staticmethod
    def error(message):
        Logger.LOGGER.error(message)
