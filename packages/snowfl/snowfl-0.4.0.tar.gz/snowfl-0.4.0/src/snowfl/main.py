from .snowfl import Snowfl


def main():
    snowfl = Snowfl()
    snowfl.initialize()
    result = snowfl.parse("single's inferno")
    print(f'len(result["data"]): {len(result["data"])}')


if __name__ == "__main__":
    main()
