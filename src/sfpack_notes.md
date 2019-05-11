
## sfpack vs sfark

- sfpack and sfark were rival compression formats for sf2 soundfonts
- sfpack is "copyright © 1999 Megota Software"
- sfark is "copyright © 1998-2000 MelodyMachine.com"

## sfpack 

- could not find any open-source decompression code
- closed-source exe is available x86 only, it does work in windows 10, but no guarentee for future versions of windows
- considered it briefly because of j\_e\_f\_f\_g's claims about the fragility of sfark, but the claims have been disputed
- no clear way to automate sfpack:
    - the documentation mentions a COM object, but
    - the only files are SFPACK.EXE (not a com object, no DllRegisterServer function)
    - and SFPSHLEX.DLL (is com object, has DllRegisterServer, but I couldn't see any useful methods)
    - I registered SFPSHLEX.DLL via windows\wow64\regsvr32 in an elevated cmd.exe
    - then made a visual studio C# project, add reference, COM object
    - SFPSHLEX was in the list, but adding it showed no useful methods
    - I then used the Oleview.exe tool (File menu, click View TypeLib) to inspect SFPSHLEX.DLL
    - it showed dllgetclassobject, so it's definitely a com object
    - interestingly, you can use midl.exe to this "type lib" [into a .h header](https://stackoverflow.com/questions/4990045/how-to-generate-type-library-from-unmanaged-com-dll)
    - but again it showed IShellExt and no useful methods
    - I could probably figure out how to call into the shell extension, maybe after observing it functioning in a win xp vm, but would require some effort
- you can pass a command-line object "sfpack myfile.sfpack"
    - but that just adds it to a list, doesn't even run extract
- at this point the best bet is to extract sfpack files manually, in Wine if necessary
- if I really need automation, use Launchorz or equivalently pywinauto

[Back](../README.md)

