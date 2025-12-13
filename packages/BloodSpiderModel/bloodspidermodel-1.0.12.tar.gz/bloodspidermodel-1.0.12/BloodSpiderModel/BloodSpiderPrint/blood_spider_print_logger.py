from loguru import logger

class BloodSpiderPrintLogger:
    def __init__(self, is_show=True):
        self.is_show = is_show

    def blood_spider_print_debug(self, text: str):
        if self.is_show:
            logger.debug(text)

    def blood_spider_print_info(self, text: str):
        if self.is_show:
            logger.info(text)

    def blood_spider_print_warning(self, text: str):
        if self.is_show:
            logger.warning(text)

    def blood_spider_print_error(self, text: str):
        if self.is_show:
            logger.error(text)
