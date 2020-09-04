from tkinter import *

from PIL import ImageTk, Image

from FinalAssignment.StudentResultDBMS import *

from tkinter.ttk import Treeview, Combobox


def Navigate(current_frame, destination_page):
    current_frame.pack_forget()
    try:
        destination_page()
    except TypeError:
        pass


def pack_destroy(label_name):
    label_name.pack()
    label_name.after(2000, lambda: label_name.destroy())


class Btn_func:
    def __init__(self):
        pass

    def Show_Login(self):
        Main_Frame.pack_forget()
        FrameConstructor.User_Login(self)

    def Show_Register(self):
        Main_Frame.pack_forget()
        FrameConstructor.User_Register(self)

    def UserLogin(self):
        def Empty_Entries():
            UserName_Login_Entry.delete(0, END)
            Password_Login_Entry.delete(0, END)

        Username_Get = UserName_Login_Entry.get()
        Password_Get = Password_Login_Entry.get()
        Credential_tuple = (Username_Get, Password_Get)

        if '' in Credential_tuple:
            Empty_Entries()
            User_Prompt(Login_Frame).Empty_Entry()
        else:
            Empty_Entries()
            Login_Status = Login(Username_Get, Password_Get)
            if Login_Status.check_username():
                if Login_Status.check_password() == 'teacher':
                    Empty_Entries()
                    User_Prompt(Login_Frame).Success()
                    Login_Frame.after(2500, lambda: Navigate(Login_Frame, self.Teacher_Main))
                elif Login_Status.check_password() == 'student':
                    Empty_Entries()
                    User_Prompt(Login_Frame).Success()
                    Login_Frame.after(2500, lambda: Navigate(Login_Frame, self.Student_Main(Username_Get)))
                elif not Login_Status.check_password():
                    Empty_Entries()
                    User_Prompt(Login_Frame).Nomatch_Error('password')
            else:
                Empty_Entries()
                User_Prompt(Login_Frame).Nomatch_Error('username')

    def UserRegister(self):
        def Empty_Entries():
            Name_Register_Entry.delete(0, END)
            UserName_Register_Entry.delete(0, END)
            Password_Register_Entry.delete(0, END)
            Confirm_Register_Entry.delete(0, END)

        Name_get = Name_Register_Entry.get()
        Faculty_Get = Faculty.get()
        Username_Get = UserName_Register_Entry.get()
        Password_Get = Password_Register_Entry.get()
        Confirm_Get = Confirm_Register_Entry.get()
        Register_tuple = (Name_get, Username_Get, Password_Get, Confirm_Get, Faculty_Get)

        if '' in Register_tuple:
            Empty_Entries()
            User_Prompt(Register_Frame).Empty_Entry()
        elif Confirm_Get != Password_Get:
            Empty_Entries()
            User_Prompt(Register_Frame).Nomatch_Error('password')
        else:
            reg = Register(Name_get, Username_Get, Password_Get, Faculty_Get)
            if reg.check_username():
                Empty_Entries()
                User_Prompt(Register_Frame).Username_Taken()
            else:
                Empty_Entries()
                User_Prompt(Register_Frame).Success()
                Register_Frame.after(2500, lambda: Navigate(Register_Frame, self.Main_Page))

    def SubmitResults(self):

        def Empty_Entries():
            Student_ID.delete(0, END)
            Subject_Code.delete(0, END)
            Subject_Marks.delete(0, END)

        StudentID_Get = Student_ID.get()
        Name_Get = Student_Name.get()
        SubjectCode_Get = Subject_Code.get()
        Marks_Get = Subject_Marks.get()

        try:
            int_marks = int(Marks_Get)
        except ValueError:
            User_Prompt(Teacher_Frame).Custom_Input('Please input numeric value')
            Subject_Marks.delete(0, END)
        else:
            if int_marks > 100:
                User_Prompt(Teacher_Frame).Custom_Input('Marks Cannot be more than 100')
                Subject_Marks.delete(0, END)
            else:
                if '' in [StudentID_Get, Name_Get, SubjectCode_Get, Marks_Get]:
                    Empty_Entries()
                    User_Prompt(Teacher_Frame).Empty_Entry()
                else:
                    res = Result(StudentID_Get, Name_Get, SubjectCode_Get, Marks_Get)
                    res.store_result()
                    User_Prompt(Teacher_Frame).Success()
                    Empty_Entries()


class User_Prompt:
    def __init__(self, frame_name):
        self.frame_name = frame_name

    def Empty_Entry(self):
        Login_Error_Label = Label(self.frame_name, text='All fields required', fg='red')
        pack_destroy(Login_Error_Label)

    def Nomatch_Error(self, prompt):
        text = prompt + " does not match"
        Nomatch_Error_Label = Label(self.frame_name, text=text, fg='red')
        pack_destroy(Nomatch_Error_Label)

    def Success(self):
        Successful_Label = Label(self.frame_name, text="Action successful!", fg='green')
        pack_destroy(Successful_Label)

    def Username_Taken(self):
        Username_Taken_Label = Label(self.frame_name, text="Username Taken", fg="red")
        pack_destroy(Username_Taken_Label)

    def Custom_Input(self, text):
        tx = text
        Invalid_Input_Label = Label(self.frame_name, text=tx, fg="red")
        pack_destroy(Invalid_Input_Label)


class FrameConstructor:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1280x600")
        self.root.title("Result Management System")
        self.Main_Page()
        self.root.mainloop()

    def Main_Page(self):
        global Main_Frame
        global background

        Main_Frame = Frame(self.root)
        Main_Frame.pack(fill="both", expand=1)

        background = ImageTk.PhotoImage(Image.open("softwarica.png"))
        Label(Main_Frame, image=background, bd=0).pack()

        Button(Main_Frame, text='Login', command=lambda: Btn_func.Show_Login(self)).pack()
        Button(Main_Frame, text='Register', command=lambda: Btn_func.Show_Register(self)).pack()

    def User_Login(self):
        global Login_Frame
        global UserName_Login_Entry
        global Password_Login_Entry

        Login_Frame = Frame(self.root)
        Login_Frame.pack(fill="both", expand=1)

        login_wrapper = LabelFrame(Login_Frame, bd=0)
        login_wrapper.pack(padx=20, pady=100)

        Label(login_wrapper, text='username: ').grid(row=1, column=1, padx=20, pady=20)
        UserName_Login_Entry = Entry(login_wrapper)
        UserName_Login_Entry.grid(row=1, column=2, padx=20, pady=20)

        Label(login_wrapper, text='password: ').grid(row=2, column=1, padx=20, pady=20)
        Password_Login_Entry = Entry(login_wrapper, show="*")
        Password_Login_Entry.grid(row=2, column=2, padx=20, pady=20)

        Button(login_wrapper, text="Login",
               command=lambda: Btn_func.UserLogin(self)).grid(row=3, column=1, padx=20, pady=20)
        Button(login_wrapper, text="Back",
               command=lambda: Navigate(Login_Frame, self.Main_Page)).grid(row=3, column=2, padx=20, pady=20)

    def User_Register(self):
        global Register_Frame
        global Name_Register_Entry
        global UserName_Register_Entry
        global Password_Register_Entry
        global Confirm_Register_Entry
        global Faculty

        Register_Frame = Frame(self.root)
        Register_Frame.pack(expand=1, fill=BOTH)

        register_wrapper = LabelFrame(Register_Frame, bd=0)
        register_wrapper.pack(padx=20, pady=75)

        Label(register_wrapper, text='name: ').grid(row=1, column=1, padx=10, pady=10)
        Name_Register_Entry = Entry(register_wrapper)
        Name_Register_Entry.grid(row=1, column=2, padx=10, pady=10)

        Label(register_wrapper, text='username: ').grid(row=2, column=1, padx=10, pady=10)
        UserName_Register_Entry = Entry(register_wrapper)
        UserName_Register_Entry.grid(row=2, column=2, padx=10, pady=10)

        Label(register_wrapper, text='password: ').grid(row=3, column=1, padx=10, pady=10)
        Password_Register_Entry = Entry(register_wrapper, show='*')
        Password_Register_Entry.grid(row=3, column=2, padx=10, pady=10)

        Label(register_wrapper, text='confirm password: ').grid(row=4, column=1, padx=10, pady=10)
        Confirm_Register_Entry = Entry(register_wrapper, show="*")
        Confirm_Register_Entry.grid(row=4, column=2, padx=10, pady=10)

        Label(register_wrapper, text='faculty').grid(row=5, column=1)
        Faculty = Combobox(register_wrapper,
                           values=['teacher', 'student'], state='readonly')
        Faculty.grid(row=5, column=2, padx=10, pady=10)

        Button(register_wrapper, text="Register",
               command=lambda: Btn_func.UserRegister(self)).grid(row=6, column=1, padx=10, pady=10)
        Button(register_wrapper, text="Back",
               command=lambda: Navigate(Register_Frame, self.Main_Page)).grid(row=6, column=2, padx=10, pady=10)

    def Teacher_Main(self):
        global Teacher_Frame
        global Student_ID
        global Student_Name
        global Subject_Code
        global Subject_Marks

        def update():
            children = Tree.get_children()
            for i in children:
                Tree.delete(i)
            x = DBMS_Connection()
            for i in x.show_result():
                Tree.insert('', 'end', values=i)

        def get_id():
            x = DBMS_Connection()
            return x.show_username()

        def callback(*args):
            sid = Student_ID.get()
            x = DBMS_Connection()
            name = x.show_name(sid)
            Student_Name.delete(0, END)
            Student_Name.insert(0, name)

        Teacher_Frame = Frame(self.root)
        Teacher_Frame.pack(expand=1, fill=BOTH)

        Teacher_Wrapper1 = LabelFrame(Teacher_Frame)
        Teacher_Wrapper1.pack(padx=15, pady=15)

        Teacher_Wrapper2 = LabelFrame(Teacher_Frame, bd=0)
        Teacher_Wrapper2.pack(padx=15, pady=15)

        Label(Teacher_Wrapper1, text="Student ID:").grid(row=1, column=1,
                                                         padx=15, pady=15)
        Student_ID = Combobox(Teacher_Wrapper1, textvariable='', values=get_id(), state='readonly')
        Student_ID.bind("<<ComboboxSelected>>", callback)
        Student_ID.grid(row=1, column=2,
                        padx=15, pady=15)

        Label(Teacher_Wrapper1, text="Student Name:").grid(row=2, column=1,
                                                           padx=15, pady=15)
        Student_Name = Entry(Teacher_Wrapper1)
        Student_Name.grid(row=2, column=2,
                          padx=15, pady=15)

        Label(Teacher_Wrapper1, text="Subject code:").grid(row=3, column=1,
                                                           padx=15, pady=15)
        Subject_Code = Entry(Teacher_Wrapper1)
        Subject_Code.grid(row=3, column=2, padx=15, pady=15)

        Label(Teacher_Wrapper1, text="Marks obtained:").grid(row=4, column=1,
                                                             padx=15, pady=15)
        Subject_Marks = Entry(Teacher_Wrapper1)
        Subject_Marks.grid(row=4, column=2, padx=15, pady=15)

        Button(Teacher_Wrapper1, text='submit',
               command=lambda: [Btn_func.SubmitResults(self), update()]).grid(row=5, column=1,
                                                                              padx=15, pady=15)

        Button(Teacher_Wrapper1, text="Done",
               command=lambda: Navigate(Teacher_Frame, self.Main_Page)).grid(row=5, column=2,
                                                                             padx=15, pady=15)
        Label(Teacher_Wrapper2, text="").grid(row=1, column=1)

        Tree = Treeview(Teacher_Wrapper2, columns=(1, 2, 3, 4), show="headings", height="10")
        Tree.grid(row=1, column=2)
        Tree.heading(1, text="Student ID")
        Tree.heading(2, text='Student Name')
        Tree.heading(3, text="Subject code")
        Tree.heading(4, text="Marks obtained")

        Label(Teacher_Wrapper2, text="").grid(row=1, column=3)

        # Button(Teacher_Wrapper2, text='Delete').grid(row=2, column=1)
        # Button(Teacher_Wrapper2, text='Edit').grid(row=2, column=3)

        update()

    def Student_Main(self, un):
        global Student_Frame
        username = un

        def get_results(lis, uname):
            """linear search algorithm"""
            l = []
            for i in lis:
                for j in i:
                    if j == uname:
                        y = (i[-2], i[-1])
                        l.append(y)
            return l

            # start = 0
            # end = len(lis) - 1
            # while start <= end:
            #     mid = (start + end) // 2
            #     if list[mid][0] == uname:
            #         return mid
            #     elif list[mid][0] > uname:
            #         end = mid - 1
            #     else:
            #         start = mid + 1
            # return -1

        def update():
            children = Tree.get_children()
            for i in children:
                Tree.delete(i)
            x = DBMS_Connection()
            ls = x.show_result()
            for i in get_results(ls, username):
                Tree.insert('', 'end', values=i)

        Student_Frame = Frame(self.root)
        Student_Frame.pack(expand=1, fill=BOTH)

        Label(Student_Frame, text=f'Welcome {username}').pack()

        student_wrapper = LabelFrame(Student_Frame)
        student_wrapper.pack()

        Tree = Treeview(student_wrapper, columns=(1, 2), show='headings', height='10')
        Tree.pack()
        Tree.heading(1, text='subject')
        Tree.heading(2, text='marks')

        Button(Student_Frame, text="Done",
               command=lambda: Navigate(Student_Frame, self.Main_Page())).pack()

        update()


if __name__ == "__main__":
    FrameConstructor()
