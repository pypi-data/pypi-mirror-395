========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - package
      - | |version| |wheel| |supported-versions|
.. |docs| image:: https://readthedocs.org/projects/robot-tasks/badge/?style=flat
    :target: https://robot-tasks.readthedocs.io/
    :alt: Documentation Status

.. |github-actions| image:: https://github.com/fmorton/robot-tasks/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/fmorton/robot-tasks/actions

.. |requires| image:: https://requires.io/github/fmorton/robot-tasks/requirements.svg?branch=main
    :alt: Requirements Status
    :target: https://requires.io/github/fmorton/robot-tasks/requirements/?branch=main

.. |codecov| image:: https://codecov.io/gh/fmorton/robot-tasks/branch/main/graphs/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://codecov.io/github/fmorton/robot-tasks

.. |version| image:: https://img.shields.io/pypi/v/robot-tasks.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/robot-tasks

.. |wheel| image:: https://img.shields.io/pypi/wheel/robot-tasks.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/robot-tasks

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/robot-tasks.svg
    :alt: Supported versions
    :target: https://pypi.org/project/robot-tasks

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/robot-tasks.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/robot-tasks


.. end-badges

Simple task library using asyncio.

* Free software: MIT License

Installation
============

::

    pip install robot-tasks

You can also install the in-development version with::

    pip install https://github.com/fmorton/robot-tasks/archive/main.zip


Tasks Example with a Birdbrain Robot
====================================

.. code-block:: python

  from robot.hummingbird import Hummingbird
  from robot.tasks import Tasks

  async def task_1(bird):
    while True:
      print("task_1 running")

      await Tasks.yield_task(1.0)


  async def task_2(bird):
    while True:
      print("task_2 running")

      await Tasks.yield_task(0.5)


  bird = Hummingbird("A")

  tasks = Tasks()

  tasks.create_task(task_1(bird))
  tasks.create_task(task_2(bird))

  tasks.run()


Testing
=======

To run all the tests run::

    pytest
