"""
setup.py - Cross-platform setup for coordinate_system package

Author: PanGuoJun
Version: 6.0.5
License: MIT
"""

from setuptools import setup, Extension, find_packages
import sys
import platform
import pybind11

# Determine platform
system = platform.system()
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"

# Read long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Platform-specific compiler flags
extra_compile_args = []
extra_link_args = []

if system == 'Windows':
    # MSVC compiler flags
    extra_compile_args = [
        '/std:c++17',           # C++17 standard
        '/O2',                  # Optimization
        '/W3',                  # Warning level
        '/EHsc',                # Exception handling
        '/MD',                  # Runtime library
    ]
elif system == 'Linux':
    # GCC compiler flags
    extra_compile_args = [
        '-std=c++17',           # C++17 standard
        '-O3',                  # Optimization
        '-Wall',                # Warnings
        '-fPIC',                # Position independent code
        '-fvisibility=hidden',  # Hide symbols by default
    ]
elif system == 'Darwin':  # macOS
    # Clang compiler flags
    extra_compile_args = [
        '-std=c++17',           # C++17 standard
        '-O3',                  # Optimization
        '-Wall',                # Warnings
        '-fPIC',                # Position independent code
        '-fvisibility=hidden',  # Hide symbols by default
        '-mmacosx-version-min=10.14',  # macOS 10.14+
    ]

# Define the extension module
ext_modules = [
    Extension(
        'coordinate_system.coordinate_system',  # Module name
        sources=['coordinate_system_binding.cpp'],  # Source file
        include_dirs=[
            pybind11.get_include(),  # pybind11 headers
            '.',                     # Current directory (for pmsys_minimal.hpp)
        ],
        language='c++',
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    name='coordinate_system',
    version='6.0.5',
    packages=find_packages(),
    ext_modules=ext_modules,  # Add extension modules

    # Metadata
    description='High-performance 3D coordinate system library with unified differential geometry, quantum frame algebra, spectral transforms, and professional curvature visualization',
    long_description=long_description,
    long_description_content_type='text/markdown',

    # Author information
    author='PanGuoJun',
    author_email='18858146@qq.com',
    url='https://github.com/panguojun/Coordinate-System',

    # License
    license='MIT',

    # Classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'License :: OSI Approved :: MIT License',

        # Python versions
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: C++',

        # Operating Systems
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],

    # Python version requirement
    python_requires='>=3.7',

    # Install dependencies
    install_requires=[
        'numpy>=1.19.0',
        'matplotlib>=3.3.0',
    ],

    # Build dependencies
    setup_requires=['pybind11>=2.6.0'],

    # Platform support
    platforms=['Windows', 'Linux', 'macOS', 'Android', 'iOS'],

    # Keywords
    keywords='3d math vector quaternion coordinate-system geometry graphics spatial-computing differential-geometry curvature curve-interpolation c2-continuity frenet-frames fourier-transform operator-overloading quantum-coordinates heisenberg-uncertainty visualization rgb-frames catmull-rom squad intrinsic-gradient spectral-analysis surface-visualization',

    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/panguojun/Coordinate-System/issues',
        'Source': 'https://github.com/panguojun/Coordinate-System',
        'Documentation': 'https://github.com/panguojun/Coordinate-System/blob/main/README.md',
    },

    # Zip safe
    zip_safe=False,
)
