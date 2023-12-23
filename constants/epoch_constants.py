# Standard
from collections import namedtuple
from enum import Enum

# Pip
# None

# Custom
# None

Epoch = namedtuple("EpochValues", ["dict_key", "range_value", "index_value"])


class EpochDefinitions(Enum):
    # TODO: check if end value for value range should be inclusive (e.g. 0-1699 or 0-1700)
    FROM_0_TO_1700 = Epoch(dict_key="E0", range_value=range(0, 1700), index_value=0)
    FROM_1700_TO_1749 = Epoch(
        dict_key="E1", range_value=range(1700, 1750), index_value=1
    )
    FROM_1750_TO_1799 = Epoch(
        dict_key="E2", range_value=range(1750, 1800), index_value=2
    )
    FROM_1800_TO_1849 = Epoch(
        dict_key="E3", range_value=range(1800, 1850), index_value=3
    )
    FROM_1850_TO_1899 = Epoch(
        dict_key="E4", range_value=range(1850, 1900), index_value=4
    )


if __name__ == "__main__":
    # how to access values in enum object
    dict_key = EpochDefinitions.FROM_1700_TO_1749.value.dict_key
    range_value = EpochDefinitions.FROM_1700_TO_1749.value.range_value
    index_value = EpochDefinitions.FROM_1700_TO_1749.value.index_value
    print(dict_key, type(dict_key))
    print(range_value, type(range_value))
    print(index_value, type(index_value))
