# importing packages
import cv2
import numpy as np

from kivy.lang import Builder
from kivymd.app import MDApp

from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.widget import Widget
from kivy.uix.image import Image

import tempData


# function to rename the uploaded original image
# takes in the uploaded image as input and renames
# def ogRename():
#     pass

# # function to rename the uploaded template
# def tempRename():
#     pass
# # reading the input upload original image

# OR? can we open the uploaded image directly 

main_image_path = ""
template_image_path = ""
accuracy = 50

class FirstScreen(Screen):
    pass

class ScreenWallpaper(Screen):
    pass

class MainScreen(Screen, MDApp):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.file_manager_obj_main = MDFileManager(
            select_path= self.select_path_main ,   # method of which window will open first
            exit_manager= self.exit_manager_main, # method to exit the file manager
            preview=True

        )

        self.file_manager_obj_template = MDFileManager(
            select_path= self.select_path_template ,   # method of which window will open first
            exit_manager= self.exit_manager_template, # method to exit the file manager
            preview=True

        )

    # gets the path of the file
    def select_path_main(self, path):
        
        tempData.saveMain(path)
        
        #print(path)
        
        self.exit_manager_main()

    # gets the path of the file
    def select_path_template(self, path):
        
        tempData.saveTemplate(path)
        
        #print(path)
        
        self.exit_manager_template()
        
    def open_file_manager_main(self):
        # opening file manager
        self.file_manager_obj_main.show('/')
        #self.file_manager_obj_main.show("E:\\")
    
    def open_file_manager_template(self):
        # opening file manager
        self.file_manager_obj_template.show('/')
        #self.file_manager_obj_template.show('E:\\')
    

    
    
    # method to close file manager
    def exit_manager_main(self):
        self.file_manager_obj_main.close()

    def exit_manager_template(self):
        self.file_manager_obj_template.close()
    
    def store_accuracy(self):
        # store this accuracy in external file
        acc = self.ids["accuracy"].text
        tempData.storeAccuracy(acc)


    # stores/writes/rewrites result into output.jpg
    def dispObj(self):
        # read the original image
        im_rgb = cv2.imread(tempData.readMain())

        # convert the real image into Gray scale
        im_gray = cv2.cvtColor(im_rgb, cv2.COLOR_BGR2GRAY)


        # reading the template in gray scale mode
        temp = cv2.imread(tempData.readTemplate(), 0)

        # reading the width and height
        # using -1 to invert the output as the 
        # output comes in the format of h,w.
        w, h = temp.shape[::-1]

        # matching template
        res = cv2.matchTemplate(im_gray, temp, cv2.TM_CCOEFF_NORMED)

        # setting the threshold (matching accuracy)
        # for now this value is manually set
        # later on it will be read by an object from frontend
        #threshold = 0.90

        # reading threshold from the text input


        # str is stored in the text file. 
        threshold = (tempData.readAccuracy())/100

        #threshold = self.root.get_screen('main').ids.accuracy.text

        # locating pixels only above the threshold matching
        loc = np.where( res>=threshold)  # setting condition

    
        # using zip, making w,h format for a point
        # then using for loop, going to each point
        # and drawing yellow boxes around them.
        


        # function to display the image containing object when needed
        # to get the dimension of the box: we will use
        # same dimensions of the template. We take a point
        # and the box will be of the same width and height
        # of that of the template.
        # also making boxes inside the original images (in-place)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(im_rgb, pt, (pt[0]+w, pt[1]+h), (0,255,255), 2)

        # resizing the output image according to the MDcard
        ims = cv2.resize(im_rgb, (480,480))
        #return cv2.imshow('Object found', ims)
        
        cv2.imwrite('output.jpg', ims)
        #return ims
        # # below code stops the python kernel from crashing
        # cv2.waitKey(0) 

        # cv2.destroyAllWindows()


class ResultDisp(Screen):

    def on_enter(self):
        self.output = Image(source='output.jpg')
        self.ids.result.add_widget(self.output)

    
    
    

sm = ScreenManager()

screens = [MainScreen(name= "main"),
            ResultDisp(name= "result"),
            FirstScreen(name= "first")]

for i in screens:
    sm.add_widget(i)


class MyApp(MDApp): 
    



    def build(self):
        self.theme_cls.theme_style = "Light"
        # loading my.kv file    # going to screenmanager
        return  Builder.load_file("myapp27.kv") 
    


#dispObj()

# # # below code stops the python kernel from crashing
# cv2.waitKey(0) 

# cv2.destroyAllWindows()




# if its the main file, execute the following code
if __name__ == "__main__":
    MyApp().run()