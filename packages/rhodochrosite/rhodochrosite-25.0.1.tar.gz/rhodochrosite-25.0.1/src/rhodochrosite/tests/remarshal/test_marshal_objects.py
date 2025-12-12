from rhodochrosite.ruby import GenericRubyUserObject, atom
from rhodochrosite.writer import write_object


def test_marshal_basic_object() -> None:
    # Ruby definition: class Test1 end
    klass = GenericRubyUserObject(name=atom("Test1"), instance_variables={})
    assert write_object(klass) == b"\x04\bo:\nTest1\x00"


def test_marshal_object_with_symlink() -> None:
    # Ruby definition: class Test2 end
    # Marshal.dump [:Test2, Test2::new]
    klass = GenericRubyUserObject(name=atom("Test2"), instance_variables={})
    assert write_object([atom("Test2"), klass]) == b"\x04\b[\a:\nTest2o;\x00\x00"


def test_marshal_object_with_ivars() -> None:
    # Ruby definition: class Test3 def initialize @ivar = 1 end end
    klass = GenericRubyUserObject(name=atom("Test3"), instance_variables={atom("@ivar"): 1})
    assert write_object(klass) == b"\x04\bo:\nTest3\x06:\n@ivari\x06"
