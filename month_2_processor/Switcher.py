import os

class Switcher(object):
    def which_instruction(self, argument):
    
        # Get the method from 'self'. Default to a lambda.
        method = getattr(self, method_name, lambda: "Invalid month")
        # Call the method as we return it
        return method()
 
    def _adc(self):
        return "add with carry"
 
    def _and(self):
        return "and logic op"
 
    def _asl(self):
        return "shift left"

    #TODO all instructions
