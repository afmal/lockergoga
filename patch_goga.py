#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.PublicKey import RSA
from Crypto import Random
from shutil import copyfile
import argparse


def gen_key_patch(file_patch, file_offset, private_key_file='private_key.pem', public_key_file='public_key.pem'):
    print('Generating RSA key...')
    rsa_key = RSA.generate(1024, Random.new().read)  # generates key
    print('RSA key generated!')

    print('Exporting RSA private key...')
    prv_exported = rsa_key.exportKey()  # exports private key as format
    print('RSA private key exported!')

    print('Exporting RSA public key...')
    pub_exported = rsa_key.publickey().exportKey()  # public key exported
    print('RSA public key exported!')

    # PATCHING FILE WITH PUBLIC KEY
    print('Backing up file (%s)...' % file_patch)
    copyfile(file_patch, file_patch + '_backup')

    print('Patching provided file (%s) using offset (%s)...' % (file_patch, hex(file_offset)))
    with open(file_patch, 'r+b') as patch_file:  # open file to patch
        patch_file.seek(file_offset)  # move to public key
        parsed_public_key = pub_exported[27:-25]  # parse public key data
        patch_file.write(parsed_public_key)  # parses extra from PEM public key
    print('File (%s) patched!' % file_patch)

    # PRIVATE KEY FILE
    print('Writing new private key to %s...' % private_key_file)
    with open(private_key_file, 'wb') as priv_file: # opens new private key file
        priv_file.write(prv_exported)  # write private key data to file
    print('New private key written to %s!' % private_key_file)

    # PUBLIC KEY FILE
    print('Writing new public key to %s...' % public_key_file)
    with open(public_key_file, 'wb') as pub_file:  # opens new public key file
        pub_file.write(pub_exported)  # write public key data to file
    print('New public key written to %s!' % public_key_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Accepts a minimum of a file to patch and file offset then generates '
                                                 'a binary patched with a newly generated public key.')

    parser.add_argument('in_file', metavar='FILENAME', type=str, nargs=1,
                        help='file that is to be patched with the public key')
    parser.add_argument('offset', metavar='OFFSET', type=str, nargs=1,
                        help='decimal/hexadecimal (with 0x) offset start of patch')
    parser.add_argument('--out_private', '--priv', metavar='FILENAME', type=str, nargs=1,
                        help='output filename for the newly generated private key')
    parser.add_argument('--out_public', '--pub', metavar='FILENAME', type=str, nargs=1,
                        help='output filename for the newly generated public key')
    args = parser.parse_args()

    if not len(args.in_file) and len(args.offset):
        raise Exception('Missing required positional arguments: in_file and offset!')  # not likely to be raised

    in_file = args.in_file[0]
    offset = int(args.offset[0].replace('\u202c', ''), 0)  # weird unicode char is appended to end requiring parse of last char
    out_private = args.out_private[0] if args.out_private else 'private_key.pem'
    out_public = args.out_public[0] if args.out_public else 'public_key.pem'

    gen_key_patch(in_file, offset, out_private, out_public)

    print('Exiting!')
    exit()

