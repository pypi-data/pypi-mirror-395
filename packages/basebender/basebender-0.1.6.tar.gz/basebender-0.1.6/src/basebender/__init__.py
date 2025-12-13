"""Basebender: A Python package. Refer to the documentation for more details."""

try:
    from importlib.metadata import PackageNotFoundError, version

    VERSION = version(
        "basebender"
    )  # <--- Replace "basebender" with your actual package name
except (PackageNotFoundError, ImportError):

    VERSION = "0.0.0+unknown"
