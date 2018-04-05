# base64_rot13_decoder
[![License](http://img.shields.io/:license-mit-blue.svg)](https://github.com/l50/base64_rot13_decoder/blob/master/LICENSE)

Used to decode a string found in a file that is ROT13 encoded and then BASE64 encoded. 

## Usage

```
python base64_rot13_decode.py -h
usage: base64_rot13_decode.py [-h] -f FILE

Path to a file containing a string that is Base64 encoded and ROT13 encoded.

optional arguments:
  -h, --help  show this help message and exit
  -f FILE     file with line that is encoded multiple times
```

Run with a file that has a string in it that's ROT13 encoded and then BASE64 encoded:
```
python base64_rot13_decode.py -f eastere.gg
```
