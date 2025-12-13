PrintMode=True
def XYZ(x,y,z):
    return (x,y,z)
def XY(x,y):
    return (x,y)
class Convert():
    def __init__(self, argument):
        self.arg=argument

    def XYZ_to_string(self,stringToChange:str):
        """Convert XYZ to String
        -
        this will convert a tuple into a str, This convertion allows you to do:
        "This is x, y, z" 
        make sure you have an "1"=X,"2"=Y,"3"=Z in your string in order for it to work"""
        String=""
        List=[]
        List_Num=0
        for s in stringToChange:
            List.append(s)
        for S in List:
            if S=="1":
                List[List_Num]=self.arg[0]
            if S=="2":
                List[List_Num]=self.arg[1]
            if S=="3":
                List[List_Num]=self.arg[2]
            
            List_Num+=1
        for S in List:
            String+=str(S)
        return String
    def XYZ_ints_to_tuple(self,x,y,z):
        return (x,y,z)
    def XYZ_list_to_tuple(self):
        x=self.arg[0]
        y=self.arg[1]
        z=self.arg[2]
        return (x,y,z)
    def XYZ_list_to_string(self,stringToChange:str):
        """Convert XYZ to String
        -
        this will convert a tuple into a str, This convertion allows you to do:
        "This is x, y, z" 
        make sure you have an "1"=X,"2"=Y,"3"=Z in your string in order for it to work"""
        String=""
        List=[]
        List_Num=0
        for s in stringToChange:
            List.append(s)
        for S in List:
            if S=="1":
                List[List_Num]=self.arg[0]
            if S=="2":
                List[List_Num]=self.arg[1]
            if S=="3":
                List[List_Num]=self.arg[2]
            
            List_Num+=1
        for S in List:
            String+=str(S)
        return String
    
    def XYZ_tuple_to_string(self,stringToChange:str):
        """Convert XYZ to String
        -
        this will convert a tuple into a str, This convertion allows you to do:
        "This is x, y, z" 
        make sure you have an "x"=X,"y"=Y in your string in order for it to work"""
        String=""
        List=[]
        List_Num=0
        for s in stringToChange:
            List.append(s)
        for S in List:
            if S=="1":
                List[List_Num]=self.arg[0]
            if S=="2":
                List[List_Num]=self.arg[1]
            if S=="3":
                List[List_Num]=self.arg[2]
            List_Num+=1
        for S in List:
            String+=str(S)
        return String
    def XY_ints_to_tuple(self,x,y):
        return (x,y)
    def XY_list_to_tuple(self):
        x=self.arg[0]
        y=self.arg[1]
        return (x,y)
    def XY_list_to_string(self,stringToChange:str):
        """Convert XYZ to String
        -
        this will convert a tuple into a str, This convertion allows you to do:
        "This is x, y" 
        make sure you have an "1"=X,"2"=Y in your string in order for it to work"""
        String=""
        List=[]
        List_Num=0
        for s in stringToChange:
            List.append(s)
        for S in List:
            if S=="1":
                List[List_Num]=self.arg[0]
            if S=="2":
                List[List_Num]=self.arg[1]
            
            List_Num+=1
        for S in List:
            String+=str(S)
        return String
    


