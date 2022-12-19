"""
    Module to store the temp data into a text files such as
    accuracy and file names and paths 

"""

# function to store the temporary accuracy into the text file accuracy.txt
def storeAccuracy(accuracy):
    with open("accuracy.txt","w") as file:
        file.write(accuracy)


# function to read the name of temporary accuracy from the file accuracy.txt
def readAccuracy():
    with open("accuracy.txt","r") as file:
        return float(file.read())

#print(type(readAccuracy()))

def saveMain(path):
    with open("mainImage.txt","w") as file:
        file.write(path)

def readMain():
    with open("mainImage.txt","r") as file:
        return file.read()

def saveTemplate(path):
    with open("templateImage.txt","w") as file:
        file.write(path)

def readTemplate():
    with open("templateImage.txt","r") as file:
        return file.read()


