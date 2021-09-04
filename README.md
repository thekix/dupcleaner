# dupcleaner  
List and remove duplicated files  
  
This Python module allow find and remove duplicated files. It uses MD5 and SHA-1 algorithms to do it.  
  
I created this module to search the duplicated files, because I have multiple copies in my backups,...  
The module also includes code to make it an application, so you can use it directly.
  
## Usage (as application)  
The application has two modes:  
  
- Read mode, used by default. The application show the duplicated files.  
- Write mode. The application show the duplicated files and, for the duplicated files, it shows a menu to apply actions. Is possible select default folder for deletion, to allow `dupcleaner` auto-remove files in the same folder.
  
The `dupcleaner.py` application requires a list of folders to check if the files are duplicated. It includes help:  
  
```  
$ ./dupcleaner.py  
usage: dupcleaner.py [-h] [-r] [--write] [-m] [-l] [-v] [--sha1] [--md5] [--test]  
 <files or folders> [<files or folders> ...]
 ```  
  
The write mode (--write) includes a submenu. Look this example:  
  
```  
$ ./dupcleaner.py --write test C:\test-c D:\test-d  
Duplicated files found.  
Files with key [MD5:1586b558c4a1334b4a9a50f37694142d SHA-1:]:  
[1] C:\test-c\20190228_MG_7411_1.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:00 2021 Size: 574302  
[2] D:\test-d\20190228_MG_7411_2.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:13 2021 Size: 574302  
[1, 2, 'f1', 'f2'], n, A, q, ?. Option: ?  
 <number>: Delete file with index number
 f<number: Delete file with index and select it's directory to remove by default
 n: Do not remove any file
 A: Remove All files (WARNING, you will lost all copies!!)
 q: Quit!
[1] C:\test-c\20190228_MG_7411_1.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:00 2021 Size: 574302  
[2] D:\test-d\20190228_MG_7411_2.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:13 2021 Size: 574302  
[1, 2, 'f1', 'f2'], n, A, q, ?. Option:  
```  
  
The menu is offering these options:  
  
- 1: Delete file `C:\test-c\20190228_MG_7411_1.jpg`  
- 2: Delete file `D:\test-d\20190228_MG_7411_2.jpg`  
- f1: Delete file `C:\test-c\20190228_MG_7411_1.jpg` and include the folder `C:\test-c` as default folder for deletion *  
- f2: Delete file `D:\test-d\20190228_MG_7411_2.jpg` and include the folder `D:\test-d` as default folder for deletion *  
- n: Do not remove any files  
- A: Remove all files  
- q: Quit  
  
NOTE: If the folder is the same, `dupcleaner` removes all files in the folder, except one. One file is never removed.  
  
  
### Arguments:  
  
`dupcleaner` can use multiple Arguments:  
  
|Argument|Mandatory|Description|Notes|  
|---|---|---|---|  
|folders|Yes|List of folders, separated by spaces. If the folder includes spaces, use quotes||  
|-r|No|Search for files in directories Recursively||  
|-m|No|List files in machine readable format (using pipe as separator)|It disables the -l flag, used by default|  
|-l|No|Do not align the extra info (dates, name, size)|Info aligned by default|  
|-v|No|Verbose mode, list the files||  
|-md5|No|Uses MD5 algorithm to search duplicated|Used by default.|  
|-sha1|No|Uses SHA-1 algorithm to search duplicated||  
|--write|No|Enable write mode to delete the duplicated files||  
|--test|No|Using write mode, do not delete the files. Used for testing|   |  
  
### Examples - Read mode  
  
Then, you can list the duplicated files, for example in the `test` folder:  
  
```  
kix@bali MINGW64 /d/kix/src/dupcleaner (master)  
$ ls test  
002.jpg  003.jpg  004.jpg  005.jpg  006.jpg  20190228_MG_7411_1.jpg  20190228_MG_7411_2.jpg  
  
kix@bali MINGW64 /d/kix/src/dupcleaner (master)  
$ ./dupcleaner.py test  
Duplicated files found.  
Files with key [MD5:1586b558c4a1334b4a9a50f37694142d SHA-1:]:  
[1] D:\kix\src\test\20190228_MG_7411_1.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:00 2021 Size: 574302  
[2] D:\kix\src\test\20190228_MG_7411_2.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:13 2021 Size: 574302  
```  
  
List with output as machine-readable mode (like CSV):  
  
```  
$ ./dupcleaner.py -m test  
WARNING: Parameters machine_mode and list align used for output.  
* Using machine mode.  
Duplicated files found.  
MD5|SHA-1|File|Creation|Last Modification|Size  
1586b558c4a1334b4a9a50f37694142d||D:\kix\src\dupcleaner\test\20190228_MG_7411_1.jpg|Wed Aug 25 18:07:00 2021|Fri Aug 20 20:12:27 2021|574302  
1586b558c4a1334b4a9a50f37694142d||D:\kix\src\dupcleaner\test\20190228_MG_7411_2.jpg|Wed Aug 25 18:07:13 2021|Fri Aug 20 20:12:27 2021|574302  
```  
  
Uses MD5 and SHA-1 (both). Using machine-readable and disabling list mode:  
  
```  
$ ./dupcleaner.py -m -l --sha1 --md5 test  
Duplicated files found.  
MD5|SHA-1|File|Creation|Last Modification|Size  
1586b558c4a1334b4a9a50f37694142d|3bec96fd41a6e77522aede0467da6b0b4d340c6b|D:\kix\src\dupcleaner\test\20190228_MG_7411_1.jpg|Wed Aug 25 18:07:00 2021|Fri Aug 20 20:12:27 2021|574302  
1586b558c4a1334b4a9a50f37694142d|3bec96fd41a6e77522aede0467da6b0b4d340c6b|D:\kix\src\dupcleaner\test\20190228_MG_7411_2.jpg|Wed Aug 25 18:07:13 2021|Fri Aug 20 20:12:27 2021|574302  
```  
  
Using recursive mode. Now the folder is not the sub folder `test`, is the current folder (`.`):  
```  
$ ./dupcleaner.py -r .  
Duplicated files found.  
Files with key [MD5:7e9e456fce756442c66305587846759a SHA-1:]:  
[1] D:\kix\src\dupcleaner\.git\logs\HEAD                Created: Fri Sep  3 12:55:49 2021 Last Modification: Sat Aug 28 12:19:51 2021 Size: 2771  
[2] D:\kix\src\dupcleaner\.git\logs\refs\heads\master   Created: Fri Sep  3 12:55:49 2021 Last Modification: Sat Aug 28 12:19:51 2021 Size: 2771  
Files with key [MD5:1586b558c4a1334b4a9a50f37694142d SHA-1:]:  
[1] D:\kix\src\dupcleaner\test\20190228_MG_7411_1.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:00 2021 Size: 574302  
[2] D:\kix\src\dupcleaner\test\20190228_MG_7411_2.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:13 2021 Size: 574302  
```  
  
### Examples - Write mode  
  
Example of deletion in test mode. Files are not removed.  
```  
kix@bali MINGW64 /d/kix/src/dupcleaner (master)  
$ ls test/  
002.jpg  003.jpg  004.jpg  005.jpg  006.jpg  20190228_MG_7411_1.jpg  20190228_MG_7411_2.jpg  
  
kix@bali MINGW64 /d/kix/src/dupcleaner (master)  
$ ./dupcleaner.py --write --test test  
Duplicated files found.  
Files with key [MD5:1586b558c4a1334b4a9a50f37694142d SHA-1:]:  
[1] D:\kix\src\dupcleaner\test\20190228_MG_7411_1.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:00 2021 Size: 574302  
[2] D:\kix\src\dupcleaner\test\20190228_MG_7411_2.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:13 2021 Size: 574302  
[1, 2, 'f1', 'f2'], n, A, q, ?. Option: A  
SURE? (type "YES" to confirm or any key to cancel) YES  
File D:\kix\src\dupcleaner\test\20190228_MG_7411_1.jpg removed  
File D:\kix\src\dupcleaner\test\20190228_MG_7411_2.jpg removed  
  
kix@bali MINGW64 /d/kix/src/dupcleaner (master)  
$ ls test/  
002.jpg  003.jpg  004.jpg  005.jpg  006.jpg  20190228_MG_7411_1.jpg  20190228_MG_7411_2.jpg  
  
kix@bali MINGW64 /d/kix/src/dupcleaner (master)  
$  
```  
  
  
## Usage (as module)  
The `dupcleaner` class is initialized using these arguments:
  
```  
DupCleaner(folders, write_mode=False, recursive=True, test_mode=False, machine_mode=False, full_list_align=True, verbose=False, md5_sum=True, sha1_sum=False)  
```
Only the `folders` list is mandatory. An example of initialization could be:
```
cleaner = DupCleaner(['/home/user1/photos'])
```

The `dupcleaner` class includes these public methods:

```
get_duplicated(self)
  This function get the duplicated files. Store it in the self.checksums
  variable for this class and returns a copy of the list.

  :return: Copy of self.checksums with the duplicated files

print_duplicated(self)
  This function prints the duplicated files on the screen
  :return: Cancel by user flag. In this case, always is false.

remove_duplicated(self)
  This function removes the duplicated files (using a menu).

  :return: Cancel by user flag (True if canceled)
```
Full example using the console:
```
>>> from dupcleaner import DupCleaner
>>> cleaner = DupCleaner(['d:\\kix\\src\\dupcleaner\\test\\'])
>>> cleaner.get_duplicated()
{'1586b558c4a1334b4a9a50f37694142d_': ['d:\\kix\\src\\dupcleaner\\test\\20190228_MG_7411_1.jpg', 'd:\\kix\\src\\dupcleaner\\test\\20190228_MG_7411_2.jpg']}
>>> cleaner.print_duplicated()
Duplicated files found.
Files with key [MD5:1586b558c4a1334b4a9a50f37694142d SHA-1:]:
[1] d:\kix\src\dupcleaner\test\20190228_MG_7411_1.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:00 2021 Size: 574302
[2] d:\kix\src\dupcleaner\test\20190228_MG_7411_2.jpg   Created: Fri Aug 20 20:12:27 2021 Last Modification: Wed Aug 25 18:07:13 2021 Size: 574302
>>> cleaner.machine_mode = True
>>> cleaner.print_duplicated()
Duplicated files found.
MD5|SHA-1|File|Creation|Last Modification|Size
1586b558c4a1334b4a9a50f37694142d||d:\kix\src\dupcleaner\test\20190228_MG_7411_1.jpg|Wed Aug 25 18:07:00 2021|Fri Aug 20 20:12:27 2021|574302
1586b558c4a1334b4a9a50f37694142d||d:\kix\src\dupcleaner\test\20190228_MG_7411_2.jpg|Wed Aug 25 18:07:13 2021|Fri Aug 20 20:12:27 2021|574302
>>>
``` 
 
Example to list files:
```
cleaner = DupCleaner(['/home/user'])  
cleaner.get_duplicated()  
cleaner.print_duplicated()  
```
Example to remove files:  
```
cleaner = DupCleaner(['/home/user'], write_mode=True)  
cleaner.get_duplicated()
if cleaner.remove_duplicated():  
    print("Canceled by user.")
```

#### Extra functions
The module includes these extra functions:
```
dupcleaner_menu()
    This function provides a method to get from the user the arguments
    used by the class DupCleaner.

    :return: A tuple with these arguments:
      folders: List of folders o files to check
      rw: Boolean value to enable the write mode and delete files
      recursive: Boolean value to enable recursive mode and deep in folders
      test: When write mode is enabled, if this boolean argument is
            enabled files are not removed.
      machine_mode: Boolean value to get the list en machine readable mode,
                    using the pipe as separator.
      list_align: Boolean value to disable the output info alignment
      verbose: Verbose calculating the MD5 and SHA-1 checksums
      l_md5: Boolean value to calculate the checksum using MD5
      l_sha1: Boolean value to calculate the checksum using SHA-1

md5(file_name)
    Function to calculate the MD5 sum for a file
    :param file_name: File to get the MD5 sum
    :return: MD5 sum in hexadecimal

sha1(file_name)
    Function to calculate the SHA-1 sum for a file
    :param file_name: File to get the SHA1 sum
    :return: SHA-1 sum in hexadecimal
```
  
### Software Disclaimer  
  
There are inherent dangers in the use of any software available for download on  
the Internet, and we caution you to make sure that you completely understand  
the potential risks before downloading any of the software.  
  
The Software and code samples available on this website are provided "as is"  
without warranty of any kind, either express or implied. Use at your own risk.  
  
The use of the software and scripts downloaded on this site is done at your own  
discretion and risk and with agreement that you will be solely responsible for  
any damage to your computer system or loss of data that results from such  
activities. You are solely responsible for adequate protection and backup of  
the data and equipment used in connection with any of the software, and we will  
not be liable for any damages that you may suffer in connection with using,  
modifying or distributing any of this software. No advice or information,  
whether oral or written, obtained by you from us or from this website shall  
create any warranty for the software.  
  
We make no warranty that  
  
- the software will meet your requirements  
- the software will be uninterrupted, timely, secure or error-free  
- the results that may be obtained from the use of the software will b  
  effective, accurate or reliable  
- the quality of the software will meet your expectations  
- any errors in the software obtained from us will be corrected.  
  
The software, code sample and their documentation made available  
on this website:  
  
 - could include technical or other mistakes, inaccuracies or typographical  
   errors. We may make changes to the software or documentation made available  
   on its website at any time without prior-notice.
 - may be out of date, and we make no commitment to update such materials.  
  
We assume no responsibility for errors or omissions in the software or  
documentation available from its website.  
  
In no event shall we be liable to you or any third parties for any special,  
punitive, incidental, indirect or consequential damages of any kind, or any  
damages whatsoever, including, without limitation, those resulting from loss  
of use, data or profits, and on any theory of liability, arising out of or in  
connection with the use of this software.