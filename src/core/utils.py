from enum import IntEnum


class BinaryEnum(IntEnum):
    @classmethod
    def get_options(cls, value):
        """Get the options included in value"""
        return [k for k, v in cls.__members__.items() if value & v]
