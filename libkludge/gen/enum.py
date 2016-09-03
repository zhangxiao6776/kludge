#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

from decl import Decl
from test import Test
from member_access import MemberAccess
from this_access import ThisAccess
from libkludge.cpp_type_expr_parser import Void, Named, DirQual, directions, qualifiers
from libkludge.value_name import this_cpp_value_name
from libkludge.this_codec import ThisCodec
from libkludge.result_codec import ResultCodec
from libkludge.param_codec import ParamCodec
from libkludge.dir_qual_type_info import DirQualTypeInfo
import hashlib

class Enum(Decl):

  def __init__(
    self,
    ext,
    desc,
    type_info,
    values,
    are_values_namespaced = False,
    ):
    Decl.__init__(self, ext, desc)
    self.type_info = type_info
    self.values = values
    self.are_values_namespaced = are_values_namespaced

  def get_test_name(self):
    return self.type_info.kl.name.compound

  def get_kl_name(self):
    return self.type_info.kl.name.compound

  def get_template_basename(self):
    return 'enum'