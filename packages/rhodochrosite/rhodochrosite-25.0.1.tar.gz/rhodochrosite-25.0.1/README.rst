Rhodochrosite
=============

Rhodochrosite is a Python 3.13+ library for loading and saving objects in the Ruby marshal format.

Usage
-----

Use ``rhodochrosite.read_object``::

    from rhodochrosite import read_object

    print(read_object(b'\x04\b"\babc'))

For custom objects, use ``MarshalReader``::

    from rhodochrosite import MarshalReader, RubySymbol

    data = MarshalReader.from_bytes(...)
    data.object_factories[RubySymbol("MyType")] = _make_my_type
    my_object = data.next_object()

Format support
--------------

Rhodochrosite supports all known features of Ruby's Marshal format, up to Ruby 3.4. Object links
are supported when *reading*, but not when *writing*; this has no practical affect other than some
written files being larger than their input size.
