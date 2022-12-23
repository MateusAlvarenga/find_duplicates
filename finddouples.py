from imagededup.methods import PHash
import os
from PIL import Image
from friendly_arguments.named import get_params_sys_args
from friendly_arguments.named import get_params_sys_args

# Make a function call, passing as an argument a list of strings,
# with the prefix '-' or '--' and the suffix '='. example '--arg1=' or '-arg1='
my_args: dict = get_params_sys_args(['-d='])

# validate your arguments as you wish
try:
    the_path = my_args['-d=']
except KeyError:
    raise ValueError('argumets -d= empty')


def get_files_to_remove(duplicates: dict[str, list]) -> list:
    """
    Get a list of files to remove.

    Args:
        duplicates: A dictionary with file name as key and a list of duplicate file names as value.

    Returns:
        A list of files that should be removed.
    """
    # iterate over dict_ret keys, get value for the key and delete the dict keys that are in the value list
    files_to_remove = set()

    for k, v in duplicates.items():
        tmp = [
            i[0] if isinstance(i, tuple) else i for i in v
        ]  # handle tuples (image_id, score)

        if k not in files_to_remove:
            files_to_remove.update(tmp)

    return list(files_to_remove)


def delete_file(path):
    os.remove(path)


if __name__ == '__main__':

    phasher = PHash()

    # Generate encodings for all images in an image directory
    encodings = phasher.encode_images(image_dir=the_path)

    # Find duplicates using the generated encodings
    duplicates = phasher.find_duplicates(encoding_map=encodings)

    files_to_remove = get_files_to_remove(duplicates)

    for file in files_to_remove:
        print("Deleting: " + file)
        delete_file(the_path + file)
