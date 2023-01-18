import argparse
import glob
import os
import subprocess
from multiprocessing import Pool

FLAC_BLOCK_SIZES = [512, 1024, 2048, 4096, 8192, 16384]


def flac_process(input_file: str, output_file: str, block_size: int) -> str:
    print("Encoding with block size {}".format(block_size))
    cmd = ['flac -8 -b {} -f -e -p -m -r 0,15 -l 32 --lax "{}" -o "{}"'.format(block_size, input_file, output_file)]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return output_file


def delete_files(size_dir: dict, min_size: int) -> None:
    for key, value in size_dir.items():
        if key == min_size:
            continue
        os.remove(value)


def recompress_flac(file: str, output_folder: str) -> None:
    file_basename = os.path.splitext(os.path.basename(file))[0]
    chunks_size_dir = {}
    print("Processing file {}".format(file))
    pool = Pool()
    os.makedirs(output_folder, exist_ok=True)
    for FLAC_BLOCK_SIZE in FLAC_BLOCK_SIZES:
        output_file = os.path.join(output_folder, file_basename + "." + str(FLAC_BLOCK_SIZE) + ".flac")
        chunks_size_dir[FLAC_BLOCK_SIZE] = output_file
        pool.apply_async(flac_process, (file, output_file, FLAC_BLOCK_SIZE))
    pool.close()
    pool.join()
    size_dir = {}
    for chunks_size in chunks_size_dir.keys():
        size_dir[os.path.getsize(chunks_size_dir[chunks_size])] = chunks_size
    min_size = min(size_dir.keys())

    print("Minimum file size details:\n"
          "Chunk: {}\n"
          "File Size: {}\n"
          "File Name: {}".format(size_dir[min_size], min_size, chunks_size_dir[size_dir[min_size]]))
    delete_files(chunks_size_dir, size_dir[min_size])


def parse_args_and_loop(args: argparse) -> None:
    files = sorted(glob.glob(args.input + "/*.flac"))
    for file in files:
        recompress_flac(file, args.output)


def main() -> None:
    parser = argparse.ArgumentParser(description='FLAC Brute-Force Encoder for finding the smallest file size.\n\n'
                                                 'It encodes FLAC using non-compliant options and uses the following '
                                                 'block sizes in an attempt to get the smallest file possible: '
                                                 '512, 1024, 2048, 4096, 8192, 16384')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-i', '--input', help="Input folder with FLAC Files.", required=True)
    required.add_argument('-o', '--output', help="Output folder to store the encoded FLAC files.", required=True)
    parse_args_and_loop(parser.parse_args())


if __name__ == '__main__':
    main()
