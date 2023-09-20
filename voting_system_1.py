import re
import string
import hashlib
import random
import logging
from tkinter import *
import tkinter as tk
from tkinter import scrolledtext
from tkinter import StringVar
from tkinter.ttk import Combobox
from tkinter import messagebox
from color_and_font_schemes import *
import voting_system_database as mysqlcon

class voterLogin:
    def __init__(self, master, app_instance, on_success=None):
        self.master = master
        self.app_instance = app_instance
        self.on_success = on_success
        
    def display(self):
        self.loginFrame = Frame(self.master)
        self.loginFrame.place(x=0, y=0, width="500", height="500")
        self.loginFrame.configure(background="white")
        self.voterId = StringVar()
        self.password1 = StringVar()

        label = Label(self.loginFrame, text="Login to Vote", font=(ARIAL, 20, "bold"), bg="white", fg=HIGHLIGHT_TEXT)
        label.place(x=150, y=50)

        label0 = Label(self.loginFrame, text="Voter Id ", font=(ARIAL, 12, "normal"), bg="white")
        label0.place(x=100, y=150)
        input0 = Entry(self.loginFrame, font=(ARIAL, 12), textvariable=self.voterId, border=0, bg="#f0f0f0")
        input0.place(x=100, y=200, width="200", height="25")
        
        label1 = Label(self.loginFrame, text="Password ", font=(ARIAL, 12, "normal"), bg="white")
        label1.place(x=100, y=250)
        input1 = Entry(self.loginFrame, font=(ARIAL, 12), textvariable=self.password1, border=0, bg="#f0f0f0")
        input1.place(x=100, y=300, width="200", height="25")
        
        Login_btn = Button(self.loginFrame, text="Login", font=(ARIAL, 13, "bold"), command=self.login, border=0, bg=HIGHLIGHT_BG, fg="white")
        Login_btn.place(x=200, y=400, width=100, height=50)

        # Assuming that VoterHome is a method in another class or a function outside
        back_btn = Button(self.loginFrame, text="<Back>", font=(ARIAL, 10, "bold"), command=self.app_instance.VoterHome, border=0, bg="white", fg="indigo")
        back_btn.place(x=0, y=0, width=100, height=50)

    def login(self):
        logging.info(f"Login attempt made with VoterID: {self.voterId.get()}")
        
        if not self.voterId.get() or not self.password1.get():
            messagebox.showwarning('Voting System Message', 'Missing fields')
            logging.warning(f"Failed login attempt due to missing fields for VoterID: {self.voterId.get()}")
            return

        hashed_password = self.hash_password(self.password1.get())
        result = mysqlcon.findByVoterIdAndPassword(self.voterId.get(), hashed_password)

        if result is None:
            messagebox.showerror('Voting System Message', 'Wrong Credentials')
            logging.warning(f"Failed login attempt due to wrong credentials for VoterID: {self.voterId.get()}")
        else:
            logging.info(f"Successful login for VoterID: {self.voterId.get()}")
            if self.on_success:
                self.on_success(self.voterId.get())
            
        self.voterId.set("")
        self.password1.set("")

    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

class dashboard:
    def __init__(self, master, app_instance, voterId):
        self.master = master
        self.app_instance = app_instance
        self.voterId = voterId

    def display(self):
        self.dashboardFrame = Frame(self.master)
        self.dashboardFrame.place(x=0, y=0, width=900, height=500)
        self.dashboardFrame.configure(background="white")

        self.poll = StringVar()
        self.district = StringVar()
        self.name = StringVar()

        result = mysqlcon.findByVoterId(self.voterId)
        self.name.set(result[2])

        IDLabel = Label(self.dashboardFrame, text=self.voterId, font=(ARIAL, 13, "normal"), bg="white", fg=HIGHLIGHT_TEXT)
        IDLabel.place(x=10, y=10)

        label = Label(self.dashboardFrame, text="Your Vote, Your Voice", font=(LUCIDA_CONSOLE, 30, "bold"), bg="white", fg=HIGHLIGHT_BG)
        label.place(x=175, y=50)

        nameLabel = Label(self.dashboardFrame, text="Hi, "+self.name.get(), font=(ARIAL, 15, "normal"), bg="white")
        nameLabel.place(x=75, y=150)

        pollLabel = Label(self.dashboardFrame, text="Select your party to vote: ", font=(ARIAL, 15, "normal"), bg="white")
        pollLabel.place(x=150, y=225)
        pollInput = Combobox(self.master, values=["Nepali Congress", "Nepal Communist Party (UML)","Nepal Communist Party (Maoist Center)","Nepal Communist Party (Unified Socialist)","Janata Samajbadi Party, Nepal","Loktantrik Samajbadi Party, Nepal"], font=(ARIAL, 13, "normal"), textvariable=self.poll)
        pollInput.place(x=400, y=225, width=200)
        districtLabel = Label(self.dashboardFrame, text="Select your District: ", font=(ARIAL, 15, "normal"), bg="white")
        districtLabel.place(x=200, y=275)
        districtInput = Combobox(self.master, values=["Achham", "Arghakhanchi", "Baglung", "Baitadi", "Bajhang", "Bajura", "Banke", "Bara", "Bardiya", "Bhaktapur", "Bhojpur", "Chitwan", "Dadeldhura", "Dailekh", "Dang", "Darchula", "Dhading", "Dhankuta", "Dhanusha", "Dolakha", "Dolpa", "Doti", "Gorkha", "Gulmi", "Humla", "Ilam", "Jajarkot", "Jhapa", "Jumla", "Kailali", "Kalikot", "Kanchanpur", "Kapilvastu", "Kaski", "Kathmandu", "Kavrepalanchok", "Khotang", "Lalitpur", "Lamjung", "Mahottari", "Makwanpur", "Manang", "Morang", "Mugu", "Mustang", "Myagdi", "Nawalparasi East", "Nawalparasi West", "Nuwakot", "Okhaldhunga", "Palpa", "Panchthar", "Parbat", "Parsa", "Pyuthan", "Ramechhap", "Rasuwa", "Rautahat", "Rolpa", "Rukum East", "Rukum West", "Rupandehi", "Salyan", "Sankhuwasabha", "Saptari", "Sarlahi", "Sindhuli", "Sindhupalchok", "Siraha", "Solukhumbu", "Sunsari", "Surkhet", "Syangja", "Tanahun", "Taplejung", "Terhathum", "Udayapur"], font=(ARIAL, 13, "normal"), textvariable=self.district)
        districtInput.place(x=400, y=275, width=200)

        Vote_btn = Button(self.dashboardFrame, text="Vote", font=(ARIAL, 13, "normal"), command=self.vote, border=0, bg=HIGHLIGHT_BG, fg="white")
        Vote_btn.place(x=375, y=350, width=150, height=50)

        logOut = Button(self.dashboardFrame, text="Log Out", font=(ARIAL, 10, "normal"), command=self.logout, border=0, bg="white", fg="grey")
        logOut.place(x=800, y=0, width=100, height=50)

    def vote(self):
        try:
            logging.info(f"Voting attempt initiated by VoterID: {self.voterId}")
            
            # Validate if all necessary fields are filled.
            if not self.poll.get() or not self.district.get():
                messagebox.showwarning('Voting System Message', 'All fields are required to be filled.')
                logging.warning(f"Incomplete voting details provided by VoterID: {self.voterId}")
                return

            # Check if the user has already voted.
            result1 = mysqlcon.findByVoterIdinVote(self.voterId)
            if result1 is not None:
                messagebox.showwarning('Voting System Message', 'Thanks, but you have voted already.')
                logging.warning(f"VoterID: {self.voterId} attempted to vote again.")
                return

            # If the user hasn't voted yet, submit their vote.
            if mysqlcon.submitVote(self.voterId, self.poll.get(), self.district.get()):
                messagebox.showinfo('Voting System Message', 'Thanks, Vote submitted successfully.')
                logging.info(f"Vote successfully recorded for VoterID: {self.voterId}")
                
                # Clear the input fields after voting.
                self.poll.set("")
                self.district.set("")
                self.logout()  # Assuming you want to log out the user after voting.

            else:
                messagebox.showwarning('Voting System Message', 'Try again later, Failed to vote.')
                logging.warning(f"Failed to record vote for VoterID: {self.voterId}")


        except Exception as e:
            messagebox.showerror('Voting System Message', 'An unexpected error occurred while voting.')
            logging.error(f"Unexpected error during voting for VoterID: {self.voterId}. Error: {str(e)}")

    def logout(self):
        # Assuming that Home is a method in another class or a function outside
        self.app_instance.Home()

class voterRegistration:
    def __init__(self, master, app_instance):
        self.master = master
        self.app_instance = app_instance
        self.voterId = StringVar()
        self.name = StringVar()
        self.citizenship = StringVar()
        self.phone = StringVar()
        self.gender = StringVar()
        self.district = StringVar()
        self.password = StringVar()
        self.cpassword = StringVar()

    def display(self):
        self.registrationFrame = Frame(self.master)
        self.registrationFrame.place(x=0, y=0, width="900", height="500")
        self.registrationFrame.configure(background="white")

        # ... [Place your widgets like Labels, Entries, and Comboboxes here]
        # For instance:
        label = Label(self.registrationFrame, text="Register to Vote", font=(ARIAL, 20, "bold"), bg="white", fg=HIGHLIGHT_TEXT)
        label.place(x=125, y=35)
        
        label0 = Label(self.registrationFrame, text="Full Name ", font=(ARIAL, 12, "normal"), bg="white")
        label0.place(x=30, y=100)
        input0 = Entry(self.registrationFrame, font=(ARIAL, 12), textvariable=self.name, border=0, bg="#f0f0f0")
        input0.place(x=250, y=100, width="200", height="22")

        # Citizenship Number
        label1 = Label(self.registrationFrame, text="Citizenship Number ", font=(ARIAL, 12, "normal"), bg="white")
        label1.place(x=30, y=140)
        input1 = Entry(self.registrationFrame, font=(ARIAL, 12), textvariable=self.citizenship, border=0, bg="#f0f0f0")
        input1.place(x=250, y=140, width="200", height="22")

        # Mobile Number
        label2 = Label(self.registrationFrame, text="Mobile Number", font=(ARIAL, 12, "normal"), bg="white")
        label2.place(x=30, y=180)
        input2 = Entry(self.registrationFrame, font=(ARIAL, 12), textvariable=self.phone, border=0, bg="#f0f0f0")
        input2.place(x=250, y=180, width="200", height="22")

        # Address
        label3 = Label(self.registrationFrame, text="Address", font=(ARIAL, 12, "normal"), bg="white")
        label3.place(x=30, y=220)
        input3 = Entry(self.registrationFrame, font=(ARIAL, 12), textvariable=self.district, border=0, bg="#f0f0f0")
        input3.place(x=250, y=220, width="200", height="22")

        # Gender
        label4 = Label(self.registrationFrame, text="Gender ", font=(ARIAL, 12, "normal"), bg="white")
        label4.place(x=30, y=260)
        input4 = Combobox(self.registrationFrame, values=["Male","Female", "Non-Binary","Intersex","Unstated"], font=(ARIAL, 12, "normal"), textvariable=self.gender, background="#f0f0f0")
        input4.place(x=250, y=260, width="200", height="22")

        # Password
        label5 = Label(self.registrationFrame, text="Password", font=(ARIAL, 12, "normal"), bg="white")
        label5.place(x=30, y=300)
        input5 = Entry(self.registrationFrame, font=(ARIAL, 12), textvariable=self.password, border=0, bg="#f0f0f0", show="*")
        input5.place(x=250, y=300, width="200", height="22")

        # Confirm Password
        label6 = Label(self.registrationFrame, text="Confirm Password", font=(ARIAL, 12, "normal"), bg="white")
        label6.place(x=30, y=340)
        input6 = Entry(self.registrationFrame, font=(ARIAL, 12), textvariable=self.cpassword, border=0, bg="#f0f0f0", show="*")
        input6.place(x=250, y=340, width="200", height="22")

        # Register button

        Register_btn = Button(self.registrationFrame, text="Register", font=(ARIAL, 13, "bold"), command=self.register, border=0, bg=HIGHLIGHT_BG, fg="white")
        Register_btn.place(x=150, y=390, width=200, height=40)
        back_btn = Button(self.registrationFrame, text="< Back", font=(ARIAL, 10, "normal"), command=self.app_instance.VoterHome, border=0, bg="white", fg="grey")  # Assuming Home is a method in the main app
        back_btn.place(x=0, y=0, width=100, height=50)

    def generate_voter_id(self, length=10):
        voter_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
        logging.info(f"Generated Voter ID: {voter_id}")
        return voter_id

    def hash_password(self, password):
        """Hash a password for storing."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def register(self):
        try:
            logging.info("Registration attempt initiated.")
            
            # Check if all fields are filled in.
            if not self.name.get() or not self.citizenship.get() or not self.phone.get() or not self.district.get() or not self.gender.get() or not self.password.get() or not self.cpassword.get():
                messagebox.showwarning('Voting System Message', 'All fields are required to be filled.')
                logging.warning("Incomplete registration details provided.")
                return
            
            # Check password validity.
            if not re.search("[a-z]", self.password.get()):
                messagebox.showerror('Voting System Message', 'Password must contain at least one lowercase character.')
                return
            if not re.search("[A-Z]", self.password.get()):
                messagebox.showerror('Voting System Message', 'Password must contain at least one uppercase character.')
                return
            if not re.search("[0-9]", self.password.get()):
                messagebox.showerror('Voting System Message', 'Password must contain at least one number.')
                return
            if not re.search("[!@#$%^&*()_-]", self.password.get()):
                messagebox.showerror('Voting System Message', 'Password must contain at least one of these special characters: !@#$%^&*()_-')
                return
            if len(self.password.get()) < 8:
                messagebox.showerror('Voting System Message', 'Password must be at least 8 characters long.')
                return

            # Confirm password matches
            if self.password.get() != self.cpassword.get():
                messagebox.showerror('Voting System Message', 'Passwords did not match.')
                logging.warning("Passwords mismatch during registration.")
                return

            # Check citizenship and phone number formats.
            if len(self.citizenship.get()) != 11 or len(self.phone.get()) != 10 or not self.citizenship.get().isdigit() or not self.phone.get().isdigit():
                messagebox.showerror('Voting System Message', 'Citizenship Number must be 11 digits and Mobile number must be 10 digits.')
                logging.warning(f"Invalid Citizenship or Phone number format for Citizenship: {self.citizenship.get()}, Phone: {self.phone.get()}")
                return

            # Check if user is already registered.
            result = mysqlcon.findByCitizenship(self.citizenship.get())
            self.voterId.set(self.generate_voter_id()) 
            result1 = mysqlcon.findByVoterId(self.voterId.get())

            if (result is None) and (result1 is None):
                hashed_password = self.hash_password(self.password.get())
                if mysqlcon.addVoter(self.voterId.get(), self.name.get(), self.citizenship.get(), self.phone.get(), self.district.get(), self.gender.get(), hashed_password, hashed_password):
                    messagebox.showinfo('Voting System Message', f'Registered as Voter.\n\nYour Voter ID is:\n\n{self.voterId.get()}\n\nPlease note it down.')
                    logging.info(f"Successful registration for Citizenship Number: {self.citizenship.get()}")
                    
                    # Clear input fields after successful registration.
                    self.voterId.set("")
                    self.name.set("")
                    self.citizenship.set("")
                    self.phone.set("")
                    self.district.set("")
                    self.gender.set("")
                    self.password.set("")
                    self.cpassword.set("")
                    
                    #for widget in self.frame.winfo_children():
                    #    widget.destroy()

                    # Assuming the main app has a login page method.
                    #showvoterLogin()

                else:
                    messagebox.showwarning('Voting System Message', 'Try again later, Failed to register.')
                    logging.warning(f"Failed to register for Citizenship Number: {self.citizenship.get()}")

            else:
                messagebox.showerror('Voting System Message', 'User already exists.')
                logging.error("Duplicate credentials detected during registration.")
                
        except Exception as e:
            detailed_error = f"Unexpected error during registration. Error: {str(e)}"
            messagebox.showerror('Voting System Message', detailed_error)
            logging.error(detailed_error)

class VotingSystem:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("900x500")
        self.root.resizable(0, 0)
        self.root.title("Voting Machine")
        self.root.iconbitmap('./Assets/icon.ico')
        self.root.configure(background="white")

        self.homeImg = PhotoImage(file="./Assets/homeImg.png")

        # Initializing all pages
        self.login_page = voterLogin(self.root, self)
        self.registration_page = voterRegistration(self.root, self)

        mysqlcon.connect()
        logging.basicConfig(filename='application.log', level=logging.INFO, format='%(asctime)s - %(message)s')

        self.Home()
    
    def Home(self):
        # Clear the existing interface
        for widget in self.root.winfo_children():
            widget.destroy()

        # Home interface setup
        homeFrame = Frame(self.root)
        homeFrame.place(x=0, y=0, width="900", height="500")
        homeFrame.configure(background="white")
        
        homeImg = PhotoImage(file="./Assets/homeImg.png")
        photo = Label(homeFrame, image=homeImg)
        photo.place(x=300, y=80, width=600, height=350) 
        
        label = Label(homeFrame, text="Future Lies in Voters' Hand", font=(ARIAL, 30, "bold"), bg="white", fg=HIGHLIGHT_TEXT)
        label.place(x=20, y=50)
        
        voter_btn = Button(homeFrame, text="Voter", font=(ARIAL, 13, "normal"), command=self.VoterHome, relief=FLAT, border=0, bg=HIGHLIGHT_BG)
        voter_btn.place(x=100, y=200, width=150, height=50)
        
        btn_border = LabelFrame(homeFrame, bd=0, bg=HIGHLIGHT_BG)
        btn_border.place(x=100, y=300, width=150, height=50)
        
        admin_btn = Button(btn_border, text="Admin", font=(ARIAL, 13, "normal"), command=self.open_admin_login, relief=FLAT, border=0, bg="white")
        admin_btn.place(x=1, y=1, width=148, height=48)
        
        # Make sure the home image is available for garbage collection
        photo.image = homeImg
    
    def VoterHome(self):
        # Clear the current interface
        for widget in self.root.winfo_children():
            widget.destroy()

        # Setup Voter Home interface
        voterFrame = Frame(self.root)
        voterFrame.place(x=0, y=0, width="900", height="500")
        voterFrame.configure(background="white")
        
        login_btn = Button(voterFrame, text="Login", font=(ARIAL, 13, "bold"), command=self.showvoterLogin, relief=FLAT, border=0, bg=HIGHLIGHT_BG, fg="white")
        login_btn.place(x=150, y=150, width=150, height=50)

        btn_border = LabelFrame(voterFrame, bd=0, bg=HIGHLIGHT_BG)
        btn_border.place(x=150, y=250, width=150, height=50)

        reg_btn = Button(btn_border, text="Register", font=(ARIAL, 13, "bold"), command=self.showvoterRegistration, relief=FLAT, border=0, bg="white", fg=HIGHLIGHT_BG)
        reg_btn.place(x=1, y=1, width=148, height=48)

        back_btn = Button(voterFrame, text="< Back", font=(ARIAL, 10, "normal"), command=self.Home, border=0, bg="white", fg="grey")
        back_btn.place(x=0, y=0, width=100, height=50)

        label = Label(voterFrame, text="Your Vote,\nYour Voice,\nYour Future", font=(LUCIDA_CONSOLE, 30, "bold"), bg=HIGHLIGHT_BG, fg="white")
        label.place(x=500, y=0, width=400, height=500)
        
    def showvoterLogin(self):
        self.login_page = voterLogin(self.root, self, on_success=self.showDashboard)
        self.login_page.display()

    def showDashboard(self, voterId):
        self.dashboard_page = dashboard(self.root, self, voterId)
        self.dashboard_page.display()

    def showvoterRegistration(self):
        self.registration_page = voterRegistration(self.root, self)
        self.registration_page.display()
    
    def open_admin_login(self):
        admin_login_instance = AdminLogin(self.root, self)
        admin_login_instance.display()

class AdminLogin:
    def __init__(self, root, voting_system_instance):
        self.root = root
        self.voting_system_instance = voting_system_instance
        self.username_var = StringVar()
        self.password_var = StringVar()

    def Login(self):
        try:
            logging.info("Login attempt initiated.")
            if self.username_var.get() == "" and self.password_var.get() == "":
                messagebox.showwarning('Voting System Message', 'Fields are required')
                logging.warning("Both username and password fields were empty during login attempt.")
                return
            hashed_username = self.hash_username(self.username_var.get())
            hashed_password = self.hash_password(self.password_var.get())
            result = mysqlcon.get_admin_details(hashed_username, hashed_password)
            
            if result is None:
                messagebox.showerror('Voting System Message', 'Wrong Credentials')
                logging.warning(f"Failed login attempt due to wrong credentials for Admin: {self.username_var.get()}")
            else:
                logging.info(f"Successful login in Admin")
                AdminDashboard(self.root, self.username_var.get())
                
            self.username_var.set("")
            self.password_var.set("")
        except Exception as e:
            messagebox.showerror('Voting System Message', 'An unexpected error occurred during login.')
            logging.error(f"Unexpected error during login. Error: {str(e)}")
    
    def display(self):
        self.LoginFrame = Frame(self.root)
        self.LoginFrame.place(x=0, y=0, width="900", height="500")
        self.LoginFrame.configure(background="white")

        label = Label(self.LoginFrame, text="Login as Admin to the Voting System", font=(ARIAL, 20, "bold"), bg="white", fg=HIGHLIGHT_TEXT)
        label.place(x=100, y=50)

        usernameLable = Label(self.LoginFrame, text="Username: ", font=(ARIAL, 12, "normal"), bg="white")
        usernameLable.place(x=100, y=150)
        usernameInput = Entry(self.LoginFrame, font=(ARIAL, 12, "normal"), textvariable=self.username_var, border=0, bg="#f0f0f0")
        usernameInput.place(x=200, y=150, width="200", height="25")

        IdLable = Label(self.LoginFrame, text="Password: ", font=(ARIAL, 12, "normal"), bg="white")
        IdLable.place(x=100, y=200)
        IdInput = Entry(self.LoginFrame, font=(ARIAL, 12, "normal"), textvariable=self.password_var, border=0, bg="#f0f0f0")
        IdInput.place(x=200, y=200, width="200", height="25")

        Login_btn = Button(self.LoginFrame, text="Login", font=(ARIAL, 13, "bold"), command=self.Login, border=0, bg=HIGHLIGHT_BG, fg="white")
        Login_btn.place(x=200, y=250, width=100, height=50)
        
        back_btn = Button(self.LoginFrame, text="< Back", font=(ARIAL, 10, "normal"), command=self.voting_system_instance.Home, border=0, bg="white", fg="grey") # Assuming the main VotingSystem class has a Home method.
        back_btn.place(x=0, y=0, width=100, height=50)
        
    @staticmethod
    def hash_username(username):
        """Hash a password for storing."""
        return hashlib.sha256(username.encode('utf-8')).hexdigest()
    
    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def cleanup(self):
        if hasattr(self, 'LoginFrame') and self.LoginFrame:
            self.LoginFrame.destroy()
        

class AdminDashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        self.dashboardFrame = Frame(self.root)
        self.dashboardFrame.place(x=0, y=0, width=900, height=500)
        self.dashboardFrame.configure(background="white")
        
        # Menu bar for the dashboard
        self.menu_bar = Frame(self.dashboardFrame, bg="#f0f0f0")
        self.menu_bar.place(x=0, y=0, width=249, height=500)
        self.menu_bar.configure(background="#f0f0f0")
        
        self.section = Frame(self.dashboardFrame)
        self.section.place(x=249, y=0, width=651, height=500)
        self.section.configure(background="grey")
        self.display_voting_results()
        
        self.admin = Frame(self.menu_bar)
        self.admin.place(x=0, y=0, width=249, height=100)
        self.admin.configure(background=HIGHLIGHT_BG)

        self.label = Label(self.admin, text=username, font=(ARIAL, 15, "bold"), bg=HIGHLIGHT_BG, fg="white")
        self.label.place(x=10, y=25)

        self.update_btn = Button(self.menu_bar, text="Dashboard", font=(ARIAL, 13, "normal"), command=self.display_voting_results, border=0, bg="beige", fg="brown", anchor="w", padx=30)
        self.update_btn.place(x=0, y=100, width=249, height=50)

        self.delete_btn = Button(self.menu_bar, text="All Records", font=(ARIAL, 13, "normal"), command=self.show_all_records, border=0, bg="beige", fg="brown", anchor="w", padx=30)
        self.delete_btn.place(x=0, y=151, width=249, height=50)

        self.search_btn = Button(self.menu_bar, text="Search User", font=(ARIAL, 13, "normal"), command=self.search_user, border=0, bg="beige", fg="brown", anchor="w", padx=30)
        self.search_btn.place(x=0, y=202, width=249, height=50)

        self.data_btn = Button(self.menu_bar, text="Update User Records", font=(ARIAL, 13, "normal"),command=self.show_update_user_form, border=0, bg="beige", fg="brown", anchor="w", padx=30)
        self.data_btn.place(x=0, y=253, width=249, height=50)

        self.result_btn = Button(self.menu_bar, text="Delete User", font=(ARIAL, 13, "normal"),command=self.transition_to_delete_user, border=0, bg="beige", fg="brown", anchor="w", padx=30)
        self.result_btn.place(x=0, y=304, width=249, height=50)

        self.logOut_btn = Button(self.menu_bar, text="Log Out", font=(ARIAL, 13, "normal"), command=self.logout, border=0, bg="beige", fg="brown", anchor="w", padx=30)
        self.logOut_btn.place(x=0, y=355, width=249, height=50)

        self.space = Label(self.menu_bar, bg="beige")
        self.space.place(x=0, y=406, width=249, height=100)
        
    
    def display_voting_results(self):
        self.voting_results = VotingResults(self.root)
        self.voting_results.display()
    
    def show_all_records(self):
        self.all_records = ShowAllRecord(self.root)
        self.all_records.display()
    
    def search_user(self):
        self.search_page = SearchUser(self.root)
        self.search_page.display()
    
    def show_update_user_form(self):
        self.update_user_instance = UpdateUser(self.root)
        self.update_user_instance.display()
    
    def transition_to_delete_user(self):
        self.delete_user_instance = DeleteUser(self.root)
        self.delete_user_instance.display()
    
    def logout(self):
        if hasattr(self, 'voting_results'):
            self.voting_results.cleanup()

        if hasattr(self, 'all_records'):
            self.all_records.cleanup()

        if hasattr(self, 'search_page'):
            self.search_page.cleanup()

        if hasattr(self, 'update_user_instance'):
            self.update_user_instance.cleanup()

        if hasattr(self, 'delete_user_instance'):
            self.delete_user_instance.cleanup()
        self.dashboardFrame.destroy()
        
        if hasattr(self, 'menu_bar'):
            self.menu_bar.destroy()

class VotingResults:
    def __init__(self, root):
        self.root = root
        self.result_frame = Frame(self.root, bg="white")

    def display(self):

        self.result_frame.place(x=250, y=0, width=650, height=500)

        total = Label(self.result_frame, text="Total vote", font=("ARIAL", 16, "bold", UNDERLINE), bg="white", fg="#05416a")
        total.place(x=150, y=50)
        party1=Label(self.result_frame,text="Nepali Congress",font=(LUCIDA_CONSOLE,12,"normal"),bg="white",fg="black")
        party1.place(x=150,y=150)
        party2=Label(self.result_frame,text="Nepal Communist Party \n(UML)",font=(LUCIDA_CONSOLE,12,"normal"),bg="white",fg="black")
        party2.place(x=150,y=200)
        party3=Label(self.result_frame,text="Nepal Communist Party \n(Maoist Center)",font=(LUCIDA_CONSOLE,12,"normal"),bg="white",fg="black")
        party3.place(x=150,y=250)
        party4=Label(self.result_frame,text="Nepal Communist Party \n(Unified Socialist)",font=(LUCIDA_CONSOLE,12,"normal"),bg="white",fg="black")
        party4.place(x=150,y=300)
        party5=Label(self.result_frame,text="Janata Samajbadi Party, \nNepal",font=(LUCIDA_CONSOLE,12,"normal"),bg="white",fg="black")
        party5.place(x=150,y=350)
        party6=Label(self.result_frame,text="Loktantrik Samajbadi \nParty, Nepal",font=(LUCIDA_CONSOLE,12,"normal"),bg="white",fg="black")
        party6.place(x=150,y=400)

        result = mysqlcon.getTotalCount()
        t_user = mysqlcon.getTotalUserCount()
        totalCount = Label(self.result_frame, text="{}  /  {}".format(result[0], t_user[0]), font=("", 15, "bold"), bg="white")
        totalCount.place(x=400, y=50)

        result1 = mysqlcon.getPartyCount("Nepali Congress")
        count1=Label(self.result_frame,text=result1, font=("",12,"bold"),bg="white")
        count1.place(x=400,y=150)

        result1 = mysqlcon.getPartyCount("Nepal Communist Party (UML)")
        count2=Label(self.result_frame,text=result1, font=("",12,"bold"),bg="white")
        count2.place(x=400,y=200)

        result1 = mysqlcon.getPartyCount("Nepal Communist Party (Maoist Center)")
        count3=Label(self.result_frame,text=result1, font=("",12,"bold"),bg="white")
        count3.place(x=400,y=250)

        result1 = mysqlcon.getPartyCount("Nepal Communist Party (Unified Socialist)")
        count4=Label(self.result_frame,text=result1, font=("",12,"bold"),bg="white")
        count4.place(x=400,y=300)
        
        result1 = mysqlcon.getPartyCount("Janata Samajbadi Party, Nepal")
        count5=Label(self.result_frame,text=result1, font=("",12,"bold"),bg="white")
        count5.place(x=400,y=350)

        result1 = mysqlcon.getPartyCount("Loktantrik Samajbadi Party, Nepal")
        count6=Label(self.result_frame,text=result1, font=("",12,"bold"),bg="white")
        count6.place(x=400,y=400)
    
    def cleanup(self):
        if hasattr(self, 'result_frame') and self.result_frame:
            self.result_frame.destroy()

class ShowAllRecord:
    def __init__(self, root):
        self.root = root
        self.data_frame = Frame(self.root, bg="white")

    def display(self):
        self.data_frame.place(x=250, y=0, width=650, height=500)

        header_label = Label(self.data_frame, text="Details of Recorded Users", font=("Arial", 15), fg="#05416a", bg="white")
        header_label.place(x=20, y=20)

        st = scrolledtext.ScrolledText(self.data_frame, wrap=tk.WORD, width=75, height=25)
        st.place(x=20, y=70)
        
        st.tag_configure("boldTNR", font=("Times New Roman", 10, "bold"))

        result = mysqlcon.getallVoters()
        
        for r in result:
            fields = ["Voter ID", "Name", "CitizenshipNo", "Phone", "Gender", "Address", "Voted Status", "Vote Casted From"]
            values = [str(value) for value in r]
            for field, value in zip(fields, values):
                st.insert(tk.END, "{}: ".format(field), "boldTNR")
                st.insert(tk.END, "{}\n".format(value))
            st.insert(tk.END, "\n")

        st.config(state=tk.DISABLED)

    def clear(self):
        if hasattr(self, 'data_frame') and self.data_frame:
            self.data_frame.destroy()

class SearchUser:
    def __init__(self, root):
        self.root = root
        self.citizenship = StringVar()

    def search(self):
        # Implementing the logic for searching a user based on their citizenship
        if self.citizenship.get() == "" or len(self.citizenship.get()) != 11 or not self.citizenship.get().isdigit():
            messagebox.showwarning('Voting System Message', '🎱 Field is required\n🎱 Citizenship number length must be 11 digit')
            return

        user = mysqlcon.getUserByCitizenship(self.citizenship.get())
        if user is None:
            messagebox.showinfo('Voting System Message', 'No such User')
        else:
            # Display user's details (this can be modified based on your UI design)
            messagebox.showinfo('Voting System Message', f"User Details:\nName: {user[0]}\nPhone: {user[1]}\nGender: {user[2]}\nDistrict: {user[3]}")

    def display(self):
        self.search_frame = Frame(self.root)
        self.search_frame.place(x=250, y=0, width=650, height=500)
        self.search_frame.configure(background="white")

        self.citizenship_label = Label(self.search_frame, text="Citizenship Number", font=("Arial", 13), bg="white")
        self.citizenship_label.place(x=100, y=150, height=30)

        citizenship_entry = Entry(self.search_frame, textvariable=self.citizenship, font=("Arial", 12), bg="#f0f0f0", border=0)
        citizenship_entry.place(x=275, y=150, width=250, height=30)

        search_btn = Button(self.search_frame, text="SEARCH", font=("Arial", 12, "bold"), command=self.search, border=0, bg=HIGHLIGHT_BG, fg="white")
        search_btn.place(x=250, y=230, width=150, height=40)
    
    def cleanup(self):
        if hasattr(self, 'search_frame') and self.search_frame:
            self.search_frame.destroy()

class UpdateUser:
    def __init__(self, root):
        self.root = root
        self.citizenship = StringVar()
        self.name = StringVar()
        self.phone = StringVar()
        self.gender = StringVar()
        self.district = StringVar()

    def search(self):
        user = mysqlcon.findByCitizenships(self.citizenship.get())
        if user is None:
            messagebox.showinfo('Voting System Message', 'No such User')
            return
        
        # Populate the fields with the fetched user details
        self.name.set(user[1])
        self.phone.set(user[2])
        self.gender.set(user[4])
        self.district.set(user[3])

    def update(self):
        try:
            if not all([self.name.get(), self.phone.get(), self.gender.get(), self.district.get()]):
                messagebox.showwarning('Voting System Message', 'All fields are required.')
                return

            if len(self.phone.get()) != 10 or not self.phone.get().isdigit():
                messagebox.showwarning('Voting System Message', 'Invalid phone number. It must be 10 digits.')
                return
            
            success = mysqlcon.updateUserByCitizenship(self.name.get(), self.phone.get(), self.gender.get(), self.district.get(), self.citizenship.get())
            
            if success:
                messagebox.showinfo('Voting System Message', 'User updated successfully.')
            else:
                messagebox.showerror('Voting System Message', 'Failed to update the user.')

        except Exception as e:
            messagebox.showerror('Voting System Message', f'An unexpected error occurred: {str(e)}')

    def display(self):
        self.update_frame = Frame(self.root)
        self.update_frame.place(x=250, y=0, width=650, height=500)
        self.update_frame.configure(background="white")

        self.citizenship_label = Label(self.update_frame, text="Citizenship Number", font=("Arial", 13), bg="white")
        self.citizenship_label.place(x=100, y=50, height=30)
        
        self.citizenship_entry = Entry(self.update_frame, textvariable=self.citizenship, font=("Arial", 12), bg="#f0f0f0", border=0)
        self.citizenship_entry.place(x=275, y=50, width=250, height=30)
        
        self.search_btn = Button(self.update_frame, text="SEARCH", font=("Arial", 12, "bold"), command=self.search, border=0, bg=HIGHLIGHT_BG, fg="white")
        self.search_btn.place(x=550, y=50, width=80, height=30)

        # Following are the fields to update the user details
        self.name_label = Label(self.update_frame, text="Name", font=("Arial", 13), bg="white")
        self.name_label.place(x=100, y=100, height=30)
        
        self.name_entry = Entry(self.update_frame, textvariable=self.name, font=("Arial", 12), bg="#f0f0f0", border=0)
        self.name_entry.place(x=275, y=100, width=250, height=30)

        self.phone_label = Label(self.update_frame, text="Phone", font=("Arial", 13), bg="white")
        self.phone_label.place(x=100, y=150, height=30)

        self.phone_entry = Entry(self.update_frame, textvariable=self.phone, font=("Arial", 12), bg="#f0f0f0", border=0)
        self.phone_entry.place(x=275, y=150, width=250, height=30)

        self.gender_label = Label(self.update_frame, text="Gender", font=("Arial", 13), bg="white")
        self.gender_label.place(x=100, y=200, height=30)

        self.gender_combobox = Combobox(self.update_frame, values=["Male", "Female", "Non-Binary", "Intersex", "Don't wanna state"], font=("Arial", 12), textvariable=self.gender)
        self.gender_combobox.place(x=275, y=200, width=250, height=30)

        self.district_label = Label(self.update_frame, text="Address", font=("Arial", 13), bg="white")
        self.district_label.place(x=100, y=250, height=30)

        self.district_entry = Entry(self.update_frame, textvariable=self.district, font=("Arial", 12), bg="#f0f0f0", border=0)
        self.district_entry.place(x=275, y=250, width=250, height=30)

        self.update_btn = Button(self.update_frame, text="UPDATE", font=("Arial", 12, "bold"), command=self.update, border=0, bg=HIGHLIGHT_BG, fg="white")
        self.update_btn.place(x=275, y=300, width=150, height=40)
        
    def cleanup(self):
        if hasattr(self, 'update_frame') and self.update_frame:
            self.update_frame.destroy()

class DeleteUser:
    def __init__(self, root):
        self.root = root
        self.citizenship = tk.StringVar()
    
    def delete(self):
        try:
            if not self.citizenship.get() or len(self.citizenship.get()) != 11 or not self.citizenship.get().isdigit():
                logging.warning('Attempt to delete with missing or invalid citizenship field.')
                messagebox.showwarning('Voting System Message', '🎱 Field is required\n🎱 Citizenship number length must be 11 digit')
            else:
                userResult = mysqlcon.findByCitizenship(self.citizenship.get())
                if not userResult:
                    logging.info(f'Attempt to delete non-existent user with citizenship {self.citizenship.get()}.')
                    messagebox.showinfo('Voting System Message', 'No such User')
                else:
                    if mysqlcon.deleteUserByCitizenship(self.citizenship.get()):
                        logging.info(f'User with citizenship {self.citizenship.get()} deleted successfully.')
                        messagebox.showinfo('Voting System Message', 'User Deleted')
                    else:
                        logging.error(f'Failed to delete user with citizenship {self.citizenship.get()}.')
                        messagebox.showwarning('Voting System Message', 'Try again later, unable to delete user')
                self.citizenship.set("")
                
        except Exception as e:
            logging.error(f'Error during delete operation: {str(e)}')
            messagebox.showerror('Voting System Message', 'An unexpected error occurred. Please try again later.')
    
    def display(self):
        self.DeleteFrame = tk.Frame(self.root)
        self.DeleteFrame.place(x=250, y=0, width=650, height=500)
        self.DeleteFrame.configure(background="white")

        self.citizenshipLabel = tk.Label(self.DeleteFrame, text="Citizenship Number", font=(ARIAL, 13, "bold"), bg="white")
        self.citizenshipLabel.place(x=100, y=150, height=30)

        self.citizenshipValue = tk.Entry(self.DeleteFrame, textvariable=self.citizenship, font=(ARIAL, 12, "normal"), bg="#f0f0f0", border=0)
        self.citizenshipValue.place(x=275, y=150, width=250, height=30)

        self.delete_btn = tk.Button(self.DeleteFrame, text="Delete", font=(ARIAL, 13, "normal"), command=self.delete, border=0, bg=HIGHLIGHT_BG, fg="white")
        self.delete_btn.place(x=250, y=230, width=150, height=40)
    
    def cleanup(self):
        if hasattr(self, 'DeleteFrame') and self.DeleteFrame:
            self.DeleteFrame.destroy()


if __name__ == "__main__":
    app = VotingSystem()
    app.root.mainloop()

