from __future__ import annotations

import sys
import platform

try:
    from setuptools import setup, Extension
except ImportError as exc:
    raise RuntimeError(
        "setuptools is required to build vacmap_index. "
        "Install it with `python -m pip install --upgrade setuptools`."
    ) from exc

sys.path.append("python")

extra_compile_args = ["-DHAVE_KALLOC"]
include_dirs = ["."]

if platform.machine() in ["aarch64", "arm64"]:
    include_dirs.append("sse2neon/")
    extra_compile_args.extend([
        "-arch", "arm64",             # Force ARM64 architecture
        "-ftree-vectorize",
        "-DKSW_SSE2_ONLY",
        "-D__SSE2__",
        "-Wno-implicit-function-declaration" # Allow older C style implicit declarations
    ])
else:
    extra_compile_args.append("-msse4.1")

setup(
    name="vacmap_index",
    version="0.0.2",
    url="https://github.com/micahvista/VACmap/tree/main",
    description="vacmap_index",
    long_description="This code is adapted from minimap2",
    author="Hongyu Ding",
    author_email="920268622@qq.com",
    license="MIT",
    keywords="sequence-alignment",
    ext_modules=[
        Extension(
            "vacmap_index",
            sources=[
                "python/mappy.pyx",
                "align.c",
                "bseq.c",
                "lchain.c",
                "seed.c",
                "format.c",
                "hit.c",
                "index.c",
                "pe.c",
                "options.c",
                "ksw2_extd2_sse.c",
                "ksw2_exts2_sse.c",
                "ksw2_extz2_sse.c",
                "ksw2_ll_sse.c",
                "kalloc.c",
                "kthread.c",
                "map.c",
                "misc.c",
                "sdust.c",
                "sketch.c",
                "esterr.c",
                "splitidx.c",
            ],
            depends=[
                "minimap.h",
                "bseq.h",
                "kalloc.h",
                "kdq.h",
                "khash.h",
                "kseq.h",
                "ksort.h",
                "ksw2.h",
                "kthread.h",
                "kvec.h",
                "mmpriv.h",
                "sdust.h",
                "python/cmappy.h",
                "python/cmappy.pxd",
            ],
            extra_compile_args=extra_compile_args,
            include_dirs=include_dirs,
            libraries=["z", "m", "pthread"],
        )
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: C",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    setup_requires=["cython"],
)
