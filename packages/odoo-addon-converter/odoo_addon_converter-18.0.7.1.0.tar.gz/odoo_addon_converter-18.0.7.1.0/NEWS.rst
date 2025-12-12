Changelog
=========

18.0.7.1.0
----------

Field converter on a binary field use data uri.

18.0.7.0.1
----------

Fix test keyfield.

18.0.7.0.0
----------

- Add a context to propagate data between converters.
- Keyfield: add a look up function.
- Add write stages to sort writing operations.

18.0.6.1.0
----------

- Image converter is copypasted from the redner Odoo Module. long term, it must
  be deleted from the redner Module

- Add QR code converter & test it

18.0.6.0.0
----------

fastjsonschema is now an optional dependency. It is listed in the dependencies of section *schema-validation*.
If validation needs to be done and the library is missing, an exception will be raised.

18.0.5.0.0
----------

Fix Switch converter to call post_hook.

Xref converter:

- Allow prefix on Xref converter
- Add option to include module name in messages. Incoming and outgoing message value have the same comportment.
  For example, if __converter__ is used as the module, both generated messages and received message will contain __converter__.<name>.
  Previously, generated messages would use the module name while received one would not.

18.0.4.1.0
----------

Add JsonLD_ID converter.

18.0.4.0.0
----------

In Model converter, also validate messages in ``message_to_odoo``.

Model converter argument changed, `__type__` is now the last argument and is optional. It is expected not to be used
anymore.
Added possible_datatypes property and odoo_datatype on Converter. Defaults to empty set and None.
On Model, it can be set.

Replace generic exception.

18.0.3.1.0
----------

Added Writeonly converter.

Add some typing information, or make it consistent.

Add more docstrings.

Fix using Skip in switch converter.

18.0.3.0.0
----------

Breaking change: validator package does not assume a odoo.addons package name, provide full package name instead.

18.0.2.2.0
----------

Remove mail dependency, to avoid forcing its installation, only needed when using some specific converters.

18.0.2.1.0
----------

Expose Context, NewinstanceType and build_context at the top level package.

18.0.2.0.2
----------

Evolve: Allow to skip update process.

18.0.2.0.1
----------

Fix RelationToMany calling undefined fonction.

18.0.2.0.0
----------

Fixes and changes after making the module typing compliant.

18.0.1.0.0
----------

Migration to Odoo 18.
