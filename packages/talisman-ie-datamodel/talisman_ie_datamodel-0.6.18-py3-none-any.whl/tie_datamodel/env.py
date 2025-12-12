import os


def get_max_spawned_processes() -> int:
    max_spawned_processes = os.environ.get('MAX_SPAWNED_PROCESSES')
    return int(max_spawned_processes) if max_spawned_processes is not None else min(os.cpu_count(), 8)
