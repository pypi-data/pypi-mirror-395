def get_platform_version_info() -> tuple[int, int, int]:
    """
    Retrieve the platform version information as a tuple of integers (major, minor, patch)

    :return: (major, minor, patch)
    """
def compare_platform_version(version: str, comparison: str = '>=') -> bool:
    '''
    Compare platform version with a provided semver version string. Supports partial version matching when using "=" comparison.

    :param version: A semver format version string like: "1.24.0" or partial like "1.24" or "1"
    :param comparison: Comparison operator, one of ">", ">=", "<", "<=", "="

    :return: bool: True if the platform version satisfies the comparison with the input version

    Examples:
        >>> platform_version = (1, 24, 0)
        >>> compare_platform_version("1.24.0", "=")   # True
        >>> compare_platform_version("1.24", "=")     # True (partial match)
        >>> compare_platform_version("1", "=")        # True (partial match)
        >>> compare_platform_version("1.23.0", ">=")  # True
        >>> compare_platform_version("1.23.0", ">")   # True
        >>> compare_platform_version("1.24.0", "<=")  # True
        >>> compare_platform_version("1.26.0", "<")   # True
    '''
