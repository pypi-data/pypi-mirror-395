def check_dependencies():
    """
    Test if numpy and numba are available.

    Returns:
        dict: A dictionary with the availability status of numpy and numba
    """
    dependencies = {}

    try:
        import numpy

        dependencies["numpy"] = {"available": True, "version": numpy.__version__}
    except ImportError:
        dependencies["numpy"] = {"available": False, "version": None}

    try:
        import numba

        dependencies["numba"] = {"available": True, "version": numba.__version__}
    except ImportError:
        dependencies["numba"] = {"available": False, "version": None}

    return dependencies
