from .cnpj_generator import CnpjGenerator


def cnpj_gen(format: bool | None = None, prefix: str | None = None) -> str:
    """Generate a valid CNPJ according to the given options."""
    generator = CnpjGenerator(format, prefix)

    return generator.generate()
