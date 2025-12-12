#!/usr/bin/env python3
# File: setup.py
# Author: Hadi Cahyadi <cumulus13@gmail.com>
# Date: 2025-12-04
# Description: 
# License: MIT

"""
Setup configuration for psqlc package
"""
from setuptools import setup, Extension
from setuptools.dist import Distribution
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist
from pathlib import Path
import traceback
import os
import sys
import shutil
import glob

NAME = 'psqlc'

# Create package directory
os.makedirs(NAME, exist_ok=True)

# Copy necessary files
shutil.copy2('__version__.py', NAME)
shutil.copy2('psqlc.py', NAME)

def fix_indentation(input_file, output_file):
    """Fix mixed tabs and spaces in Python file"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace tabs with 4 spaces
        content = content.replace('\t', '    ')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed indentation: {input_file} -> {output_file}")
        return True
    except Exception as e:
        print(f"✗ Warning: Could not fix indentation: {e}")
        return False

# Read version from __version__.py
def get_version():
    """Get version from __version__.py file"""
    try:
        version_file = Path(__file__).parent / "__version__.py"
        if not version_file.is_file():
            version_file = Path(__file__).parent / NAME / "__version__.py"
        if version_file.is_file():
            with open(version_file, "r") as f:
                for line in f:
                    if line.strip().startswith("version"):
                        parts = line.split("=")
                        if len(parts) == 2:
                            return parts[1].strip().strip('"').strip("'")
    except Exception as e:
        if os.getenv('TRACEBACK') and os.getenv('TRACEBACK') in ['1', 'true', 'True']:
            print(traceback.format_exc())
        else:
            print(f"ERROR: {e}")
    return "2.0"

# Create __init__.py
with open(Path(NAME, '__init__.py'), 'w') as f:
    f.write("""from .psqlc import rich_print, load_settings_from_path, find_settings_recursive, parse_django_settings, get_connection, show_databases, show_tables, show_users, describe_table, execute_query, create_user_db, backup_database, show_connections, show_indexes, show_size, drop_database, drop_user, main, print_exception, get_version, get_db_config_or_args

from .__version__ import version as __version__
__author__ = "Hadi Cahyadi"
__email__ = "cumulus13@gmail.com"
__all__ = ["rich_print",
            "load_settings_from_path",
            "find_settings_recursive",
            "parse_django_settings",
            "get_connection",
            "show_databases",
            "show_tables",
            "show_users",
            "describe_table",
            "execute_query",
            "create_user_db",
            "backup_database",
            "show_connections",
            "show_indexes",
            "show_size",
            "drop_database",
            "drop_user",
            "main",
            "print_exception",
            "get_version",
            "get_db_config_or_args"]
""")

# Custom build_py to exclude .py files when building with Cython
class BuildPyExcludeSource(build_py):
    """Custom build_py that excludes source .py files for cythonized modules"""
    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        # Exclude psqlc.py if we're building with Cython
        if hasattr(self.distribution, 'ext_modules') and self.distribution.ext_modules:
            return [
                (pkg, module, filename) 
                for pkg, module, filename in modules
                if module != 'psqlc'  # Exclude psqlc.py since we have psqlc.pyd/.so
            ]
        return modules

# Custom sdist command to include pre-compiled binaries
class SdistWithBinaries(sdist):
    """Custom sdist that includes pre-compiled .so/.pyd files"""
    
    def make_release_tree(self, base_dir, files):
        """Create release tree and add compiled binaries"""
        super().make_release_tree(base_dir, files)
        
        # After creating the release tree, copy any compiled binaries
        print("\nAdding pre-compiled binaries to sdist...")
        
        # Find all .so and .pyd files in the build directory
        binary_patterns = [
            'build/**/*.so',
            'build/**/*.pyd',
            f'{NAME}/**/*.so',
            f'{NAME}/**/*.pyd',
        ]
        
        binaries_found = []
        for pattern in binary_patterns:
            binaries_found.extend(glob.glob(pattern, recursive=True))
        
        # Copy binaries to sdist
        for binary in binaries_found:
            # Determine relative path
            if binary.startswith('build/'):
                # Extract path after build/lib*/
                parts = binary.split(os.sep)
                try:
                    lib_idx = next(i for i, p in enumerate(parts) if p.startswith('lib'))
                    rel_path = os.path.join(*parts[lib_idx + 1:])
                except (StopIteration, IndexError):
                    rel_path = os.path.basename(binary)
            else:
                rel_path = binary
            
            dest = os.path.join(base_dir, rel_path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            
            if os.path.exists(binary):
                shutil.copy2(binary, dest)
                print(f"  ✓ Added: {rel_path}")
        
        if binaries_found:
            print(f"✅ Added {len(binaries_found)} binary file(s) to sdist")
        else:
            print("⚠️  No pre-compiled binaries found - sdist will require compilation")

# Custom Distribution class for binary-only wheel
class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True

print(f"NAME   : {NAME}")
print(f"VERSION: {get_version()}")

# Read README
this_directory = Path(__file__).parent
try:
    long_description = (this_directory / "README.md").read_text(encoding='utf-8')
except:
    long_description = "Feature-rich command-line interface tool for managing PostgreSQL databases. Built with `asyncpg` and featuring beautiful output formatting with Rich, it provides intelligent auto-detection of database configurations from Django settings, environment files, and various configuration formats."

_extensions = []
extensions = None
cmdclass = {}

# Try to build Cython extensions
try:
    from Cython.Build import cythonize
    
    # Copy fixed file to .pyx for Cython compilation
    print("Preparing Cython compilation...")
    # fix_indentation(f"{NAME}/psqlc.py", f'{NAME}/psqlc.pyx')
    shutil.copy2(f"{NAME}/psqlc.py", f'{NAME}/psqlc.pyx')
    
    _extensions = [
        Extension(
            'psqlc.psqlc', 
            ['psqlc/psqlc.pyx'],
            extra_compile_args=['/O2'] if sys.platform == 'win32' else ['-O3'],
        ),
    ]
    
    extensions = cythonize(
        _extensions,
        compiler_directives={
            'language_level': '3',
            'embedsignature': True,
            'boundscheck': False,
            'wraparound': False,
        }
    )
    
    # Use custom build_py to exclude source files from wheels
    cmdclass['build_py'] = BuildPyExcludeSource
    
    # Use custom sdist to include binaries
    cmdclass['sdist'] = SdistWithBinaries
    
    # MANIFEST.in for Cython build
    with open('MANIFEST.in', 'w') as fm:
        fm.write("""include README.md
include __version__.py
include LICENSE*

# Include package metadata files
include psqlc/__init__.py
include psqlc/__version__.py

# Include pre-compiled binaries in sdist
recursive-include psqlc *.so
recursive-include psqlc *.pyd
recursive-include build *.so
recursive-include build *.pyd

# Include images
recursive-include psqlc *.png

# Exclude source files from binary wheels (but keep in sdist)
global-exclude *.py[cod]
global-exclude __pycache__
global-exclude .git*
global-exclude *.ini
global-exclude *.c

# For sdist, we want binaries; for bdist_wheel, exclude source
prune psqlc/psqlc.py
prune psqlc/psqlc.pyx
""")
    
    print("✓ Cython extensions configured successfully")
    print("✓ Binary wheels will exclude .py/.pyx/.c files")
    print("✓ Sdist will include pre-compiled .so/.pyd files if available")
        
except ImportError as e:
    print(f"✗ Cython not installed: {e}")
    print("  Install with: pip install cython")
    print("  Building without Cython extensions - source files will be included")
    
    with open('MANIFEST.in', 'w') as fm:
        fm.write("""include README.md
include __version__.py
recursive-include psqlc *.py
recursive-include psqlc *.png
include psqlc/__init__.py
include psqlc/__version__.py

global-exclude *.py[cod]
global-exclude __pycache__
global-exclude .git*
global-exclude *.ini

include LICENSE*
""")

except Exception as e:
    print(f"✗ Cython build failed: {e}")
    print("  Building without Cython extensions - source files will be included")
    if os.getenv('TRACEBACK', '0').lower() in ['1', 'true', 'yes']:
        print(traceback.format_exc())
    
    with open('MANIFEST.in', 'w') as fm:
        fm.write("""include README.md
include __version__.py
recursive-include psqlc *.py
recursive-include psqlc *.png
include psqlc/__init__.py
include psqlc/__version__.py

global-exclude *.py[cod]
global-exclude __pycache__
global-exclude .git*
global-exclude *.ini

include LICENSE*
""")

setup(
    name=NAME,
    version=get_version(),
    author='cumulus13',
    author_email='cumulus13@gmail.com',
    description='Feature-rich command-line interface tool for managing PostgreSQL databases. Built with `asyncpg` and featuring beautiful output formatting with Rich, it provides intelligent auto-detection of database configurations from Django settings, environment files, and various configuration formats.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cumulus13/psqlc',
    packages=[NAME],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: System :: Filesystems',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Environment :: Console',
    ],
    keywords='postgresql, automation, analytics, developer tools, monitoring, devops, django, asyncpg, dotenv',
    python_requires='>=3.6',
    install_requires=['rich', 'asyncpg', 'licface', 'envdot', 'pwinput', 'richcolorlog'],
    entry_points={
        'console_scripts': [
            'psqlc=psqlc.psqlc:main',
        ],
    },
    include_package_data=True,
    project_urls={
        'Bug Reports': 'https://github.com/cumulus13/psqlc/issues',
        'Source': 'https://github.com/cumulus13/psqlc',
        "Documentation": f"https://psqlc.readthedocs.io",
    },
    ext_modules=extensions,
    cmdclass=cmdclass,
    zip_safe=False,
    distclass=BinaryDistribution if extensions else None,
    package_data={
        'psqlc': [f'*{sys.version_info.major}{sys.version_info.minor}*.pyd'] if sys.platform == 'win32' else [f'*{sys.version_info.major}{sys.version_info.minor}*.so', ],
    },
    license="MIT",
    license_files=["LICENSE"]
)