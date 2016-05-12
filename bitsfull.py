# Josh Klaus
# CS131A
# Python

# A class extending int, objects of which have a string representation in binary 
# A test suite of class functionality will run when the class is invoked directly.


class bitsnumber(int):         #class extending int

    def __new__(cls, value):  
        try:
            if value < 0:    # addresses negative numbers
                print('only positive numbers are acceptable')
            else:
            # objects are represented by a string in binary
                return str(bin(value)[2:])     
        except TypeError :   # prints exception for str and float
            print('You must instantiate an object that is an int')

# test suite to test class functionality        

print("bitsnumber(4) = ")   
bitsnumber4 = bitsnumber(4)    # test the int 4
print(bitsnumber4)
print('Does result = 100')
print(bitsnumber4 == '100')   # test results are correct
   
print("bitsnumber(8) = ")
bitsnumber8 = bitsnumber(8)     # test the int 8
print(bitsnumber8)
print('Does result = 1000')
print(bitsnumber8 == '1000')  # test results are correct

print("bitsnumber(67) = ")
bitsnumber67 = bitsnumber(67)     # test the int 8
print(bitsnumber67)
print('Does result = 1000011')    
print(bitsnumber67 == '1000011')  # test results are correct

print("bitsnumber('four') = ")
bitsnumbstr = bitsnumber('four')   # test the str four
print(bitsnumbstr)

print("bitsnumber(4.005132) = ")
bitsnumbfloat = bitsnumber(4.005132)  # test the float 4.005132
print(bitsnumbfloat)

print("bitsnumber(-8) = ")
bitsnumberneg8 = bitsnumber(-8)     # test the negative numbers by using -8
print(bitsnumberneg8)

