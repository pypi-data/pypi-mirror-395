project('purelib-and-platlib', 'cpp',
default_options : ['c_std=c11', 'cpp_std=c++14'])

py = import('python').find_installation(pure: false)

py.install_sources(
    ['misc/__init__.py', 'misc/py.typed', 'kraken_decompressor.pyi'],
    subdir: 'kraken_decompressor'
)

py.extension_module(
    'kraken_decompressor',
    'kraken_decompressor.cpp',
    'kraken.cpp',
    install: true,
    install_dir: py.get_install_dir() / 'kraken_decompressor'
)
