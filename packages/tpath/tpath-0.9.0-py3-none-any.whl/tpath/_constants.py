"""
Constants used throughout the TPath package.
"""

# Size conversion constants (binary - 1024-based)
BYTES_PER_KIB = 1024
BYTES_PER_MIB = 1024 * 1024
BYTES_PER_GIB = 1024 * 1024 * 1024
BYTES_PER_TIB = 1024 * 1024 * 1024 * 1024
BYTES_PER_PIB = 1024 * 1024 * 1024 * 1024 * 1024

# Size conversion constants (decimal - 1000-based)
BYTES_PER_KB = 1000
BYTES_PER_MB = 1000 * 1000
BYTES_PER_GB = 1000 * 1000 * 1000
BYTES_PER_TB = 1000 * 1000 * 1000 * 1000
BYTES_PER_PB = 1000 * 1000 * 1000 * 1000 * 1000

# Access mode specifications
ACCESS_MODE_READ = "R"
ACCESS_MODE_WRITE = "W"
ACCESS_MODE_EXECUTE = "X"
ACCESS_MODE_READ_ONLY = "RO"
ACCESS_MODE_WRITE_ONLY = "WO"
ACCESS_MODE_READ_WRITE = "RW"
ACCESS_MODE_ALL = "RWX"
