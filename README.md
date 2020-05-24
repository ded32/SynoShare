# SynoShare
A Synology Share command-line python script based on Synology FileStation REST API.

## Purpose

This is a Python 3 script for creating http://gofile.me public sharing links from command line.

## Description

Creates a public http://gofile.me link for path/file located on Synology server.

The script is based on Synology FileStation REST API and written on Python 3.
I was failed to find any simple working solutions in the Internet, so I wrote it by myself.
Python is not my native language, so it may be some C++-ish.

## Usage

SynoShare.py <path / filename_to_share> [--debug]

NB: File paths are relative to the Synology File Station root folder. So if you have a top-level folder in the File Station named "Backup" and a file in "Backup" folder names "text.txt", the path to the file is "/Backup/text.txt".

## Copyright

(c) 2020, Ded (Ilya Dedinsky, mail@ded32.ru)

## Notes

#### 1. This script uses the values are imported from OS environment variables to avoid exposing of private data:

```
.SynoShareNAS     - Synology NAS IP or DNS name
.SynoShareAccount - Synology NAS Account used for creating links
.SynoSharePasswd  - Synology NAS Account password
```

Set these variables BEFORE calling this script. They may be crypted, see below.

#### 2. This script contains Decode() function for decoding login data, which may be crypted.

Now this function works transparently, simply returning its parameters. You can update this
function to support your scheme of encrypting login credentials.
