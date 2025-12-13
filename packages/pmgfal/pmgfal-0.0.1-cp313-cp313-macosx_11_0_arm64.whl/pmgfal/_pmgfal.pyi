"""type stubs for rust bindings."""

__version__: str

def generate(
    lexicon_dir: str,
    output_dir: str,
    namespace_prefix: str | None = None,
) -> list[str]:
    """generate pydantic models from lexicon files.

    Args:
        lexicon_dir: directory containing lexicon json files
        output_dir: directory to write generated python files
        namespace_prefix: optional filter for specific nsid prefix

    Returns:
        list of generated file paths
    """
