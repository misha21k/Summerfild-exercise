import optparse


def read_commands():
    """Reads arguments of command line"""
    parser = optparse.OptionParser(usage='Usage: %prog [options] file1 [file2 [... fileN]]',
                                   version='01')
    parser.add_option('-b', '--blocksize',
                      default=16,
                      dest='blocksize',
                      help='block size (8..80) [default: %default]',
                      type='int')
    parser.add_option('-d', '--decimal',
                      action='store_true',
                      dest='decimal',
                      help='decimal block numbers [default: hexadecimal]')
    parser.add_option('-e', '--encoding',
                      default='UTF-8',
                      dest='encoding',
                      help='encoding (ASCII..UTF-32) [default: %default]')
    parser.disable_interspersed_args()
    opts, files = parser.parse_args()
    if not (8 <= opts.blocksize <= 80):
        parser.error("invalid blocksize")
    if not files:
        parser.error("no files specified")
    return opts, files


def seq_of_bytes(bytes, decimal):
    """Transforms sequence of bytes in sequence hexadecimal digits"""
    if decimal:
        ft = '{0:0>3}'
    else:
        ft = '{0:0>2x}'
    line = ''
    i = 0
    for byte in bytes:
        if i == 4:
            line += ' '
            i = 0
        line += ft.format(byte)
        i += 1
    return line


def decode_to_string(bytes, encoding):
    """Decodes sequence of bytes in string"""
    line = bytes.decode(encoding, errors='replace')
    changed_line = ''
    for char in line:
        if char.isprintable() and char != '\uFFFD':
            changed_line += char
        else:
            changed_line += '.'
    return changed_line


def len_seq(blocksize, decimal):
    """Returns length of sequence of hexadecimal digits"""
    if decimal:
        return max(5, 3*blocksize + (blocksize - 1) // 4)
    return max(5, 2*blocksize + (blocksize - 1) // 4)


def main():
    opts, files = read_commands()
    len_seq_bytes = len_seq(opts.blocksize, opts.decimal)
    len_seq_chars = max(len(opts.encoding) + 11, opts.blocksize)
    print('{0:<10}{1:<{2}}  {3:<{4}}'.format('Block', 'Bytes', len_seq_bytes,
                                           opts.encoding + ' characters', len_seq_chars))
    print('{0:-<8}  {0:-<{1}}  {0:-<{2}}'.format('', len_seq_bytes, len_seq_chars))
    i = 0
    for filename in files:
        fh = open(filename, 'rb')
        while True:
            seq_bytes = ''
            bytes = fh.read(opts.blocksize)
            if not bytes:
                break
            seq_bytes += seq_of_bytes(bytes, opts.decimal)
            seq_chars = decode_to_string(bytes, opts.encoding)
            print('{0:0>8}  {1:<{2}}  {3:<{4}}'.format(i, seq_bytes, len_seq_bytes,
                                                       seq_chars, len_seq_chars))
            i += 1
        fh.close()


main()
