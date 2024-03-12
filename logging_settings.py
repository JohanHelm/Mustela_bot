from loguru import logger


def init_logger():
    logger.remove(0)
    return logger

def configure_logger(logger, file_path, rotation):
    logger.add(file_path, rotation=f"{rotation} MB")
    logger.debug(
        f"Configure: basic logger update conf with write to {file_path} and set file rotation at {rotation} MB"
    )
