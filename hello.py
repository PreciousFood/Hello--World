# imports...
import time  # the time
import asyncio  # multitasking
from typing import Any  # PEP
import sys  # Import our system stuff (because aparently we didn't already know that)
import io  # not .io games
import atexit  # cleanup
import warnings  # for stupid people
# These are just some of the hundreds of libraries/modules/packages availale fo python
# If you need a script that can do a task, a module exists for it somewhere...


class PrinterError(BaseException):  # Here we are demonstrating Object Oriented Programming (OOP) basics as well as practicing clean code.
    pass  # By creating our own exception, potential errors will be easier to trace

class Printable:  # This is some more comlicated OOP. Here we create a Printable class to ensure that only things that can be printed are printed.
    def __init__(self, value: Any):  # This class takes one argument upon creation.
        # don't worry if you don't understand what `: Any` does. It doesn't do anything.
        self.value = value  # the value of value is storred in self.value. Long lines of code saying self.something = something are not uncommon in OOP.
        if isinstance(value, Printer):  # This protects us from recursion...
            self.value = value.__repr__()  # I don't know why we need it. And you don't need to know why either :)

    def __repr__(self) -> str:  # This is here in case we want to p_built() an instance of our Printable class for debug reasons...
        return str(self.value)  # Basically, when asked for a string value, it returns the string value of its value

p_built = print  # rename built in function print to p_built as recomended in PEP 3.14
# PEP stands for Python Enhancement Proposal
# If a PEP says to do something, you must do it...   or else...
# unless its PEP 8. YOu don't have to follow PEP 8


class Printer:  # This is the heart and soul of the Hello World program
    def __init__(self, id_: int, location: str|io.TextIOBase):  # We give every printer an id to help keep track of them.
        self.id = id_
        self.location = location  # like I said. Lots of self.something = something
        if isinstance(location, str):  # If the location is a string
            location =  open(location, "w")  # It is a file path, open in w mode
            self.location = location  # and save the location
        elif isinstance(location, io.TextIOBase):  # if it is a TextIOBase (whatever that is)
            self.location = location # then we don't need to open it (because the open function can't open it)
        else:  # otherwise
            self.location = sys.stdout
            warnings.warn("Corupt location. Using system default instead...", Warning)  # something funky happend
            # Just use the system default

        self.recent = None  # Used for error tracing...

    def __repr__(self) -> str:  # The string representation of the Printer class
        return f"{__class__.__name__}(id={self.id}, recent=`{self.recent}`)"
        # __class__.__name__ is Printer, unless this is used by a child class, than it is the child class's name...
    
    def __call__(self, x):  # This lets us use our class as a function
        if not isinstance(x, Printable):  # We can'tprint unprintable stuff!!!
            raise PrinterError("Can't print unprintable objects...")
        self.recent = x  # our most recently printed thingis this one
        try:  # try p_builting it
            p_built(x, file=self.location)
        except ValueError: # if that doesn't work, open the file and try again :)
            with open(self.location, "a") as location:
                p_built(x, file=location)
        return None  # return None
    
    def onexit(self):  # safety/cleanup stuff
        self.location.close()  # probably not that important...

# async!!!!  This allows us to leave a program running and then come back to it!
async def  construct_printer(output="output.txt"):  # this function passes arguemtns to Printer and than returns that instance
    return Printer(time.time(), output)  # we use the current time for the id because that will probably be unique

async def main(output_location="output.hello"):  # What pumps the heart and soul of this code
    print = await construct_printer(output=output_location)  # create an instance of Printer called print
    atexit.register(print.onexit)  # This is maybe important????
    return print  # return print



if __name__ == '__main__':  # I fthe file that is running is this one...
    print = asyncio.run(main(sys.stdout))  # Create an instance of Printer
    # The big moment!!!!!
    print(Printable("Hello, World!"))

    # we can do other stuff here as well...
    # print(Printable(print))
    # print(Printable("Hello"))
    # print(Printable(p_built))
    # print(Printable(124))



# If you understood all of the abve code, then CONGRAGULATIONS!!!
#You are well on your way to becoming an expert coder.
#   - PreciousFood