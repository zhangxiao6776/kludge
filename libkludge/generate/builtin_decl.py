#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

import os, abc
from decl import Decl

class BuiltinDecl(Decl):
  def __init__(
    self,
    parent_namespace,
    desc,
    template_path,
    test_name,
    ):
    Decl.__init__(self, parent_namespace)
    self.desc = desc

    for method_name in [
      'error',
      'warning',
      'info',
      'debug',
      ]:
      setattr(self, method_name, getattr(parent_namespace, method_name))

  def get_desc(self):
    return self.desc

  def get_test_name(self):
    return self.test_name

  def get_template_path(self):
    return self.template_path

  def render(self, context, lang):
    return self.ext.jinjenv.get_template(
      self.get_template_path()+'.'+context+'.'+lang
      ).render({
      'decl': self,
      os.path.basename(path): self,
      })