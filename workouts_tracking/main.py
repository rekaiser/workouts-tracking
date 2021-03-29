import sys

from .gui import run_app, create_app, create_and_show_main_window


def main():
    q_app = create_app(sys.argv)
    main_window = create_and_show_main_window()
    exit_code = run_app(q_app)
    if exit_code != 0:
        print(f"Program exited with failure: Exit Code {exit_code}")


if __name__ == '__main__':
    main()
