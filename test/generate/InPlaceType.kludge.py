#
# Copyright (c) 2010-2016, Fabric Software Inc. All rights reserved.
#

ext.add_cpp_quoted_include('InPlaceType.hpp')

ty = ext.add_in_place_type('Class')
ty.add_ctor()
ty.add_ctor(['int', 'float']).add_test("""
Class c(-7, 1.52);
report("c.intValue = " + c.intValue);
report("c.get_intValue() = " + c.get_intValue());
""", """
Class::Class(-7, 1.52)
c.intValue = -7
c.get_intValue() = -7
Class::~Class()
""")
ty.add_test("""
Class c1(6, 1.3);
Class c2(c1);
c1 = c2;
""", """
Class::Class(6, 1.3)
Class::Class(Class const &)
Class::operator=(Class const &)
Class::~Class()
Class::~Class()
""")
ty.add_member('intValue', 'int')
ty.set_default_access(MemberAccess.private)
ty.add_member('floatValue', 'float')
ty.add_const_method('publicConstMethod', 'float')
ty.add_mutable_method('publicMutableMethod', 'float')
ty.add_const_method('publicVoidConstMethod')
ty.add_mutable_method('publicVoidMutableMethod')
ty.add_method('GetStaticFloat', 'float', this_access=ThisAccess.static)\
  .add_test("""
report(Class_GetStaticFloat());
""", """
+3.3
""")
ty.add_get_ind_op('int').add_test("""
Class c(-7, 3.14);
report(c.getAt(56));
Class_CxxConstRef cr = Make_Class_CxxConstRef(c);
report(cr.getAt(56));
""", """
Class::Class(-7, 3.14)
Class::operator[] const(56)
-7
Class::operator[] const(56)
-7
Class::~Class()
""")
ty.add_set_ind_op('int').add_test("""
Class c(-7, 3.14);
c.setAt(56, 4);
report(c);
""", """
Class::Class(-7, 3.14)
Class::operator[](56)
{intValue:4,floatValue:+3.14}
Class::~Class()
""")
ty.add_test("""
Class c(14, -8.9);
report("c.get_intValue() = " + c.get_intValue());
report("c.publicConstMethod() = " + c.publicConstMethod());
report("c.publicMutableMethod() = " + c.publicMutableMethod());
Class_CxxConstRef cr = Make_Class_CxxConstRef(c);
report("cr.get_intValue() = " + cr.get_intValue());
report("cr.publicConstMethod() = " + cr.publicConstMethod());
Class_CxxRef mr = Make_Class_CxxRef(c);
report("mr.get_intValue() = " + mr.get_intValue());
report("mr.publicConstMethod() = " + mr.publicConstMethod());
report("mr.publicMutableMethod() = " + mr.publicMutableMethod());
Class_CxxConstPtr cp = Make_Class_CxxConstPtr(c);
report("cp.get_intValue() = " + cp.get_intValue());
report("cp.publicConstMethod() = " + cp.publicConstMethod());
Class_CxxPtr mp = Make_Class_CxxPtr(c);
report("mp.get_intValue() = " + mp.get_intValue());
report("mp.publicConstMethod() = " + mp.publicConstMethod());
report("mp.publicMutableMethod() = " + mp.publicMutableMethod());
""", """
Class::Class(14, -8.9)
c.get_intValue() = 14
c.publicConstMethod() = -8.9
c.publicMutableMethod() = -8.9
cr.get_intValue() = 14
cr.publicConstMethod() = -8.9
mr.get_intValue() = 14
mr.publicConstMethod() = -8.9
mr.publicMutableMethod() = -8.9
cp.get_intValue() = 14
cp.publicConstMethod() = -8.9
mp.get_intValue() = 14
mp.publicConstMethod() = -8.9
mp.publicMutableMethod() = -8.9
Class::~Class()
""")
ty.add_test("""
Class c(14, -8.9);
report("c.publicVoidConstMethod()");
c.publicVoidConstMethod();
report("c.publicVoidMutableMethod()");
c.publicVoidMutableMethod();
Class_CxxConstRef cr = Make_Class_CxxConstRef(c);
report("cr.publicVoidConstMethod()");
cr.publicVoidConstMethod();
Class_CxxRef mr = Make_Class_CxxRef(c);
report("mr.publicVoidConstMethod()");
mr.publicVoidConstMethod();
report("mr.publicVoidMutableMethod()");
mr.publicVoidMutableMethod();
Class_CxxConstPtr cp = Make_Class_CxxConstPtr(c);
report("cp.publicVoidConstMethod()");
cp.publicVoidConstMethod();
Class_CxxPtr mp = Make_Class_CxxPtr(c);
report("mp.publicVoidConstMethod()");
mp.publicVoidConstMethod();
report("mp.publicVoidMutableMethod()");
mp.publicVoidMutableMethod();
""", """
Class::Class(14, -8.9)
c.publicVoidConstMethod()
c.publicVoidMutableMethod()
cr.publicVoidConstMethod()
mr.publicVoidConstMethod()
mr.publicVoidMutableMethod()
cp.publicVoidConstMethod()
mp.publicVoidConstMethod()
mp.publicVoidMutableMethod()
Class::~Class()
""")
ext.add_func('ReturnClass', 'Class')\
  .add_test("""
Class c1 = ReturnClass();
report("ReturnClass: c1 = " + c1);
""", """
Class::Class()
Class::Class(92, 6.74)
Class::operator=(Class const &)
Class::~Class()
ReturnClass: c1 = {intValue:92,floatValue:+6.74}
Class::~Class()
""")

dty = ext.add_in_place_type('DerivedClass', extends='Class')
dty.add_member('shortValue', 'short')
dty.add_ctor(['int', 'float', 'short'])
dty.add_const_method('anotherPublicMethod', 'short')\
  .add_test("""
DerivedClass dc(5, -1.34e9, 56);
report("dc.shortValue = " + dc.shortValue);
report("dc.anotherPublicMethod() = " + dc.anotherPublicMethod());
""", """
Class::Class(5, -1.34e+09)
DerivedClass::DerivedClass(5, -1.34e+09, 56)
dc.shortValue = 56
dc.anotherPublicMethod() = -168
DerivedClass::~DerivedClass()
Class::~Class()
Class::~Class()
""")

#   std::string getDesc() const {
#     char buf[256];
#     snprintf( buf, 256, "intValue:%d floatValue:%f", intValue, floatValue );
#     return std::string( buf );
#   }

# std::vector<Class> ReturnClassVec() {
#   std::vector<Class> result;
#   result.push_back( Class( 3, 3.14 ) );
#   result.push_back( Class( -14, -3.45 ) );
#   return result;
# }
