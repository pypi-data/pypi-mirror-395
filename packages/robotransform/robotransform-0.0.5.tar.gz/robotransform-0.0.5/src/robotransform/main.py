from dataclasses import dataclass, fields
from functools import lru_cache
from pathlib import Path

import arklog
from textx import metamodel_from_str
from jinja2 import Environment, FileSystemLoader, Template
import io
from typing import Union, Optional, Iterable, Iterator

from robotransform.concepts import all_concepts, Package
from robotransform.filters import type_to_port, type_to_aadl_type
from robotransform.processors import processors


@dataclass
class Store:
    packages: Iterable[Path]

    def __iter__(self) -> Iterator[Path]:
        for f in fields(self):
            value = getattr(self, f.name)
            if isinstance(value, Path):
                yield value
                continue
            if isinstance(value, Iterable):
                for item in value:
                    if isinstance(item, Path):
                        yield item
                continue

    def parse_imports(self, package: Package, parent_path: Path, visited):
        stack = [package]
        while stack:
            package = stack.pop()
            for imp in package.imports:
                name = imp.name.name.parts[-1]
                if name in visited:
                    continue
                path = parent_path / f"{name}.rct"
                if not path.exists():
                    arklog.debug(f"Can't import {path}.")
                    continue
                sub_package = parse_robochart(path)
                visited[path] = sub_package
                stack.append(sub_package)
        return visited

    def load(self, imports: bool = True) -> dict[Path, Package]:
        visited = {}
        for path in self:
            package = parse_robochart(path)
            visited[path] = package
            if imports:
                visited |= self.parse_imports(package, path.parent, visited)
        return visited


@dataclass
class MapleKStore(Store):
    monitor: Path
    analysis: Path
    plan: Path
    legitimate: Path
    execute: Path
    knowledge: Path

    def __init__(self, monitor: Path, analysis: Path, plan: Path, legitimate: Path, execute: Path, knowledge: Path,
                 additional: Optional[Iterable[Path]] = None):
        self.monitor = monitor
        self.analysis = analysis
        self.plan = plan
        self.legitimate = legitimate
        self.execute = execute
        self.knowledge = knowledge
        self.packages = [monitor, analysis, plan, legitimate, execute, knowledge]
        if additional is not None:
            self.packages += additional

    def verify(self):
        pass


@lru_cache(maxsize=1)
def get_robochart_metamodel(name: str = "robochart.tx"):
    arklog.debug(f"Loading ({name}) metamodel.")
    metamodel_path = Path(__file__).resolve().parent / name
    metamodel = metamodel_from_str(metamodel_path.read_text(), classes=all_concepts(), memoization=True)
    metamodel.register_obj_processors(processors)
    return metamodel


@lru_cache(maxsize=1)
def parse_robochart(source: Path | str) -> Package:
    arklog.debug(f"Parsing ({source}).")
    metamodel = get_robochart_metamodel()
    data = source.read_text() if isinstance(source, Path) else source
    return metamodel.model_from_str(data)


@lru_cache(maxsize=2)
def get_template(name: str) -> Template:
    environment = Environment(loader=FileSystemLoader(Path(__file__).resolve().parent / "templates"))
    environment.filters["type_to_port"] = type_to_port # For use with pipes
    environment.filters["type_to_aadl_type"] = type_to_aadl_type # For use with pipes
    # environment.globals["type_to_port"] = type_to_port # For use as a function
    templates = {
        "messages": "messages.aadl",
        "logical": "logical.aadl",
    }
    if found := templates.get(name):
        return environment.get_template(found)
    else:
        raise ValueError(f"No template found for name ({name}).")


def write_output(data: str, output: Optional[Union[io.TextIOBase, Path, str]] = None) -> str:
    if output is None:
        return data
    if isinstance(output, (str, Path)):
        output = Path(output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(data)
    elif isinstance(output, io.TextIOBase):
        output.write(data)
        output.flush()
    else:
        raise TypeError(f"Unsupported output type ({type(output)}).")
    return data


def dump_messages(store: Store, output: Optional[Union[io.TextIOBase, Path, str]] = None) -> None:
    template = get_template("messages")
    output = output if output else Path("output/generated/messages/messages.aadl")
    write_output(template.render(packages=store.load().values()), output)


def dump_logical(store: Store, output: Optional[Union[io.TextIOBase, Path, str]] = None) -> None:
    template = get_template("logical")
    output = output if output else Path("output/generated/LogicalArchitecture.aadl")
    write_output(template.render(packages=store.load().values()), output)


def main():
    pass


if __name__ == "__main__":
    main()
