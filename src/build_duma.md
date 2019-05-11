
# Building Duma in 2019

- Use cvs, because the latest "published release" on sourceforge doesn't have the latest revisions for building in modern gcc
- Run `cvs.exe -z3 -d:pserver:anonymous@duma.cvs.sourceforge.net:/cvsroot/duma co -P duma`
- Download [this patch](https://github.com/crosstool-ng/crosstool-ng/blob/master/packages/duma/2_5_15/0002-cpp11-new-operator.patch) and save it to newpatch.patch in the duma directory
- If in Windows, open a msys2 shell and put gcc binaries in the PATH (as described on the [README.md](../README.md) page), otherwise open a terminal
- `cd` to the duma directory
- Run `patch < newpatch.patch` to apply the patch we downloaded
- If in Windows, run `mingw32-make OSTYPE=msys`. Otherwise run configure and make.
- Get libduma.a and copy it to the directory `/path/to/sfarkxtc-windows/src/duma`
- `cd` to `/path/to/sfarkxtc-windows/src`
- Running `make USE_DUMA=1` should now produce a sfarkxtc with Duma's memory protections enabled.

## Confirming that Duma is active
I wrote an intentional bounds violation, added to `Decode()` in `skflCoding.cpp` to test Duma:

```
BLOCK_DATA	*buffer = (BLOCK_DATA *)malloc(sizeof(BLOCK_DATA));
char *asChars = (char *)buffer;
printf("please type y to cause an invalid memory write or n to continue\n");
// I don't think any current form of static analysis or inference or compiler trimming of undefined behavior will detect this.
// Without a line taking some form of arbitrary input, a clever-enough compiler 
// might skip over the invalid write, after deducing that it is invalid behavior
int getEntropy = getc(stdin);
int shouldDoInvalidWrite = (getEntropy == 'n') ? 0 : 1;
int index = sizeof(BLOCK_DATA) * shouldDoInvalidWrite;
printf("writing to index %d when max index is %d\n", (int)index, (int)(sizeof(BLOCK_DATA)-1));
asChars[index] = 23;
```

Without Duma, the program continued silently. With Duma enabled, this successfully trigger a failure and exited! The same occurred for writing to `asChars[-1]`, just as expected.

[Back](../README.md)
