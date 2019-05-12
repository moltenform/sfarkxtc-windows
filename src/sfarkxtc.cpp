// Basic sfArk decompressor for Mac
// Copyright 2002 Andy Inman
// Contact via: http://netgenius.co.uk or http://melodymachine.com

// Forked for win32 by Ben Fisher (moltenform) in 2019,
// https://github.com/moltenform/sfarkxtc-windows

// This file is part of sfArkLib.
//
// sfArkLib is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// sfArkLib is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with sfArkLib.  If not, see <http://www.gnu.org/licenses/>.

//  based on SDL_Test

//  Reads an existing .sfArk file and writes an sf2 file using standard file i/o
//	Return 0 if successful, 1 if some error occurred.
//  Info and error messages are printed to stdout

//	Initial version,	andyi, 14-Sep-2002

const char	*ThisProg = "sfarkxtc";
const char	*ThisVersion = "3.0-snapshot";	// Version of program

// Standard includes...
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "sfArkLib.h"

// Application-supplied functions...
void sfkl_msg(const char *MessageText, int Flags);				// Message display function
void sfkl_UpdateProgress(int ProgressPercent);						// Progress indication
bool sfkl_GetLicenseAgreement(const char *LicenseText);	// Display/confirm license
void sfkl_DisplayNotes(const char *NotesFileName, const char *OutFileName);				// Display notes text file
bool quiet = false;

int ReportError(long error)
{
	// Display an error message, return 0 if there was no error else 1
	const char *msg;

	switch (error)
	{
		case SFARKLIB_SUCCESS:
			msg = "Successful";
			break;
		case SFARKLIB_ERR_INIT:
			msg = "Failed initialisation";
			break;
		case SFARKLIB_ERR_MALLOC:
			msg = "Memory allocation error";
			break;
		case SFARKLIB_ERR_SIGNATURE:
			msg = "Signature not found (file is corrupt or is not a sfArk file)";
			break;
		case SFARKLIB_ERR_HEADERCHECK:
			msg = "Header check fails (file is corrupt)";
			break;
		case SFARKLIB_ERR_INCOMPATIBLE:
			msg = "File was created by incompatible sfArk version (not 2.x)";
			break;
		case SFARKLIB_ERR_UNSUPPORTED:
			msg = "Unsupported feature was used";
			break;
		case SFARKLIB_ERR_CORRUPT:
			msg = "Invalid compressed data (file is corrupt)";
			break;
		case SFARKLIB_ERR_FILECHECK:
			msg = "Checksum failed (file is corrupt)";
			break;
		case SFARKLIB_ERR_FILEIO:
			msg = "File i/o failed";
			break;
		case SFARKLIB_ERR_OTHER:
			msg = "Other error";
			break;
		default:
			msg = "Undefined error";
	}
	printf("Result:	%s  errorcode %ld\n", msg, -error);

	if(error != SFARKLIB_SUCCESS)
	{
		printf("*** FAILED ***\n");
		return 1;
	}
	else
	{
		return 0;
	}
}

bool StringEndsWith(const char* s1, const char*s2)
{
	size_t len1 = strlen(s1);
	size_t len2 = strlen(s2);
	if (len2 > len1)
	{
		return false;
	}
	else
	{
		return strcmp(s1 + len1 - len2, s2) == 0;
	}
}

bool StringEndsWithCaseInsensitive(const char *s, const char *lowerCaseSuffix)
{
	char *sLower = strdup(s);
	for (int i = 0, len = strlen(sLower); i < len; i++)
	{
		sLower[i] = tolower(sLower[i]);
	}

	bool ret = StringEndsWith(sLower, lowerCaseSuffix);
	free(sLower);
	return ret;
}

static_assert(sizeof(unsigned long) == 4, 
	"\nThis type of x64 build is untested!\n"
	"We might fail to correctly extract from sfark files\n"
	"See https://github.com/raboof/sfArkLib/issues/12\n"
	"or\n"
	"http://linux-audio.4202.n7.nabble.com/sfArk-for-Linux-git-repo-access-tp93130p93161.html\n"
	"for a potential patch+fix");

// ============================ m a i n ==============================================

int main(int argc, char** argv)
{
	// Print welcome message...

	printf("========================================================================\n");
	printf("%s %s ", ThisProg, ThisVersion);
	printf("(using sfArkLib version: %d)\n", sfkl_GetVersion());
	printf("copyright (c) 1998-2002 melodymachine.com, distributed under the GNU GPL\n");
	printf("========================================================================\n");

	// Open input and output files...

	char *InFileName = argv[1];
	char *OutFileName = NULL;
	// usage
	if (argc < 2)
	{
		printf("Specify input and output files on the command line, i.e:\n");
		printf("%s <InputFilename> [OutputFilename] [--quiet]\n", ThisProg);
		return 1;
	}

	if (argc >= 3)
	{
		OutFileName = argv[2];
		printf("Uncompressing %s to %s...\n", InFileName, OutFileName);
	}
	
	if (argc >= 4 && strcmp("--quiet", argv[3]) == 0)
	{
		quiet = true;
	}
	
	if (!StringEndsWithCaseInsensitive(InFileName, ".sfark"))
	{
		char c;
		printf("Input file does not end with .sfArk. Are you sure you want to continue? (Y/N)");
		c = getc(stdin);
		if (!(c == 'y' || c == 'Y'))
		{
			return 0;
		}
	}

	// Uncompress the file...
	long StartTime = clock();
	int err = sfkl_Decode(InFileName, OutFileName);	//call decompression, report & return
	long TimeTaken = 1000 * (clock() - StartTime) / CLOCKS_PER_SEC;
	
	if (!quiet) {
		printf("cpu time taken %ld ms\n", TimeTaken);
	}

	return ReportError(err);
}

// ============================================================================================
void sfkl_msg(const char *MessageText, int Flags)
{
	if (Flags & SFARKLIB_MSG_PopUp)	printf("*** ");
	printf("%s\n", MessageText);
}

// ============================================================================================
void sfkl_UpdateProgress(int ProgressPercent)
{
	if (!quiet)
	{
		printf("\r");
		printf("Progress: %d%%", ProgressPercent);
		fflush(stdout);
		if (ProgressPercent == 100)  printf("\n");
	}
}

// ==========================================================================================
// Display/confirm license
bool sfkl_GetLicenseAgreement(const char *LicenseText, const char *OutFileName)
{
	if (quiet)
	{
		printf("\nLicense written to %s\n", OutFileName ? OutFileName : "");
		return true;
	}
	else
	{
		char c;
		printf("%s\n\nDo you agree to the above terms? (Y/N) ", LicenseText);
		c = getc(stdin);
		while (c != 'y' && c != 'Y' && c != 'n' &&  c != 'N')
		{
			printf("\nPlease answer Y or N and press return: ");
			c = getc(stdin);
		}
		if (c == 'y' || c == 'Y')
			return true;
		else
			return false;
	}
}

// ============================================================================================
void sfkl_DisplayNotes(const char *NotesFilePath, const char* /* OutFileName */)				// Display notes text file
{
	printf("Notes text file extracted to: %s\n ", NotesFilePath);
}

// =====================================================================================
