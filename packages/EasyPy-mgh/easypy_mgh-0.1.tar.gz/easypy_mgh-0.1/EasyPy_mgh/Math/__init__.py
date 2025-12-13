from EasyPy.Math import SpecialCharacters
from EasyPy.Math import Convertions
class Number():
    def __init__(self,number:float):
        self.num=number
        pass
    def Squared(self):
        for int in range(1):
            self.num*=self.num
        return float(self.num)
    def Cubed(self):
        return self.num*self.num*self.num
    def ToThePowerOf(self,Power:float):
        SavedNumber=self.num
        self.num=1
        for i in range(Power):
            self.num*=SavedNumber
        return self.num
    
    def Add(self, add:float):
        return self.num+add
    def Subtract(self,subtract:float):
        return self.num-subtract
    def Takeaway(self,Take_Away:float):
        return self.Subtract(Take_Away)
    def Multiply(self,By:float):
        return self.num*By
    def Times(self,By:float):
        return self.Multiply(By)
    def Divied(self,By:float):
        return self.num/By
    
    def of(self,of):
        of/=100
        return of * self.num
    
    
    
    
    

