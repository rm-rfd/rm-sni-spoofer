import argparse
from src.core.runtime import runtime_state
from src.core.runtime.relay_server import run_headless


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SNI-Spoofing relay and control panel.")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run the relay without launching the control panel.",
    )
    parser.add_argument(
        "--config",
        help="Optional path to an alternate config.json file.",
    )
    parser.add_argument(
        "--delay-test-runtime",
        action="store_true",
        help="Run headless without taking ownership of runtime state or system proxy; used for temporary delay tests.",
    )
    args = parser.parse_args()
    if args.delay_test_runtime and not args.headless:
        parser.error("--delay-test-runtime requires --headless")
    return args


def cli_main() -> int:
    args = parse_args()
    runtime_state.set_config_path_override(args.config)
    if args.headless:
        return run_headless(args.config, isolated_runtime=args.delay_test_runtime)

    from src.gui.window import launch_gui

    launch_gui()
    return 0


if __name__ == "__main__":
    raise SystemExit(cli_main())
