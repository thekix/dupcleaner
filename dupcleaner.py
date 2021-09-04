#!/usr/bin/env python

"""
Script to remove duplicated files, using MD5 and SHA-1 checksum.

Rodolfo García Peñas (kix) <kix@kix.es>
https://www.kix.es/
https://www.github.com/thekix/dupcleaner
"""
import hashlib
import argparse
import sys
import io
import time
import os
from os.path import isfile, isdir, abspath, islink, \
    getmtime, getctime, getsize, dirname


def md5(file_name):
    """
    Function to calculate the MD5 sum for a file
    :param file_name: File to get the MD5 sum
    :return: MD5 sum in hexadecimal
    """
    block_size = 8192

    with open(file_name, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(block_size):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def sha1(file_name):
    """
    Function to calculate the SHA-1 sum for a file
    :param file_name: File to get the SHA1 sum
    :return: SHA-1 sum in hexadecimal
    """
    block_size = 8192

    with open(file_name, "rb") as f:
        file_hash = hashlib.sha1()
        while chunk := f.read(block_size):
            file_hash.update(chunk)

    return file_hash.hexdigest()


def dupcleaner_menu():
    """
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
    """
    parser = argparse.ArgumentParser(description='Check for duplicated files.')
    parser.add_argument('folders', metavar='<files or folders>', type=str,
                        nargs='+', help='list of file and folders to check.')
    parser.add_argument('-r', action='store_true',
                        help='Recursive. Deep in the directories.')
    parser.add_argument('--write', action='store_true',
                        help='List duplicated files. Do not remove.')
    parser.add_argument('-m', action='store_true',
                        help='List duplicated in machine readable mode. '
                             'Only for list mode (default).')
    parser.add_argument('-l', action='store_true',
                        help='Do not align the extra info.')
    parser.add_argument('-v', action='store_true',
                        help='Verbose calculating the MD5 and SHA-1 checksums.')
    parser.add_argument('--sha1', action='store_true',
                        help='Use SHA-1 to calculate the checksum.')
    parser.add_argument('--md5', action='store_true',
                        help='Use MD5 to calculate the checksum (default).')
    parser.add_argument('--test', action='store_true',
                        help='Do not remove files, only test the process. '
                             'Only for write mode.')

    arguments = parser.parse_args()

    # Set the values in the class
    recursive = True if arguments.r else False
    l_sha1 = True if arguments.sha1 else False
    l_md5 = True if arguments.md5 else False
    test = True if arguments.test else False
    rw = True if arguments.write else False
    machine_mode = True if arguments.m else False
    list_align = False if arguments.l else True
    verbose = True if arguments.v else False

    folders = arguments.folders

    return folders, rw, recursive, test, machine_mode, list_align, verbose, l_md5, l_sha1


class DupCleaner:
    def __init__(self, folders, write_mode=False, recursive=True,
                 test_mode=False, machine_mode=False, full_list_align=True,
                 verbose=False, md5_sum=True, sha1_sum=False):
        """
        Init function for DupCleaner. Set the parameters to run the class.

        The "folder" argument is mandatory.

        :param folders: List of folders o files to check
        :param write_mode: Boolean value to enable the write mode and delete
               files
        :param recursive: Boolean value to enable recursive mode and deep in
               folders
        :param test_mode: When write mode is enabled, if this boolean argument
               is enabled
               files are not removed.
        :param machine_mode: Boolean value to get the list en machine readable
               mode, using the pipe as separator.
        :param full_list_align: Boolean value to disable the output info
               alignment
        :param md5_sum: Boolean value to calculate the checksum using MD5
        :param sha1_sum: Boolean value to calculate the checksum using SHA-1
        """
        self.in_folders = folders
        self.write_mode = write_mode
        self.recursive = recursive
        self.test_mode = test_mode
        self.machine_mode = machine_mode
        self.md5 = md5_sum
        self.sha1 = sha1_sum
        self.full_list_align = full_list_align
        self.verbose = verbose

        # Set the default values
        if not self.md5 and not self.sha1:
            self.md5 = True

        # Show some warnings
        if not self.write_mode and self.test_mode:
            print("WARNING: Parameter test_mode "
                  "does not have effect in list mode.")

        if self.write_mode and self.machine_mode:
            print("WARNING: Parameter machine_mode "
                  "does not have effect in write mode.")
            self.machine_mode = False

        if self.machine_mode and self.full_list_align:
            print("WARNING: Parameters machine_mode "
                  "and list align used for output.")
            print("* Using machine mode.")
            self.full_list_align = False

        # Set global variables
        self.files = {}
        self.checksums = {}
        self.def_action_folder = {}

    def __get_files__(self, files):
        """
        This function find the all files in the files and folders included
        in the "files" argument and store the value in the "self.files"
        dictionary.

        :param files: List of files and folders
        :return: None
        """
        for file_name in os.listdir(files):
            # Do not include symbolic links files
            full_name = files + file_name
            if isfile(full_name) and not islink(full_name):
                self.files[full_name] = self.files.get(full_name, 0) + 1
            elif isdir(full_name):
                if self.recursive:
                    self.__get_files__(full_name + os.sep)
                else:
                    pass
            else:
                print("File {} not included".format(full_name))

    def __get_full_path__(self):
        """
        This function sets the full path for the input folders.

        For example, for a file:
          - file.txt -> /home/kix/file.txt
        For a folder:
          - . -> /home/kix/

        :return: None
        """
        lst_ret = []
        for l_files in self.in_folders:
            if isfile(l_files):
                lst_ret.append(abspath(l_files))
            elif isdir(l_files):
                lst_ret.append(abspath(l_files) + os.sep)
            else:
                print("File {} not found".format(l_files))

            self.in_folders = lst_ret

    def __get_files_checksums__(self):
        """
        This function creates a dictionary of checksums
        using the MD5 and SHA-1 algorithms
        It stores the results in the dictionary self.checksums
        using the MD5_SHA-1 as key and a list of files with
        these checksums as value.

        :return: None
        """
        for k, _ in self.files.items():
            l_md5 = md5(k) if self.md5 else ''
            l_sha1 = sha1(k) if self.sha1 else ''
            l_new_key = l_md5 + '_' + l_sha1
            if self.checksums.get(l_new_key) is None:
                self.checksums[l_new_key] = [k]
            else:
                self.checksums[l_new_key].append(k)

            if self.verbose:
                print("Processing file. MD5:{} SHA-1:{} Name: {}".format(
                    l_md5, l_sha1, k))

    def __remove_not_dups__(self):
        """
        Remove the not duplicated files in the self.checksums dictionary.

        :return: None
        """
        new_dups = {}
        for k, v in self.checksums.items():
            if len(v) > 1:
                new_dups[k] = v

        self.checksums = new_dups

    def __print_output_header__(self, l_md5, l_sha1):
        """
        Print the output header for a set of files with the same
        MD5 / SHA-1 checksum.

        :param l_md5: MD5 checksum for the set of files.
        :param l_sha1: SHA-1 checksum for the set of files.
        :return: None
        """
        if self.machine_mode:
            print("MD5|SHA-1|File|Creation|Last Modification|Size")
        else:
            print("Files with key [MD5:{} SHA-1:{}]:".format(l_md5, l_sha1))

    def __get_max_file_name_len__(self, lst_files):
        """
        Return the longest filename in the lst_files list.

        :param lst_files: List of files.
        :return: Numeric value of the longest file name
        """
        if self.machine_mode:
            return 0

        txt_len = 0
        for l_file in lst_files:
            if len(l_file) > txt_len:
                txt_len = len(l_file)

        return txt_len

    def __get_max_file_name_len_full__(self):
        """
        Return the longest filename for all files in the values
        of the self.checksums dictionary.

        :return: Numeric value of the longest file name
        """
        if self.machine_mode:
            return 0

        txt_len = 0
        for _, v in self.checksums.items():
            for l_file in v:
                f_len = len(l_file)
                if f_len > txt_len:
                    txt_len = f_len

        return txt_len

    def __print_list_files__(self, l_md5, l_sha1, lst_files, max_file_name_len):
        """
        This function prints the list of files included in the list "lst_files"
        with the same MD5/SHA-1 checksum.

        The output will align the extra data (Date of creation, last
        modification date and the size) using the max_file_name_len
        argument for a global (all files) alignment or only for this
        set (list) if max_file_name_len is zero.

        :param l_md5: MD5 for the list of files
        :param l_sha1: SHA-1 for the list of files
        :param lst_files: List of files to print
        :param max_file_name_len: Max file name length or zero
        :return: None
        """
        if not max_file_name_len and not self.machine_mode:
            max_file_name_len = self.__get_max_file_name_len__(lst_files)

        for idx, l_file in enumerate(lst_files):
            l_size = getsize(l_file)
            l_last_mod = time.ctime(getmtime(l_file))
            l_creation = time.ctime(getctime(l_file))
            if not self.machine_mode:
                print("[{}] ".format(idx + 1) +
                      ("{:" + str(max_file_name_len + 2) + "} ").format(l_file)
                      + "Created: {} Last Modification: {} Size: {}".format(
                    l_last_mod, l_creation, l_size))
            else:
                print('{}|{}|{}|{}|{}|{}'.format(
                    l_md5, l_sha1, l_file, l_creation, l_last_mod, l_size))

    @staticmethod
    def __print_help__():
        """
        Prints the help for the actions menu

        :return: None
        """
        print("  <number>: Delete file with index number")
        print("  f<number: Delete file with index and select it's "
              "directory to remove by default")
        print("         n: Do not remove any file")
        print("         A: Remove All files (WARNING, "
              "you will lost all copies!!)")
        print("         q: Quit!")

    @staticmethod
    def __print_action_menu__(lst_files):
        """
        Print the action menu for the list of files "lst_files".

        The user will select the desired option:
         - A number: Number of the file in the list
         - f + number: Number of the file in the list and select the
           directory as default directory for deletion.
         - "A": All files
         - "q": Quit
         - "?": Help

        :param lst_files: List of files to apply the actions
        :return: The selected option.
        """
        lst_options = []
        lst_folder_options = []
        for idx, _ in enumerate(lst_files):
            lst_options.append(idx + 1)
            lst_folder_options.append('f{}'.format(idx + 1))

        lst_options.extend(lst_folder_options)

        opc = input('{}, n, A, q, ?. Option: '.format(lst_options))
        return opc

    def __delete_file__(self, l_file):
        """
        This function is used to remove a file. If test-mode
        is set, the file is not deleted.

        :param l_file: File to be deleted.
        :return: True if the file is removed. False if it fails.
        """
        if self.test_mode:
            print('File {} removed'.format(l_file))
            return True

        try:
            os.remove(l_file)
            print('File {} removed'.format(l_file))
            return True
        except OSError as e:
            print("Error removing file: {}".format(e))
            return False

    def __take_auto_action__(self, lst_files):
        """
        This function apply auto deletion for the list of files.
        This function checks if the files are in the default action
        folders to delete their files.

        If all folders for all files are in the default action list,
        the function also checks that at least one file is not deleted.

        :param lst_files: List of files to delete.
        :return: Remaining files
        """
        ret_list = []
        changed = False

        # Avoid remove all files, at least hold one.
        max_deletion = len(lst_files) - 1
        deleted_files = 0

        for l_file in lst_files:
            l_path = dirname(l_file)
            if self.def_action_folder.get(l_path) \
                    and deleted_files < max_deletion:
                print("Removing file automatically: {}".format(l_file))
                removed = self.__delete_file__(l_file)
                if removed:
                    deleted_files += 1
                    changed = True
            else:
                ret_list.append(l_file)

        return ret_list, changed

    def __take_action__(self, l_md5, l_sha1, lst_files, max_length):
        """
        This function takes actions (deletion) about the "lst_files" list.

        :param l_md5: MD5 checksum for the "lst_files" list
        :param l_sha1: SHA-1 checksum for the "lst_files" list
        :param lst_files: List of files to apply actions.
        :param max_length: Output max file name length
        :return: Tuple, three elements:
                 * Remaining files list,
                 * More action needed boolean flag,
                 * Quit selected flag.
        """
        # Apply automatic deletion
        lst_files, changed = self.__take_auto_action__(lst_files)

        # For the remaining files, get the options for the menu
        file_valid_options = [str(x + 1) for x, _ in enumerate(lst_files)]
        folder_valid_options = ['f' + str(x+1) for x, _ in enumerate(lst_files)]
        if changed:
            self.__print_list_files__(l_md5, l_sha1, lst_files, max_length)

        while 1:
            # Only one file remaining, exit
            if len(lst_files) < 2:
                return lst_files, False, False

            # Print the action menu and get the selected option
            opc = self.__print_action_menu__(lst_files)

            # Option is "No delete any files"
            if opc.lower() == 'n':
                # Return the remaining list, do not continue
                return lst_files, False, False
            elif opc == '?':
                # Help request. Print the help, print the file list, ask again.
                self.__print_help__()
                self.__print_list_files__(
                    l_md5, l_sha1, lst_files, max_length)
            elif opc.lower() == 'q':
                # Quit selected!
                return lst_files, False, True
            elif opc in file_valid_options:
                # File option selected. Delete the file
                removed = self.__delete_file__(lst_files[int(opc) - 1])
                if removed:
                    # Remove the file from the list
                    lst_files.pop(int(opc) - 1)
                # Print the new list. If only one file, will exist in next loop
                if len(lst_files) > 1:
                    self.__print_list_files__(
                        l_md5, l_sha1, lst_files, max_length)
            elif opc in folder_valid_options:
                # File option selected and folder selected by default
                # Get the file to delete
                idx = int(opc.replace('f', '')) - 1
                # Get the folder name and include it in the default folder list
                folder = dirname(lst_files[idx])
                self.def_action_folder[folder] = 1
                # Delete the file, remove it from the list
                removed = self.__delete_file__(lst_files[idx])
                if removed:
                    lst_files.pop(idx)
                    # Print the new list. If only one, will exist in next loop
                if len(lst_files) > 1:
                    self.__print_list_files__(
                        l_md5, l_sha1, lst_files, max_length)
            elif opc == 'A':
                # Remove all files
                re_check = input('SURE? (type "YES" to confirm or '
                                 'any key to cancel) ')
                if re_check == 'YES':
                    new_lst_files = []
                    for lf in lst_files:
                        removed = self.__delete_file__(lf)
                        if not removed:
                            new_lst_files.append(lf)
                    lst_files = new_lst_files
            else:
                print("No valid option")

    def __process_duplicated__(self, write_mode=False):
        """
        Function to process the duplicated files, in read only (for printing)
        or write mode (for deletion)

        :param write_mode: Flag to write mode, False by default.
        :return: Cancel by user flag (True if canceled)
        """
        if not len(self.checksums):
            return False

        # Get the filename max length to align the output
        max_length = self.__get_max_file_name_len_full__() if \
            self.full_list_align else 0

        print("Duplicated files found.")
        for k, v in self.checksums.items():
            l_md5 = k.split('_')[0]
            l_sha1 = k.split('_')[1]
            self.__print_output_header__(l_md5, l_sha1)

            lst_work = v.copy()
            again = True
            while again:
                self.__print_list_files__(l_md5, l_sha1, lst_work, max_length)
                if write_mode:
                    lst_files, again, quit_flag = self.__take_action__(
                        l_md5, l_sha1, lst_work, max_length)
                    self.checksums[k] = lst_files
                    if quit_flag:
                        return True
                else:
                    again = False

    def print_duplicated(self):
        """
        This function prints the duplicated files on the screen
        :return: Cancel by user flag. In this case, always is false.
        """
        return self.__process_duplicated__()

    def remove_duplicated(self):
        """
        This function removes the duplicated files (using a menu).

        :return: Cancel by user flag (True if canceled)
        """
        l_mode = self.write_mode
        return self.__process_duplicated__(l_mode)

    def get_duplicated(self):
        """
        This function get the duplicated files. Store it in the self.checksums
        variable for this class and returns a copy of the list.

        :return: Copy of self.checksums with the duplicated files
        """
        # Set the base folder for the input files/folders
        self.__get_full_path__()
        # Get the list of files (all)
        for folder in self.in_folders:
            self.__get_files__(folder)
        # Get the checksums for the files (all)
        self.__get_files_checksums__()
        # Remove files without duplicates
        self.__remove_not_dups__()
        # Return the duplicated files
        return self.checksums.copy()


# Main function example
if __name__ == '__main__':
    # Avoid problems with filenames and console encoding
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

    ret = dupcleaner_menu()
    cleaner = DupCleaner(*ret)
    cleaner.get_duplicated()
    # cleaner.print_duplicated()
    if cleaner.remove_duplicated():
        print("Canceled by user.")
