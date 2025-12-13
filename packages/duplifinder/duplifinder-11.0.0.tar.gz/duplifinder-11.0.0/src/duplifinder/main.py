# src/duplifinder/main.py

"""Main entry point for Duplifinder."""

import sys
import time
from typing import Dict, List, Tuple
from pydantic import ValidationError

from .cli import create_parser, build_config
from .utils import PerformanceTracker
from .banner import print_logo
from .exceptions import DuplifinderError, ConfigError
from .application import WorkflowFactory


def main() -> None:
    """Run the main Duplifinder workflow."""
    print_logo()
    parser = create_parser()
    args = parser.parse_args()

    # Pre-parse verbose for tracker init (config not built yet)
    # We can check args.verbose directly since build_config also checks it
    tracker = PerformanceTracker(verbose=args.verbose)
    tracker.start()

    try:
        try:
            config = build_config(args)
            tracker.mark_phase("Configuration")
        except (ConfigError, ValidationError, SystemExit) as e:
            if isinstance(e, SystemExit):
                raise
            # If it's a ConfigError from build_config (which calls load_config_file), print nicely
            # If it's a ValidationError from Pydantic, print nicely
            error_msg = str(e)
            if isinstance(e, ValidationError):
                # Format Pydantic errors a bit nicer if possible, or just dump string
                # e.errors() gives list of dicts.
                msgs = []
                for err in e.errors():
                    msgs.append(f"- {err['loc'][0]}: {err['msg']}")
                error_msg = "\n".join(msgs)

            print(f"Configuration Error:\n{error_msg}", file=sys.stderr)
            sys.exit(2)

        workflow_start = time.perf_counter()  # Start timing post-config

        workflow = WorkflowFactory.create(config, tracker, workflow_start)

        if config.watch_mode:
            exit_code = workflow.run_with_watch()
        else:
            exit_code = workflow.run()

        sys.exit(exit_code)

    except DuplifinderError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
