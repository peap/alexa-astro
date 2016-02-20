#!/usr/bin/env python
import argparse

from PIL import Image

SMALL_ICON_DIMS = (108, 108)
LARGE_ICON_DIMS = (512, 512)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Create small and large icons for Alexa Skill.',
    )
    parser.add_argument('img_path')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    img_path = args.img_path
    Image.open(img_path).resize(SMALL_ICON_DIMS).save('icon_small.jpg')
    Image.open(img_path).resize(LARGE_ICON_DIMS).save('icon_large.jpg')


if __name__ == '__main__':
    main()
