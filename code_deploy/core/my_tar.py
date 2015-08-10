#!/usr/bin/env python
# coding:utf-8

import tarfile
import os
import commands


def get_tar(dirname, dst_dir):
    try:
        tar_dirname = os.path.basename(dirname)
        dst_filename = tar_dirname + ".tar.gz"
        dst_path = os.path.join(dst_dir, dst_filename)
        out = tarfile.TarFile.open(dst_path, "w:gz")
        out.add(dirname, tar_dirname)
        out.close()
        status = 0
        return status, dst_filename
    except:
        status = -1
        dst_filename = None
        return status, dst_filename

# if __name__ == "__main__":
#     get_tar("/Users/gladiator/Documents/workspace/my_scripts/tmp/a", "/Users/gladiator/Documents/workspace/my_scripts/tardst")


# if __name__ == "__main__":
#     untar("/Users/gladiator/Documents/workspace/my_scripts/tardst/a.tar.gz", "/Users/gladiator/Documents/workspace/")