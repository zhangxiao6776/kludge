# ext.set_prefix('KludgeTest_')
ext.add_cpp_global_include('string')
ext.add_func(
  'hello'
  ).add_cpp_local_include('vector')#.add_test("""
# {{name}}(),
# """, """
# Hello, world!
# """)
