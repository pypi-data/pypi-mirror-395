import asyncio
import collections.abc
import functools
import importlib
import inspect
import itertools
import pathlib
import sys

import typing_extensions as typing


def coroutine(function: collections.abc.Callable) -> collections.abc.Callable:
    """Wrap click cli commands to run asynchronously."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):  # noqa: ANN202
        return asyncio.run(function(*args, **kwargs))

    return wrapper


def find_factory() -> str:
    """
    Search the factory method in the current working directory.

    Returns:
      The location of the factory method in the form 'module:name'.
    """

    sys_paths = [pathlib.Path(path) for path in sys.path]

    exception: typing.Optional[Exception] = None
    factories: list[str] = []
    for root, dirs, files in walk(pathlib.Path.cwd()):
        dirs[:] = [
            d
            for d in dirs
            if any(
                path in itertools.chain([pathlib.Path(root) / d], (pathlib.Path(root) / d).parents)
                for path in sys_paths
            )
        ]

        for name in files:
            filepath = pathlib.Path(root) / name

            if filepath.suffix != ".py":
                continue

            module_name = None
            for path in sys_paths:
                if path in filepath.parents:
                    rel_path = filepath.relative_to(path)
                    module_name = rel_path.parent.as_posix().replace("/", ".") + "." + rel_path.stem

            if module_name is None:
                continue

            try:
                module = importlib.import_module(module_name)
                if (
                    (factory := getattr(module, "create_app", None))
                    and (module := inspect.getmodule(factory))
                    and inspect.getsourcefile(factory) == str(filepath)
                ):
                    factories.append(f"{module.__name__}:create_app")
            except Exception as error:  # noqa: BLE001
                exception = exception or error

    if len(factories) > 1:
        raise ImportError(
            "Multiple `create_app` factories found. Please specify the correct one explicitly:\n"
            + "\n".join(f" - `{factory}`" for factory in factories)
        )

    if not factories:
        raise exception or ImportError(
            "No `create_app` factory found. Please check your application setup or provide the factory explicitly."
        )

    return factories[0]


# Polyfill `pathlib.Path.walk` (only available on python 3.12) from
# https://github.com/python/cpython/blob/main/Lib/pathlib/_abc.py#L651
def walk(self, top_down=True, on_error=None) -> typing.Iterable[tuple[str, list[str], list[str]]]:  # noqa
    """Walk the directory tree from this directory, similar to os.walk()."""
    paths = [self]
    while paths:
        path = paths.pop()
        if isinstance(path, tuple):
            yield path
            continue
        dirnames = []
        filenames = []
        if not top_down:
            paths.append((path, dirnames, filenames))
        try:
            for child in path.iterdir():
                try:
                    if child.is_dir():
                        if not top_down:
                            paths.append(child)
                        dirnames.append(child.name)
                    else:
                        filenames.append(child.name)
                except OSError:
                    filenames.append(child.name)
        except OSError as error:
            if on_error is not None:
                on_error(error)
            if not top_down:
                while not isinstance(paths.pop(), tuple):
                    pass
            continue
        if top_down:
            yield path, dirnames, filenames
            paths += [path.joinpath(d) for d in reversed(dirnames)]
