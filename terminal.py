import sys
from multiprocessing import freeze_support

from openbb_terminal.core.config.paths_helper import init_userdata 
from openbb_terminal.terminal_helper import is_auth_enabled

def main():
    command_args = sys.argv[1:]

    load_env_files()
    init_userdata()

    if "-t" in command_args or "--test" in command_args:
        from openbb_terminal.core.integration_tests.integ_controller import main
        main()
    else:
        from openbb_terminal.core.session.session_ctrlr import main as session_main

        if is_auth_enabled():
            session_main()
        else:
            session_controller.launch_terminal()


if __name__ == "__main__":
    freeze_support()
    main()
