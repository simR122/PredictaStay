import traceback # lib for tracking errors
import sys #system lib

class CustomException(Exception): #inherit from predefined Exception class because we are just adding some on top of it.

    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message) #inherit: show exception iff that error msg doesn't exist in parent fn
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod #make this fn independent of creating Custom class everytime to show messages
    def get_detailed_error_message(error_message, error_detail:sys): #: means error_details belong to sys
        
        #error msg have 3 things and we need only last thing, i.e traceback
        _, _, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename #to display the filename having error
        line_number = exc_tb.tb_lineno
        #f-string,feature in Python used for string interpolation
        return f"Error in{file_name}, line{line_number} : {error_message}"
    
    # "Magic fn"The str function is called when you attempt to print an object or convert it into a string using str()...String_Interpretation
    def __str__(self):
        return self.error_message
    
# # Testing.py file for confirming it works fine.
# from src.logger import get_logger 
# from src.custom_exception import CustomException 
# import sys 

# logger = get_logger(__name__) 

# def divide_number(a,b): 
#     try: 
#         result = a/b 
#         logger.info("dividing two numbers")
#         return result
#     except Exception as e:
#         logger.error("Error occured")
#         raise CustomException("Custom Error zero", sys) #used static fn without creating object
    
# if __name__=="__main__":
#     try:
#         logger.info("Starting main program")
#         divide_number(10,0)
#     except CustomException as ce:
#         logger.error(str(ce))#for string interpretation of error
