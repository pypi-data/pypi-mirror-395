import os
import shutil
#from distutils.command.build_ext import build_ext
#from distutils.core import Distribution, Extension

#from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension
from setuptools.dist import Distribution
import numpy as np
import ailist

from Cython.Build import build_ext, cythonize


include_dirs = [".", np.get_include(), ailist.get_include()]


def declare_cython_extension(extName, use_openmp=False, include_dirs=None, use_zlib=False):
    """
    Declare a Cython extension module for setuptools.

    Arguments:
        extName : str
            Absolute module name, e.g. use `mylibrary.mypackage.mymodule`
            for the Cython source file `mylibrary/mypackage/mymodule.pyx`.
        use_math : bool
            If True, set math flags and link with ``libm``.
        use_openmp : bool
            If True, compile and link with OpenMP.
        use_zlib : bool
            If True, link with zlib library.

    Returns:
        Extension object
            that can be passed to ``setuptools.setup``.
    """
    extPath = extName.replace(".", os.path.sep)+".pyx"

    # Remove -lz from compile_args - it's a linker flag, not a compiler flag
    compile_args = ["-O3"]
    link_args    = []
    libraries    = []

    # OpenMP
    if use_openmp:
        compile_args.extend(['-fopenmp'])
        link_args.extend(['-fopenmp'])
    
    # zlib linking
    if use_zlib:
        libraries.append('z')  # This is the correct way to link zlib

    # Convert empty list to None if no libraries (setuptools convention)
    if not libraries:
        libraries = None

    return Extension( extName,
                      [extPath],
                      extra_compile_args=compile_args,
                      extra_link_args=link_args,
                      include_dirs=include_dirs,
                      libraries=libraries
                    )


def build():
    # declare Cython extension modules here
    ext_module_illumina = declare_cython_extension( "MethylVerse.core.microarray.read_illumina", use_openmp=False , include_dirs=include_dirs )
    ext_module_methyldackel = declare_cython_extension( "MethylVerse.core.sequencing.read_methyldackel.read_methyldackel", use_openmp=False , include_dirs=include_dirs, use_zlib=True )
    ext_module_merge = declare_cython_extension( "MethylVerse.tools.merge_regions.merge_regions", use_openmp=False , include_dirs=include_dirs )


    # this is mainly to allow a manual logical ordering of the declared modules
    cython_ext_modules = [ext_module_illumina, ext_module_methyldackel, ext_module_merge]

    # Call cythonize() explicitly, as recommended in the Cython documentation. See
    # This will favor Cython's own handling of '.pyx' sources over that provided by setuptools.
    # cythonize() just performs the Cython-level processing, and returns a list of Extension objects.
    ext_modules = cythonize(cython_ext_modules, include_path=include_dirs, gdb_debug=False, language_level=3)

    distribution = Distribution({"name": "extended", "ext_modules": ext_modules})
    distribution.package_dir = "extended"

    cmd = build_ext(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # Copy built extensions back to the project
    #files = os.listdir(cmd.build_lib)
    #print(files)
    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        shutil.copyfile(output, relative_extension)
    #    mode = os.stat(relative_extension).st_mode
    #    mode |= (mode & 0o444) >> 2
    #    os.chmod(relative_extension, mode)


if __name__ == "__main__":
    build()