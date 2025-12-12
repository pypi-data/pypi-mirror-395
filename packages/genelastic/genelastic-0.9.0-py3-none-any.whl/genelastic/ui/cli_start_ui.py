from genelastic.common.cli import parse_server_launch_args
from genelastic.common.server import start_dev_server, start_prod_server


def main() -> None:
    app_module = "genelastic.ui.server:app"
    args = parse_server_launch_args("Start UI server.", 8001)
    if args.env == "dev":
        start_dev_server(
            app_module, args, reload_includes=["*.html", "*.js", "*.css"]
        )
    elif args.env == "prod":
        start_prod_server(app_module, args)
    else:
        msg = f"Environment '{args.env}' is not implemented."
        raise NotImplementedError(msg)


if __name__ == "__main__":
    main()
