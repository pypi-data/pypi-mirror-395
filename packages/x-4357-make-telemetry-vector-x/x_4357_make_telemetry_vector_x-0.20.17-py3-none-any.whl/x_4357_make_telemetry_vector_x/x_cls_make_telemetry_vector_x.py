"""Entry module for packaging `x_make_telemetry_vector_x` artifacts."""

from __future__ import annotations

from collections.abc import Sequence

from .scripts import package_telemetry_vector


def main(argv: Sequence[str] | None = None) -> int:
    """Invoke the telemetry vector packaging pipeline."""

    extra_args = list(argv) if argv is not None else []
    if extra_args:
        unknown = " ".join(extra_args)
        raise SystemExit(f"unexpected arguments: {unknown}")

    package_telemetry_vector.main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
