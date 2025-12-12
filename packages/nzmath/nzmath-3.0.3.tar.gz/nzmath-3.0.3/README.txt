NZMATH 3.0.3 (Python Calculator on Number Theory)
===================================================

Introduction
------------

NZMATH is a Python calculator on number theory.  It is freely available and distributed under the BSD license.  All programs are written only by Python so that you can easily see their algorithmic number theory.  You can get NZMATH with a single command::

    % python -m pip install -U nzmath

Here % is the command line prompt of Windows or Unix/macOS.

This release contains several program corrections and additions obtained by writing a programming "notebook" of the book 'Lectures on Elementary Number Theory' (TAKAGI, Teiji) in Python-NZMATH language.  The "notebook" itself is also available together with NZMATH calculator.  It is designed for beginning students of algorithmic number theory to self-study Number Theory, Programming and scientific English together.  It is possible only by running and reading the programs.  You can get the `notebook here`_.

.. _`notebook here`: https://sourceforge.net/projects/nzmath/files/nzmath-enttakagi/

Installation
------------

Detailed `tutorial on installing packages`_ will help you to install
NZMATH on your machine.

.. _`tutorial on installing packages`: https://packaging.python.org/en/latest/tutorials/installing-packages/

First, you must have Python 3.9 or later.  Ensure you can run Python
from the command line::

    % python --version

Python is available from https://www.python.org/ .

Next, ensure you can run pip from the command line::

    % python -m pip --version

Usually, you must have appropriate write permission.  Then, ensure pip,
setuptools, and wheel are up to date::

    % python -m pip install -U pip setuptools wheel

Only when you worry about garbage of previous NZMATH, clean it::

    % python -m pip uninstall nzmath

Finally, install NZMATH from PyPI::

    % python -m pip install -U nzmath

This final step, you may install from local archives.  For that, you
need to download sdist and/or wheel::

    nzmath-3.0.3-tar.gz
    nzmath-3.0.3-py3-none-any.whl

in advance.  You can get them at SourceForge_.

.. _SourceForge: https://sourceforge.net/projects/nzmath/files/nzmath/

You can also find them at PyPI_.

.. _PyPI: https://pypi.org/project/nzmath/

Now, go to the directory archives are put, and install NZMATH::

    % python -m pip install -U nzmath-3.0.3.tar.gz

by using sdist.  You may use wheel nzmath-3.0.3-py3-none-any.whl or
both.  See the `tutorial on installing packages`_ in detail.

Usage
-----

NZMATH is provided as a Python library package named 'nzmath', so
please use it as a usual package.  For more information please refer
Tutorial_.

.. _Tutorial: https://nzmath.sourceforge.io/tutorial.html

Feedback
--------

Your feedbacks are always welcomed.  Please consider to join the
`mailing list`_.

.. _`mailing list`: https://nzmath.sourceforge.io/ml.html

Copyright
---------

NZMATH is distributed under the BSD license.  Please read LICENSE.txt_.

.. _LICENSE.txt: https://nzmath.sourceforge.io/LICENSE.txt


