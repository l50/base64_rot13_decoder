import argparse, base64, codecs, os, sys

__auth__ = 'jayson.e.grace@gmail.com'


def __parse_args__():
    """Parse CLI arguments.

    """
    parser = argparse.ArgumentParser(description='Path to a file containing a string that is Base64 encoded and ROT13 encoded.')
    parser.add_argument('-f', dest="filename", required=True,
                        help='file with line that is encoded multiple times', metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    return parser.parse_args()


def is_valid_file(parser, arg):
    """Used to validate a files existence and get a file handle.

    Checks if input is a file that exists on the system.
    If it does, then it returns a file handle.

    Args:
        parser (argparse.ArgumentParser): parser object
        arg (str): The file to open

    Returns:
        A file handle for the input file with 'r' if the file exists; otherwise an error
        if the input file does not exist.

    Example:
        >>> from base64_rot13_decode import is_valid_file
        >>> import argparse
        >>> is_valid_file(argparse.ArgumentParser(description='A file on the filesystem.'), '/etc/passwd')
        <_io.TextIOWrapper name='/etc/passwd' mode='r' encoding='UTF-8'>
        >>> is_valid_file(argparse.ArgumentParser(description='A file that is not on the filesystem.'), 'bla.csv')
        error: The file bla.csv does not exist!
        *** SystemExit: 2

    """
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


def file_to_list(file):
    """Read file line by line into a list.

    Parse input file and return a list.

    Args:
        file (file): File handle for the file to parse

    Returns:
        The content of the input file as a list.

    Example:
        >>> from base64_rot13_decode import file_to_list
        >>> from base64_rot13_decode import is_valid_file
        >>> import argparse
        >>> file = is_valid_file(argparse.ArgumentParser(description='CLI for interacting with base64_rot13_decode.'), '/etc/passwd')
        >>> file_to_list(file)
        # The contents of /etc/passwd with \n for each line

    """
    with open(file.name) as f:
        list = f.readlines()
        return list


def strip_whitespace(content):
    """Strip whitespace from an input list.

    Take a list as input and strip whitespace from each entry.

    Args:
        content (list): The input list

    Returns:
        The input list without whitespaces.

    Example:
        >>> from base64_rot13_decode import strip_whitespace
        >>> list = ['bla\n', 'bla2\n', 'bla3\n']
        >>> list
        ['bla\n', 'bla2\n', 'bla3\n']
        >>> strip_whitespace(list)
        ['bla', 'bla2', 'bla3']

    """
    return [x.strip() for x in content]


def find_base64_line(content):
    """Find a line in input list with a Base64 string in it.

    Take an input list with a Base64 string in it, pull it out, and return it.
    Otherwise, throw an error.

    Input file should have the following format:

    ['"Congratulations, you found the easter egg!"', '- The incredibly funny developers',
    'L2d1ci9xcmlmL25lci9mYi9zaGFhbC9ndXJsL3V2cS9uYS9ybmZncmUvcnR0L2p2Z3V2YS9ndXIvcm5mZ3JlL3J0dA==',
    'Good luck, egg hunter!']

    Args:
        content (list): The input list which may or may not have a Base64 encoded string

    Returns:
        A Base64 encoded string which was pulled from the input list.

    Example:
        >>> from base64_rot13_decode import find_base64_line as find_b64
        >>> test = ['stuff', 'L2d1ci9xcmlmL25lci9mYi9zaGFhbC9ndXJsL3V2cS9uYS9ybmZncmUvcnR0L2p2Z3V2YS9ndXIvcm5mZ3JlL3J0dA==', 'more stuff']
        >>> find_b64(test)
        ['L2d1ci9xcmlmL25lci9mYi9zaGFhbC9ndXJsL3V2cS9uYS9ybmZncmUvcnR0L2p2Z3V2YS9ndXIvcm5mZ3JlL3J0dA==']

    """
    b64_line = [x for x in content if "==" in x]
    if not b64_line:
        raise FileError('This file does not contain a Base64 encoded string in it, exiting.')
    return b64_line


def base64_decode(b64_str):
    """Decode a Base64 encoded string.

    Args:
        b64_str (str): Base64 encoded string

    Returns:
        The decoded version of the input Base64 encoded string.

    Example:
        >>> from base64_rot13_decode import base64_decode
        >>> base64_decode('L2d1ci9xcmlmL25lci9mYi9zaGFhbC9ndXJsL3V2cS9uYS9ybmZncmUvcnR0L2p2Z3V2YS9ndXIvcm5mZ3JlL3J0dA==')
        '/gur/qrif/ner/fb/shaal/gurl/uvq/na/rnfgre/rtt/jvguva/gur/rnfgre/rtt'

    """

    return bytes.decode(base64.b64decode(b64_str))


def rot13_decode(enc_str):
    """Decode a ROT13 encoded string.

    Args:
        enc_str (str): ROT13 encoded string

    Returns:
        The decoded version of the input ROT13 encoded string.

    Example:
        >>> from base64_rot13_decode import rot13_decode
        >>> rot13_decode('/gur/qrif/ner/fb/shaal/gurl/uvq/na/rnfgre/rtt/jvguva/gur/rnfgre/rtt')
        '/the/devs/are/so/funny/they/hid/an/easter/egg/within/the/easter/egg'

    """
    encoder = codecs.getencoder("rot-13")
    return encoder(enc_str)[0]


def main():
    """Main entry point.

    """
    arg = __parse_args__()
    content = file_to_list(arg.filename)
    content = strip_whitespace(content)
    egg = find_base64_line(content)
    e64 = base64_decode(egg[0])
    print(rot13_decode(e64))


if __name__ == '__main__':
    main()
