from typing import get_args

from yabra.doc.generate_doc import (
    DocumentGenerator,
    SupportedDocTypes,
    SupportedMissingDigitsAlgorithm,
)

try:
    import click
except ImportError as e:
    raise ImportError("Cannot import `click`, make sure you install `yabra[cli]`") from e


@click.group()
def cli() -> None: ...


@cli.command(
    help="""Generates one or many valid documents""",
    no_args_is_help=True,
)
@click.argument(
    "doc-type",
    type=click.Choice(get_args(SupportedDocTypes)),
    nargs=1,
    required=True,
)
@click.option(
    "--prefix",
    "prefix",
    nargs=1,
    required=False,
    type=str,
    default="",
    help="""
The initial digits of the document. Can have up to doc_max_digits - doc_check_digits. For example,
cpf can have up to 9 chars and cnpj up to 12""",
)
@click.option(
    "--algorithm",
    "algorithm",
    nargs=1,
    required=False,
    type=click.Choice(get_args(SupportedMissingDigitsAlgorithm)),
    default="random",
    help="""
The algorithm that is going to be used to generate the missing digits, defaults to `random`
where missing digits is the difference between the maximum number digits for the given
document type - the prefix digits. We recommend that you use the `sequential` like algorithms
if generating a high number of documents in order to get the expected number of documents,
since the `random` algorithms aren't deterministic, you can get lesser documents than requested.""",
)
@click.option(
    "--number",
    "number",
    nargs=1,
    required=False,
    type=int,
    default=1,
    help="""
The number of documents to generate, defaults to 1. The maximum number of generatable documents depends on the
given prefix, it's also worth reading the note about the `algorithm` option when generating a large number of
documents (TLDR: Use `sequential` or `alpha_sequential`).""",
)
@click.option(
    "--mask",
    is_flag=True,
    default=False,
    help="""Controls if the output documents are masked or not, defaults to unmasked""",
)
def generate(
    doc_type: SupportedDocTypes,
    prefix: str,
    algorithm: SupportedMissingDigitsAlgorithm,
    number: int,
    mask: bool,
) -> None:
    try:
        generator = DocumentGenerator(
            doc_type=doc_type, algorithm=algorithm, prefix=prefix, number=number
        )
    except ValueError as e:
        click.echo(click.style("".join(e.args), "red"))
        raise click.exceptions.Exit(code=1)

    for doc in generator.iter_documents():
        click.echo(doc.masked_value() if mask else doc.validated_value())


if __name__ == "__main__":
    cli()
