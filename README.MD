# Python FLAC Recompressor Script

This is a script that attempts to run FLAC with several different block size numbers and other options in an attempt to 
get the smallest file size.

It encodes FLAC using non-compliant options and uses the following block sizes in an attempt to get the 
smallest file possible:

* 512
* 1024
* 2048
* 4096
* 8192
* 16384

Other options used are the following:  
`--lax -8 -f -e -p -m -r 0,15 -l 32 -b {block_size}`  
With `block_size` being a block size number from the above list.

The script will use up to 6 threads, to speed up encoding for each file. Once finished, the script will keep the 
smallest file and delete the others.

The filename format is:  
`file_name.block_size.flac`

For example:  
`my song.2048.flac`  
Which implies that the smallest file size was accomplished by using a block size of 2048.

Do note that it is highly recommended to run this script on a 6-core or 6-thread machine, to speed up the encoding. 
Otherwise, it will take several hours to recompress a whole album. 
(Tested on Dual Core Intel Pentium and Celeron processors).

Be sure to have the `flac` package installed in your Linux machine.

## Usage

```
usage: main.py [-h] -i INPUT -o OUTPUT

FLAC Brute-Force Encoder for finding the smallest file size. It encodes FLAC
using non-compliant options and uses the following block sizes in an attempt
to get the smallest file possible: 512, 1024, 2048, 4096, 8192, 16384

options:
  -h, --help            show this help message and exit

required arguments:
  -i INPUT, --input INPUT
                        Input folder with FLAC Files.
  -o OUTPUT, --output OUTPUT
                        Output folder to store the encoded FLAC files.
```

