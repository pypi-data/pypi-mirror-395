#
#   Imandra Inc.
#
#   api_ref.py
#

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Final, Self
from uuid import UUID

import typer


@dataclass
class IMLAPIReference:
    id: UUID
    module: str
    name: str
    signature: str
    doc: str | None = None
    pattern: str | None = None

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Self:
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_iar_cache: list[IMLAPIReference] | None = None

DOC_DIR: Final = Path(__file__).parent / '../data'


@dataclass
class MDDoc:
    title: str
    content: str


md_docs: list[MDDoc] | None = None


def _load_md_docs() -> list[MDDoc]:
    """
    Load documents in addition to the IML overview and API reference.
    """
    global md_docs
    if md_docs is None:
        md_docs = []
        doc_names = [
            'tactics.md',
            'ordinal.md',
            'termination_proofs.md',
        ]
        for doc_name in doc_names:
            doc_file = DOC_DIR / doc_name
            doc = MDDoc(doc_file.stem, doc_file.read_text())
            md_docs.append(doc)
    return md_docs


def _load_iar() -> list[IMLAPIReference]:
    """
    Load IML API Reference data lazily.
    """
    global _iar_cache
    if _iar_cache is None:
        iar_path = DOC_DIR / 'iml_api_reference_202510011126.json'
        iar_data = json.loads(iar_path.read_text())
        _iar_cache = [IMLAPIReference.from_dict(i) for i in iar_data]
    return _iar_cache


def iml_overview_api_dump(dir_path: Path):
    """
    Writes the IML overview and API reference to a directory.

    Output will be like this:
        - iml_overview.md
        - iml_api_reference/
            - global.md
            - module1.md
            - module2.md
            - etc...
    """
    if not dir_path.exists():
        dir_path.mkdir(exist_ok=False, parents=True)

    if not dir_path.is_dir():
        typer.secho(
            f'Path is not a directory: {dir_path}', fg=typer.colors.RED, err=True
        )
        raise typer.Exit(1)

    from codelogician.doc.utils.prompts import (
        iml_caveats,
        iml_intro,
        lang_agnostic_meta_eg_overview,
        lang_agnostic_meta_egs_str,
    )

    # Write overview
    iml_overview = (
        iml_intro
        + iml_caveats
        + lang_agnostic_meta_eg_overview
        + lang_agnostic_meta_egs_str
    )
    overview_path = dir_path / 'iml_overview.md'
    overview_path.write_text(iml_overview)
    typer.secho(f'✓ Written overview to {overview_path}', fg=typer.colors.GREEN)

    # Write API reference
    iar = _load_iar()
    api_ref_dir = dir_path / 'iml_api_reference'
    api_ref_dir.mkdir(exist_ok=True)

    # Group by module
    modules = sorted({entry.module for entry in iar})
    for module in modules:
        module_entries = [entry for entry in iar if entry.module == module]
        module_name = module or 'global'

        is_global: bool = module_name == 'global'

        # Create markdown content for this module
        module_lines = [
            f'# Module `{module_name}`\n' if not is_global else '# Global\n',
            f'\n{len(module_entries)} entries\n\n',
        ]

        if is_global:
            module_lines.append(
                f'The following entries are qualified by the module `{module_name}`.'
                '\n\n'
            )

        for entry in module_entries:
            module_lines.append(f'`{entry.name}`\n')
            module_lines.append(f'- Signature: `{entry.signature}`\n')
            if entry.doc:
                module_lines.append(f'- Doc: {entry.doc}.\n')
            # if entry.pattern:
            #     module_lines.append(f"\n**Pattern:** `{entry.pattern}`\n")
            module_lines.append('\n')

        # Write module file
        module_filename = f'{module_name}.md' if module else 'global.md'
        module_path = api_ref_dir / module_filename
        module_path.write_text(''.join(module_lines))

    typer.secho(
        f'✓ Written API reference to {api_ref_dir} ({len(modules)} modules)',
        fg=typer.colors.GREEN,
    )

    ## Write md_docs
    # md_docs = _load_md_docs()
    # for doc in md_docs:
    #    doc_path = dir_path / f"{doc.title}.md"
    #    doc_path.write_text(doc.content)
    #    typer.secho(f"✓ Written {doc.title} to {doc_path}", fg=typer.colors.GREEN)
