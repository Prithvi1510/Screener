import re 
import sys
'''
Marketcapitalization > 500 AND
    Pricetoearning < 15 AND
      Returnoncapitalemployed > 22% '''

def checkOperatorCondition(parameter,operator,digit):  
    operatorsList = ["<" , "<=" , ">" , "=>" , "==" ]
    if(operator == operatorsList[0]): 
        return(parameter < digit)
    
    if(operator == operatorsList[1]): 
        return(parameter <= digit)
    
    if(operator == operatorsList[2]):
        return(parameter > digit)
    
    if(operator == operatorsList[3]): 
        return(parameter >= digit)
    
    if(operator == operatorsList[4]): #check for floating point have an epsilon of error here 
        return(parameter == digit)

def checkConditional(condition1 , conditionalString , condition2): 
    if(conditionalString == "AND"): 
        return(condition1 and condition2)
    
    if(conditionalString == "OR"):
        return(condition1 or condition2)



class Query(): 

    def __init__(self,query):
        self.conditionals = [] # AND OR 
        self.operators = [] # [< , <= , < , <= , == ]
        self.digit = [] #float
        self.parameter = []  #the name of the type of the parameter
        self.queryList = []
        #self.mistakeList = [] 
        self._originalQuery = query
        self.TruthTable = [] 
    
    


    def preprocessString(self): 
        query = self._originalQuery 
        query = query.replace("\n", "")
        query = " ".join(query.split())
        return(list(query.split(" ")))


    def checkAlphanumeric(self,string): 
        if(string.isalnum or string.isalpha): 
            self.parameter.append(string.upper())
            return True 
        else: 
            print((string +  " is not alphabhet/alphanumeric or not in the right position"))
            return False 
    
    def checkFloat(self,string): 
        if(string[-1] == '%' and string[-2].isdigit()): 
            if(string[:-1].isdigit()):
                self.digit.append(float(string[:-1])/100) 
                return True
            else: 
                print(string + " Not a Digit or Percentage")
                return False 
            
        if(string.isdigit()):
            self.digit.append(float(string))
            return True
        elif(string.isalnum() or string.isalpha()):
            if(self.isDigitStringValid(string)): #Value is appended in the fucntion
                return True 
            else: 
                return False 


        
    def checkOperations(self,string):
        operatorsList = ["<" , "<=" , ">" , "=>" , "==" ]
        if (string in operatorsList):
            self.operators.append(string)
            return True 
        else: 
            print(string + " Not an oprator or not in right place")

        pass 

    def checkConditional(self,string):
        conditionals = ["AND", "OR"]
        if(string.upper() in conditionals):
            self.conditionals.append(string.upper()) 
            return True 
        else: 
            print(string + "Not an conditional or not in right place")
            return False 
    

    def populate(self): 
        self.queryList = self.preprocessString()
        pointer = 0 
        functionList = [self.checkAlphanumeric,self.checkOperations,self.checkFloat,self.checkConditional] 
        for i in range(0,len(self.queryList)): 
            if(pointer > 3 ): pointer = 0 
            function = functionList[pointer]
            pointer += 1 
            if(function(self.queryList[i]) != True ): #every function from functionList must return a boolean value
                return False
        return True
    

    def isDigitStringIsValid(self,string):
        #Method to check if your digig is a string and not a float example bearish or Bullish 
        keyList = {"BULLISH": True , "BEARISH" : False 
                   , "TRUE" : True , "FALSE" : False } #Once keyList is long enough load through a json or pckl file 
        duplicateString  = string.upper()
        try:
            self.digit.append(keyList[duplicateString])
            return True
        except KeyError:
            print("Invalid Key:",string)
            return False
        except Exception as e:
            print('Error',e)
            return False 
    

    def evaluateOperator(self,stockData): 
        for index in range(0,len(self.parameter)):
            try: 
                parameter = float(stockData.trimmedData[self.parameter[index]][0])    
            except (KeyError,IndexError) as e : 
                print("Parameter Does not Exist \n" ,e)
                sys.exit(1)
            except Exception as e:
                print(parameter," does not exist")
                sys.exit(1)

            self.TruthTable.append(checkOperatorCondition(parameter = parameter,operator = self.operatorList[index],
                                   digit = self.digit[index]))
        
        condition = True

        for i in range(0,len(self.conditionals)):
            condition = condition and checkConditional(condition1= self.conditionals[i],conditionalString=self.conditionals[i] 
                             ,condition2= self.conditionals[i+1])
        
        return condition 

        



string13 = Query(query= '''
    Returnoninvestedcapital > 25 and
    Earningsyield > 15 and
    Bookvalue > 0 AND
    MarketCapitalization > 15
''')

string13.populate()