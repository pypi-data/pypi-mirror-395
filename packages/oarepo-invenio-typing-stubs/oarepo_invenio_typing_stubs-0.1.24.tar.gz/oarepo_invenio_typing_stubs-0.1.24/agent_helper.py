import sys
from pathlib import Path


def get_file_list(package):
    pkg = __import__(package, fromlist=[""])
    # Handle both packages (with __path__) and single-file modules (with __file__ only)
    if hasattr(pkg, "__path__"):
        pkg_path = Path(pkg.__path__[0])
        file_list = []
        for p in pkg_path.rglob("*.py"):
            if "alembic" in p.parts:
                continue
            file_list.append(str(p.relative_to(pkg_path)))
        # sort file list to keep the files in packages together
        file_list.sort(key=lambda x: (x.count("/"), x))
        return pkg_path.relative_to(Path.cwd()), file_list
    else:
        # Single-file module; emulate a one-file "package"
        pkg_file = Path(pkg.__file__)
        pkg_path = pkg_file.parent
        file_list = [pkg_file.name]
        return pkg_path.relative_to(Path.cwd()), file_list


def stubs_path(package):
    return Path(f"{package}-stubs")


ALL_DONE = -1


def get_actual_pos(package):
    idx_file = stubs_path(package) / "idx.txt"
    if not idx_file.exists():
        return 0
    contents = idx_file.read_text().strip()
    if contents == "done":
        return ALL_DONE
    return int(contents)


def save_actual_pos(package, pos):
    idx_file = stubs_path(package) / "idx.txt"
    if pos == ALL_DONE:
        idx_file.write_text("done")
    else:
        idx_file.write_text(str(pos))


def get_imported_files(root: Path, source_file: Path) -> list[str]:
    python_content = source_file.read_text()
    imported_files = []
    for line in python_content.splitlines():
        line = line.strip()
        if line.startswith("import "):
            module = line[len("import ") :].split()[0]
        elif line.startswith("from "):
            module = line[len("from ") :].split()[0]
        else:
            continue
        module_path: str | None = None
        if module.startswith("."):
            # relative import
            p = source_file
            while module.startswith("."):
                module = module[1:]
                p = p.parent
            if module:
                module_path = str(p / (module.replace(".", "/")))
        else:
            module_path = str(root.parent / (module.replace(".", "/")))
        if module_path is not None:
            if Path(module_path).is_dir():
                module_path = str(Path(module_path) / "__init__.py")
            else:
                module_path = module_path + ".py"
            if Path(module_path).exists():
                imported_files.append(module_path)
    return imported_files


def next_files(package, max_count=1) -> tuple[list[tuple[str, str]], set[str]]:

    root_path, file_list = get_file_list(package)
    actual_pos = get_actual_pos(package)
    if actual_pos == ALL_DONE or actual_pos >= len(file_list):
        save_actual_pos(package, ALL_DONE)
        return [], set()

    paths: list[str] = []
    end = actual_pos + max_count
    while actual_pos < min(len(file_list), end):
        next_file = file_list[actual_pos]
        actual_pos += 1
        if not paths:
            paths.append(next_file)
        else:
            prevpackage = f"a/{paths[-1]}".rsplit("/", maxsplit=1)[0]
            currentpackage = f"a/{next_file}".rsplit("/", maxsplit=1)[0]
            if prevpackage != currentpackage:
                break
            paths.append(next_file)

    output_paths: list[tuple[str, str]] = []
    imports = set[str]()
    for p in paths:
        # convert py to pyi
        output_paths.append((str(root_path / p), str(stubs_path(package) / p) + "i"))
        imported_files = get_imported_files(Path(root_path), Path(root_path) / Path(p))
        imports.update(imported_files)

    save_actual_pos(package, actual_pos if actual_pos < len(file_list) else ALL_DONE)

    return output_paths, imports


def create_prompt(package):

    to_process, imported_files = next_files(package, max_count=5)
    stub_dir = stubs_path(package)
    if not to_process:
        print(
            f"It seems that the task has been completed. "
            f"Please run the mypy on the whole {stub_dir} directory to verify that everything is fine."
            "Thank you!"
        )
        return

    prompt = Path("prompt.txt").read_text()
    prompt = prompt.format(
        file_list="\n".join(f"{py} -> {pyi}" for py, pyi in to_process),
        package=package,
        imported_files=" ".join(sorted(imported_files)),
    )

    print(prompt)


if __name__ == "__main__":
    create_prompt(sys.argv[1])
