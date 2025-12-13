import traceback

from kunlun.service import cli


def main():
    try:
        cli.main()
    except Exception as e:
        print(e)
        error = traceback.format_exc()
        print(error)
    except KeyboardInterrupt as e:
        print(e)
        print("\nUser Keyboard Interrupt")


if __name__ == "__main__":
    main()
