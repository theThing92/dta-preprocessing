# Standard
import logging

# Pip
# None

# Custom
# None

# Configure the logger
logging.basicConfig(
    filename="dta_processor.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def log_output(log_msg: str = ""):
    logger = logging.getLogger(__name__)
    logger.info(msg=log_msg)

    print(1, log_msg)
    return logger


if __name__ == "__main__":
    # Your main code goes here
    pass
