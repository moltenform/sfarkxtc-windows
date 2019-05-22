#!/usr/bin/env python3

# test_sfarkxtc.py
# Ben Fisher, 2019

import sys
import os
import hashlib
import time
sys.path.append('bn_python_common.zip')
from bn_python_common import *

# for 9 large soundfonts, average of 5 runs:
# with Duma disabled, sfark compression 2, not-hardened: 13.5 seconds wall time
# with Duma enabled, sfark compression 2, not-hardened: 14.9 seconds wall time
# with Duma enabled, sfark compression 2, all hardened flags on: 15.0 seconds wall time

originals = r'./originals'
testdir = r'./sfarks'
isUnix = sys.platform != 'win32'
sfarkxtc_binary = r'../sfarkxtc_out' if isUnix else r'../sfarkxtc_out.exe'
sfarkxtc_shared = [] if isUnix else ['zlib1.dll' , 'libssp-0.dll']

# in case you're running the original sfarkxtc, which needs a call to chdir
needToChdir = False

originals = os.path.abspath(originals)
testdir = os.path.abspath(testdir)
sfarkxtc_binary = os.path.abspath(sfarkxtc_binary)

def getActualChecksums():
    actualChecksums = {}
    for f, short in files.listfiles(originals):
        actualChecksums[short] = hash(f)
    
    licenseFile = files.join(testdir, 'alicense.txt')
    actualChecksums[files.getname(licenseFile)] = hash(licenseFile)
    return actualChecksums

def hash(s):
    if s.endswith('.txt'):
        # normalize newline characters
        hasher = hashlib.md5()
        with open(s, 'rb') as f:
            content = f.read()
        content = content.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
        hasher.update(content)
        return hasher.hexdigest()
    else:
        return files.computeHash(s, 'md5')

def runSfark(f):
    import os
    a, b = os.path.splitext(files.getname(f))
    if not b.lower().endswith('.sfark'):
        trace('found a leftover file', f)
        return
    wantOutname = a + '__out__.sf2'
    assertTrue(files.exists(sfarkxtc_binary), 'binary not found', sfarkxtc_binary)
    if needToChdir:
        os.chdir(files.getparent(f))
        fIn = files.getname(f)
        fOut = wantOutname
    else:
        fIn = f
        fOut = files.join(files.getparent(f), wantOutname)
    trace(fIn, fOut)
    args = [sfarkxtc_binary, fIn, fOut, '--quiet']
    files.run(args)

def withNewExt(s, newext):
    a, b = os.path.splitext(s)
    return a + newext

def goDir(d, actualChecksums):
    trace('checking directory:', files.getname(d))
    shouldContainLicense = not '0license' in files.getname(d)
    shouldContainNotes = not '0notes' in files.getname(d)
    
    for f, short in files.listfiles(d):
        if not short.lower().endswith('.sfark') and not short.endswith('.dll'):
            warn('about to delete temporary file ' + f + ' ok?')
            files.delete(f)
    prevItemsInDir = {short:True for f, short in files.listfiles(d)}
    workToDo = [(f, short) for f, short in files.listfiles(d)]
    
    for f, short in workToDo:
        if short.endswith('.dll'): continue
        assertTrue(f.endswith('.sfArk'), f)
        runSfark(f)
        nowItemsInDir = {short:True for f, short in files.listfiles(d)}
        newItems = {k:v for k,v in nowItemsInDir.items() if k not in prevItemsInDir}
        expectCountNewItems = 1 + (1 if shouldContainLicense else 0) + (1 if shouldContainNotes else 0)
        assertEq(expectCountNewItems, len(newItems), newItems)
        
        expectSf2 = withNewExt(f, '__out__.sf2')
        trace('checking hash for', expectSf2)
        assertTrue(files.getname(expectSf2) in newItems, expectSf2, newItems)
        nameToCompare = files.getname(expectSf2).replace('__out__', '')
        assertTrue(files.getname(nameToCompare) in actualChecksums, expectSf2, actualChecksums)
        trace(hash(expectSf2), actualChecksums[nameToCompare])
        assertEq(hash(expectSf2), actualChecksums[nameToCompare], f)
        files.deletesure(expectSf2)
        
        if shouldContainNotes:
            expectNotes = withNewExt(f, '__out__.txt')
            trace('checking hash for', expectNotes)
            assertTrue(files.getname(expectNotes) in newItems, expectNotes, newItems)
            nameToCompare = files.getname(expectNotes).replace('__out__', '')
            assertTrue(files.getname(nameToCompare) in actualChecksums, expectNotes, actualChecksums)
            trace(hash(expectNotes), actualChecksums[nameToCompare])
            assertEq(hash(expectNotes), actualChecksums[nameToCompare], f)
            files.deletesure(expectNotes)
            
        if shouldContainLicense:
            expectLicense = withNewExt(f, '__out__.license.txt')
            trace('checking hash for', expectLicense)
            assertTrue(files.getname(expectLicense) in newItems, expectLicense, newItems)
            assertTrue('alicense.txt' in actualChecksums, expectLicense, actualChecksums)
            trace(hash(expectLicense), actualChecksums[files.getname('alicense.txt')])
            assertEq(hash(expectLicense), actualChecksums[files.getname('alicense.txt')], f)
            files.deletesure(expectLicense)

def go():
    actualChecksums = getActualChecksums()
    start = time.time()
    
    for f, short in files.listdirs(testdir):


        for dll in sfarkxtc_shared:
            dllsrc = files.join(files.getparent(sfarkxtc_binary), dll)
            if not files.exists(dllsrc):
                warn('file not found: ' + dllsrc)
            dlldest = files.join(f, dll)
            trace('copying dependency', dllsrc, dlldest)
            files.copy(dllsrc, dlldest, True)
            
        goDir(f, actualChecksums)
    
    end = time.time()
    trace('wall-clock time taken, in seconds:', end - start)

if __name__=='__main__':
    go()

