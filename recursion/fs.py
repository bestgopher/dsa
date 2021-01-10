import os


def disk_usage(path):
    """Return the number of bytes used by a file/folder and any descendents."""

    total = os.path.getsize(path)  # account for direct usage
    if os.path.isdir(path):  # if this is a directory
        for filename in os.listdir(path):  # the for each child
            child_path = os.path.join(path, filename)  # compose full path to child
            total += disk_usage(child_path)  # add child's usage to total
    print("{0:<7}".format(total), path)
    return total
