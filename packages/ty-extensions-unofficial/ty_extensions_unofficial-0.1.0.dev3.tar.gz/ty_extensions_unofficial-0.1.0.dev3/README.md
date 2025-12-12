# `ty-extensions-unofficial`

This repository contains a properly packaged fork
of [the official `ty-extensions`][1], whose [PyPI project][2] is empty.

At runtime, the package simply raises a `RuntimeError`.
As such, do not import it normally.


  [1]: https://github.com/astral-sh/ruff/blob/HEAD/crates/ty_vendored/ty_extensions/ty_extensions.pyi
  [2]: https://pypi.org/project/ty-extensions/
