from PIL import Image, ImageEnhance
from warnings import warn
import glob
import os
import sys

SRC_EXT = ['.jpg', '.jpeg', '.png']
DST_EXT = '.bmp'

palette7c = Image.new("P", (1,1))
palette7c.putpalette(
    (0x00,0x00,0x00, 0xff,0xff,0xff, 0x00,0xff,0x00, 0x00,0x00,0xff,
     0xff,0x00,0x00, 0xff,0xff,0x00, 0xff,0x80,0x00) +
    (0x00,0x00,0x00)*249
)


def scale_image(image: Image, target_width=800, target_height=480) -> Image:
    """
    Given an Pillow image and the two dimensions scale it,
    cropping centrally if required.
    """
    width, height = image.size

    if width < height:
        print('    rotated')
        image = image.rotate(-90, expand=True)
        width, height = image.size

    if height/width < target_height/target_width:
        new_height = target_height
        new_width = int(width * new_height / height)
    else:
        new_width = target_width
        new_height = int(height * new_width / width)

    print(f'    {width} x {height} -> {target_width} x {target_height}')

    # Image.ANTIALIAS is depracated --> Image.Resampling.LANCZOS
    # but a fresh install of pillow via ``ARCHFLAGS='-arch arm6' python3 -m pip install pillow``
    # yielded 8.1.2 as of 26/02/23
    ANTIALIAS = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.ANTIALIAS
    img = image.resize((new_width, new_height), ANTIALIAS)
    # (left, top, right, bottom)
    half_width_delta = (new_width - target_width) // 2
    half_height_delta = (new_height - target_height) // 2
    img = img.crop((half_width_delta, half_height_delta,
                    half_width_delta + target_width, half_height_delta + target_height
                   ))
    return img


def apply_floyd_steinberg(src_file, dst_file):
    print('{} -> {}'.format(src_file, dst_file))

    img = Image.open(src_file)
    scaled = scale_image(img)

    image = ImageEnhance.Color(scaled).enhance(2)
    image = image.quantize(dither=Image.FLOYDSTEINBERG, palette=palette7c).convert('RGB')
    image.save(dst_file, "BMP")


def run_batch(src_dir, dst_dir):
    filelist = glob.glob(src_dir + "/*")

    for file in filelist:
        basename = os.path.basename(file)
        (name, ext) = os.path.splitext(basename)
        if(ext.lower() in SRC_EXT):
            converted = dst_dir + '/' + name + DST_EXT
            apply_floyd_steinberg(file, converted)


def usage(name):
    print('python3 ' + name + ' <src-dir-path> [dst-dir-path]')
    print('    if dst-dir-path is not specified, src-dir-path/output will be used')


def parse_arguments():
    argc = len(sys.argv)
    argv = sys.argv

    if (argc < 2 or argc > 4):
        usage(argv[0])
        exit(1)

    src_dir = argv[1]
    if (not os.path.exists(src_dir)):
        print('source folder not exists: ' + src_dir)
        exit(1)

    dst_dir = src_dir + '/output'
    if (argc == 3):
        dst_dir = argv[2]

    if (not os.path.exists(dst_dir)):
        os.mkdir(dst_dir)

    return src_dir, dst_dir


if __name__ == '__main__':
    src_dir, dst_dir = parse_arguments()
    run_batch(src_dir, dst_dir)
