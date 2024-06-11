# highsbox

[![](https://img.shields.io/pypi/v/highsbox.svg?color=brightgreen)](https://pypi.org/pypi/highsbox/)

This is the python wheel distribution for binaries of [HiGHS](https://github.com/ERGO-Code/HiGHS) optimizer.

The current version is 1.7.1 built for the following platforms:
- Windows (x86_64)
- Linux (x86_64)
- MacOS (x86_64)
- MacOS (arm64)

```
pip install highsbox
```

After installation, you can use `python -m highsbox` to invoke the `highs` command-line tool.

```
>>> python -m highsbox --version
HiGHS version 1.7.0 Githash 50670fd. Copyright (c) 2024 HiGHS under MIT licence terms
```

It includes the `highs` command-line tool, the `highs.lib`/`highs.dll`/`libhighs.so` library and the `Highs.h` header files.

Their paths can be found using the `highsbox` module:

```python
>>> import highsbox
>>> highsbox.highs_bin_path()
'D:\\mambaforge\\Lib\\site-packages\\highsbox\\highs_dist\\bin\\highs.exe'
>>> highsbox.highs_lib_dir()
'D:\\mambaforge\\Lib\\site-packages\\highsbox\\highs_dist\\lib
>>> highsbox.highs_include_dir()
'D:\\mambaforge\\Lib\\site-packages\\highsbox\\highs_dist\\include\\highs'
```
