import argparse


def main(args):
    pass


def init_parser():
    parser = argparse.ArgumentParser(description='CompanyContactsScrapper', prog="compsearch")

    parser.add_argument(
        'input',
        help='input file'
    )

    parser.add_argument(
        '-o', '--output',
        help='output file',
        default='output.csv'
    )

    parser.add_argument(
        '-b', '--blacklist',
        help='black list file',
        default='blacklist.csv'
    )

    parser.add_argument(
        '-d', '--depth',
        help='crawler depth',
        type=int,
        default=1
    )

    parser.add_argument(
        '-p', '--pages',
        help='number of pages to look up in search engine results',
        type=int,
        default=3
    )

    return parser


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()

    main(args)
