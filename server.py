from flask import Flask, redirect, url_for, render_template, request, session, flash
import datetime
from datetime import timedelta
from passlib.handlers.sha2_crypt import sha512_crypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import between

app = Flask(__name__)
app.secret_key = "SecretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRA CK_MODIFICATIONS"] = False
##app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    players = db.relationship('player', backref='users', lazy=True)

    def __init__(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email
        self.password = password

class player(db.Model):
    pId = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    pName = db.Column(db.String(100), nullable=False)
    Position = db.Column(db.String(100))
    Height = db.Column(db.String(100))
    Weight = db.Column(db.String(100))
    DOB = db.Column(db.Date, nullable=False)
    statistics = db.relationship('statistic', backref='player', lazy=True)

    def __init__(self, userId, pName, Position, Height, Weight, DOB):
        self.userId = userId
        self.pName = pName
        self.Position = Position
        self.Height = Height
        self.Weight = Weight
        self.DOB = DOB

class statistic(db.Model):
    statID = db.Column(db.Integer, primary_key=True)
    playerId = db.Column(db.Integer, db.ForeignKey('player.pId'))
    position = db.Column(db.String(100), nullable=False)
    playerTeam = db.Column(db.String(100), nullable=False)
    oppositionTeam = db.Column(db.String(100), nullable=False)
    dribbleSuc = db.Column(db.Integer, nullable=False)
    dribbleUnSuc = db.Column(db.Integer, nullable=False)
    passCompleted = db.Column(db.Integer,  nullable=False)
    passUnCompleted = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)
    chancesCreated = db.Column(db.Integer, nullable=False)
    goalsScored = db.Column(db.Integer, nullable=False)
    shotsOnTarget = db.Column(db.Integer, nullable=False)
    shotsOffTarget = db.Column(db.Integer, nullable=False)
    clearances = db.Column(db.Integer, nullable=False)
    interceptions = db.Column(db.Integer, nullable=False)
    tacklesSuc = db.Column(db.Integer, nullable=False)
    foulsSuffered = db.Column(db.Integer, nullable=False)
    foulsCommitted = db.Column(db.Integer, nullable=False)
    yellowCard = db.Column(db.Integer, nullable=False)
    redCard = db.Column(db.Integer, nullable=False)
    minutesPlayed = db.Column(db.Integer, nullable=False)
    statDate = db.Column(db.Date, nullable=False)

    def __init__(self, playerId, position, playerTeam, oppositionTeam, dribbleSuc, dribbleUnSuc, passCompleted, passUnCompleted, assists, chancesCreated, goalsScored, shotsOnTarget, shotsOffTarget, clearances, interceptions, tacklesSuc, foulsSuffered, foulsCommitted, yellowCard, redCard, minutesPlayed, statDate):
        self.playerId = playerId
        self.position = position
        self.playerTeam = playerTeam
        self.oppositionTeam = oppositionTeam
        self.dribbleSuc = dribbleSuc
        self.dribbleUnSuc = dribbleUnSuc
        self.passCompleted = passCompleted
        self.passUnCompleted = passUnCompleted
        self.assists = assists
        self.chancesCreated = chancesCreated
        self.goalsScored = goalsScored
        self.shotsOnTarget = shotsOnTarget
        self.shotsOffTarget = shotsOffTarget
        self.clearances = clearances
        self.interceptions = interceptions
        self.tacklesSuc = tacklesSuc
        self.foulsSuffered = foulsSuffered
        self.foulsCommitted = foulsCommitted
        self.yellowCard = yellowCard
        self.redCard = redCard
        self.minutesPlayed = minutesPlayed
        self.statDate = statDate

@app.route("/")
def home():
    return render_template("players.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        ##session.permanent = True
        username = request.form["username"]
        password = request.form["password"]

        #found_user = users.query.filter_by(username=username, password=password).first()
        found_user = users.query.filter_by(username=username).first()

        ##Used to check if user exists and log them in if they do exist
        ##If they dont exist then they are sent back to the login page
        if found_user:
            #Used to compare the password that the user entered to the users actual password
            #If they are equal then the user is redirected to the players page
            #Else the user is redirected to the login page and is told the login was unsuccessfull
            if sha512_crypt.verify(password, found_user.password):
                session["user"] = username
                session["email"] = found_user.email
                flash("Login Successful")
                return redirect(url_for("players"))
            else:
                flash("Login Unsuccessful")
                return render_template("login.html")
        else:
            flash("Login Unsuccessful")
            return render_template("login.html")
    else:
        ##Used to redirect if user is logged in away from the login page, as they are already logged in
        if "user" in session:
            username = session["user"]
            flash("Already logged in as " + username)
            return redirect(url_for("players"))

        return render_template("login.html")

@app.route("/createAccount", methods=["POST", "GET"])
def createAccount():
    print("inside createAccount")
    if request.method == "POST":
        ##session.permanent = True
        username = request.form["username"]
        user = request.form["nm"]
        password = request.form["pw"]
        email = request.form["email"]

        #Used to encrypt the password the user entered
        secure_password = sha512_crypt.encrypt(str(password))
        found_user = users.query.filter_by(username=username).first()

        ##Used to check if user already exists
        if found_user:
            flash("Username already exists")
            return render_template("createAccount.html")
        else:
            session["user"] = username
            usr = users(username, user, email, secure_password)
            print("Users password = " + password)
            db.session.add(usr)
            db.session.commit()

        flash("Account created")
        return redirect(url_for("players"))
    else:
        ##Used to redirect if user is logged in away from the login page, as they are already logged in
        if "user" in session:
            username = session["user"]
            flash("Already logged in as " + username)
            return redirect(url_for("players"))

        return render_template("createAccount.html")

@app.route("/updateAccount", methods=["POST", "GET"])
def updateAccount():
    if "user" in session:
        username = session["user"]

        usersDetails = users.query.filter_by(username=username).first()
        if request.method == "POST":

            #Used to update user details such as name and email
            if "UpdateDet" in request.form:
                print("Update user details works")
                userName = request.form["nm"]
                userEmail = request.form["email"]

                usersDetails.name = userName
                usersDetails.email = userEmail
                db.session.add(usersDetails)
                db.session.commit()
                flash("Account details updated successfully")
                return redirect(url_for("updateAccount"))

            #Used to update the users password
            if "updatePass" in request.form:
                print("Update user password works")
                currentPass = request.form["currentPass"]
                newPass = request.form["newPass"]
                reNewPass = request.form["reNewPass"]

                #To check if the new password entered is equal to the re-enter new password
                if newPass != reNewPass:
                    flash("New password and Re-enter New Password were not the same")
                    return redirect(url_for("updateAccount"))

                #To check the current password is actually the users current password
                if sha512_crypt.verify(currentPass, usersDetails.password):
                    #Used to encrypt the users new password
                    secure_password = sha512_crypt.encrypt(str(newPass))
                    usersDetails.password = secure_password
                    db.session.add(usersDetails)
                    db.session.commit()

                    flash("Accounts password updated successfully")
                    return redirect(url_for("updateAccount"))
                #If the current password is not equal to the password in the database then they are redirected with an error message
                flash("Current password is incorrect")
                return redirect(url_for("updateAccount"))

        return render_template("updateAccount.html", userDetails=usersDetails)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/recordStats", methods=["POST", "GET"])
def recordStats():
    #Used to check if a user is logging in, instead of just typing /user
    if "user" in session:
        username = session["user"]

        usersDetails = users.query.filter_by(username=username).first()

        if request.method == "POST":
            playerSelected = request.form["PlayerSelected"]
            position = request.form["Position"]
            playerTeam = request.form["playerTeam"]
            oppositionTeam = request.form["oppositionTeam"]
            dribbleSuc = request.form["dribbleSuc"]
            dribbleUnSuc = request.form["dribbleUnSuc"]
            passCompleted = request.form["passesCompleted"]
            passUnCompleted = request.form["passesMissed"]
            assists = request.form["assists"]
            chancesCreated = request.form["chancesCreated"]
            goalsScored = request.form["goalsScored"]
            shotsOnTarget = request.form["shotsOnTarget"]
            shotsOffTarget = request.form["shotsOffTarget"]
            clearances = request.form["clearances"]
            interceptions = request.form["interceptions"]
            tacklesSuc = request.form["tacklesSuc"]
            foulsSuffered = request.form["foulsSuffered"]
            foulsCommitted = request.form["foulsCommitted"]
            yellowCard = request.form["yellowCard"]
            redCard = request.form["redCard"]
            minutesPlayed = request.form["minutesPlayed"]
            statDate = request.form["statDate"]

            #Used to check if the user has selected a player and a player position
            if playerSelected == "Select Player" and position == "Players Position":
                flash("Select a player and a player position")
                return render_template("recordStats.html", values=player.query.filter_by(userId=usersDetails._id).all())

            #Used to get the selected players id, so the statistcs entered can be entered into the statistics table using the players id as it is a foreign key
            playersDetails = player.query.filter_by(userId=usersDetails._id, pName=playerSelected).first()
            print("Got players ID")
            print(playersDetails.pId)

            #statDetails = statistic.query.filter_by(playerId=playersDetails.pId).all()

            #Used to spilt the date given by the form and reassemble it to a python date
            x = statDate.split("-")
            year = x[0]
            yearInt = int(year)
            month = x[1]
            monthInt = int(month)
            day = x[2]
            dayInt = int(day)

            pytStatDate = datetime.date(yearInt, monthInt, dayInt)
            print("Testing month")
            print(pytStatDate.month)

            statCheck = statistic.query.filter_by(playerId=playersDetails.pId, statDate=pytStatDate).first()

            #Used to check if the info from the given player and date already exists
            if statCheck:
                flash("Data already exists for " + playerSelected + " on " + statDate)
                return redirect(url_for("recordStats"))

            playerStatistic = statistic(playersDetails.pId, position, playerTeam, oppositionTeam, dribbleSuc, dribbleUnSuc, passCompleted, passUnCompleted, assists, chancesCreated, goalsScored, shotsOnTarget, shotsOffTarget, clearances, interceptions, tacklesSuc, foulsSuffered, foulsCommitted, yellowCard, redCard, minutesPlayed, pytStatDate)
            db.session.add(playerStatistic)
            db.session.commit()
            #statDetails = statistic.query.filter_by(playerId=playersDetails.pId).all()
            #print(statDetails.goalMissed)

            flash("Player statistics added successfully")
            return redirect(url_for("recordStats"))

        #values = player.query.filter_by(userId=usersDetails._id).all()
        #values is used to pass all the players belonging to the user to the recordStats page
        return render_template("recordStats.html", values=player.query.filter_by(userId=usersDetails._id).all())
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("You have been logged out " + user, "info")
    ##Used to remove the users name from the session
    session.pop("user", None)
    #Second part is used for category warning,info,error
    return redirect(url_for("login"))


##Used to view if the database was working
@app.route("/viewUsers", methods=["POST", "GET"])
def viewUsers():
    if request.method == "POST":
        userName = request.form["userName"]
        userEmail = request.form["userEmail"]

        if "update" in request.form:
            ##updateUser = users.query.filter_by(name=userName, email=userEmail).update()
            #db.session.commit()
            print(userName)
            print(userEmail)
            print("Player has been updated")
            session["userName"] = userName
            session["userEmail"] = userEmail
            return redirect(url_for("updatePlayer"))

        #Used to delete User
        if "delete" in request.form:
            deleteUser = users.query.filter_by(name=userName, email=userEmail).delete()

            #Used to check if the user being deleted exists
            if deleteUser:
                db.session.commit()
                print("User = " + userName + " has been deleted")
                print("Player has been delete")
            else:
                print("Player does not exist")

        return redirect(url_for("viewUsers"))
    else:
        return render_template("viewUsers.html", values=users.query.all())

@app.route("/players", methods=["POST", "GET"])
def players():
    if "user" in session:
        username = session.get("user")
        if request.method == "POST":
            username = session.get("user")
            playerName = request.form["playerName"]
            pos = request.form["position"]
            height = request.form["height"]
            weight = request.form["weight"]
            playerDOB = request.form["playerDOB"]

            #Used to update a selected players details and redirects the user to the update page
            if "update" in request.form:
                print("update works")
                session["playerName"] = playerName
                session["playerDOB"] = playerDOB
                return redirect(url_for("updatePlayer"))

            #Used to delete a selected players details and statitic data
            if "delete" in request.form:
                print("delete works")
                playerDetails = player.query.filter_by(pName=playerName, DOB=playerDOB).first()
                deletePlayer = player.query.filter_by(pName=playerName, DOB=playerDOB).delete()
                playerStats = statistic.query.filter_by(playerId=playerDetails.pId).delete()

                #Used to check if the user being deleted exists
                if deletePlayer:
                    db.session.commit()
                    print("User = " + playerName + " has been deleted")
                    print("Player has been delete")
                    flash("Player deleted successfully")
                else:
                    print("Player does not exist")

            #Used to add a new player
            if "add" in request.form:
                print("add works")
                playerName = request.form["playerName"]
                playerDOB = request.form["playerDOB"]
                found_player = player.query.filter_by(pName=playerName, DOB=playerDOB).first()
                userId = users.query.filter_by(username=username).first()

                #Used to check if the player already exists and if they dont then the new player is added to the database
                if found_player:
                    flash("Player already exists")
                else:
                    x = playerDOB.split("-")
                    year = x[0]
                    yearInt = int(year)
                    month = x[1]
                    monthInt = int(month)
                    day = x[2]
                    dayInt = int(day)

                    date1 = datetime.date(yearInt, monthInt, dayInt)
                    plyer = player(userId._id, playerName, pos, height, weight, date1)
                    db.session.add(plyer)
                    db.session.commit()

            return redirect(url_for("players"))

        else:
            #Used to get the players relating to the user
            usersDetails = users.query.filter_by(username=username).first()
            return render_template("players.html", values=player.query.filter_by(userId=usersDetails._id).all())
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/updatePlayer", methods=["POST", "GET"])
def updatePlayer():
    if "user" in session:
        userName = session.get("user")
        usersDetails = users.query.filter_by(username=userName).first()
        playerName = session.get("playerName")
        playerDOB = session.get("playerDOB")
        print("Inside updatePlayer")
        print(playerName)
        print(playerDOB)
        findPlayer = player.query.filter_by(pName=playerName).first()

        if request.method == "POST":
            print("REQUEST WORKS")
            newPlayerName = request.form["newPlayerName"]
            newPlayerPos = request.form["newPlayerPos"]
            newPlayerHeight = request.form["newPlayerHeight"]
            newPlayerWeight = request.form["newPlayerWeight"]
            newPlayerDOB = request.form["newPlayerDOB"]

            chkPlayer = player.query.filter_by(pName=newPlayerName).first()

            x = newPlayerDOB.split("-")
            year = x[0]
            yearInt = int(year)
            month = x[1]
            monthInt = int(month)
            day = x[2]
            dayInt = int(day)
            date1 = datetime.date(yearInt, monthInt, dayInt)

            #Used to check if the new name entered for the player already exists
            #If it does then the there is another if statement to deal with
            #If the name doesnt exist in the database then the players details are updated with the newly entered data
            if chkPlayer:
                #Since the new name entered for the user exists in the database then i check if the new name is equal to the current name
                #If they are equal then the player can be updated
                #If they are not equal then the user is told that the name already exists
                if playerName == newPlayerName:
                    print("NewPlayersID")
                    print(findPlayer.pId)
                    findPlayer.pName = newPlayerName
                    findPlayer.Position = newPlayerPos
                    findPlayer.Height = newPlayerHeight
                    findPlayer.Weight = newPlayerWeight
                    findPlayer.DOB = date1
                    db.session.add(findPlayer)
                    db.session.commit()
                    session.pop("playerName", None)
                    session.pop("playerDOB", None)
                    return redirect(url_for("players"))
                else:
                    flash("Player already exists, please enter a different name")
                    return redirect(url_for("updatePlayer"))

            else:
                print("NewPlayersID")
                print(findPlayer.pId)
                findPlayer.pName = newPlayerName
                findPlayer.Position = newPlayerPos
                findPlayer.Height = newPlayerHeight
                findPlayer.Weight = newPlayerWeight
                findPlayer.DOB = date1
                db.session.add(findPlayer)
                db.session.commit()
                session.pop("playerName", None)
                session.pop("playerDOB", None)
                return redirect(url_for("players"))

        return render_template("updatePlayer.html", displayPlayerName=playerName, displayPlayerPos=findPlayer.Position, displayPlayerHeight=findPlayer.Height, displayPlayerWeight=findPlayer.Weight, displayPlayerDOB=playerDOB)
            #return render_template("updatePlayer.html")

    else:
        flash("You are not logged in")
        return redirect(url_for("login"))

@app.route("/deleteUser/<name>")
def deleteUser(name):
    #foundUser = users.query.filter_by(name=name).delete()
    #db.session.commit()
    print("User = " + name + " has been deleted")
    #session.pop("user", None)
   # session.pop("email", None)
    flash("Account deleted")
    return redirect(url_for("login"))

@app.route("/updateStatistics", methods=["POST", "GET"])
def updateStatistics():
    if "user" in session:
        username = session["user"]

        #Used to fill in the data on the page updateStatistics, when the user selects a player and date the array will be filled with that date
        #An error would occur if this array was empty
        resultData = ["Select Player", "Players Position", " ", " ", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "0000-00-00"]
        #Used to get user details from the Database
        usersDetails = users.query.filter_by(username=username).first()

        if request.method == "POST":
            #Used to search for the data using the name and date given by the user and retrieve that data and isaply the data on the page updateStatistics
            if "search" in request.form:
                playerSelected = request.form["PlayerSelected"]
                dateSearched = request.form["dateSearch"]

                print("Player being searched")
                print(playerSelected)
                print(dateSearched)

                #Used to check if the user has selected a player and entered a date
                if playerSelected == "Select Player" or not dateSearched:
                    flash("Please select a player and date before clicking search")
                    return redirect(url_for("updateStatistics"))

                playersDetails = player.query.filter_by(userId=usersDetails._id, pName=playerSelected).first()

                # Used to spilt the date given by the form and reassemble it to a python date
                x = dateSearched.split("-")
                year = x[0]
                yearInt = int(year)
                month = x[1]
                monthInt = int(month)
                day = x[2]
                dayInt = int(day)

                pytStatDate = datetime.date(yearInt, monthInt, dayInt)

                statCheck = statistic.query.filter_by(playerId=playersDetails.pId, statDate=pytStatDate).first()

                #Used to check if there is data in the database for the given player name and date
                #If there is data then that data is added to the array
                if statCheck:
                    print("Data exists")
                    session["playerSelected"] = playerSelected
                    session["dateSearched"] = dateSearched

                    resultData.clear()
                    resultData.append(playerSelected)
                    resultData.append(statCheck.position)
                    resultData.append(statCheck.playerTeam)
                    resultData.append(statCheck.oppositionTeam)
                    resultData.append(statCheck.dribbleSuc)
                    resultData.append(statCheck.dribbleUnSuc)
                    resultData.append(statCheck.passCompleted)
                    resultData.append(statCheck.passUnCompleted)
                    resultData.append(statCheck.assists)
                    resultData.append(statCheck.chancesCreated)
                    resultData.append(statCheck.goalsScored)
                    resultData.append(statCheck.shotsOnTarget)
                    resultData.append(statCheck.shotsOffTarget)
                    resultData.append(statCheck.clearances)
                    resultData.append(statCheck.interceptions)
                    resultData.append(statCheck.tacklesSuc)
                    resultData.append(statCheck.foulsSuffered)
                    resultData.append(statCheck.foulsCommitted)
                    resultData.append(statCheck.yellowCard)
                    resultData.append(statCheck.redCard)
                    resultData.append(statCheck.minutesPlayed)
                    resultData.append(statCheck.statDate)
                else:
                    flash("Data does not exist for " + playerSelected + " on " + dateSearched)
                    return redirect(url_for("updateStatistics"))

            #Used to update the statistics
            if "update" in request.form:
                print("Update Works")
                #Used to check if the search returned data and if it didnt then the user is told to search for a players statistics
                if "playerSelected" and "dateSearched" in session:
                    sessionPlayer = session.get("playerSelected")
                    sessionDate = session.get("dateSearched")

                    #Get the data from the form
                    playerSelected = request.form["PlayerSelected"]
                    position = request.form["Position"]
                    playerTeam = request.form["playerTeam"]
                    oppositionTeam = request.form["oppositionTeam"]
                    dribbleSuc = request.form["dribbleSuc"]
                    dribbleUnSuc = request.form["dribbleUnSuc"]
                    passCompleted = request.form["passesCompleted"]
                    passUnCompleted = request.form["passesMissed"]
                    assists = request.form["assists"]
                    chancesCreated = request.form["chancesCreated"]
                    goalsScored = request.form["goalsScored"]
                    shotsOnTarget = request.form["shotsOnTarget"]
                    shotsOffTarget = request.form["shotsOffTarget"]
                    clearances = request.form["clearances"]
                    interceptions = request.form["interceptions"]
                    tacklesSuc = request.form["tacklesSuc"]
                    foulsSuffered = request.form["foulsSuffered"]
                    foulsCommitted = request.form["foulsCommitted"]
                    yellowCard = request.form["yellowCard"]
                    redCard = request.form["redCard"]
                    minutesPlayed = request.form["minutesPlayed"]
                    statDate = request.form["statDate"]

                    print(sessionPlayer)
                    print(sessionDate)

                    #Used to spilt the current date entered by the user and reassemble it so it can be used to query the database
                    x = sessionDate.split("-")
                    year = x[0]
                    yearInt = int(year)
                    month = x[1]
                    monthInt = int(month)
                    day = x[2]
                    dayInt = int(day)
                    currentDate = datetime.date(yearInt, monthInt, dayInt)

                    #Used to spilt the new date entered by the user and reassemble it so it can be used to query the database
                    x = statDate.split("-")
                    year = x[0]
                    yearInt = int(year)
                    month = x[1]
                    monthInt = int(month)
                    day = x[2]
                    dayInt = int(day)
                    newDate = datetime.date(yearInt, monthInt, dayInt)

                    currentPlayersDetails = player.query.filter_by(userId=usersDetails._id, pName=sessionPlayer).first()
                    newPlayersDetails = player.query.filter_by(userId=usersDetails._id, pName=playerSelected).first()

                    getcurrentStats = statistic.query.filter_by(playerId=currentPlayersDetails.pId, statDate=currentDate).first()

                    getNewStats = statistic.query.filter_by(playerId=newPlayersDetails.pId, statDate=newDate).first()

                    #Used to check if the new player name and new date entered already exist in the database
                        #if they do then i check if the new player name and new date
                        #is equal to the player name and date that the user searched
                        #and if they are equal then the update of the statistic occurs

                        #if the new player name and new date are not equal to the
                        #player name and date searched by the user then the
                        #update does not happen as a player does not play more than
                        #one match a day
                        #and this would cause an error when calling statistics from the database

                    #if the new player name and new date dont exist in the database
                        #The update to the statistics occurs

                    #(Basicaly just to stop a player having more than one match on the same day)

                    if getNewStats:
                        if sessionDate == statDate and sessionPlayer == playerSelected:
                            print("update data")
                            flash("Statistic updated successfully")
                            getcurrentStats.playerId = newPlayersDetails.pId
                            getcurrentStats.position = position
                            getcurrentStats.playerTeam = playerTeam
                            getcurrentStats.oppositionTeam = oppositionTeam
                            getcurrentStats.dribbleSuc = dribbleSuc
                            getcurrentStats.dribbleUnSuc = dribbleUnSuc
                            getcurrentStats.passCompleted = passCompleted

                            getcurrentStats.passUnCompleted = passUnCompleted
                            getcurrentStats.assists = assists
                            getcurrentStats.chancesCreated = chancesCreated
                            getcurrentStats.goalsScored = goalsScored
                            getcurrentStats.shotsOnTarget = shotsOnTarget
                            getcurrentStats.shotsOffTarget = shotsOffTarget
                            getcurrentStats.clearances = clearances
                            getcurrentStats.interceptions = interceptions
                            getcurrentStats.tacklesSuc = tacklesSuc
                            getcurrentStats.goalMissed = foulsSuffered
                            getcurrentStats.goalMissed = foulsCommitted
                            getcurrentStats.goalMissed = yellowCard
                            getcurrentStats.goalMissed = redCard
                            getcurrentStats.goalMissed = minutesPlayed
                            getcurrentStats.statDate = newDate
                            db.session.add(getcurrentStats)
                            db.session.commit()
                            session.pop("playerSelected", None)
                            session.pop("dateSearched", None)
                            return redirect(url_for("updateStatistics"))

                        flash("Statistics already exist on that given date and player")
                        return redirect(url_for("updateStatistics"))
                    else:
                        print("update data")
                        flash("Statistic updated successfully")
                        getcurrentStats.playerId = newPlayersDetails.pId
                        getcurrentStats.position = position
                        getcurrentStats.playerTeam = playerTeam
                        getcurrentStats.oppositionTeam = oppositionTeam
                        getcurrentStats.dribbleSuc = dribbleSuc
                        getcurrentStats.dribbleUnSuc = dribbleUnSuc
                        getcurrentStats.passCompleted = passCompleted
                        getcurrentStats.passUnCompleted = passUnCompleted
                        getcurrentStats.assists = assists
                        getcurrentStats.chancesCreated = chancesCreated
                        getcurrentStats.goalsScored = goalsScored
                        getcurrentStats.shotsOnTarget = shotsOnTarget
                        getcurrentStats.shotsOffTarget = shotsOffTarget
                        getcurrentStats.clearances = clearances
                        getcurrentStats.interceptions = interceptions
                        getcurrentStats.tacklesSuc = tacklesSuc
                        getcurrentStats.goalMissed = foulsSuffered
                        getcurrentStats.goalMissed = foulsCommitted
                        getcurrentStats.goalMissed = yellowCard
                        getcurrentStats.goalMissed = redCard
                        getcurrentStats.goalMissed = minutesPlayed
                        getcurrentStats.statDate = newDate
                        db.session.add(getcurrentStats)
                        db.session.commit()
                        session.pop("playerSelected", None)
                        session.pop("dateSearched", None)
                        return redirect(url_for("updateStatistics"))
                else:
                    flash("Please select a player and a date and click search")
                    return redirect(url_for("updateStatistics"))

            #Used to delete the statistics that the user searched for
            if "delete" in request.form:
                print("delete works")
                sessionPlayer = session.get("playerSelected")
                sessionDate = session.get("dateSearched")
                currentPlayersDetails = player.query.filter_by(userId=usersDetails._id, pName=sessionPlayer).first()
                deleteStat = statistic.query.filter_by(playerId=currentPlayersDetails.pId, statDate=sessionDate).delete()

                #Used to check if the user being deleted exists
                if deleteStat:
                    db.session.commit()
                    flash("Statistic deleted successfully")
                else:
                   print("Statistic does not exist")

                return redirect(url_for("updateStatistics"))

        return render_template("updateStatistics.html", playersNames=player.query.filter_by(userId=usersDetails._id).all(), resultData=resultData)
    else:
        flash("Please login")
        return redirect(url_for("login"))


fullPlayerStats = []
playerStatsTable = []

@app.route("/displayStats", methods=["POST", "GET"])
def displayStats():
    if "user" in session:
        username = session["user"]
        #session["user"] = username
        #Used to get user details from the Database
        usersDetails = users.query.filter_by(username=username).first()
        #Used to get player details from the Database
        #playersDetails = player.query.filter_by(userId=usersDetails._id, pName="Glen").first()

        #Used to check if the list is empty
        #if it is empty then we add "Empty" to the list so the bar chart can be created (if theres nothing in fullPlayerStats we get errors due to the bar chart cannot be created without data)
        if len(fullPlayerStats) == 0:
            print("The list is empty")
            fullPlayerStats.append(["Empty"])

        #Used to see if the player has any data in the 12 months
        #If they dont then no data will be added to the bar chart
        monthCounter = 0

        if request.method == "POST":
            print("Inside post")

            #If the user clicked the add button then it would trigger this if
            #and add the requested data to the barchart
            if "add" in request.form:
                playerNameBar = request.form["PlayerSelected"]
                statChoice = request.form["StatChoice"]
                yearChoice = request.form["yearChoice"]
                startYear = "-01-01"
                endYear = "-12-31"

                startYear = yearChoice + startYear
                endYear = yearChoice + endYear

                #statDetails = statistic.query.filter(statistic.statDate.between(startYear, endYear)).all()

                #Used to check if the user has not chosen a stat or year
                #and if they havnt, the page is reloaded with a warning asking the user to select a stat and year
                if playerNameBar == "Select Player" or statChoice == "statSelected" or yearChoice == "yearSelected":
                    flash("Please select Player, Stat and Year")
                    #return render_template("displayStats.html", values=fullPlayerStats, tableData=playerStatsTable)
                    return redirect(url_for("displayStats"))

                playersDetails = player.query.filter_by(userId=usersDetails._id, pName=playerNameBar).first()
                #statDetails = statistic.query.filter_by(playerId=playersDetails.pId).all()
                statDetails = statistic.query.filter(statistic.playerId == playersDetails.pId, statistic.statDate.between(startYear, endYear)).all()
                intYearChoice = int(yearChoice)

                playerStats = []

                #Used to add the title for the stats being requested eg 2018/Passing (The pass % for each month of the year of 2018)
                statTitle = yearChoice + "/" + statChoice + " (" + playerNameBar + ")"
                playerStats.append(statTitle)

                #Used to extract data from database and spilt the data into months
                for i in range(1, 13):
                    #Used to store the data, for example completed would be eqaul to passes completed and uncompleted would be passes uncompleted
                    completed = 0
                    uncompleted = 0
                    for x in statDetails:
                        #Used to get the month of the cureent statistic
                        getDate = x.statDate
                        getMonth = getDate.month

                        print("This is the date")
                        print(getDate)

                        if i == getMonth:
                            if statChoice == "Passing":
                                completed = completed + x.passCompleted
                                uncompleted = uncompleted + x.passUnCompleted

                            if statChoice == "Shooting":
                                completed = completed + x.shotsOnTarget
                                uncompleted = uncompleted + x.shotsOffTarget

                            if statChoice == "Finishing":
                                completed = completed + x.goalsScored
                                uncompleted = uncompleted + x.shotsOnTarget

                            if statChoice == "Dribbling":
                                completed = completed + x.dribbleSuc
                                uncompleted = uncompleted + x.dribbleUnSuc

                            if statChoice == "Tackling":
                                completed = completed + x.tacklesSuc
                                uncompleted = uncompleted + x.foulsCommitted

                    attempted = completed + uncompleted

                    #This is done because goalsScored is already part shotsOnTarget, no need to add them together
                    if statChoice == "Finishing":
                        attempted = uncompleted

                    # Used to check if the player has attempted a pass
                    # and if they have then the accuracy will be calculated
                    if attempted != 0:
                        accuracy = completed / attempted * 100 / 1
                        playerStats.append(round(accuracy))
                    else:
                        playerStats.append(0)
                        monthCounter = monthCounter + 1


                if monthCounter == 12:
                    flash("No data can be found")
                else:
                    fullPlayerStats.append(playerStats)

                #Used to remove "Empty" from fullPlayerStats
                if ["Empty"] in fullPlayerStats and len(fullPlayerStats) > 1:
                    print("The list is not empty")
                    fullPlayerStats.remove(["Empty"])

                return redirect(url_for("displayStats"))

            #Used to clear the barchart
            if "clearBar" in request.form:
                if ["Empty"] in fullPlayerStats:
                    flash("Barchart is already empty")
                else:
                    flash("Barchart is cleared")
                    fullPlayerStats.clear()
                    fullPlayerStats.append(["Empty"])

            #Used to add data to the table that is placed under the barChart
            if "addToTable" in request.form:
                playerNameTable = request.form["PlayerSelectedTable"]
                position = request.form["Position"]
                fromDate = request.form["fromDate"]
                toDate = request.form["toDate"]

                playerStatsRow = []

                #Used count how many matches a player played between two selected dates
                gameCounter = 0
                goalAttempts = 0
                goalScored=0
                passAttempts = 0
                passesCompleted=0

                shotAttempts = 0
                shotsOnTarget = 0
                assists = 0
                chancesCreated = 0
                clearances = 0
                interceptions = 0
                tacklesSuc = 0
                tacklesAttempted = 0
                fouled = 0
                yellowCard = 0
                redCard = 0
                minutesPlayed = 0

                #Used to check if the user has selected
                #If they havnt selected a player then the page reloads
                if playerNameTable == "Select Player":
                    flash("Please select a player when adding to the Table")
                    return redirect(url_for("displayStats"))

                playersDetails = player.query.filter_by(userId=usersDetails._id, pName=playerNameTable).first()

                #To check if the user wants statistics between two selected dates
                if fromDate:
                    print("Two dates have been entered")
                    if toDate and fromDate:
                        print("Both dates have been selected")

                        if position == "All":
                            playerStatDetailsToFrom = statistic.query.filter(statistic.playerId == playersDetails.pId, statistic.statDate.between(fromDate, toDate)).all()
                        else:
                            playerStatDetailsToFrom = statistic.query.filter(statistic.playerId == playersDetails.pId, statistic.position == position, statistic.statDate.between(fromDate, toDate)).all()

                        #Used to check if the query on the database returned any data
                        #If no data is returned then the displayStats page is loaded with a message telling the user that no data was found
                        if not playerStatDetailsToFrom:
                            flash("Not data found")
                            #return render_template("displayStats.html", values=fullPlayerStats, tableData=playerStatsTable)
                            return redirect(url_for("displayStats"))

                        for x in playerStatDetailsToFrom:
                            gameCounter = gameCounter + 1

                            goalAttempts = goalAttempts + x.shotsOnTarget
                            goalScored = goalScored + x.goalsScored

                            shotAttempts = shotAttempts + x.shotsOnTarget + x.shotsOffTarget
                            shotsOnTarget = shotsOnTarget + x.shotsOnTarget

                            passAttempts = passAttempts + x.passCompleted + x.passUnCompleted
                            passesCompleted = passesCompleted + x.passCompleted

                            assists = assists + x.assists

                            chancesCreated = chancesCreated + x.chancesCreated

                            clearances = clearances + x.clearances

                            interceptions = interceptions + x.interceptions

                            tacklesAttempted = tacklesAttempted + x.tacklesSuc + x.foulsCommitted
                            tacklesSuc = tacklesSuc + x.tacklesSuc

                            fouled = fouled + x.foulsSuffered

                            yellowCard = yellowCard + x.yellowCard
                            redCard = redCard + x.redCard

                            minutesPlayed = minutesPlayed + x.minutesPlayed


                    #Used to get the data if only one data is selected (FromDate)
                    else:
                        print("From Date only selected")
                        if position == "All":
                            playerStatDetailsToFrom = statistic.query.filter_by(playerId=playersDetails.pId, statDate=fromDate).first()
                        else:
                            playerStatDetailsToFrom = statistic.query.filter_by(playerId=playersDetails.pId, position=position, statDate=fromDate).first()

                        # Used to check if the query on the database returned any data
                        # If no data is returned then the displayStats page is loaded with a message telling the user that no data was found
                        if not playerStatDetailsToFrom:
                            flash("Not data found")
                            #return render_template("displayStats.html", values=fullPlayerStats, tableData=playerStatsTable)
                            return redirect(url_for("displayStats"))

                        gameCounter = gameCounter + 1
                        goalAttempts = goalAttempts + playerStatDetailsToFrom.shotsOnTarget
                        goalScored = goalScored + playerStatDetailsToFrom.goalsScored

                        shotAttempts = shotAttempts + playerStatDetailsToFrom.shotsOnTarget + playerStatDetailsToFrom.shotsOffTarget
                        shotsOnTarget = shotsOnTarget + playerStatDetailsToFrom.shotsOnTarget

                        passAttempts = passAttempts + playerStatDetailsToFrom.passCompleted + playerStatDetailsToFrom.passUnCompleted
                        passesCompleted = passesCompleted + playerStatDetailsToFrom.passCompleted

                        assists = assists + playerStatDetailsToFrom.assists

                        chancesCreated = chancesCreated + playerStatDetailsToFrom.chancesCreated

                        clearances = clearances + playerStatDetailsToFrom.clearances

                        interceptions = interceptions + playerStatDetailsToFrom.interceptions

                        tacklesAttempted = tacklesAttempted + playerStatDetailsToFrom.tacklesSuc + playerStatDetailsToFrom.foulsCommitted
                        tacklesSuc = tacklesSuc + playerStatDetailsToFrom.tacklesSuc

                        fouled = fouled + playerStatDetailsToFrom.foulsSuffered

                        yellowCard = yellowCard + playerStatDetailsToFrom.yellowCard
                        redCard = redCard + playerStatDetailsToFrom.redCard

                        minutesPlayed = minutesPlayed + playerStatDetailsToFrom.minutesPlayed


                    finishingAcurracy = str(round(goalScored/goalAttempts * 100/1)) + "%" + " " + "(" + str(goalScored) + "/" + str(goalAttempts) + ")"

                    passAcurracy = str(round(passesCompleted/passAttempts * 100 / 1)) + "%" + " " + "(" + str(passesCompleted) + "/" + str(passAttempts) + ")"

                    shotAccuracy = str(round(shotsOnTarget / shotAttempts * 100 / 1)) + "%" + " " + "(" + str(shotsOnTarget) + "/" + str(shotAttempts) + ")"

                    tacklingAccuracy = str(round(tacklesSuc / tacklesAttempted * 100 / 1)) + "%" + " " + "(" + str(tacklesSuc) + "/" + str(tacklesAttempted) + ")"

                    redYellowCard = str(yellowCard) + "/" + str(redCard)

                    tableDate = str(fromDate) + "/" + str(toDate)
                    playerStatsRow.append(position)
                    playerStatsRow.append(playerNameTable)
                    playerStatsRow.append(shotAccuracy)
                    playerStatsRow.append(finishingAcurracy)
                    playerStatsRow.append(passAcurracy)
                    playerStatsRow.append(assists)
                    playerStatsRow.append(chancesCreated)
                    playerStatsRow.append(clearances)
                    playerStatsRow.append(interceptions)
                    playerStatsRow.append(tacklingAccuracy)
                    playerStatsRow.append(fouled)
                    playerStatsRow.append(redYellowCard)
                    playerStatsRow.append(minutesPlayed)
                    playerStatsRow.append(gameCounter)
                    playerStatsRow.append(tableDate)
                    playerStatsTable.append(playerStatsRow)
                    print("Checking how many games a player played")
                    print(gameCounter)
                    return redirect(url_for("displayStats"))
                else:
                    flash("Please choose a date for fromDate")
                    return redirect(url_for("displayStats"))

            if "clearTable" in request.form:
                if not playerStatsTable:
                    flash("Table is already empty")
                else:
                    flash("Table is cleared")
                    playerStatsTable.clear()

                return redirect(url_for("displayStats"))

        #print(stat[0])
        return render_template("displayStats.html", values=fullPlayerStats, tableData=playerStatsTable, playersNames=player.query.filter_by(userId=usersDetails._id).all())
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))


##@app.route("/<name>")
##def user(name):
##    return "Hello " + name

##@app.route("/admin")
##def admin():
##    return redirect(url_for("user", name="Admin" ))


if __name__ == "__main__":
    db.create_all()
    app.run()