from sequences import get_next_value


def get_next_id_with_prefix(sequence_name: str, prefix: str) -> int:
    return int(f'{get_next_value(sequence_name)}{prefix}')
