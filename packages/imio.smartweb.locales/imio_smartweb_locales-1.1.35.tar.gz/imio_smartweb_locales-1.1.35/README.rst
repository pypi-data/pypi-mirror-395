.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://img.shields.io/pypi/v/imio.smartweb.locales.svg
    :target: https://pypi.python.org/pypi/imio.smartweb.locales/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/imio.smartweb.locales.svg
    :target: https://pypi.python.org/pypi/imio.smartweb.locales
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/l/imio.smartweb.locales.svg
    :target: https://pypi.python.org/pypi/imio.smartweb.locales/
    :alt: License


=====================
imio.smartweb.locales
=====================

Locales for iMio smartweb packages :
 - imio.directory.core
 - imio.directory.policy
 - imio.events.core
 - imio.events.policy
 - imio.news.core
 - imio.news.policy
 - imio.smartweb.core
 - imio.smartweb.common
 - imio.smartweb.policy


Documentation
-------------

Make buildout::

  make buildout

Update translations::

  make update_translations


Translations
------------

This product has been translated into

- French


Installation
------------

Install imio.smartweb.locales by adding it to your buildout::

    [buildout]

    ...

    eggs =
        imio.smartweb.locales


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/imio/imio.smartweb.locales/issues
- Source Code: https://github.com/imio/imio.smartweb.locales


License
-------

The project is licensed under the GPLv2.
