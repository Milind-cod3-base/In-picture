# importing packages
import cv2
import numpy as np

from kivy.lang import Builder
from kivymd.app import MDApp

from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
# from kivymd.uix.button import MDFlatButton
# from kivymd.uix.dialog import MDDialog

import os


from plyer import filechooser


Window.maximize()

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
    global main_image_path
    global template_image_path
    global accuracy

    def __init__(self, **kw):
        super().__init__(**kw)
        self.manager_open = False
        self.file_manager_obj_main = MDFileManager(
            select_path= self.select_path_main ,   # method of which window will open first
            exit_manager= self.exit_manager_main, # method to exit the file manager
            preview=True
            )
        #self.path = ""

        self.file_manager_obj_template = MDFileManager(
            select_path= self.select_path_template ,   # method of which window will open first
            exit_manager= self.exit_manager_template, # method to exit the file manager
            preview=True

        )

    # gets the path of the file
    def select_path_main(self, path):
        global main_image_path
        #tempData.saveMain(path)
        #self.path=path
        
        #print(path)
        self.ids.image.source = path
        main_image_path= path
        
        self.exit_manager_main()

        #return main_image_path

    # gets the path of the file
    def select_path_template(self, path):
        global template_image_path
        #tempData.saveTemplate(path)
        
        #print(path)
        
        template_image_path= path
        self.ids.image1.source = path
        self.exit_manager_template()

        #return template_image_path

        
    def open_file_manager_main(self):
        # opening file manager
        #self.file_manager_obj_main.show('/')
        self.file_manager_obj_main.show("E:\In-picture\Test_images")
        #self.file_manager_obj_main.show("*\Test_images")
        self.manager_open = True
        #E:\In-picture\main.py
    
    def open_file_manager_template(self):
        # opening file manager
        #self.file_manager_obj_template.show('/')
        self.file_manager_obj_template.show('E:\In-picture\Test_images')
        
        self.manager_open = True
    

    
    
    # method to close file manager
    def exit_manager_main(self):
        self.file_manager_obj_main.close()

    def exit_manager_template(self):
        self.file_manager_obj_template.close()
    
    def store_accuracy(self):
        global accuracy
        # store this accuracy in external file
        #accuracy = self.ids["accuracy"].text

        accuracy = self.ids.progress_slider.value
        #tempData.storeAccuracy(acc)
        return accuracy

    def dialog_callback(self, *args):
        self.dialog.dismiss()

    # stores/writes/rewrites result into output.jpg
    def dispObj(self):

        # read the original image
        im_rgb = cv2.imread(main_image_path)
        
        # convert the real image into Gray scale
        im_gray = cv2.cvtColor(im_rgb, cv2.COLOR_BGR2GRAY)


        # reading the template in gray scale mode
        temp = cv2.imread(template_image_path, 0)

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
        threshold = (accuracy)/100
        #threshold = accuracy
        #threshold = self.root.get_screen('main').ids.accuracy.text

        # locating pixels only above the threshold matching
        loc = np.where( res>=threshold)  # setting condition

    
        # using zip, making w,h format for a point
        # then using for loop, going to each point
        # and drawing yellow boxes around them.
        

        if loc[0].size == 0:
            self.dialog = MDDialog(title="Error", 
                     text="Template not found in the image", 
                     size_hint=(0.8, 0.5))

                     
                     #events_callback = self.dialog.dismiss())
            self.dialog.open()
            #self.dialog.dismiss()

        else:



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
    # def dialog_callback(self, *args):
    #     self.dialog.dismiss()



    def dispResult(self):
        self.ids.image2.source = 'output.jpg'
        self.ids.image2.reload()
        # shutil.copy("output.jpg","output1.jpg")
        # self.ids.image2.source = "output1.jpg"
        # os.remove('E:\In-picture\output1.jpg')

    # def show_alert_dialog(self):
    #     if not self.dialog:
    #         self.dialog = MDDialog(
    #             text="Discard draft?",
    #             buttons=[
    #                 MDFlatButton(
    #                     text="CANCEL",
    #                     theme_text_color="Custom",
    #                     text_color=self.theme_cls.primary_color,
    #                 ),
    #                 MDFlatButton(
    #                     text="DISCARD",
    #                     theme_text_color="Custom",
    #                     text_color=self.theme_cls.primary_color,
    #                 ),
    #             ],
    #         )
    #     self.dialog.open()
        


# class ResultDisp(Screen):
#     pass

#     def on_enter(self):
#         self.output = Image(source='output.jpg')
#         self.ids.result.add_widget(self.output)

    
    
    

# sm = ScreenManager()

# screens = [MainScreen(name= "main")
#             #ResultDisp(name= "result"),
#             #FirstScreen(name= "first")]

# for i in screens:
#     sm.add_widget(i)

class ScreenWallpaper(BoxLayout):
    pass
class WindowManager(ScreenManager):
    pass


class MainApp(MDApp): 
    
    def __init__(self, **kwargs):
        self.title = "In Picture by SHRESTH SHARMA(12201944), DHARMESH PATEL(12203573), MILIND MILIND(12200002), AAYUSH SURANA(12200044), JAYDIP BORAD(12203473)"
        super().__init__(**kwargs)


    def build(self):
        global sm
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return Builder.load_file("myappnew.kv") 
 
    


#dispObj()

# # # below code stops the python kernel from crashing
# cv2.waitKey(0) 

# cv2.destroyAllWindows()




# if its the main file, execute the following code
if __name__ == "__main__":
    MainApp().run()
    
