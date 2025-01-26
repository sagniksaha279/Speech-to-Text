import speech_recognition as sr
import pyttsx3 as pt
import pywhatkit as pw
from Phonedatabase import phone_book
import datetime as dt
import qrcode as qr
from gtts import gTTS


recognizer = sr.Recognizer()

def sendWhatsappMessage(text_read):
    text_read = text_read.lower()    
    
    #trace out name
    subStr = "to"
    name = text_read.split(subStr)[1]
    name = name.strip()   
    name_list = list(phone_book.keys())
    if(name not in name_list):
        print("Name is not present in our database")
        name_new_entered = input("Please again,enter the name:")
        if(name_new_entered not in name_list):
            print(f"Sorry {name} is not present in our database")
            return
        else:
            name = name_new_entered
    phone_no = "+91" + str(phone_book[name])
    
    #trace out message
    message_to_sent = text_read.split(subStr)[0]
    message_to_sent = message_to_sent.replace("send ","")
    
    #trace current hour and minute
    hour = dt.datetime.now().hour
    minute = dt.datetime.now().minute
    if(minute==0):
        minute +=1 
    
    pw.sendwhatmsg(phone_no,message_to_sent,hour,minute+1)
    print("Message sent")
    
def makeQrCode(text_read):
    subStr = "of"
    text_read = text_read.split(subStr)[1]
    img = qr.make(text_read)
    img.save("new2.jpg")
    print("QR CODE SUCCESFULLY CREATED")

def makeSpeech(text_read):
    language = "en"
    
    subStr = "for"
    text_read = text_read.split(subStr)[1]
    
    speech = gTTS(text=text_read, lang=language, slow=False, tld="co.uk")
    speech.save("TextToSpeech.mp3")
    print("MP3 version succesfully created")
    

#MAIN WORK    
print("\n1.To sent a whatsapp message say--> send {(message)} to {name(desired contact)} if it exists in our database")
print("2.To create qr code of any text say--> make qr code of {(your desired message)}")
print("3.Want to save your text into a speech or mp3  version say--> make a speech for {(your desired message)}")
print("\n***** Say :) Stop :) to end the process and now start to speak *****\n")


process = "no"
while process!="yes" or process!="Yes":
    process = input("Shall we start the process(yes/no):")
    if(process=="yes" or process=="Yes"):
        break



while True:
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic,duration=0.4)
            print("Voice:")
            audio = recognizer.listen(mic)
            
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print(f"Your text is:{text}")
            if("stop" in text):
                break
            with open("recognize.txt","w+") as f:
                f.write(text)

            with open("recognize.txt","r") as f:
                text_read = f.read()
                text_read = text_read.lower()
                if("send" in text_read and "to" in text_read):
                    sendWhatsappMessage(text_read)
                elif("make qr code of" in text_read):
                    makeQrCode(text_read)
                elif("make a speech for" in text_read):
                    makeSpeech(text_read)
                    
    except sr.UnknownValueError():
        print("Sorry, I did not get that")

print("Thank You for using our speech converter")
