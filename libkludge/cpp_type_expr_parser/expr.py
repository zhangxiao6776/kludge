import abc
import directions, qualifiers
import sys, traceback
from dir_qual import DirQual

class CPPTypeExprException(Exception):

  def __init__(self, desc):
    Exception.__init__(desc)

class Type:

  __metaclass__ = abc.ABCMeta

  def __init__(self, qualifier=qualifiers.Unqualified):
    self.qualifier = qualifier

  @property
  def is_const(self):
    return qualifiers.is_const(self.qualifier)
  
  @property
  def is_mutable(self):
    return not self.is_const
  
  @property
  def is_volatile(self):
    return qualifiers.is_volatile(self.qualifier)

  def make_const(self):
    if qualifiers.is_const(self.qualifier):
      return self
    else:
      copy = self.__copy__()
      copy.qualifier = qualifiers.make_const(self.qualifier)
      return copy

  def make_volatile(self):
    if qualifiers.is_volatile(self.qualifier):
      return self
    else:
      copy = self.__copy__()
      copy.qualifier = qualifiers.make_volatile(self.qualifier)
      return copy

  def make_unqualified(self):
    if self.qualifier == qualifiers.Unqualified:
      return self
    else:
      copy = self.__copy__()
      copy.qualifier = qualifiers.Unqualified
      return copy

  def get_desc(self):
    lhs, rhs = self.build_desc()
    return lhs + rhs

  @abc.abstractmethod
  def get_kl_desc(self):
    pass

  @staticmethod
  def maybe_bracket_desc(lhs, rhs):
    if rhs and not rhs.startswith(")"):
      lhs = lhs + "("
      rhs = ")" + rhs
    return lhs, rhs

  def build_desc(self):
    lhs, rhs = self.build_unqualified_desc()
    if self.is_const:
      lhs, rhs = self.maybe_bracket_desc(lhs, rhs)
      if lhs and not lhs.endswith(" "):
        lhs += " "
      lhs += "const"
    if self.is_volatile:
      lhs, rhs = self.maybe_bracket_desc(lhs, rhs)
      if lhs and not lhs.endswith(" "):
        lhs += " "
      lhs += "volatile"
    return lhs, rhs

  @abc.abstractmethod
  def build_unqualified_desc(self):
    pass

  def get_undq(self):
    if isinstance(self, Direct):
      direction = directions.Direct
      undq_cpp_type_expr = self
    elif isinstance(self, PointerTo):
      direction = directions.Pointer
      undq_cpp_type_expr = self.pointee
    elif isinstance(self, ReferenceTo):
      direction = directions.Reference
      undq_cpp_type_expr = self.pointee
    else:
      raise CPPTypeExprException("internal error")

    qualifier = undq_cpp_type_expr.qualifier
    if qualifier != qualifiers.Unqualified:
      undq_cpp_type_expr = undq_cpp_type_expr.__copy__()
      undq_cpp_type_expr.qualifier = qualifiers.Unqualified

    return (undq_cpp_type_expr, DirQual(direction, qualifier))

  def get_redq(self, dq):
    cpp_type_expr = self
    if dq.is_const:
      cpp_type_expr = Const(cpp_type_expr)
    if dq.is_reference:
      cpp_type_expr = ReferenceTo(cpp_type_expr)
    elif dq.is_pointer:
      cpp_type_expr = PointerTo(cpp_type_expr)
    return cpp_type_expr

  def tranform_names(self, cb):
    pass

  def __str__(self):
    return self.get_desc()

  def __hash__(self):
    return hash((type(self), self.qualifier))

  def __eq__(self, other):
    return type(self) == type(other) \
      and self.qualifier == other.qualifier

  def __ne__(self, other):
    return not self == other

class Direct(Type):

  def __init__(self):
    Type.__init__(self)

class Void(Direct):

  def __init__(self):
    Direct.__init__(self)

  def build_unqualified_desc(self):
    return "void", ""

  def get_kl_desc(self):
    return "VOID"

  def __copy__(self):
    return Void()

class Bool(Direct):

  def __init__(self):
    Direct.__init__(self)

  def build_unqualified_desc(self):
    return "bool", ""

  def get_kl_desc(self):
    return "Boolean"

  def __copy__(self):
    return Bool()

class Numeric(Direct):

  def __init__(self):
    Direct.__init__(self)

class Integer(Numeric):

  def __init__(self, is_signed=True):
    Numeric.__init__(self)
    self.is_signed = is_signed

  def make_unsigned(self):
    self.is_signed = False
    return self

  def make_signed(self):
    self.is_signed = True
    return self

  def build_unqualified_desc(self):
    if not self.is_signed:
      return "unsigned " + self.get_signed_desc(), ""
    else:
      return self.get_signed_desc(), ""

  @abc.abstractmethod
  def get_signed_desc(self):
    pass

  def __hash__(self):
    return Numeric.__hash__(self) ^ hash(self.is_signed)

  def __eq__(self, other):
    return Numeric.__eq__(self, other) \
      and self.is_signed == other.is_signed

class Char(Integer):

  def __init__(self, is_signed=True):
    Integer.__init__(self, is_signed)

  def get_signed_desc(self):
    return "char"

  def get_kl_desc(self):
    if self.is_signed:
      return "SInt8"
    else:
      return "UInt8"

  def __copy__(self):
    return Char(self.is_signed)

class Short(Integer):

  def __init__(self, is_signed=True):
    Integer.__init__(self, is_signed)

  def get_signed_desc(self):
    return "short"

  def get_kl_desc(self):
    if self.is_signed:
      return "SInt16"
    else:
      return "UInt16"

  def __copy__(self):
    return Short(self.is_signed)

class Int(Integer):

  def __init__(self, is_signed=True):
    Integer.__init__(self, is_signed)

  def get_signed_desc(self):
    return "int"

  def get_kl_desc(self):
    if self.is_signed:
      return "SInt32"
    else:
      return "UInt32"

  def __copy__(self):
    return Int(self.is_signed)

class Long(Integer):

  def __init__(self, is_signed=True):
    Integer.__init__(self, is_signed)

  def get_signed_desc(self):
    return "long"

  def get_kl_desc(self):
    if self.is_signed:
      return "SInt32"
    else:
      return "UInt32"

  def __copy__(self):
    return Long(self.is_signed)

class LongLong(Integer):

  def __init__(self, is_signed=True):
    Integer.__init__(self, is_signed)

  def get_signed_desc(self):
    return "long long"

  def get_kl_desc(self):
    if self.is_signed:
      return "SInt64"
    else:
      return "UInt64"

  def __copy__(self):
    return LongLong(self.is_signed)

class FloatingPoint(Numeric):

  def __init__(self):
    Numeric.__init__(self)

class Float(FloatingPoint):

  def __init__(self):
    FloatingPoint.__init__(self)

  def build_unqualified_desc(self):
    return "float", ""

  def get_kl_desc(self):
    return "Float32"

  def __copy__(self):
    return Float()

class Double(FloatingPoint):

  def __init__(self):
    FloatingPoint.__init__(self)

  def build_unqualified_desc(self):
    return "double", ""

  def get_kl_desc(self):
    return "Float64"

  def __copy__(self):
    return Double()

class FixedArrayOf(Direct):

  def __init__(self, element, size):
    Direct.__init__(self)
    self.element = element
    self.size = size

  def build_unqualified_desc(self):
    lhs, rhs = self.element.build_desc()
    rhs = "[%u]%s" % (self.size, rhs)
    return lhs, rhs

  def get_kl_desc(self):
    return "%s_FA%d" % (self.element.get_desc(), self.size)

  def tranform_names(self, cb):
    self.element.tranform_names(cb)

  def __hash__(self):
    return Direct.__hash__(self) ^ hash((self.element, self.size))

  def __eq__(self, other):
    return Direct.__eq__(self, other) \
      and self.element == other.element \
      and self.size == other.size

  @property
  def range(self):
    return range(0, self.size)

  def __copy__(self):
    return FixedArrayOf(self.element, self.size)

class Component(object):

  def __init__(self):
    pass

  @abc.abstractmethod
  def get_desc(self):
    pass

  @abc.abstractmethod
  def get_kl_desc(self):
    pass

  def tranform_names(self, cb):
    pass

  def __str__(self):
    return self.get_desc()

  def __hash__(self):
    return hash(type(self))

  def __eq__(self, other):
    return type(self) == type(other)

  def __ne__(self, other):
    return not self == other

def iscomponentlist(components):
  return isinstance(components, list) \
    and all(isinstance(component, Component) for component in components)

class Simple(Component):

  def __init__(self, name):
    Component.__init__(self)
    if not isinstance(name, basestring):
      raise Exception("name: expecting a string")
    self.name = name

  def get_desc(self):
    return self.name

  def get_kl_desc(self):
    return self.name

  def __hash__(self):
    return Component.__hash__(self) ^ hash(self.name)

  def __eq__(self, other):
    return Component.__eq__(self, other) \
      and self.name == other.name

  def __copy__(self):
    return Simple(self.name)

class Template(Component):

  def __init__(self, name, params):
    Component.__init__(self)
    if not isinstance(name, basestring):
      raise Exception("name: expecting a string")
    self.name = name
    if not isinstance(params, list):
      raise Exception("params: expecting a list")
    self.params = params

  def tranform_names(self, cb):
    for i in range(0, len(self.params)):
      self.params[i].tranform_names(cb)

  def get_desc(self):
    return self.name + "< " + ", ".join(
      [param.get_desc() for param in self.params]
      ) + " >"

  def get_kl_desc(self):
    return '__'.join([self.name] + [param.get_kl_desc() for param in self.params])

  def __hash__(self):
    result = Component.__hash__(self) ^ hash(self.name)
    for param in self.params:
      result ^= hash(param)
    return result

  def __eq__(self, other):
    return Component.__eq__(self, other) \
      and self.name == other.name \
      and self.params == other.params

  def __copy__(self):
    return Template(self.nested_name, self.params)

class Named(Direct):

  def __init__(self, components):
    Direct.__init__(self)
    assert isinstance(components, list)
    for component in components:
      assert isinstance(component, Component)
    self.components = components

  def tranform_names(self, cb):
    self.components = cb(self.components)
    assert iscomponentlist(self.components)
    for component in self.components:
      component.tranform_names(cb)

  def build_unqualified_desc(self):
    return '::'.join(
      [component.get_desc() for component in self.components]
      ), ""

  def get_kl_desc(self):
    return '_'.join([component.get_kl_desc() for component in self.components])

  def prefix(self, components):
    assert iscomponentlist(components)
    self.components = components + self.components
    return self

  def __hash__(self):
    result = Direct.__hash__(self)
    for component in self.components:
      result ^= hash(component)
    return result

  def __eq__(self, other):
    return Direct.__eq__(self, other) \
      and self.components == other.components

  def __copy__(self):
    return Named(self.components)

class Indirect(Type):

  def __init__(self, pointee):
    Type.__init__(self)
    self.pointee = pointee

  def tranform_names(self, cb):
    self.pointee.tranform_names(cb)

  def __hash__(self):
    return Type.__hash__(self) ^ hash(self.pointee)

  def __eq__(self, other):
    return Type.__eq__(self, other) \
      and self.pointee == other.pointee

class PointerTo(Indirect):

  def __init__(self, pointee):
    Indirect.__init__(self, pointee)

  def build_unqualified_desc(self):
    lhs, rhs = self.pointee.build_desc()
    lhs, rhs = self.maybe_bracket_desc(lhs, rhs)
    if lhs and not lhs.endswith(" "):
      lhs += " "
    lhs += "*"
    return lhs, rhs

  def get_kl_desc(self):
    return "%s_PTR" % self.pointee.get_kl_desc()

  def __copy__(self):
    return PointerTo(self.pointee)

class ReferenceTo(Indirect):

  def __init__(self, pointee):
    Indirect.__init__(self, pointee)

  def build_unqualified_desc(self):
    lhs, rhs = self.pointee.build_desc()
    lhs, rhs = self.maybe_bracket_desc(lhs, rhs)
    if lhs and not lhs.endswith(" "):
      lhs += " "
    lhs += "&"
    return lhs, rhs

  def get_kl_desc(self):
    return "%s_REF" % self.pointee.get_kl_desc()

  def __copy__(self):
    return ReferenceTo(self.pointee)

def Unsigned(ty):
  return ty.make_unsigned()

def Signed(ty):
  return ty.make_signed()

def Const(ty):
  return ty.make_const()

def SimpleNamed(name):
  return Named([Simple(name)])
