import argparse
import subprocess
import sys

import uvicorn


def start_dev_server(
    app_module: str,
    args: argparse.Namespace,
    reload_includes: list[str] | None = None,
) -> None:
    """Start the development server using Uvicorn.
    :args app_module: The module containing the Flask server to start.
    :args argparse.Namespace: The parsed arguments.
    """
    if reload_includes is None:
        reload_includes = []

    uvicorn.run(
        app_module,
        host=args.host,
        port=args.port,
        log_level=args.log_level,
        reload=True,
        reload_includes=reload_includes,
    )


def start_prod_server(app_module: str, args: argparse.Namespace) -> None:
    """Start the production server using Gunicorn.
    It will spawn one primary process and workers
    :args app_module: The module containing the Flask server to start.
    :args argparse.Namespace: The parsed arguments.
    :raises subprocess.CalledProcessError: If gunicorn exits with a non-zero status code.
    """
    cmd = [
        sys.executable,
        "-m",
        "gunicorn",
        "-k",
        "uvicorn.workers.UvicornWorker",
        "--workers",
        str(args.workers),
        "--log-level",
        args.log_level,
        "-b",
        f"{args.host}:{args.port}",
        "--capture-output",
        app_module,
    ]

    if args.log_file:
        cmd.extend(["--log-file", args.log_file])

    if args.access_logfile:
        cmd.extend(["--access-logfile", args.access_logfile])

    subprocess.run(cmd, check=True)  # noqa: S603
