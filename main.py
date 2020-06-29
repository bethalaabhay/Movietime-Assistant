from tkinter import *
import json
import re
from PIL import ImageTk, Image



seatLayout = [
    "A1", "A10", "A2", "A9", "A3", "A8", "A4", "A7", "A5", "A6",
    "B1", "B10", "B2", "B9", "B3", "B8", "B4", "B7", "B5", "B6",
    "C1", "C10", "C2", "C9", "C3", "C8", "C4", "C7", "C5", "C6",
    "D1", "D10", "D2", "D9", "D3", "D8", "D4", "D7", "D5", "D6",
    "E1", "E10", "E2", "E9", "E3", "E8", "E4", "E7", "E5", "E6",
    "F1", "F10", "F2", "F9", "F3", "F8", "F4", "F7", "F5", "F6",
    "G1", "G10", "G2", "G9", "G3", "G8", "G4", "G7", "G5", "G6",
    "H1", "H10", "H2", "H9", "H3", "H8", "H4", "H7", "H5", "H6",
    "I1", "I10", "I2", "I9", "I3", "I8", "I4", "I7", "I5", "I6",
    "J1", "J10", "J2", "J9", "J3", "J8", "J4", "J7", "J5", "J6",
]

seatState = {
    "A1": False, "A10": False, "A2": False, "A9": False, "A3": False, "A8": False, "A4": False, "A7": False, "A5": False, "A6": False,
    "B1": False, "B10": False, "B2": False, "B9": False, "B3": False, "B8": False, "B4": False, "B7": False, "B5": False, "B6": False,
    "C1": False, "C10": False, "C2": False, "C9": False, "C3": False, "C8": False, "C4": False, "C7": False, "C5": False, "C6": False,
    "D1": False, "D10": False, "D2": False, "D9": False, "D3": False, "D8": False, "D4": False, "D7": False, "D5": False, "D6": False,
    "E1": False, "E10": False, "E2": False, "E9": False, "E3": False, "E8": False, "E4": False, "E7": False, "E5": False, "E6": False,
    "F1": False, "F10": False, "F2": False, "F9": False, "F3": False, "F8": False, "F4": False, "F7": False, "F5": False, "F6": False,
    "G1": False, "G10": False, "G2": False, "G9": False, "G3": False, "G8": False, "G4": False, "G7": False, "G5": False, "G6": False,
    "H1": False, "H10": False, "H2": False, "H9": False, "H3": False, "H8": False, "H4": False, "H7": False, "H5": False, "H6": False,
    "I1": False, "I10": False, "I2": False, "I9": False, "I3": False, "I8": False, "I4": False, "I7": False, "I5": False, "I6": False,
    "J1": False, "J10": False, "J2": False, "J9": False, "J3": False, "J8": False, "J4": False, "J7": False, "J5": False, "J6": False,
}

MOVIEDATA_PATH = "data.json"

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 575
WINDOW_PADX = (10, 0)

COLOR_GREY = "#132226"
COLOR_BLACK = "#A4978E"
COLOR_WHITE = "#040C0E"
COLOR_RED = "#ED2939"

CHAT_WINDOW_TITLE = "VIT Cinemas"
INITIAL_GREETING = "Hey! How may I help you?"
INITIAL_OPTION1 = "Movies and Shows"
INITIAL_OPTION2 = "Book a Ticket.."
INITIAL_OPTION3 = "Your tickets"
SELECT_MOVIE = "Select a movie to view shows.."
ENTER_EMAIL = "Enter your Email Id"



def SetMessageAttributes(widget):
    widget["borderwidth"] = 1
    widget["relief"] = "solid"
    widget["anchor"] = CENTER
    widget["bg"] = COLOR_BLACK
    widget["fg"] = COLOR_WHITE
    widget["padx"] = 10
    widget["pady"] = 5
    widget["font"] = ("Georgia", 10)
    widget["width"] = 35

def SetButtonAttributes(widget):
    widget["borderwidth"] = 1
    widget["relief"] = "solid"
    widget["anchor"] = CENTER
    widget["bg"] = COLOR_WHITE
    widget["fg"] = COLOR_BLACK
    widget["padx"] = 10
    widget["pady"] = 5
    widget["font"] = ("Georgia", 10)
    widget["width"] = 34

def SetEntryAttributes(widget):
    widget["borderwidth"] = 1
    widget["relief"] = "solid"
    widget["bg"] = COLOR_WHITE
    widget["fg"] = COLOR_BLACK
    widget["font"] = ("Georgia", 13)
    widget["justify"] = CENTER
    widget["width"] = 29

def ResetSeatState():
    for seat in seatState:
        seatState[seat] = False

def OnSignupSuccess():
    #remove everything on screen
    for widget in ChatFrame.winfo_children():
            widget.destroy()

    LoginSuccess = Label(ChatFrame, text = "Account Created\nSuccessfully")
    LoginSuccess["font"] = ("Sans serif", 16, "bold")
    LoginSuccess["height"] = 2
    LoginSuccess["bg"] = COLOR_GREY
    LoginSuccess["fg"] = COLOR_BLACK
    LoginSuccess.pack(padx = (3, 0), pady = (100, 30))

    Login = Button(ChatFrame, text = "Login Now!", command = OnStartup)
    SetMessageAttributes(Login)
    Login["width"] = 17
    Login.pack()

def ValidateSignup():
    global tempEmail
    global tempPass
    global tempConfirmPass
    global loginEmailErrorMsg
    global loginPassErrorMsg

    loginEmailErrorMsg.set("")
    loginPassErrorMsg.set("")

    emailRegex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not (re.search(emailRegex, tempEmail.get())):
        loginEmailErrorMsg.set("Enter a valid email address")
        return

    #checking if user already exists
    userExists = False
    for user in movieData["users"]:
        if tempEmail.get() == user["email"]:
            userExists = True
    if userExists == True:
        loginEmailErrorMsg.set("User with specified Email ID already exists")
        return

    if tempPass.get() == "":
        loginPassErrorMsg.set("Password cannot be empty")
        return

    if not tempPass.get() == tempConfirmPass.get():
        loginPassErrorMsg.set("Passwords do not match")
        return

    #register user
    movieData["users"].append({"email" : tempEmail.get(), "password": tempPass.get()})

    OnSignupSuccess()

def OnSignup():
    global tempEmail
    global tempPass
    global tempConfirmPass
    global loginEmailErrorMsg
    global loginPassErrorMsg
    
    #remove everything on screen
    for widget in ChatFrame.winfo_children():
            widget.destroy()
    
    Signup = Label(ChatFrame, text = "Welcome to VIT Cinemas!")
    Signup["font"] = ("Sans serif", 16, "bold")
    Signup["height"] = 2
    Signup["bg"] = COLOR_GREY
    Signup["fg"] = COLOR_BLACK
    Signup.pack(padx = (3, 0), pady = (35, 0))

    EmailLabel = Label(ChatFrame, text = "Email")
    EmailLabel["font"] = ("Georgia", 14)
    EmailLabel["bg"] = COLOR_GREY
    EmailLabel["fg"] = COLOR_BLACK
    EmailLabel.pack(padx = (0, 240), pady = (30, 0))
    
    Email = Entry(ChatFrame, textvariable = tempEmail)
    SetEntryAttributes(Email)
    Email.pack(padx = (50, 50), pady = (2, 2))
    Email["justify"] = LEFT
    Email.focus()

    EmailErrorMessage = Label(ChatFrame, textvariable = loginEmailErrorMsg)
    EmailErrorMessage["fg"] = COLOR_RED
    EmailErrorMessage["bg"] = COLOR_GREY
    EmailErrorMessage["justify"] = LEFT
    EmailErrorMessage.pack() 

    PassLabel = Label(ChatFrame, text = "Password")
    PassLabel["font"] = ("Georgia", 14)
    PassLabel["bg"] = COLOR_GREY
    PassLabel["fg"] = COLOR_BLACK
    PassLabel.pack(padx = (0, 208), pady = (15, 0))
    
    Pass = Entry(ChatFrame, textvariable = tempPass, show = "*")
    SetEntryAttributes(Pass)
    Pass.pack(padx = (50, 50), pady = (2, 2))
    Pass["justify"] = LEFT

    PassErrorMessage = Label(ChatFrame, textvariable = loginPassErrorMsg)
    PassErrorMessage["fg"] = COLOR_RED
    PassErrorMessage["bg"] = COLOR_GREY
    PassErrorMessage["justify"] = LEFT
    PassErrorMessage.pack()

    ConfirmPassLabel = Label(ChatFrame, text = "Confirm Password")
    ConfirmPassLabel["font"] = ("Georgia", 14)
    ConfirmPassLabel["bg"] = COLOR_GREY
    ConfirmPassLabel["fg"] = COLOR_BLACK
    ConfirmPassLabel.pack(padx = (0, 135), pady = (15, 0))
    
    ConfirmPass = Entry(ChatFrame, textvariable = tempConfirmPass, show = "*")
    SetEntryAttributes(ConfirmPass)
    ConfirmPass.pack(padx = (50, 50), pady = (2, 2))
    ConfirmPass["justify"] = LEFT
    ConfirmPass.bind('<Return>', lambda dummy: ValidateSignup())

    SignupButton = Button(ChatFrame, text = "Signup", command = ValidateSignup)
    SetMessageAttributes(SignupButton)
    SignupButton["width"] = 17
    SignupButton.pack(pady = (45, 0))

    Login = Button(ChatFrame, text = "Already have an account? Login", command = OnStartup)
    Login["bg"] = COLOR_GREY
    Login["fg"] = COLOR_BLACK
    Login["borderwidth"] = 0
    Login.pack()


def ValidateLogin():
    global userEmail
    global tempEmail
    global tempPass
    global loginEmailErrorMsg
    global loginPassErrorMsg

    loginEmailErrorMsg.set("")
    loginPassErrorMsg.set("")

    userExists = False

    for user in movieData["users"]:
        if tempEmail.get() == user["email"]:
            userExists = True
            if tempPass.get() == user["password"]:
                userEmail.set(tempEmail.get())
                StartChat()
            else:
                loginPassErrorMsg.set("Incorrect Password")
    
    if userExists == False:
        loginEmailErrorMsg.set("User with specified Email ID does not exist")

def OnStartup():
    global tempEmail
    global tempPass
    global loginEmailErrorMsg
    global loginPassErrorMsg

    #remove everything on screen
    for widget in ChatFrame.winfo_children():
            widget.destroy()

    Login = Label(ChatFrame, text = "Welcome to VIT Cinemas!")
    Login["font"] = ("Sans serif", 16, "bold")
    Login["height"] = 2
    Login["bg"] = COLOR_GREY
    Login["fg"] = COLOR_BLACK
    Login.pack(padx = (3, 0), pady = (35, 0))

    EmailLabel = Label(ChatFrame, text = "Email")
    EmailLabel["font"] = ("Georgia", 14)
    EmailLabel["bg"] = COLOR_GREY
    EmailLabel["fg"] = COLOR_BLACK
    EmailLabel.pack(padx = (0, 240), pady = (30, 0))
    
    Email = Entry(ChatFrame, textvariable = tempEmail)
    SetEntryAttributes(Email)
    Email.pack(padx = (50, 50), pady = (2, 2))
    Email["justify"] = LEFT
    Email.focus()
    Email.bind('<Return>', lambda dummy: ValidateLogin())

    EmailErrorMessage = Label(ChatFrame, textvariable = loginEmailErrorMsg)
    EmailErrorMessage["fg"] = COLOR_RED
    EmailErrorMessage["bg"] = COLOR_GREY
    EmailErrorMessage["justify"] = LEFT
    EmailErrorMessage.pack() 

    PassLabel = Label(ChatFrame, text = "Password")
    PassLabel["font"] = ("Georgia", 14)
    PassLabel["bg"] = COLOR_GREY
    PassLabel["fg"] = COLOR_BLACK
    PassLabel.pack(padx = (0, 208), pady = (15, 0))
    
    Pass = Entry(ChatFrame, textvariable = tempPass, show = "*")
    SetEntryAttributes(Pass)
    Pass.pack(padx = (50, 50), pady = (2, 2))
    Pass["justify"] = LEFT
    Pass.bind('<Return>', lambda dummy: ValidateLogin())

    PassErrorMessage = Label(ChatFrame, textvariable = loginPassErrorMsg)
    PassErrorMessage["fg"] = COLOR_RED
    PassErrorMessage["bg"] = COLOR_GREY
    PassErrorMessage["justify"] = LEFT
    PassErrorMessage.pack() 

    LoginButton = Button(ChatFrame, text = "Login", command = ValidateLogin)
    SetMessageAttributes(LoginButton)
    LoginButton["width"] = 17
    LoginButton.pack(pady = (25, 0))

    Signup = Button(ChatFrame, text = "New User? Signup", command = OnSignup)
    Signup["bg"] = COLOR_GREY
    Signup["fg"] = COLOR_BLACK
    Signup["borderwidth"] = 0
    Signup.pack()

def EndChat():
    ChatWindow.destroy()

def HomeExit():
    Home = Button(ChatFrame, text = "Go Back Home...", command = lambda:StartChat(0))
    SetButtonAttributes(Home)
    Home.pack(padx = WINDOW_PADX, pady = (40,0))

    Exit = Button(ChatFrame, text = "Exit", command = lambda:EndChat())
    SetButtonAttributes(Exit)
    Exit.pack(padx = WINDOW_PADX, pady = (5,20))

def OnClickMovieShows(title):

    for widget in ChatFrame.winfo_children():
            widget.destroy()

    strViewShows = f"{title} shows..." 
    listShows = Label(ChatFrame, text = strViewShows)
    SetMessageAttributes(listShows)
    listShows["height"] = 2
    listShows.pack(padx = WINDOW_PADX, pady = (40,0))

    for show in movieData["shows"]:
        if show["title"] == title:
            strShowInfo = f'Date: {show["date"]} |  Time: {show["time"]}\nScreen: {show["screen"]}'
            Show = Button(ChatFrame, text = strShowInfo)
            SetButtonAttributes(Show)
            Show.pack(padx = WINDOW_PADX)

    HomeExit()

def OnClickInitialOption1():
    global option1Active
    global option2Active
    global option3Active

    if option2Active or option3Active:
        for widget in ChatFrame.winfo_children():
            widget.destroy()
        option2Active = False
        option3Active = False
        StartChat(1)

    if(option1Active == False):
        ListMovies = Label(ChatFrame, text = SELECT_MOVIE)
        SetMessageAttributes(ListMovies)
        ListMovies["height"] = 2
        ListMovies.pack(padx = WINDOW_PADX, pady = (10,0))

        for movie in movieData["movies"]:
            strMovieInfo = f'{movie["title"]}\n{movie["rating"]} | {movie["language"]} | {movie["genre"]}'
            Movie = Button(ChatFrame, text = strMovieInfo, command = lambda strMovieTitle = movie["title"] : OnClickMovieShows(strMovieTitle))
            SetButtonAttributes(Movie)
            Movie.pack(padx = WINDOW_PADX)

        option1Active = True
        option2Active = False
        option3Active = False

def BookTicket(title, date):
    
    bookedSeats = []

    seatsSelected = False
    for seat in seatState:
        if seatState[seat] == True:
            seatsSelected = True
            bookedSeats.append(seat)
    
    if seatsSelected == False:
        return
    
    for widget in ChatFrame.winfo_children():
            widget.destroy()

    bookShow = []
    for show in movieData["shows"]:
        if title == show["title"] and date == show["date"]:
            bookShow = show
            break

    email = userEmail.get()
    movieData["tickets"].append({"email": email, "title": title, "date": date, "time": bookShow["time"], "screen": bookShow["screen"], "seats": bookedSeats})

    for bookedSeat in bookedSeats:
        bookShow["seatsbooked"].append(bookedSeat)
    
    MessageBooked = Button(ChatFrame, text = "Your ticket has been booked successfully!")
    MessageBooked["font"] = ("Sans serif", 10)
    MessageBooked["height"] = 2
    MessageBooked["bg"] = COLOR_GREY
    MessageBooked["fg"] = COLOR_BLACK
    MessageBooked["borderwidth"] = 0
    MessageBooked.pack(padx = WINDOW_PADX, pady = (30, 0))

    TicketHeader = Label(ChatFrame, text = "Ticket")
    SetMessageAttributes(TicketHeader)
    TicketHeader["height"] = 2
    TicketHeader.pack(padx = WINDOW_PADX, pady = (30,0))

    ticketDetails = f'Movie: {title}\nDate: {date}\nTime: {bookShow["time"]}\nScreen: {bookShow["screen"]}\nSeats: {bookedSeats}'
    TicketDetails = Button(ChatFrame, text = ticketDetails)
    TicketDetails["font"] = ("Georgia", 16)
    TicketDetails["bg"] = COLOR_WHITE
    TicketDetails["padx"] = 0
    TicketDetails["borderwidth"] = 1
    TicketDetails["relief"] = "solid"
    TicketDetails["fg"] = COLOR_BLACK
    TicketDetails["width"] = 24
    TicketDetails.pack(padx = WINDOW_PADX, pady = (0, 10))

    HomeExit()

def OnSeatSelected(selSeat, title, date):
    for seat in seatState:
        if seat == selSeat:
            if seatState[seat] == False:
                seatState[seat] = True
            else:
                seatState[seat] = False
            break
    
    OnBookSeats(title, date)

def OnBookSeats(title, date):

    for widget in ChatFrame.winfo_children():
            widget.destroy()

    bookShow = []
    
    for show in movieData["shows"]:
        if title == show["title"] and date == show["date"]:
            bookShow = show
            break
    
    reviewDetails = f'Movie: {bookShow["title"]}\nDate: {bookShow["date"]} |  Time: {bookShow["time"]}\nScreen: {bookShow["screen"]}'
    Review = Button(ChatFrame, text = reviewDetails)
    SetButtonAttributes(Review)
    Review["bg"] = COLOR_GREY
    Review["borderwidth"] = 0
    Review.pack(padx = WINDOW_PADX, pady = (15,0))

    strBookSeats = "Select your seats.." 
    ListSeats = Label(ChatFrame, text = strBookSeats)
    SetMessageAttributes(ListSeats)
    ListSeats["height"] = 2
    ListSeats.pack(padx = WINDOW_PADX, pady = (15,0))
   
    imageReserved = Image.open("reservedseat.jpg")
    imageReserved = imageReserved.resize((25, 22))
    photoReserved = ImageTk.PhotoImage(imageReserved)

    imageSelected = Image.open("selectedseat.jpg")
    imageSelected = imageSelected.resize((25, 22))
    photoSelected = ImageTk.PhotoImage(imageSelected)

    imageAvailable = Image.open("availableseat.jpg")
    imageAvailable = imageAvailable.resize((25, 22))
    photoAvailable = ImageTk.PhotoImage(imageAvailable)

    #seats alignment
    seatNo = 1
    rowFrame = Frame(ChatFrame, bg = COLOR_WHITE)
    rowFrame.pack(padx = WINDOW_PADX,pady = (2, 0))
    for seat in seatLayout:

        if seat in bookShow["seatsbooked"]:
            Seat = Button(rowFrame, text = seat, image = photoReserved, compound = TOP)
            Seat.image = photoReserved
        else:
            if seatState[seat] == True:
                Seat = Button(rowFrame, text = seat, image = photoSelected, compound = TOP, command = lambda selSeat = seat, movTitle = title, movDate = date: OnSeatSelected(selSeat, title, date))
                Seat.image = photoSelected
            else:
                Seat = Button(rowFrame, text = seat, image = photoAvailable, compound = TOP, command = lambda selSeat = seat, movTitle = title, movDate = date: OnSeatSelected(selSeat, title, date))
                Seat.image = photoAvailable

        Seat["borderwidth"] = 0
        Seat["bg"] = COLOR_WHITE
        Seat["fg"] = COLOR_BLACK
        Seat["font"] = ("Arial", 6)
        Seat["padx"] = 0
        Seat["pady"] = 0
        
        if seatNo % 2 == 0:
            if seatNo % 10 == 0:
                Seat.pack(side = RIGHT, padx = (20,0))
            else:
                Seat.pack(side = RIGHT)
        else:
            Seat.pack(side = LEFT)

        if seatNo % 10 == 0:
            rowFrame = Frame(ChatFrame, bg = COLOR_WHITE)
            rowFrame.pack(padx = WINDOW_PADX)

        seatNo = seatNo + 1

    ConfirmBooking = Button(ChatFrame, text = "Book Tickets", command = lambda movTitle = title, movDate = date: BookTicket(movTitle, movDate))
    SetButtonAttributes(ConfirmBooking)
    ConfirmBooking.pack(padx = WINDOW_PADX, pady = (30,0))

    CancelBooking = Button(ChatFrame, text = "Cancel Booking", command = lambda: StartChat(0))
    SetButtonAttributes(CancelBooking)
    CancelBooking.pack(padx = WINDOW_PADX, pady = (5,10))

def OnClickBookMovie(title):
    for widget in ChatFrame.winfo_children():
            widget.destroy()

    strBookShows = "Select a show" 
    ListShows = Label(ChatFrame, text = strBookShows)
    SetMessageAttributes(ListShows)
    ListShows["height"] = 2
    ListShows.pack(padx = WINDOW_PADX, pady = (40,0))

    for show in movieData["shows"]:
        if show["title"] == title:
            strShowInfo = f'Date: {show["date"]} |  Time: {show["time"]}\nScreen: {show["screen"]}'
            Show = Button(ChatFrame, text = strShowInfo, command = lambda strMovieTitle = title, strMovieDate = show["date"] : OnBookSeats(strMovieTitle, strMovieDate))
            SetButtonAttributes(Show)
            Show.pack(padx = WINDOW_PADX)

def OnBookMovie():
    strMovieSelect = "Choose Movie..."
    ListMovies = Label(ChatFrame, text = strMovieSelect)
    SetMessageAttributes(ListMovies)
    ListMovies["height"] = 2
    ListMovies.pack(padx = WINDOW_PADX, pady = (20,0))

    for movie in movieData["movies"]:
        strMovieInfo = f'{movie["title"]}\n{movie["rating"]} | {movie["language"]} | {movie["genre"]}'
        Movie = Button(ChatFrame, text = strMovieInfo, command = lambda strMovieTitle = movie["title"] : OnClickBookMovie(strMovieTitle))
        SetButtonAttributes(Movie)
        Movie.pack(padx = WINDOW_PADX)

def OnClickInitialOption2():
    global option1Active
    global option2Active
    global option3Active

    if option1Active or option3Active:
        for widget in ChatFrame.winfo_children():
            widget.destroy()
        option1Active = False
        option3Active = False
        StartChat(2)

    if option2Active == False:
        OnBookMovie()

        option1Active = False
        option2Active = True
        option3Active = False

def OnViewTickets():

    for widget in ChatFrame.winfo_children():
            widget.configure(state = "disabled")

    email = userEmail.get()
    emailExists = False

    for ticket in movieData["tickets"]:
        if ticket["email"] == email:
            if emailExists == False:
                emailExists = True
                strTickets = f'Dear {email},\nYour Tickets'
                YourTickets = Label(ChatFrame, text = strTickets)
                SetMessageAttributes(YourTickets)
                YourTickets.pack(padx = WINDOW_PADX, pady = (20,0))

            if emailExists == True:
                ticketDetails = f'Movie: {ticket["title"]}\nDate: {ticket["date"]} |  Time: {ticket["time"]}\nScreen: {ticket["screen"]}\nSeats: {ticket["seats"]}'
                Ticket = Button(ChatFrame, text = ticketDetails)
                SetButtonAttributes(Ticket)
                Ticket.pack(padx = WINDOW_PADX)

    if emailExists == False:
        strEmailAlert = "You have not booked any tickets with us\nAll booked tickets will show up here"
        EmailInvalid = Label(ChatFrame, text = strEmailAlert)
        SetMessageAttributes(EmailInvalid)
        EmailInvalid.pack(padx = WINDOW_PADX, pady = (20,0))

    HomeExit()

def OnClickInitialOption3():
    global option1Active
    global option2Active
    global option3Active

    if option1Active or option2Active:
        for widget in ChatFrame.winfo_children():
            widget.destroy()
        option1Active = False
        option2Active = False
        StartChat(3)

    if option3Active == False:
        OnViewTickets()

        option1Active = False
        option2Active = False
        option3Active = True

def StartChat(optionActive = 0):
    global option1Active
    global option2Active
    global option3Active

    option1Active = False
    option2Active = False
    option3Active = False
    for widget in ChatFrame.winfo_children():
        widget.destroy()


    ResetSeatState()

    initialGreeting = Label(ChatFrame, text = INITIAL_GREETING)
    SetMessageAttributes(initialGreeting)
    initialGreeting["height"] = 2
    initialGreeting.pack(padx = WINDOW_PADX, pady = (35,0))

    initialOption1 = Button(ChatFrame, text = INITIAL_OPTION1, command = OnClickInitialOption1)
    SetButtonAttributes(initialOption1)
    initialOption1.pack(padx = WINDOW_PADX)

    initialOption2 = Button(ChatFrame, text = INITIAL_OPTION2, command = OnClickInitialOption2)
    SetButtonAttributes(initialOption2)
    initialOption2.pack(padx = WINDOW_PADX)

    initialOption3 = Button(ChatFrame, text = INITIAL_OPTION3, command = OnClickInitialOption3)
    SetButtonAttributes(initialOption3)
    initialOption3.pack(padx = WINDOW_PADX, pady = (0,30))


    if optionActive == 1:
        OnClickInitialOption1()
    elif optionActive == 2:
        OnClickInitialOption2()
    elif optionActive == 3:
        OnClickInitialOption3()



#loading data from file
movieData = {}
with open(MOVIEDATA_PATH, "r") as dataFile:
  movieData = json.load(dataFile)

#creating chat app
ChatWindow = Tk()
ChatWindow.title(CHAT_WINDOW_TITLE)
ChatWindow.configure(bg = COLOR_GREY)
ChatWindow.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
ChatWindow.resizable(0, 0)

Container = Frame(ChatWindow)
Canvas = Canvas(Container, highlightthickness = 0)
Canvas.configure(bg = COLOR_GREY)
VScrollbar = Scrollbar(Container, orient="vertical", command=Canvas.yview, width = 15)
ChatFrame = Frame(Canvas)
ChatFrame.configure(bg = COLOR_GREY)

ChatFrame.bind(
    "<Configure>",
    lambda e: Canvas.configure(
        scrollregion = Canvas.bbox("all")
    )
)

Canvas.create_window((0, 0), window = ChatFrame, anchor = N)
Canvas.configure(yscrollcommand = VScrollbar.set)
Container.pack(expand = True, fill = BOTH)
Canvas.pack(side = LEFT, fill = BOTH, expand=True)
VScrollbar.pack(side = RIGHT, fill = Y)

#login variables
userEmail = StringVar()
tempEmail = StringVar()
tempConfirmPass = StringVar()
tempPass = StringVar()
loginEmailErrorMsg = StringVar()
loginPassErrorMsg = StringVar()

option1Active = False
option2Active = False
option3Active = False

OnStartup()
ChatWindow.mainloop()

#writing data to file
with open(MOVIEDATA_PATH, "w") as dataFile:
  json.dump(movieData, dataFile)