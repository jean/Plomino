Introduction
============

Plomino is a powerful and flexible web-based application builder for Plone.

Features
========

* create your own custom applications from a web interface without programming
* create and design forms in WYSIWYG mode
* easily embed charts or maps
* create specific actions with formulas (compute fields, send emails, ...)
* adapt the application behaviour depending on the user access rights and roles
* import/export your application structure and/or your application data,
  including replication between Plomino instances

Positioning
===========

Plomino is a **through-the-web application builder**, hence:

* it is not a **through-the-web content-type builder** like 
  `Dexterity <http://plone.org/products/dexterity>`_, which is perfect to
  create a custom content type but that will always stick to the standard
  content management scenario, while Plomino allows any custom scenario,
* it is not just a **form generator** like 
  `PloneFormGen <http://plone.org/products/ploneformgen>`_, as Plomino provides
  all the services (data storage, search, automation, import/export, etc.) to
  build an entire application. Regarding form generation itself, a major
  difference with PloneFormGen is that Plomino allows editing the form layout
  in its entirety, while PloneFormGen uses a fixed pre-defined form layout.

Resources and documentation
===========================

Screencasts and how-tos are available on http://www.plomino.net/ .

Plomino documentation is available on 
`ReadTheDocs <http://readthedocs.org/docs/plomino/>`_.

Note: if you think something is missing in the documentation, please send your
pull request at https://github.com/plomino/PlominoDoc .

Internationalization
====================

Plomino itself is internationalized and translated in seven languages.
Applications built with Plomino can be internationalized (see the 
`related documentation
<https://plomino.readthedocs.org/en/latest/features/#i18n-support>`_).

Installation
============

To deploy Plomino, you need to edit your ``buildout.cfg`` file
and add the following in the ``eggs`` section::

    eggs =
         ...
         Products.CMFPlomino

Then you have to run ``buildout`` to realize your configuration::

    bin/buildout -N

Installation on Plone 4.0 and 4.1
=================================

If you're using Plone version older than 4.2 you'll need to add some
more directives to your ``buildout.cfg``.

Plomino depends on ``plone.app.registry``, and ``plomino.tinymce`` requires
``Products.TinyMCE>=1.2.13``. To make Plomino work on pre-4.2 Plone sites
you need to pin those versions in your ``versions.cfg`` section::

    Products.TinyMCE=1.2.13
    collective.js.jqueryui=1.8.16.9

and use a known good set for ``plone.app.registry``.

This means extending your buildout from::

    http://good-py.appspot.com/release/plone.app.registry/1.0b2?plone=4.0.9

replacing 4.0.9 with the actual version you need.

Support
=======

You can find support on the freenode IRC channel #plomino or using the 
`GitHub issue tracker <https://github.com/plomino/Plomino/issues>`_

Tests
=====

Plomino is continuously tested on Travis |travisstatus|_ and the code coverage 
is tracked on coveralls.io |coveralls|_.

.. |travisstatus| image:: https://secure.travis-ci.org/plomino/Plomino.png?branch=github-main
.. _travisstatus:  http://travis-ci.org/plomino/Plomino

.. |coveralls| image:: https://coveralls.io/repos/plomino/Plomino/badge.png?branch=github-main
.. _coveralls: https://coveralls.io/r/plomino/Plomino?branch=github-main

Credits
=======

Maintainers
-----------

* Eric BREHAULT <eric.brehault@makina-corpus.org>
* Jean Jordaan <jean.jordaan@gmail.com>
* Silvio Tomatis <silviot@gmail.com>

Contributors
------------

The complete list is available `here <http://www.plomino.net/credits>`.

Companies
---------

|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_

|Bitdeli|_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

.. |Bitdeli| image:: https://d2weczhvl823v0.cloudfront.net/plomino/plomino/trend.png
.. _Bitdeli: https://bitdeli.com/plomino

