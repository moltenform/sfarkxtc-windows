
# sfarkxtc-windows

Windows binaries for the sfarkxtc tool. You can use `sfarkxtc.exe` to decompress .sfark files into .sf2 soundfonts. A fork of https://github.com/raboof/sfArkXTm

## Download+Usage

Go to the releases tab on Github (https://github.com/moltenform/sfarkxtc-windows/releases) and download the latest release that says "win64". Unzip the archive to get `sfarkxtc.exe`.

Copy a .sfark file into the same directory as sfarkxtc. From the commandline, run a command like

`sfarkxtc.exe mySoundfont.sfark mySoundfont.sf2`

and it will extract the .sf2!

## Why sfarkxtc-windows?

Interestingly, sfark still compresses .sf2 files significantly better than even modern .7z and .rar compression. However, I want to store my files in a format that will still be readable, even 20 years in the future, so any type of unique or proprietary format is dangerous. Moltenform's thoughts on storing soundfonts:

- Store the full .sf2 files
    - Pros: no need to decompress
    - Cons: takes a lot of disk space
- Store in .tar.gz, or .7z format
    - Pros: software to decompress is open-source and available
    - Cons: does not compress .sf2 files very well, even with a large buffer size
- Store in .sfpack format
    - Pros: good compression ratio
    - Cons: no open source decompression = unsafe for long term storage!
    - [More notes](./src/sfpack_notes.md)
- Store in .sfark format
    - Pros: good compression ratio
    - Pros: some tools like SynthFont can read .sfark directly
    - Pros: easily automate decompression via cmd line tool
    - Pros: open source decompression available
    - Cons: compression still relies on closed-source win32 binary
    - Cons: sfarkxtc doesn't support 100% of sfark files

(Note that in 2012, j\_e\_f\_f\_g, who wrote "unsfark", [claimed](https://www.linuxmusicians.com/viewtopic.php?t=9854) that sfark is an extremely fragile format relying on intel rounding errors, but this has been disputed by further research... in any case, we'll probably have x86 emulators for a long time. The fact that sfarkxtc can build and work targeting both x86 and x86-64 is a good sign.)

Conclusion: I'll use sfark to store my soundfonts. For long term storage, I'll run a script to run everything through `sfarkxtc.exe` and ensure that `sfarkxtc` can extract a bitwise-identical .sf2 file compared with the input.

### Building from source

There are many ways to accomplish this, here's a pretty straightforward route:

- Get the latest sfarkxtc-windows source
    - for example `git clone https://github.com/moltenform/sfarkxtc-windows.git`
- Go to https://rubyinstaller.org/downloads/
- Download "Ruby+DevKit" for x64, for example `rubyinstaller-devkit-2.5.3-1-x64.exe`
- Run this installer, it will set up a working mingw/msys2 environment
- If you installed ruby to `C:\ruby`, open the directory `C:\ruby\Ruby25-x64\msys64`
- Run `msys2_shell.cmd` to open a msys2 shell.
- `cd` to where the sfarkxtc-windows source is.
    - Remember that you need to use / forward slashes in the path, not backslashes.
- Run `make`
    - if you get the error `make: g++: Command not found`
    - add g++ to the PATH by running
    - `export PATH=$PATH:/c/ruby/Ruby25-x64/msys64/mingw64/bin`
- Optional: for additional security, you can build with Duma enabled.
    - adds protection against potential memory bugs triggered by malformed sfark files
    - build Duma to get libduma.a
    - copy libduma.a to sfarkxtc-windows/src/duma
    - run `make USE_DUMA=1`
- Optional: for additional security, you can build with stack protection.
    - adds protection against potential overflow bugs triggered by malformed sfark files
    - I recommend running `pacman -Syu` a few times to get the latest MSYS2
    - the 2018 version of MSYS2 I had was affected by [this bug](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=86832); enabling stack protection caused crashes in every function.
    - run `make USE_DUMA=1 PROTECT_STACK=1`
- There should now be a file `sfarkxtc_out.exe`
- Copy `C:\ruby\Ruby25-x64\msys64\mingw64\bin\zlib1.dll` into the same directory as `sfarkxtc_out.exe`
- Done!

### Zlib

For the truly paranoid (I guess I'll have to include myself here) I've included the source of zlib, in case I'm trying to build this 20 years in the future and it's hard to find the right version of zlib's source. The easiest way for it to be built on Windows is to:

```
(use a mingw shell as described above)
(untar the archive)
(cd into the directory)
make -f win32/Makefile.gcc BINARY_PATH=/bin INCLUDE_PATH=/usr/local/include LIBRARY_PATH=/usr/local/lib
```

This will generate `zlib1.dll` and so on. You can now modify sfarkxtc's Makefile to point to the newly built zlib, and modify all headers that refer to "zlib.h" to a relative path like "zlib-1.2.11/zlib.h".

