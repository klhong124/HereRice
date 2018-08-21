from tkinter import *
import tkinter.messagebox
import pymysql
db = pymysql.connect('localhost','root','','hererice',autocommit=True)
#db = pymysql.connect('175.159.85.220','hererice','hererice','hererice',autocommit=True)
cursor = db.cursor()
class TitleBar:#*********************************************************************************************************

    def __init__(self, master):

        #Title Bar Config
        self.titlebar = Menu(master)
        master.config(menu = self.titlebar)

        #Items showed on Title Bar(HereRice...etc)
        self.HereRice_menu = Menu(self.titlebar)
        self.Help_menu = Menu(self.titlebar)

        #Details in HereRice(Title Bar)
        self.titlebar.add_cascade(label = 'HereRice',menu = self.HereRice_menu)
        self.HereRice_menu.add_command(label = 'About HereRice',command = self.aboutHereRice)
        self.HereRice_menu.add_separator()
        self.HereRice_menu.add_command(label = 'Exit',command = self.titlebar.quit)

        #Details in HereRice(Title Bar)
        self.titlebar.add_cascade(label = 'Help',menu = self.Help_menu)

    #def command function
    def aboutHereRice(self):
        tkinter.messagebox.showinfo('About HereRice','HereRice is written by All Boy Ltd.')

class LoginPage:#********************************************************************************************************

    def __init__(self, master):

        global userID
        global open_shop
        open_shop=IntVar()
        open_shop.set(1)
        userID = None
        username = None
        password = None
        #Organizing Main Frame Layout
        self.topFrame = Frame (master)
        self.topFrame.pack()

        self.bottomFrame = Frame(master)
        self.bottomFrame.pack()

        #Top Frame
        self.photo_logo=PhotoImage(file = 'LOGIN.png')
        self.hello_label = Label(self.topFrame, image = self.photo_logo)
        self.hello_label.pack()

        #Bottom Frame
        self.username_label = Label(self.bottomFrame, text = 'Username')
        self.username_label.grid(row = 0, sticky = E)
        try:
            file = open("rememberme.txt","r")
            username = StringVar(value=file.readlines()[0].split())
            file.close()
        except IndexError :
            pass
        self.username_entry = Entry(self.bottomFrame,textvariable=username)
        self.username_entry.grid(row = 0, column = 1)
        #Password
        self.password_label = Label(self.bottomFrame, text = 'Password')
        self.password_label.grid(row = 1, sticky = E)
        try:
            file = open("rememberme.txt","r")
            password = StringVar(value=file.readlines()[1])
            file.close()
        except IndexError :
            pass
        self.password_entry = Entry(self.bottomFrame,textvariable=password,show = '*')
        self.password_entry.grid(row = 1, column = 1)
        #Remember Me
        self.rememberme_variable = BooleanVar()
        file = open("rememberme.txt","r")
        if file.read() == '':
            self.rememberme_variable.set(False)
        else:
            self.rememberme_variable.set(True)
        file.close()
        self.rememberme_checkbutton = Checkbutton(self.bottomFrame,text = 'Remember me',variable = self.rememberme_variable)
        self.rememberme_checkbutton.grid(row = 2,columnspan=2)
        #Login Button
        self.login_button = Button(self.bottomFrame,text = 'Log in',command = self.readLoginInfo)
        self.login_button.grid(row = 3,columnspan=2,sticky = E,ipadx=55)
        #Sign Up Button
        self.signup_button = Button(self.bottomFrame,text = 'Sign up',command = self.toRegisterPage)
        self.signup_button.grid(row = 4,columnspan=2,sticky = E,ipadx=51)

        #Keyboard events
        master.unbind('<Return>')
        master.bind('<Return>',self.pressEnter)

    #def function
    def pressEnter(self,event):
        self.login_button.invoke()

#     def checkbuttonCommand(self):
#         if self.rememberme_variable.get() :
#             print('remember_me:'+str(self.rememberme_variable.get()))
#         else :
#             print('remember_me:'+str(self.rememberme_variable.get()))

    def readLoginInfo(self):
        global userID
        #print ('^^^^^^^^^test^^^^^^^^^')
        #print('username:\t'+self.username_entry.get())
        #print('password:\t'+self.password_entry.get())
        #print('remember_me:\t'+str(self.rememberme_variable.get()))
        #print ('vvvvvvvvvvvvvvvvvvvvvv')
        #Check Remember Button
        if self.rememberme_variable.get():
            file = open("rememberme.txt","w")
            file.write(self.username_entry.get()+"\r")
            file.write(self.password_entry.get())
            file.close()
        else:
            file = open("rememberme.txt","w")
            file.close()
        #Connet DB Here
        self.login_system()
        if userIDcheck:
            if (self.username_entry.get() == read_login_system[1] and self.password_entry.get() == read_login_system[4]):
                self.user_info(userID)

                if read_login_system[5]:
                        self.toHomePage()
                else:
                    self.UpdateShopInfo()
            else :
                tkinter.messagebox.showerror('Login Failed','Sorry, your password was incorrect. Please double-check your password.')
        else:
            tkinter.messagebox.showerror('Login Failed','Sorry, your user-name was incorrect. Please click Sign Up.')
    def user_info(self,userID):
        global read_user_info
        cursor.execute("SELECT * FROM `user_info` WHERE `User_ID`='"+userID+"'")
        for read_user_info in cursor:
            read_user_info=read_user_info
    def login_system(self):
        global userIDcheck
        global read_login_system
        global userID
        userIDcheck = cursor.execute("SELECT * FROM `login_system` WHERE `User_Name`='"+self.username_entry.get()+"'")
        if userIDcheck:
            for read_login_system in cursor:
                userID=str(read_login_system[0])
                #print(userID)
                #print(read_login_system)
    def toHomePage(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return HomePage(root)
    def UpdateShopInfo(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return UpdateShopInfo(root)
    def toRegisterPage(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return RegisterPage(root)

class HomePage:#*************************************************************************************************************

    def __init__(self,master):

        global open_shop
        open_shop.set(0)

        cursor.execute("SELECT * FROM `user_info` WHERE `User_ID`='"+userID+"'")
        for read_user_info in cursor:
            read_user_info=read_user_info

        #Organizing Main Frame Layout
        self.topFrame = Frame (master)
        self.topFrame.pack()

        self.bottomFrame = Frame(master)
        self.bottomFrame.pack()

        #Top Frame
        self.photo_logo=PhotoImage(file = 'HOMEPAGE.png')
        self.hello_label = Label(self.topFrame, image = self.photo_logo)
        self.hello_label.pack()

        #Bottom Frame
        self.text='Welcome back,'+read_user_info[2]+" "+read_user_info[1]+"\nplease select:"
        self.login_label = Label(self.bottomFrame,text=self.text)
        self.login_label.pack(fill=X,anchor=W)
        self.edit_button = Button(self.bottomFrame,text = 'Edit Mode',command = self.setGoing_edit)
        self.edit_button.pack(fill=X)
        self.updateshopinfo_button = Button(self.bottomFrame,text = 'Update Shop Info',command = self.setGoing_update)
        self.updateshopinfo_button.pack(fill=X)
        self.updateuserinfo_button = Button(self.bottomFrame,text = 'Update User Info',command = self.toRegisterPage)
        self.updateuserinfo_button.pack(fill=X)
        self.changepassword_button = Button(self.bottomFrame,text = 'Change Password',command = self.toChangePassword)
        self.changepassword_button.pack(fill=X)
        self.logout_button = Button(self.bottomFrame, text = 'Log Out',command = self.toLoginPage)
        self.logout_button.pack(fill=X)

    def setGoing_edit(self):
        global Going
        Going = "Edit"
        self.toSelectShop()
    def setGoing_update(self):
        global Going
        Going = "Update"
        self.toSelectShop()
    def toSelectShop(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return SelectShop(root)
    def toRegisterPage(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return RegisterPage(root)
    def toChangePassword(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return ChangePassword(root)
    def toLoginPage(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return LoginPage(root)
class ChangePassword:#*******************************************************************************************************

    def __init__(self,master):
        #Organizing Main Frame Layout
        self.topFrame = Frame (master)
        self.topFrame.pack()

        self.bottomFrame = Frame(master)
        self.bottomFrame.pack()

        #Top Frame
        self.photo_logo=PhotoImage(file = 'HOMEPAGE.png')
        self.hello_label = Label(self.topFrame, image = self.photo_logo)
        self.hello_label.pack()

        #Bottom Frame
        self.changepassword_label = Label(self.bottomFrame,text="Change Password:")
        self.changepassword_label.grid(row = 0, columnspan = 3)
        #Current Password
        self.current_password_label = Label(self.bottomFrame, text = 'Current Password :')
        self.current_password_label.grid(row = 1,sticky = E)
        self.current_password_entry = Entry(self.bottomFrame,show = '*')
        self.current_password_entry.grid(row = 1,column = 1)
        #New Password
        self.new_password_label = Label(self.bottomFrame, text = 'New Password :')
        self.new_password_label.grid(row = 2, sticky = E)
        self.new_password_entry = Entry(self.bottomFrame,show = '*')
        self.new_password_entry.grid(row = 2, column = 1)
        #RetypePassword
        self.retypepassword_label = Label(self.bottomFrame, text = 'Retype Password :')
        self.retypepassword_label.grid(row = 3, sticky = E)
        self.retypepassword_entry = Entry(self.bottomFrame,show = '*')
        self.retypepassword_entry.grid(row = 3, column = 1)
        #Confirm Button
        self.confirm_button = Button(self.bottomFrame, text = 'Confoirm',command = self.readEntry)
        self.confirm_button.grid(row = 10, columnspan=3,ipadx=51)
        #Go Back Button
        self.goback_button = Button(self.bottomFrame, text = 'Go back',command = self.toHomePage)
        self.goback_button.grid(row = 11,columnspan=3,ipadx=55)

        #Keyboard events
        master.unbind('<Return>')
        master.bind('<Return>',self.pressEnter)

    #def function
    def pressEnter(self,event):
        self.confirm_button.invoke()
    def readEntry(self):
        self.checkEntry()
        if checkresult:
            cursor.execute("UPDATE `login_system` SET `password` = '"+self.new_password_entry.get()+"' WHERE `login_system`.`user_id` ="+userID)
            tkinter.messagebox.showinfo('Updated','Success! Your Password have been changed.')
            self.toHomePage()
    def checkEntry(self):
        global checkresult
        checkresult = True
        #Old Password
        cursor.execute("SELECT * FROM `login_system` WHERE `User_id`='"+userID+"'")
        for read_password in cursor:
            self.oldpassword = read_password[4]
        #print(self.oldpassword)
        if self.oldpassword != self.current_password_entry.get():
            tkinter.messagebox.showerror('Update Failed','Current password is incorrect.')
            checkresult = False
        #Password
        if self.new_password_entry.get() =="" and self.retypepassword_entry.get() =="":
            tkinter.messagebox.showerror('Failed','You must Set a Password.')
            checkresult = False
        elif self.retypepassword_entry.get() != self.new_password_entry.get():
            tkinter.messagebox.showerror('Failed','The two password fields didn\'t match.')
            checkresult = False
    def toHomePage(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return HomePage(root)

class RegisterPage:#*********************************************************************************************************

    def __init__(self, master):

        global userID
        global new_user
        new_user = BooleanVar()
        if userID == None:
            new_user.set(True)
        else:
            new_user.set(False)
        if not new_user.get():
            cursor.execute("SELECT * FROM `login_system` WHERE `user_id`='"+userID+"'")
            for login_Info_old in cursor:
                login_Info_old = login_Info_old
            cursor.execute("SELECT * FROM `user_info` WHERE `user_id`='"+userID+"'")
            for user_Info_old in cursor:
                user_Info_old = user_Info_old
        #Organizing Master Layout
        self.topFrame = Frame(master)
        self.topFrame.pack()

        self.bottomFrame = Frame(master)
        self.bottomFrame.pack()

        #Top Frame
        self.photo_logo=PhotoImage(file = 'HOMEPAGE.png')
        self.hello_label = Label(self.topFrame, image = self.photo_logo)
        self.hello_label.pack()

        #BottomFrame
        if new_user.get():
            self.heading_label = Label(self.bottomFrame,text = 'Create an account')
        else:
            self.heading_label = Label(self.bottomFrame,text = 'Update User Infromation')
        self.heading_label.grid(row = 0,columnspan = 2)
        #Name
        self.firstname_label = Label(self.bottomFrame, text = 'Firstname :')
        self.firstname_label.grid(row = 1, sticky = E)
        if new_user.get():
            self.firstname_entry = Entry(self.bottomFrame)
        else:
            firstname_entry = StringVar(value=user_Info_old[2])
            self.firstname_entry = Entry(self.bottomFrame,textvariable=firstname_entry)
        self.firstname_entry.grid(row = 1, column = 1)
        self.surname_label = Label(self.bottomFrame, text = 'Surname :')
        self.surname_label.grid(row = 2, sticky = E)
        if new_user.get():
            self.surname_entry = Entry(self.bottomFrame)
        else:
            surname_entry = StringVar(value=user_Info_old[1])
            self.surname_entry = Entry(self.bottomFrame,textvariable=surname_entry)
        self.surname_entry.grid(row = 2, column = 1)
        #Gender
        self.gender_label = Label(self.bottomFrame, text = 'Gender :')
        self.gender_label.grid(row = 3, sticky = E)
        self.gender_variable = StringVar()
        if new_user.get():
            self.gender_variable.set('male')
        else:
            self.gender_variable.set(user_Info_old[3])
        self.gender_radiobutton = Radiobutton(self.bottomFrame,text = 'Male',variable = self.gender_variable,value = 'male')
        self.gender_radiobutton.grid(row = 3,column=1,columnspan=2,sticky = W)
        self.gender_radiobutton = Radiobutton(self.bottomFrame,text = 'Female',variable = self.gender_variable,value = 'female')
        self.gender_radiobutton.grid(row = 3,column=1,columnspan=2,sticky = E)
        #Brithdate
        self.birthdate_label = Label(self.bottomFrame, text = 'Birthdate :')
        self.birthdate_label.grid(row = 4, sticky = E)

        self.year_list = list(range(2018,1960,-1))
        self.birthyear_variable = IntVar()
        if new_user.get():
            self.birthyear_variable.set(2000)
        else:
            self.birthyear_variable.set(int(str(user_Info_old[4]).split('-')[0]))
        self.birthyear = OptionMenu(self.bottomFrame, self.birthyear_variable, *self.year_list)
        self.birthyear.grid(row = 4, column = 1,columnspan=2,sticky = W)

        self.month_list = list(range(1, 12))
        self.birthmonth_variable = IntVar()
        if new_user.get():
            self.birthmonth_variable.set(1)
        else:
            self.birthmonth_variable.set(int(str(user_Info_old[4]).split('-')[1]))
        self.birthmonth = OptionMenu(self.bottomFrame, self.birthmonth_variable, *self.month_list)
        self.birthmonth.grid(row = 4, column = 1,columnspan=2)

        self.day_list = list(range(1, 31))
        self.birthday_variable = IntVar()
        if new_user.get():
            self.birthday_variable.set(1)
        else:
            self.birthday_variable.set(int(str(user_Info_old[4]).split('-')[2]))
        self.birthday = OptionMenu(self.bottomFrame, self.birthday_variable, *self.day_list)
        self.birthday.grid(row = 4, column = 1,columnspan=2,sticky = E)

        #Username
        if new_user.get():
            self.username_label = Label(self.bottomFrame, text = 'Username :')
            self.username_label.grid(row = 5, sticky = E)
            self.username_entry = Entry(self.bottomFrame)
            self.username_entry.grid(row = 5, column = 1)
        #Email
        self.email_label = Label(self.bottomFrame, text = 'Email :')
        self.email_label.grid(row = 6, sticky = E)
        if new_user.get():
            self.email_entry = Entry(self.bottomFrame)
        else:
            email_entry = StringVar(value=login_Info_old[3])
            self.email_entry = Entry(self.bottomFrame,textvariable=email_entry)
        self.email_entry.grid(row = 6, column = 1)
        #Phone Number
        self.phone_label = Label(self.bottomFrame, text = 'Phone :')
        self.phone_label.grid(row = 7, sticky = E)
        if new_user.get():
            self.phone_entry = Entry(self.bottomFrame)
        else:
            phone_entry=IntVar(value=login_Info_old[2])
            self.phone_entry = Entry(self.bottomFrame,textvariable=phone_entry)
        self.phone_entry.grid(row = 7, column = 1)
        #Password
        if new_user.get():
            self.password_label = Label(self.bottomFrame, text = 'Password :')
            self.password_label.grid(row = 8, sticky = E)
            self.password_entry = Entry(self.bottomFrame,show = '*')
            self.password_entry.grid(row = 8, column = 1)
            #RetypePassword
            self.retypepassword_label = Label(self.bottomFrame, text = 'Retype Password :')
            self.retypepassword_label.grid(row = 9, sticky = E)
            self.retypepassword_entry = Entry(self.bottomFrame,show = '*')
            self.retypepassword_entry.grid(row = 9, column = 1)
        #Register Button
            self.register_button = Button(self.bottomFrame, text = 'Register',command = self.readEntry)
        else:
            self.register_button = Button(self.bottomFrame, text = 'Update',command = self.readEntry)
        self.register_button.grid(row = 10, columnspan=3,sticky = E,ipadx=55)
        #Go Back Button
        if new_user.get():
            self.goback_button = Button(self.bottomFrame, text = 'Go back',command = self.toLoginPage)
        else:
            self.goback_button = Button(self.bottomFrame, text = 'Go back',command = self.toHomePage)
        self.goback_button.grid(row = 11,columnspan=3,sticky = E,ipadx=55)

        #Keyboard events
        master.unbind('<Return>')
        master.bind('<Return>',self.pressEnter)

    #def function
    def pressEnter(self,event):
        self.register_button.invoke()

    def readEntry(self):
        global userID
        self.birthdate_entry = str(self.birthyear_variable.get())+"-"+str(self.birthmonth_variable.get())+"-"+str(self.birthday_variable.get())
        #print ('^^^^^^^^^^test^^^^^^^^^^')
        #print ('fullname:\t'+self.surname_entry.get()+' '+self.firstname_entry.get())
        #print ('username:\t'+self.username_entry.get())
        #print ('email:\t\t'+self.email_entry.get())
        #print ('phone:\t\t'+self.phone_entry.get())
        #print ('password:\t'+self.password_entry.get())
        #print ('repassword:\t'+self.retypepassword_entry.get())
        #print ('gender:\t\t'+self.gender_variable.get())
        #print ('birth_date:\t'+ self.birthdate_entry)
        #print('vvvvvvvvvvvvvvvvvvvvvvvvv')
        self.checkEntry()
        if checkresult:
            if new_user.get():
                #print("ok")
                cursor.execute("INSERT INTO `login_system` (`User_ID`, `User_Name`, `phone`, `Email`,`Password`,`owner`)"
                           "VALUES (NULL, '"+self.username_entry.get()+"', '"+self.phone_entry.get()+"', '"+self.email_entry.get()+"', '"+self.password_entry.get()+"','0');")
                cursor.execute("SELECT * FROM `login_system` WHERE `User_Name`='"+self.username_entry.get()+"'")
                for read_login_system in cursor:
                    userID=str(read_login_system[0])
                cursor.execute("INSERT INTO `user_info` (`User_ID`, `surname`, `first_name`, `Gender`,`birthday`)"
                           "VALUES ('"+userID+"', '"+self.surname_entry.get()+"', '"+self.firstname_entry.get()+"', '"+self.gender_variable.get()+"', '"+self.birthdate_entry+"');")
                tkinter.messagebox.showinfo('SignUp','Success! Now return to login Page.')
                cursor.execute("INSERT INTO `shop_menu` (`shop_id`,`menu_id`,`menu_name`,`set_or_not`)"
                               "VALUES ('"+shopID+"',NULL,'Drink Menu','0');")
                self.toLoginPage()
            else:
                #print("OK?")
                cursor.execute("UPDATE `login_system` SET `phone` = '"+self.phone_entry.get()+"',`Email`='"+self.email_entry.get()+"' WHERE `login_system`.`user_id` = "+userID)
                cursor.execute("UPDATE `user_info` SET `surname` = '"+self.surname_entry.get()+"',`birthday` = '"+self.birthdate_entry+"',`Gender` = '"+self.gender_variable.get()+"',`first_name`='"+self.firstname_entry.get()+"' WHERE `user_info`.`user_id` = "+userID)
                tkinter.messagebox.showinfo('Updated','Success! Now return to Home Page.')
                self.toHomePage()
    def checkEntry(self):
        global checkresult
        checkresult = True
        #User Name
        try:
            if self.username_entry.get() =="":
                tkinter.messagebox.showerror('SignUp Failed','You must Enter a User Name.')
                checkresult = False
        except AttributeError:
            pass
        #Phone Number
        try:
            if len(str(int(self.phone_entry.get()))) != 8:
                tkinter.messagebox.showerror('SignUp Failed','Please check your phone number.')
                checkresult = False
        except ValueError:
            tkinter.messagebox.showerror('SignUp Failed','Please check your phone number.')
            checkresult = False
        #Password
        try:
            if self.password_entry.get() =="" and self.retypepassword_entry.get() =="":
                tkinter.messagebox.showerror('SignUp Failed','You must Set a Password.')
                checkresult = False
            elif self.retypepassword_entry.get() != self.password_entry.get():
                tkinter.messagebox.showerror('SignUp Failed','The two password fields didn\'t match.')
                checkresult = False
        except AttributeError:
            pass
    def toHomePage(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return HomePage(root)
    def toLoginPage(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return LoginPage(root)

class UpdateShopInfo:#*********************************************************************************************************

    def __init__(self, master):

        global new_shop
        global open_shop
        global shop_info_old
        try:
            cursor.execute("SELECT * FROM `shop_info` WHERE `shop_id`='"+shopID+"'")
            for shop_info_old in cursor:
                shop_info_old = shop_info_old
#         print(shop_info_old)
        except NameError:
            pass

        #Organizing Master Layout
        self.topFrame = Frame (master)
        self.topFrame.pack()

        self.bottomFrame = Frame(master)
        self.bottomFrame.pack()

        #Top Frame
        self.photo_logo=PhotoImage(file = 'HOMEPAGE.png')
        self.hello_label = Label(self.topFrame, image = self.photo_logo)
        self.hello_label.pack()

        #BottomFrame
        if  open_shop.get():
            self.heading_label = Label(self.bottomFrame,text = 'Enter New ShopInfo.')
        else:
            self.heading_label = Label(self.bottomFrame,text = 'Change ShopInfo.')
        self.heading_label.grid(row = 0,columnspan = 2)
        #Shop Name
        self.shopname_label = Label(self.bottomFrame, text = 'Shop Name :')
        self.shopname_label.grid(row = 1, sticky = E)
        if open_shop.get():
            self.shopname = StringVar()
        else:
            self.shopname = StringVar(value=shop_info_old[4])
        self.shopname_entry = Entry(self.bottomFrame,textvariable=self.shopname)
        self.shopname_entry.grid(row = 1, column = 1)
        #Phone Number
        self.shopphone_label = Label(self.bottomFrame, text = 'Shop Phone :')
        self.shopphone_label.grid(row = 2, sticky = E)
        self.shopphone = StringVar()
        if open_shop.get():
            self.shopphone.set("")
        else:
            self.shopphone.set(shop_info_old[6])
        self.shopphone_entry = Entry(self.bottomFrame,textvariable=self.shopphone)
        self.shopphone_entry.grid(row = 2, column = 1)
        #Shop Address
        self.shopaddress_label = Label(self.bottomFrame, text = 'Shop Address :')
        self.shopaddress_label.grid(row = 3, sticky = E)
        if open_shop.get():
            self.shopaddress = StringVar()
        else:
            self.shopaddress = StringVar(value=shop_info_old[5])
        self.shopaddress_entry = Entry(self.bottomFrame,textvariable=self.shopaddress)
        self.shopaddress_entry.grid(row = 3, column = 1)
        #Brithdate
        self.opening_label = Label(self.bottomFrame, text = 'Opening Time :')
        self.opening_label.grid(row = 4, sticky = E)

        self.openhour_list = list(range(0,24))
        self.openhour_variable = IntVar()
        if open_shop.get():
            self.openhour_variable.set(0)
        else:
            self.openhour_variable.set(shop_info_old[2].seconds//3600)
        self.openhour = OptionMenu(self.bottomFrame, self.openhour_variable, *self.openhour_list)
        self.openhour.grid(row = 4, column = 1,columnspan=2,sticky = W)

        self.openminute_list = list(range(0,60,5))
        self.openminute_variable = IntVar()
        if open_shop.get():
            self.openminute_variable.set(0)
        else:
            self.openminute_variable.set(shop_info_old[2].seconds//60%60)
        self.openminute = OptionMenu(self.bottomFrame, self.openminute_variable, *self.openminute_list)
        self.openminute.grid(row = 4, column = 1,columnspan=2,sticky = E)

        self.closing_label = Label(self.bottomFrame, text = 'Closing Time :')
        self.closing_label.grid(row = 5, sticky = E)

        self.closehour_list = list(range(0,24))
        self.closehour_variable = IntVar()
        if open_shop.get():
            self.closehour_variable.set(0)
        else:
            self.closehour_variable.set(shop_info_old[3].seconds//3600)
        self.closehour = OptionMenu(self.bottomFrame, self.closehour_variable, *self.closehour_list)
        self.closehour.grid(row = 5, column = 1,columnspan=2,sticky = W)

        self.closeminute_list = list(range(0,60,5))
        self.closeminute_variable = IntVar()
        if open_shop.get():
            self.closeminute_variable.set(0)
        else:
            self.closeminute_variable.set(shop_info_old[3].seconds//60%60)
        self.closeminute = OptionMenu(self.bottomFrame, self.closeminute_variable, *self.closeminute_list)
        self.closeminute.grid(row = 5, column = 1,columnspan=2,sticky = E)

        #Register Button
        if  open_shop.get():
            self.update_button = Button(self.bottomFrame, text = 'Create',command = self.readEntry)
        else:
            self.update_button = Button(self.bottomFrame, text = 'Update',command = self.readEntry)
        self.update_button.grid(row = 10, columnspan=3,sticky = E,ipadx=58)
        #Go Back Button
        if  open_shop.get()=="1":
            self.goback_button = Button(self.bottomFrame, text = 'Go back',command = self.toLoginPage)
        else:
            self.goback_button = Button(self.bottomFrame, text = 'Go back',command = self.toSelectShop)
        self.goback_button.grid(row = 11,columnspan=3,sticky = E,ipadx=55)

        if  open_shop.get()=="1":
            tkinter.messagebox.showinfo('Welcome','AAAAAAAABBBBBBBBBBBBBBCCCCCCCCCC')
        #Keyboard events
        master.unbind('<Return>')
        master.bind('<Return>',self.pressEnter)

    #def function
    def pressEnter(self,event):
        self.update_button.invoke()

    def readEntry(self):
        self.opening_entry = str(self.openhour_variable.get())+":"+str(self.openminute_variable.get())+":00"
        self.closing_entry = str(self.closehour_variable.get())+":"+str(self.closeminute_variable.get())+":00"
#         print ('^^^^^^^^^^test^^^^^^^^^^')
#         print ('fullname:\t'+self.surname_entry.get()+' '+self.firstname_entry.get())
#         print ('username:\t'+self.username_entry.get())
#         print ('email:\t\t'+self.email_entry.get())
#         print ('phone:\t\t'+self.phone_entry.get())
#         print ('password:\t'+self.password_entry.get())
#         print ('repassword:\t'+self.retypepassword_entry.get())
#         print ('gender:\t\t'+self.gender_variable.get())
#         print ('birth_date:\t'+ self.birthdate_entry)
#         print('vvvvvvvvvvvvvvvvvvvvvvvvv')
        self.checkEntry()
        if checkresult:
            if  open_shop.get():
                cursor.execute("INSERT INTO `shop_info` (`user_id`,`shop_id`,`opening_time`,`closing_time`, `shop_name`, `shop_address`,`shop_phone`)"
                                   "VALUES ('"+userID+"',NULL,'"+self.opening_entry+"','"+self.closing_entry+"','"+self.shopname_entry.get()+"','"+self.shopaddress_entry.get()+"','"+self.shopphone_entry.get()+"');")
                #cursor.execute("UPDATE `shop_info` SET `opening_time` = '"+self.opening_entry+"', `closing_time`='"+self.closing_entry+"',`shop_name`='"+self.shopname_entry.get()+"',`shop_address`='"+self.shopaddress_entry.get()+"',`shop_phone`='"+self.shopphone_entry.get()+"'WHERE `user_id` = "+userID+";")
                cursor.execute("UPDATE `login_system` SET `owner` = '1' WHERE `login_system`.`user_id` = "+userID+" ")
                tkinter.messagebox.showinfo('Account Created','Success! Now return to Home Page.')
                self.toHomePage()
            else:
                cursor.execute("UPDATE `shop_info` SET `opening_time` = '"+self.opening_entry+"', `closing_time`='"+self.closing_entry+"',`shop_name`='"+self.shopname_entry.get()+"',`shop_address`='"+self.shopaddress_entry.get()+"',`shop_phone`='"+self.shopphone_entry.get()+"'WHERE `user_id` = "+userID+";")
                tkinter.messagebox.showinfo('Updated','Success! Now return to Home Page.')
                self.toHomePage()
    def checkEntry(self):
        global checkresult
        checkresult = True
        #User Name
        if self.shopname_entry.get() =="":
            tkinter.messagebox.showerror('Update Failed','You must Enter a Shop Name.')
            checkresult = False
        #Phone Number
        try:
            if len(str(int(self.shopphone_entry.get()))) != 8:
                tkinter.messagebox.showerror('Update Failed','Please check your phone number.')
                checkresult = False
        except ValueError:
            tkinter.messagebox.showerror('Update Failed','Please check your phone number.')
            checkresult = False
    def toSelectShop(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return SelectShop(root)
    def toLoginPage(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return LoginPage(root)
    def toHomePage(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return HomePage(root)

class SelectShop:#*********************************************************************************************************

    def __init__(self,master):

        global shop_option
        global open_shop
        global shopID
        open_shop.set(2)

        cursor.execute("SELECT `shop_name` FROM `shop_info` WHERE `user_id`='"+userID+"'")
        read_shop_name=list()
        for shop_name in cursor:
            read_shop_name.append(shop_name[0])
        #print(read_shop_name)

        #Organizing Main Frame Layout
        self.topFrame = Frame (master)
        self.topFrame.pack()

        self.bottomFrame = Frame(master)
        self.bottomFrame.pack()

        #Top Frame
        self.photo_logo=PhotoImage(file = 'EDITMODE.png')
        self.hello_label = Label(self.topFrame, image = self.photo_logo)
        self.hello_label.pack()

        #Bottom Frame
        self.heading_label = Label(self.bottomFrame,text = 'Select Restaurant:')
        self.heading_label.pack()
        shop_option = StringVar()
        for text in read_shop_name:
            self.option_radiobutton = Radiobutton(self.bottomFrame, text=text,variable=shop_option,value = text,indicatoron=0,command=self.checkGoing)
            self.option_radiobutton.pack(fill=X)
        self.newshop_button = Button(self.bottomFrame,text = 'New Shop',command = self.toUpdateShopInfo)
        self.newshop_button.pack(fill=X)
        self.goback_button = Button(self.bottomFrame, text = 'Go back',command = self.toHomePage)
        self.goback_button.pack(fill=X)

    def checkGoing(self):
        global open_shop
        global shopID
        cursor.execute("SELECT `shop_id` FROM `shop_info` WHERE `shop_name`='"+shop_option.get()+"'")
        for read_shop_name in cursor:
            shopID=str(read_shop_name[0])
        if Going == "Update":
            open_shop.set(0)
            self.toUpdateShopInfo()
        if Going == "Edit":
            self.toEditMode()
    def toEditMode(self):
        global shop_option
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        #print(shop_option.get())
        return EditMode(root)
    def toUpdateShopInfo(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return UpdateShopInfo(root)
    def toHomePage(self):
        self.topFrame.destroy()
        self.bottomFrame.destroy()
        return HomePage(root)
class EditMode: #*********************************************************************************************************

    global menuID
    menuID = None
    global shop_option
    def __init__(self,master):
#         print("test userID: "+userID)
#         print(shop_option.get())
        cursor.execute("SELECT `shop_id` FROM `shop_info` WHERE `shop_name`='"+shop_option.get()+"'")
        for read_shop_id in cursor:
            read_shop_id=read_shop_id
#             print(read_shop_id)
        #Organizing Main Frame Layout
        self.topFrame = Frame (master)
        self.topFrame.pack()

        self.middleFrame = Frame(master)
        self.middleFrame.pack()

        self.bottomFrame = Frame(master)
        self.bottomFrame.pack(fill=X)

        self.OptionFrame = Frame (self.middleFrame)
        self.OptionFrame.pack(side=LEFT,anchor=N)
        self.CommandFrame = Frame(self.middleFrame)
        self.CommandFrame.pack(side=LEFT,anchor=N)
        self.DisplayFrame = Frame(self.middleFrame)
        self.DisplayFrame.pack(side=LEFT,anchor=N)
        self.AddOnFrame = Frame(self.middleFrame)
        self.AddOnFrame.pack(side=LEFT,anchor=N)

        #Top Frame
        self.photo_logo=PhotoImage(file = 'EDITMODE.png')
        self.hello_label = Label(self.topFrame,compound = TOP,text='\nWelcome,user', image = self.photo_logo)
        self.hello_label.pack()

        #Middle-Option Frame
        self.OptionF5()
        #Middle-Command Frame
        self.CommandF5()
        #Middle-Display Frame
        self.DisplayF5()
        #Middle-Add-On Frame
        self.AddOnF5()

        #Bottom Frame
        self.goback_button = Button(self.bottomFrame, text = 'Return to Home Page',command = self.toSelectShop)
        self.goback_button.pack()

    def OptionF5(self):
        for widget in self.OptionFrame.winfo_children():
            widget.destroy()
        self.Option(self.OptionFrame)
    def Option(self,place):
        global menuID
        global shopID
#         print("Option"+shopID)
        global option_variable
        self.option_label = Label(place, text = 'Option :')
        self.option_label.pack(anchor=W)
        option_variable = StringVar()
        try:
            option_variable.set(menuname_entry)
            self.CommandF5()
        except NameError:
            option_variable.set("add menu...")
            self.CommandF5()
        self.option_radiobutton = Radiobutton(place,text = "add menu...",variable = option_variable,value = "add menu...",command = self.MenuIDreset)
        self.option_radiobutton.pack(anchor=W)
        cursor.execute("SELECT `menu_name` FROM `shop_menu` WHERE `shop_id`='"+shopID+"'")
        read_menu=list()
        for shop_name in cursor:
            read_menu.append(shop_name[0])
        for text in read_menu:
            self.option_radiobutton = Radiobutton(place,text = text,variable = option_variable,value = text,command = self.CommandF5)
            self.option_radiobutton.pack(anchor=W)
        self.delete_button = Button(place, text = 'Delete Menu',command = self.deleteCommand)
        self.delete_button.pack(fill=X)

    def MenuIDreset(self):
        global menuID
        menuID = None
        self.CommandF5()
        self.DisplayF5()
    def CommandF5(self):
        global menuID
        cursor.execute("SELECT `menu_id` FROM `shop_menu` WHERE `menu_name`= '"+option_variable.get()+"'")
        for read_menu_ID in cursor:
            menuID = str(read_menu_ID[0])
        self.DisplayF5()
        self.AddOnF5()
        for widget in self.CommandFrame.winfo_children():
            widget.destroy()
        #Command Item
        if option_variable.get() != 'add menu...':
            self.Commanditem(self.CommandFrame)
        #Command Menu
        else:
            self.Commandmenu(self.CommandFrame)
        #Keyboard events
        root.unbind('<Return>')
        root.bind('<Return>',self.pressEnter)
    def Commandmenu(self,place):
        self.menuname_label = Label(place, text = 'Name of Menu :')
        self.menuname_label.pack(anchor=W)
        self.menuname_entry = Entry(place)
        self.menuname_entry.pack(anchor=W)
        self.setmenu_variable = BooleanVar()
        self.setmenu_checkbutton = Checkbutton(place,text = 'set',variable = self.setmenu_variable,command=self.setMessage)
        self.setmenu_checkbutton.pack(anchor=W)
        self.add_button = Button(place, text = 'Create Menu',command = self.createMenu)
        self.add_button.pack(anchor=W)
    def setMessage(self):
        tkinter.messagebox.showinfo("Set Menu", "Set Menu default linked to \"Drink Menu\"")
    def Commanditem(self,place):
        self.itemname_label = Label(place, text = 'Item Name :')
        self.itemname_label.pack(anchor=W)
        self.itemname_entry = Entry(place)
        self.itemname_entry.pack(anchor=W)
        self.itemprice_label = Label(place, text = 'Item Price :')
        self.itemprice_label.pack(anchor=W)
        self.itemprice_entry = Entry(place)
        self.itemprice_entry.pack(anchor=W)
        self.add_button = Button(place, text = 'Confirm',command = self.addItem)
        self.add_button.pack(anchor=W)

    def DisplayF5(self):
        for widget in self.DisplayFrame.winfo_children():
            widget.destroy()
        self.Display(self.DisplayFrame)
    def Display(self,place):
        #print(menuID)
        self.title_label = Label(place, text = 'Display :')
        self.title_label.pack(side=TOP,anchor=W)
        self.menu_label = Label(self.DisplayFrame, text =option_variable.get(),bg='white')
        self.menu_label.pack(fill=X)
        self.DisplayFrameL = Frame(self.DisplayFrame)
        self.DisplayFrameL.pack(side=LEFT,anchor=N)
        self.DisplayFrameR = Frame(self.DisplayFrame)
        self.DisplayFrameR.pack(side=LEFT,anchor=N)
        self.name_label = Label(self.DisplayFrameL, text = "NAME",bg='white',anchor=W)
        self.price_label = Label(self.DisplayFrameR, text = "PRICE",bg='white',anchor=E)
        self.name_label.pack(fill=X)
        self.price_label.pack(fill=X)
        try:
            cursor.execute("SELECT `item_name`,`item_price` FROM `menu_item` WHERE `menu_id`= '"+menuID+"'")
            for (name,price) in cursor:
                self.name_label = Label(self.DisplayFrameL, text = name,bg='white',anchor=W)
                self.price_label = Label(self.DisplayFrameR, text = price,bg='white',anchor=E)
                self.name_label.pack(fill=X)
                self.price_label.pack(fill=X)
        except TypeError:
            pass

    def AddOnF5(self):
        for widget in self.AddOnFrame.winfo_children():
            widget.destroy()
        self.AddOn(self.AddOnFrame)
    def AddOn(self,place):
        self.title_label=Label(place,text="Setting:")
        self.title_label.pack(anchor=W)
        if menuID == None:
            self.none_label = Label(place, text = "pick a menu...",bg='white')
            self.none_label.pack(fill=BOTH)
        else:
            self.changename_button = Button(place, text = 'Change Menu Name',command = self.ChangeNameF5)
            self.changename_button.pack(anchor=W,fill=X)
            self.time_button = Button(place, text = 'Set Available Time*',command = self.NotDone)
            self.time_button.pack(anchor=W,fill=X)
            self.set_button = Button(place, text = 'Change Set Menu Setting',command = self.ChangeSetF5)
            self.set_button.pack(anchor=W,fill=X)
            self.remove_button = Button(place, text = 'Remove Item',command = self.RemoveItemF5)
            self.remove_button.pack(anchor=W,fill=X)
    def ChangeNameF5(self):
        for widget in self.AddOnFrame.winfo_children():
            widget.destroy()
        self.ChangeName(self.AddOnFrame)
    def ChangeName(self,place):
        self.currenttitle_label=Label(place,text="Current Menu title:")
        self.currenttitle_label.pack(anchor=W)
        self.currentname_label=Label(place,text=option_variable.get(),bg='white',anchor=W)
        self.currentname_label.pack(anchor=W,fill=X)
        self.newtitle_label=Label(place,text="Enter New Menu title:")
        self.newtitle_label.pack(anchor=W)
        self.newname_entry=Entry(place)
        self.newname_entry.pack(anchor=W)
        self.ok_button = Button(place, text = 'Confirm',command = self.ChangeNameCommand)
        self.ok_button.pack(anchor=W,fill=X)
        self.goback_button = Button(place, text = 'Go Back',command = self.AddOnF5)
        self.goback_button.pack(anchor=W,fill=X)
    def ChangeNameCommand(self):
        self.checkEntry_addon()
        if checkresult:
            cursor.execute("UPDATE `shop_menu` SET `menu_name` = '"+self.newname_entry.get()+"' WHERE `shop_menu`.`menu_id` = "+menuID+" ")
            tkinter.messagebox.showinfo("Updated", "Success! Now reture to previous page")
            self.OptionF5()
            self.AddOnF5()
    def ChangeSetF5(self):
        for widget in self.AddOnFrame.winfo_children():
            widget.destroy()
        self.ChangeSet(self.AddOnFrame)
    def ChangeSet(self,place):
        global selectedmenu
        self.currentset_label=Label(place,text="Current Linked Menu:")
        self.currentset_label.pack(anchor=W)
        cursor.execute("SELECT `set_or_not` FROM `shop_menu` WHERE `menu_id` = "+menuID)
        for linkedsetid in cursor:
            oldsetid = linkedsetid[0]
        linkedset = StringVar()
        if oldsetid == 0:
            linkedset.set("No Menu Linked.")
        else:
            cursor.execute("SELECT `menu_name` FROM `shop_menu` WHERE `menu_id` = "+str(oldsetid))
            for setname in cursor:
                linkedset.set(setname[0])
        self.oldset_label=Label(place,text=linkedset.get(),bg='white',anchor=W)
        self.oldset_label.pack(anchor=W,fill=X)
        self.newset_label=Label(place,text="Select New Menu to Link:")
        self.newset_label.pack(anchor=W)
        selectedmenu = StringVar()
        if oldsetid == 0:
            selectedmenu.set("Unlinked")
        else:
            selectedmenu.set(linkedset.get())
        cursor.execute("SELECT `menu_name` FROM `shop_menu` WHERE `shop_id`='"+shopID+"'")
        read_menu=list()
        read_menu.append("Unlinked")
        for shop_name in cursor:
            read_menu.append(shop_name[0])
        cursor.execute("SELECT `menu_name` FROM `shop_menu` WHERE `menu_id` = "+menuID)
        for menu_name in cursor:
            read_menu.remove(menu_name[0])
        for text in read_menu:
            self.option_radiobutton = Radiobutton(place,text = text,variable = selectedmenu,value = text,indicatoron = 0,command=self.ChangeSetCommand)
            self.option_radiobutton.pack(anchor=W,fill=X)
        self.goback_button = Button(place, text = 'Go Back',command = self.AddOnF5)
        self.goback_button.pack(anchor=W,fill=X)
    def ChangeSetCommand(self):
        if selectedmenu.get() == "Unlinked":
            cursor.execute("UPDATE `shop_menu` SET `set_or_not` = 0 WHERE `shop_menu`.`menu_id` = "+menuID+" ")
            self.ChangeSetF5()
        else:
            cursor.execute("SELECT `menu_id` FROM `shop_menu` WHERE `menu_name` = '"+selectedmenu.get()+"'")
            for selectedmenuid in cursor:
                linkedsetid = str(selectedmenuid[0])
            cursor.execute("UPDATE `shop_menu` SET `set_or_not` = '"+linkedsetid+"' WHERE `shop_menu`.`menu_id` = "+menuID+" ")
            self.ChangeSetF5()
    def RemoveItemF5(self):
        for widget in self.AddOnFrame.winfo_children():
            widget.destroy()
        self.RemoveItem(self.AddOnFrame)
    def RemoveItem(self,place):
        global selecteditem
        self.title_label=Label(place,text="Select an item to Remove:")
        self.title_label.pack(anchor=W)
        selecteditem = StringVar()
        cursor.execute("SELECT `item_name`,`item_id` FROM `menu_item` WHERE `menu_id`= '"+menuID+"'")
        read_items=list()
        for items,itemID in cursor:
            read_items.append([items,itemID])
        for text,textID in read_items:
            self.option_radiobutton = Radiobutton(place,text = text,variable = selecteditem,value = textID,indicatoron = 0,command=self.RemoveItemCommand)
            self.option_radiobutton.pack(anchor=W,fill=X)
        self.goback_button = Button(place, text = 'Go Back',command = self.AddOnF5)
        self.goback_button.pack(anchor=W,fill=X)
    def RemoveItemCommand(self):
        answer = tkinter.messagebox.askquestion("Warning", "Are you sure to delete '"+selecteditem.get()+"'?",icon='warning')
        if answer == 'yes':
            cursor.execute("DELETE FROM `menu_item` WHERE `item_id` = '"+selecteditem.get()+"'")
            self.DisplayF5()
            self.RemoveItemF5()
    def NotDone(self):
        tkinter.messagebox.showwarning("Sorry", "This function is still on Development Stage")
    def createMenu(self):
        global menuname_entry
        menuname_entry = self.menuname_entry.get()
        self.checkEntry_menu()
        if checkresult:
#             print ('^^^^^^^^^test^^^^^^^^^')
#             print(self.menuname_entry.get())
#             print('vvvvvvvvvvvvvvvvvvvvvvvvv')
            cursor.execute("SELECT menu_id FROM `shop_menu` WHERE `menu_name`='Drink Menu'")
            for menuid in cursor:
                self.owner = str(menuid[0])
            try:
                if self.setmenu_variable.get():
                    cursor.execute("INSERT INTO `shop_menu` (`shop_id`,`menu_id`,`menu_name`,`set_or_not`)"
                                   "VALUES ('"+shopID+"',NULL,'"+self.menuname_entry.get()+"','"+self.owner+"');")
                else:
                    cursor.execute("INSERT INTO `shop_menu` (`shop_id`,`menu_id`,`menu_name`,`set_or_not`)"
                                   "VALUES ('"+shopID+"',NULL,'"+self.menuname_entry.get()+"','0');")
                self.OptionF5()
            except AttributeError:
                cursor.execute("INSERT INTO `shop_menu` (`shop_id`,`menu_id`,`menu_name`,`set_or_not`)"
                               "VALUES ('"+shopID+"',NULL,'Drink Menu','0');")
                self.createMenu()
    def addItem(self):
        # DB CREATE TABLE !!!!!!!!!!!!!!!!!!!!
#         print ('^^^^^^^^^test^^^^^^^^^')
#         print ('menuname:\t'+self.itemname_entry.get())
#         print ('menuprice:\t'+self.itemprice_entry.get())
#         print('vvvvvvvvvvvvvvvvvvvvvvvvv')
        try:
            cursor.execute("INSERT INTO `menu_item` (`menu_id`,`item_name`,`item_price`)"
                           "VALUES ('"+menuID+"','"+self.itemname_entry.get()+"','"+str(int(self.itemprice_entry.get()))+"');")
            self.CommandF5()
            self.DisplayF5()
        except ValueError:
            tkinter.messagebox.showerror('Failed','Price must be a number.')
    def checkEntry_menu(self):
        global checkresult
        checkresult = True
        self.result = ""
        cursor.execute("SELECT `menu_id` FROM `shop_menu` WHERE `menu_name`= '"+self.menuname_entry.get()+"'")
        for check in cursor:
            self.result = check[0]
        if self.menuname_entry.get() =="":
            tkinter.messagebox.showerror('Create Failed','You must Enter a Menu Name.')
            checkresult = False
        if self.result != "":
            tkinter.messagebox.showerror('Create Failed','Menu already existed.')
            checkresult = False
    def checkEntry_addon(self):
        global checkresult
        checkresult = True
        if self.newname_entry.get() == "":
            tkinter.messagebox.showerror('Create Failed','You must Enter a Menu Name.')
            checkresult = False
    def deleteCommand(self):
        #print(option_variable.get())
        #print(menuID)
        if option_variable.get() == "add menu...":
            pass
        else:
            answer = tkinter.messagebox.askquestion("Warning", "Are you sure to delete '"+option_variable.get()+"'?",icon='warning')
            if answer == 'yes':
                cursor.execute("DELETE FROM `menu_item` WHERE `menu_id`='"+menuID+"'")
                cursor.execute("DELETE FROM `shop_menu` WHERE `menu_id`='"+menuID+"'")
                self.OptionF5()
    def pressEnter(self,event):
        self.add_button.invoke()
    def toSelectShop(self):
        self.topFrame.destroy()
        self.middleFrame.destroy()
        self.bottomFrame.destroy()
        return SelectShop(root)

#Main Program
root = Tk()
root.title('All Project(Group 3) - HereRice')
TitleBar(root)
LoginPage(root)
root.mainloop()
