import weakref


class MyClass:
    pass


obj = MyClass()
weak_obj = weakref.ref(obj)

print(weak_obj())  # Returns the object
del obj
print(weak_obj())  # Returns None, since the object was garbage collected
