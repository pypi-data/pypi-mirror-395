# assign-overload
This library makes it possible to overload assignment (=) operator. Inspired by [assign](https://github.com/RyanKung/assign).
Along with other things, main difference from that library is [assign](https://github.com/RyanKung/assign) calls the overloaded operator of the right hand side while this library calls of the left hand side.

# Installation
```pip install assign-overload```

# How To Use
First you need to overload the assignment operator using the function ```_assign_```:
```python
class T:        
    def _assign_(self, value, *annotation):
        print(f"called with {value}")
        return self
```
_value_ is the value of right hand side. If the assignment is annotated, _annotation_ will take a single argument carrying the annotation. Return value specifies the value of left hand side.

Next, in order to make this method automatically called you should call assign_overload.**patch_and_reload_module**():
```python
import assign_overload

class T:        
    def _assign_(self, value, *annotation):
        print(f"called with {value}")
        return self


def main():
    a = T()
    a = 10 # a will keep holding the T object


if assign_overload.patch_and_reload_module():
    if __name__ == "__main__":
        main()
```
This function will find and modify the current module's source code, replacing right hand side of assignments with calls to ```_assign_```, then execute the modified code. 
Once called, this function will introduce a new global variable to the current module: ```modified_source```. 
This variable will be accessible while both executing the original module and modified module. 
It represents the source code of the modified module.
Since module's ```__dict__``` attribute is passed as the globals parameter of ```exec```, names created in the modified module will be reflected on the original module along with their values, creating a reloading effect. 
Return value of this function specifies which module we are currently executing. True means modified module and False means original module.
Any code outside the first if block will be executed twice. 
Codes before this function call will first be executed while executing the original module and second while executing the modified module.
Codes after the first if block will first be executed while executing the modified module and second while executing the original module. 
This is especially bad because if a piece of code last executed while executing the original module, any function or class definition will have its original definition, not the modified definition they should have.
Codes inside the first if block will only be executed while executing the modified module.
You can wrap all your module code including functions and classes inside a single if block like this:
```python
import assign_overload

if assign_overload.patch_and_reload_module():
    class T:        
        def _assign_(self, value, *annotation):
            print(f"called with {value}")
            return self


    def main():
        a = T()
        a = 10 # a will keep holding the T object


    if __name__ == "__main__":
        main()
```
But that doesn't look nice. 
Functions, classes and constant definitions are most probably okay to be executed twice but actual code should be executed once.
Thus, the location in the first example is the best location for calling this function.
This function should be called even if this module isn't the ```__main__``` module because function and class definitions should be modified even if no real code is ought to be executed.
This function should be called once. Consecutive calls doesn't modify and execute the source code again. 
Lastly, this function will introduce 2 other global varriables to the current module: ```patched``` and ```executing_patch```.
These variables are internally used by the library and they are documented here only to prevent the user from changing them.

# Limitations
Unpacking during assignment and the walrus operator are not supported. 
If you attempt to call assign_overload.patch_and_reload_module() from a module using these features, you will face an error.
