from ..config import config

def main():
    if config["source"]=="kattis":
        from . import kattis
        kattis.main()
    else:
        raise NotImplementedError

if __name__ == "__main__":
    main()