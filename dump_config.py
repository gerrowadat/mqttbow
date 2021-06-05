from anseo import config


def main():
    c = config.Config()
    c.Load(filename='example_config.cf')


if __name__ == '__main__':
    main()
