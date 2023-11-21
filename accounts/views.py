from cbmcps.settings import BASE_DIR
from django.shortcuts import render,redirect
from .forms import CustomerRegistraitonForm,LoginForm
from django.views import View
from django.contrib import messages
from .models import *
import datetime
import os.path
import os, hashlib
from pathlib import Path


# Create your views here.
# def login(request):
#     return render(request, 'Login.html')

# def register(request):
#     return render(request, 'register.html')

class CustomerRegistraitonView(View):
    def get(self,request):
        form = CustomerRegistraitonForm()
        return render(request, 'register/register.html',{'forms':form})

    def post(self,request):
        form = CustomerRegistraitonForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations... You succesufully registered ')
            form.save()
        return render(request, 'register/register.html',{'forms':form})


def changepass(request):
    return render(request, 'changepassword.html')


def homepage(request):
    return render(request, 'homepage/homepage.html')



def media(request):
    if request.method == "POST":
        print(request.FILES.get('file1'))
        newfilehash = hashlib.md5(request.FILES.get('file1').read()).hexdigest()
        print(newfilehash)
        
        if os.path.exists("media/multimedia/"+str(request.FILES.get('file1'))):
           
            messages.error(request,'File Already Exists You Are Entering Dublicate Files ')
            return redirect("media")

        elif testcheck(newfilehash):
            messages.error(request,'File Already Exists You Are Entering Dublicate Files ')
            return redirect("media")


        else:
            up = Upload()
            user = request.user
            date = datetime.datetime.today()
            up.user = user
            up.option = request.POST['option']
            up.file1 = request.FILES.get('file1')
            up.date = date
            up.save()
            messages.success(request,'Your File  succesufully Uploaded !!! ')
            return redirect("media")
      
    else:
        return render(request, "media/media.html")

 # making a dictionary named unique

def testcheck(newfilehash):
    print("test case")
    

    # files_list = os.listdir(path)  # take all the filename as a list
    path = BASE_DIR/"media/multimedia/"
    unique = dict() 
   
    for file in os.listdir(path):   # looping over the file list

        file_name = Path(os.path.join(path, file))  # make a absolute file name using os.path.join function
        if file_name.is_file():  # checking the the the item is file or not

            # A tool for creating an MD5 hash from a string
            # The Python hashlib module is an interface for hashing messages easily. This contains numerous methods which
            # will handle hashing any raw message in an encrypted format
            # hexdigest() : Returns the encoded data in hexadecimal format
            fileHash = hashlib.md5(open(file_name, 'rb').read()).hexdigest()

            if fileHash not in unique:
                unique[fileHash] = file_name
            
        else:
            print("Path not exits")
    # print(unique)

    if newfilehash in unique:
        # print("True")
        return True
    else:
        # print("False")
        return False

        



def history(request):
    his = Upload.objects.filter(user = request.user , date=datetime.datetime.today() ).order_by("-id")
    return render(request,"history.html",{"his":his})

def multimedia(request):
    his = Upload.objects.filter(user = request.user).order_by("-id")
    return render(request, "multimedia.html",{'his':his})