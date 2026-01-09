import random, pygame, aubio, os
from files.cmu_112_graphics import *
import files.module_manager

# from previous homework files
def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)


def getOnsetTimes(filePath):
    windowSize = 1024 # FFT size
    hopSize = windowSize // 4

    sampleRate = 0
    srcFunc = aubio.source(filePath, sampleRate, hopSize)
    sampleRate = srcFunc.samplerate
    onsetFunction = aubio.onset('default', windowSize, hopSize)
    
    duration = float(srcFunc.duration) / srcFunc.samplerate

    onsetTimes = [] # seconds
    while True: # read frames
        samples, framesRead = srcFunc()
        if onsetFunction(samples):
            onsetTime = onsetFunction.get_last_s()
            if onsetTime < duration:
                onsetTimes.append(onsetTime)
            else:
                break
        if framesRead < hopSize:
            break
    return onsetTimes


class Pygame(object):
    def __init__(self, path):
        self.path = path
        pygame.mixer.music.load(path)
    
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())
    
    def start(self):
        pygame.mixer.music.play()
    
    def stop(self):
        pygame.mixer.music.stop()
    
    # pauses the current sound at it's location
    def pause(self):
        pygame.mixer.music.pause()
    
    # unpauses the current sound
    def unpause(self):
        pygame.mixer.music.unpause()

# code adapted from website, modified by me
# https://www.freecodecamp.org/news/use-python-to-detect-music-onsets/
# gets the onset times of the songs and returns a list of the timestamps

def getOnsetTimes(file_path):
    windowSize = 1024 # FFT size
    hopSize = windowSize // 4

    sampleRate = 0
    srcFunc = aubio.source(file_path, sampleRate, hopSize)
    sampleRate = srcFunc.samplerate
    onsetFunction = aubio.onset('default', windowSize, hopSize)
    
    duration = float(srcFunc.duration) / srcFunc.samplerate

    onsetTimes = [] # seconds
    while True: # read frames
        samples, num_frames_read = srcFunc()
        if onsetFunction(samples):
            onsetTime = onsetFunction.get_last_s()
            if onsetTime < duration:
                onsetTimes.append(onsetTime)
            else:
                break
        if num_frames_read < hopSize:
            break
    
    return onsetTimes

def appStarted(app):
    # starting screen
    app.playButton = False
    app.playTimer = 0
    app.gameStatus = "not started"
    app.song = ""
    app.timerDelay = 0
    app.enteredName = ""
    app.baseArrowSpeed = 5
    app.maxArrowSpeed = 12

    # all songs downloaded from https://mp3download.to/26-downloader
    app.songList = ["Just Dance", "Call Me Maybe", "BLACKPINK",
                    "Firework", "We Are Young"]
    app.songFileMap = {
        "Just Dance": "songs/JustDance.mp3",
        "Call Me Maybe": "songs/CallMeMaybe.mp3",
        "BLACKPINK": "songs/BLACKPINK.mp3",
        "Firework": "songs/Firework.mp3",
        "We Are Young": "songs/WeAreYoung.mp3"}


    # playing the game
    pygame.mixer.init()
    app.pygame = None
    app.paused = False
    app.duration = 0

    app.windowSize = 1024 
    app.hopSize = app.windowSize // 4
    app.sampleRate = None
    app.songDuration = None
    app.onsetTimes = None
    app.beatTimes = None
    app.beat = None
    app.beatTimer = 0

    app.tracks = 4 # number of "tracks" to have the arrows come down
    app.trackWidth = (app.width - 40) // app.tracks
    app.score = 0

    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fsearch%2Fimages%3Fk%3Dvertical%2Bgame%2Bbackground&psig=AOvVaw08wS2IMSErT677wudflBuC&ust=1638453002227000&source=images&cd=vfe&ved=0CAwQjhxqFwoTCLiKuKDfwvQCFQAAAAAdAAAAABAD
    newSize1 = (673, 850)
    app.trackBackground = Image.open("images/TrackBackground.jpeg").resize(newSize1)
    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fsearch%2Fimages%3Fk%3Dvertical%2Bgame%2Bbackground&psig=AOvVaw08wS2IMSErT677wudflBuC&ust=1638453002227000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCLiKuKDfwvQCFQAAAAAdAAAAABAJ
    newSize2 = (654, 850)
    app.startBackground = Image.open("images/StartBackground.jpeg").resize(newSize2)
    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fstock.adobe.com%2Fsearch%2Fimages%3Fk%3Dvertical%2Bgame%2Bbackground&psig=AOvVaw08wS2IMSErT677wudflBuC&ust=1638453002227000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCLiKuKDfwvQCFQAAAAAdAAAAABAQ
    newSize3 = (850, 850)
    app.playerPickBackground = Image.open("images/PlayerPickBackground.jpeg").resize(newSize3)
    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.shutterstock.com%2Fnb%2Fvideo%2Fclip-1040844308-abstract-light-neon-frame-on-black-background&psig=AOvVaw08wS2IMSErT677wudflBuC&ust=1638453002227000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCLiKuKDfwvQCFQAAAAAdAAAAABAb
    newSize4 = (575, 850)
    app.multiBackground = Image.open("images/MultiBackground.jpeg").resize(newSize4)
    # https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.shutterstock.com%2Fimage-illustration%2F3d-render-abstract-futuristic-neon-background-1766849291&psig=AOvVaw08wS2IMSErT677wudflBuC&ust=1638453002227000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCLiKuKDfwvQCFQAAAAAdAAAAABAn
    newSize5 = (665, 850)
    app.endBackground = Image.open("images/EndBackground.jpeg").resize(newSize5)

    # https://www.pinterest.com/pin/259308891017480341
    app.dArrow = Image.open("images/DownArrow.png")
    app.dArrowPress = Image.open("images/DownArrowPressed.png")
    app.uArrow = Image.open("images/UpArrow.png").rotate(180)
    app.uArrowPress = Image.open("images/UpArrowPressed.png").rotate(180)
    app.lArrow = Image.open("images/LeftArrow.png").rotate(270)
    app.lArrowPress = Image.open("images/LeftArrowPressed.png").rotate(270)
    app.rArrow = Image.open("images/RightArrow.png").rotate(90)
    app.rArrowPress = Image.open("images/RightArrowPressed.png").rotate(90)

    app.dArrowPressed = False
    app.uArrowPressed = False
    app.lArrowPressed = False
    app.rArrowPressed = False
    
    app.dTimer = 0
    app.uTimer = 0
    app.lTimer = 0
    app.rTimer = 0
    app.dTimer2 = 0
    app.uTimer2 = 0
    app.lTimer2 = 0
    app.rTimer2 = 0

    app.dStatus = None
    app.uStatus = None
    app.lStatus = None
    app.rStatus = None

    app.arrowMids = [(20 + 3*app.trackWidth//2, app.dArrow), 
                        (20 + 5*app.trackWidth//2, app.uArrow),
                        (20 + app.trackWidth//2, app.lArrow), 
                        (20 + 7*app.trackWidth//2, app.rArrow),
                        [(20 + 3*app.trackWidth//2, app.dArrow), 
                        (20 + 5*app.trackWidth//2, app.uArrow)],
                        [(20 + app.trackWidth//2, app.lArrow), 
                        (20 + 7*app.trackWidth//2, app.rArrow)],
                        [(20 + 3*app.trackWidth//2, app.dArrow), 
                        (20 + app.trackWidth//2, app.lArrow)],
                        [(20 + 5*app.trackWidth//2, app.uArrow), 
                        (20 + 7*app.trackWidth//2, app.rArrow)]]
    # add combos, up down and left right
    app.arrowRadius = 62//2
    app.arrowsPresent = []
    app.combo = 0
    app.multiplier = 1

    f = open("files/highscores.txt")
    file = f.read()
    f.close()

    app.highscores = []
    app.highscoreNames = []

    if file.strip() != "":
        entries = file.split(",")
        scorePairs = []

        for entry in entries:
            if ":" in entry:
                name, score = entry.split(":")
                scorePairs.append((name, int(score)))

        scorePairs.sort(key=lambda x: x[1], reverse=True)

        while len(scorePairs) < 5:
            scorePairs.append(("---", 0))

        app.highscoreNames = [name for (name, _) in scorePairs]
        app.highscores = [score for (_, score) in scorePairs]


    
def appStopped(app):
    if app.pygame is not None:
        app.pygame.stop()

def goodArrow(app, ymid):
    if ((7*app.height//8 + app.height - 20)//2 - 30 < ymid < 
        (7*app.height//8 + app.height - 20)//2 + 30):
        return True
    return False

def greatArrow(app, ymid):
    if ((7*app.height//8 + app.height - 20)//2 - 15 < ymid < 
        (7*app.height//8 + app.height - 20)//2 + 15):
        return True
    return False

def perfectArrow(app, ymid):
    if ((7*app.height//8 + app.height - 20)//2 - 5 < ymid < 
        (7*app.height//8 + app.height - 20)//2 + 5):
        return True
    return False

def timerFired(app):
    if app.gameStatus == "not started":
        app.playTimer += 0.001
        if almostEqual(app.playTimer, 0.01):
            app.playButton = True
        elif almostEqual(app.playTimer, 0.05):
            app.playButton = False
            app.playTimer = 0
    
    elif app.gameStatus == "playing":
        if app.dArrowPressed:
            app.dTimer += 0.001
            if almostEqual(app.dTimer, 0.002):
                app.dArrowPressed = False
                app.dTimer = 0
        if app.uArrowPressed:
            app.uTimer += 0.001
            if almostEqual(app.uTimer, 0.002):
                app.uArrowPressed = False
                app.uTimer = 0
        if app.lArrowPressed:
            app.lTimer += 0.001
            if almostEqual(app.lTimer, 0.002):
                app.lArrowPressed = False
                app.lTimer = 0
        if app.rArrowPressed:
            app.rTimer += 0.001
            if almostEqual(app.rTimer, 0.002):
                app.rArrowPressed = False
                app.rTimer = 0


        if app.dStatus != None:
            app.dTimer2 += 0.001
            if almostEqual(app.dTimer2, 0.015):
                app.dStatus = None
                app.dTimer2 = 0
        if app.uStatus != None:
            app.uTimer2 += 0.001
            if almostEqual(app.uTimer2, 0.015):
                app.uStatus = None
                app.uTimer2 = 0
        if app.lStatus != None:
            app.lTimer2 += 0.001
            if almostEqual(app.lTimer2, 0.015):
                app.lStatus = None
                app.lTimer2 = 0
        if app.rStatus != None:
            app.rTimer2 += 0.001
            if almostEqual(app.rTimer2, 0.015):
                app.rStatus = None
                app.rTimer2 = 0
        

        if app.pygame.isPlaying():
            app.duration = pygame.mixer.music.get_pos()/1000
            createArrows(app)
            d = app.duration
            if app.duration == app.songDuration:
                app.gameStatus = "over"
                app.song.stop()
            b = app.beatTimes
            if ((d in b) or (d + 0.001 in b) or (d + 0.002 in b) or 
                    (d - 0.001 in b) or (d - 0.002 in b)):
                app.beat = "yes"
        
        # moves the arrows down
        if app.pygame.isPlaying():
            i = 0
            while i < len(app.arrowsPresent):
                # calculate arrow speed based on song progress
                progress = app.duration / float(app.songDuration or 1)
                currentSpeed = app.baseArrowSpeed + progress * (app.maxArrowSpeed - app.baseArrowSpeed)
                currentSpeed = min(currentSpeed, app.maxArrowSpeed)

                app.arrowsPresent[i][1] += currentSpeed

                if app.arrowsPresent[i][1] > app.height:
                    arrow = app.arrowsPresent[i][2]
                    if arrow == app.dArrow:
                        app.dStatus = "Missed"
                    elif arrow == app.uArrow:
                        app.uStatus = "Missed"
                    elif arrow == app.lArrow:
                        app.lStatus = "Missed"
                    elif arrow == app.rArrow:
                        app.rStatus = "Missed"
                    app.combo = 0
                    app.multiplier = 1
                    app.arrowsPresent.pop(i)
                else:
                    i += 1



def inSystem(song, path):
    for root, dirs, files in os.walk(path):
        if song in files:
            return os.path.join(root, song)
    return None

def keyPressed(app, event):
    if app.gameStatus == "not started":
        if event.key == "s":
            app.gameStatus = "player pick"
    elif app.gameStatus == "player pick":
        if event.key == "i":
            app.gameStatus = "import song"
        elif event.key == "p":
            app.gameStatus = "pick song"
    elif app.gameStatus == "pick song":
        if event.key == "Tab":
            app.gameStatus = "player pick"
    elif app.gameStatus == "import song" or app.gameStatus == "invalid song":
        if event.key == "Delete":
            app.song = app.song[:-1]
        elif event.key == "Tab":
            app.gameStatus = "player pick"
        elif event.key == "Enter":
            path = os.getcwd()
            result = inSystem(app.song, path)
            if result:
                app.pygame = Pygame(result)
                song = aubio.source(result, 0, app.hopSize)
                app.sampleRate = song.samplerate
                app.songDuration = format(float(song.duration) / song.samplerate, ".3f")
                app.onsetTimes = set(getOnsetTimes(app.song))
                temp = set()
                for time in app.onsetTimes:
                    time -= 6
                    if time > 0:
                        temp.add(float(format(time, ".3f")))
                app.beatTimes = temp
                app.gameStatus = "playing"
                app.pygame.start()
            else:
                app.song = ""
                app.gameStatus = "invalid song"
        else:
            app.song += str(event.key) 

    elif app.gameStatus == "playing":
        if event.key == "Down":
            app.dArrowPressed = True
            i = 0
            while i < len(app.arrowsPresent):
                if app.arrowsPresent[i][0] == 20 + 3*app.trackWidth//2:
                    if perfectArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 10
                        app.dStatus = "Perfect"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    elif greatArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 5
                        app.dStatus = "Great"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    elif goodArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 1
                        app.dStatus = "Good"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    else: i += 1
                else: i += 1
        elif event.key == "Up":
            app.uArrowPressed = True
            i = 0
            while i < len(app.arrowsPresent):
                if app.arrowsPresent[i][0] == 20 + 5*app.trackWidth//2:
                    if perfectArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 10
                        app.uStatus = "Perfect"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    elif greatArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 5
                        app.uStatus = "Great"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    elif goodArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 1
                        app.uStatus = "Good"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    else: i += 1
                else: i += 1
        elif event.key == "Left":
            app.lArrowPressed = True
            i = 0
            while i < len(app.arrowsPresent):
                if app.arrowsPresent[i][0] == 20 + app.trackWidth//2:
                    if perfectArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 10
                        app.lStatus = "Perfect"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    elif greatArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 5
                        app.lStatus = "Great"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    elif goodArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 1
                        app.lStatus = "Good"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    else: i += 1
                else: i += 1
        elif event.key == "Right":
            app.rArrowPressed = True
            i = 0
            while i < len(app.arrowsPresent):
                if app.arrowsPresent[i][0] == 20 + 7*app.trackWidth//2:
                    if perfectArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 10
                        app.rStatus = "Perfect"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    elif greatArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 5
                        app.rStatus = "Great"
                        app.combo += 1
                        app.multiplier = app.combo//20 + 1
                        break
                    elif goodArrow(app, app.arrowsPresent[i][1]):
                        app.arrowsPresent.pop(i)
                        app.score += 1
                        app.rStatus = "Good"
                        app.combo += 1
                        app.multiplier = app.combo//15 + 1
                        break
                    else: i += 1
                else: i += 1

        elif event.key == "s":
            app.pygame.stop()
            if app.score > 0:
                for i in range(5):
                    if app.score >= int(app.highscores[4-i]):
                        app.gameStatus = "enter name"
                        break
            if app.gameStatus == "playing": 
                app.gameStatus = "scoreboard"
        elif event.key == "p": # pauses at current duration
            if app.paused:
                app.pygame.unpause()
                app.paused = False
            else:
                app.pygame.pause()
                app.paused = True
    elif app.gameStatus == "enter name":
        print(f"Key pressed: {repr(event.key)}")
        if event.key in ("BackSpace", "Delete"):
            app.enteredName = app.enteredName[:-1]
        elif event.key in ("Return", "Enter"):
            app.highscoreNames.append(app.enteredName)
            app.highscores.append(app.score)

            # sort and trim to top 5 scores
            scorePairs = list(zip(app.highscoreNames, app.highscores))
            scorePairs.sort(key=lambda x: x[1], reverse=True)
            scorePairs = scorePairs[:5]

            app.highscoreNames = [name for (name, _) in scorePairs]
            app.highscores = [score for (_, score) in scorePairs]

            # save to highscores file
            with open("files/highscores.txt", "w") as f:
                entries = []
                for name, score in zip(app.highscoreNames, app.highscores):
                    if score > 0:
                        entries.append(f"{name}:{score}")
                f.write(",".join(entries))

            app.enteredName = ""
            app.gameStatus = "scoreboard"
        else:
            if len(event.key) == 1 and event.key.isalnum():
                app.enteredName += event.key
    elif app.gameStatus == "scoreboard":
        if event.key == "s":
            runApp(width=500, height=800)
    

def mousePressed(app, event):
    xmid = app.width//2
    ymid = app.height//2
    if app.gameStatus == "not started":
        if ((xmid - 50 < event.x < xmid + 50) and 
            (ymid - 25 < event.y < ymid + 25)):
            app.gameStatus = "player pick"
    elif app.gameStatus == "playing":
        if (5 < event.x < app.height//16 - 5) and (5 < event.y < 
            app.height//16 - 5):
            app.pygame.pause()
            app.paused = True
    elif app.gameStatus == "player pick":
        if app.width//4 < event.x < 3*app.width//4:
            if app.height//2 < event.y < app.height//2 + 40:
                app.gameStatus = "import song"
            elif 5*app.height//8 < event.y < 5*app.height//8 + 40:
                app.gameStatus = "pick song"
    elif app.gameStatus == "pick song":
        if app.width//4 < event.x < 3*app.width//4:
            margin = (3*app.height//4 - 6*app.height//15)//5
            for i in range(len(app.songList)):
                if (6*app.height//15 - 10 + margin * i <
                    event.y <
                    6*app.height//15 + 10 + margin * i):
                    
                    displayName = app.songList[i]
                    filePath = app.songFileMap[displayName] 
                    app.song = filePath

                    app.pygame = Pygame(filePath)
                    song = aubio.source(filePath, 0, app.hopSize)
                    app.sampleRate = song.samplerate
                    app.songDuration = format(float(song.duration) / song.samplerate, ".3f")
                    app.onsetTimes = set(getOnsetTimes(filePath))
                    temp = set()
                    for time in app.onsetTimes:
                        time -= 6
                        if time > 0:
                            temp.add(float(format(time, ".3f")))
                    app.beatTimes = temp
                    app.gameStatus = "playing"
                    app.pygame.start()
                    break


def createArrows(app):
    if app.beat == "yes":
        app.beat = "no"
        arrow = random.choice(app.arrowMids)
        if type(arrow) == tuple:
            app.arrowsPresent.append([arrow[0], 70 + app.arrowRadius, arrow[1]])
        else:
            app.arrowsPresent.append([arrow[0][0], 70 + app.arrowRadius, 
                                    arrow[0][1]])
            app.arrowsPresent.append([arrow[1][0], 70 + app.arrowRadius, 
                                    arrow[1][1]])

def drawStartScreen(app, canvas):
    xmid = app.width//2
    canvas.create_image(xmid, app.height//2, 
                        image=ImageTk.PhotoImage(app.startBackground))
    canvas.create_text(xmid, 2*app.height//8 - 35, text="Beat Beat", 
                        font="Arial 40 bold", fill="white")
    canvas.create_text(xmid, 2*app.height//8, text="Revolution",
                        font="Arial 40 bold", fill="white")
    if app.playButton:
        canvas.create_rectangle(xmid - 50, app.height//2 - 25, 
                                xmid + 50, app.height//2 + 25, fill="white")
        canvas.create_text(xmid, app.height//2, text="Play", 
                            font="Arial 24 bold")
    margin = (7*app.height//8 - 2*app.height//3) // 3
    canvas.create_text(xmid, 2*app.height//3, text="Press s to start/stop game", 
                        font="Arial 20", fill="white")
    canvas.create_text(xmid, 2*app.height//3 + margin, 
                        text="Press p to pause/unpause game", 
                        font="Arial 20", fill="white")
    canvas.create_text(xmid, 2*app.height//3 + 2*margin,
                        text="Have fun!", font="Arial 20", fill="white")

def drawPlayerPickScreen(app, canvas):
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.playerPickBackground))
    canvas.create_text(app.width//2, app.height//4,
                    text="Import or", font="Arial 40 bold", fill="white")
    canvas.create_text(app.width//2, 4*app.height//12,
                        text="Pick song?", font="Arial 40 bold", fill="white")
    canvas.create_rectangle(app.width//4, app.height//2, 
                            3*app.width//4, app.height//2 + 40, fill="white")
    canvas.create_rectangle(app.width//4, 5*app.height//8, 
                            3*app.width//4, 5*app.height//8 + 40, fill="white")
    canvas.create_text(app.width//2, app.height//2 + 20,
                        text="Import any song (i)", font="Arial 20")
    canvas.create_text(app.width//2, 5*app.height//8 + 20,
                        text="Pick song from list (p)", font="Arial 20")
    canvas.create_text(app.width//2, 3*app.height//4,
                        text="or click on the boxes to choose", 
                        font="Arial 16", fill="white")
    
def drawImportScreen(app, canvas):
    xmid = app.width//2
    canvas.create_image(xmid, app.height//2,
                        image=ImageTk.PhotoImage(app.multiBackground))
    canvas.create_text(xmid//2, 40, text="Press Tab to go back", 
                        font="Arial 16", fill="white")
    canvas.create_text(xmid, app.height//4, text="Import Any Song", 
                        font = "Arial 40 bold", fill="white")
    canvas.create_text(xmid, 11*app.height//32,
                    text="Type in any mp3 song file exactly how it's stored",
                    font="Arial 16", fill="white")
    canvas.create_text(xmid, 12*app.height//32,
                text="Song file MUST be in the songs folder",
                font="Arial 16", fill="white")
    canvas.create_text(xmid, 13*app.height//32, text="Example: JustDance.mp3", 
                        font="Arial 16", fill="white")
    canvas.create_rectangle(app.width//4, app.height//2 - 20,
                            3*app.width//4, app.height//2 + 20, fill="white")
    canvas.create_text(xmid, app.height//2, text=f"{app.song}", font="Arial 16")
    margin = (7*app.height//8 - 5*app.height//8) // 5
    canvas.create_text(xmid, 5*app.height//8,
                        text="How to play:", font="Arial 24 bold", fill="white")
    canvas.create_text(xmid, 5*app.height//8 + margin,
                        text="When the game starts, arrows will generate to", 
                        font="Arial 16", fill="white")
    canvas.create_text(xmid, 5*app.height//8 + 2*margin,
                        text="the beat of the music. Press the arrow keys in",
                        font="Arial 16", fill="white")
    canvas.create_text(xmid, 5*app.height//8 + 3*margin,
                        text="line with the arrows at the bottom as they fall.",
                        font="Arial 16", fill="white")
    canvas.create_text(xmid, 5*app.height//8 + 4*margin,
                    text="The more accurate you are, the higher your score is!",
                        font="Arial 16", fill="white")

def drawInvalidScreen(app, canvas):
    drawImportScreen(app, canvas)
    canvas.create_text(app.width//2, app.height//2 + 35, 
                        text="Invalid file, not found in system. Try Again",
                        font="Arial 16", fill="red")

def drawPickSongScreen(app, canvas):
    xmid = app.width//2
    canvas.create_image(xmid, app.height//2,
                        image=ImageTk.PhotoImage(app.multiBackground))
    canvas.create_text(xmid//2, 40, text="Press Tab to go back", 
                        font="Arial 16", fill="white")
    canvas.create_text(xmid, app.height//4, text="Click on any song", 
                        font = "Arial 40 bold", fill="white")
    canvas.create_rectangle(xmid//2, app.height//3, 
                            3*app.width//4, 3*app.height//4, fill="white")
    margin = (3*app.height//4 - 6*app.height//15)//5
    for i in range(len(app.songList)):
        song = app.songList[i]
        canvas.create_text(xmid, 6*app.height//15 + (margin * i),
                            text=f"{song}", font="Arial 18")

def drawPausedScreen(app, canvas):
    margin = (3*app.height//4 - 20 - 5*app.height//8) // 3
    canvas.create_rectangle(app.width//4, app.height//4, 
                            3*app.width//4, 3*app.height//4, fill="white")
    canvas.create_text(app.width//2, 3*app.height//8,  
                        text="Paused", font="Arial 30 bold")
    canvas.create_text(app.width//2, app.height//2,
                        text=f"Score: {app.score}", font="Arial 24")
    canvas.create_text(app.width//2, 5*app.height//8,
                        text="Press p to unpause", font="Arial 16")
    canvas.create_text(app.width//2, 5*app.height//8 + margin,
                        text="Press s to stop game", font="Arial 16")
    canvas.create_text(app.width//2, 5*app.height//8 + 2*margin,
                        text=f"Current song: {app.song}", font="Arial 16")

def drawStatus(app, canvas):
    if app.dStatus != None:
        canvas.create_text(20 + 3*app.trackWidth//2, 7*app.height//8 - 10, 
                            text=f"{app.dStatus}", font="Arial 24 bold")
    if app.uStatus != None:
        canvas.create_text(20 + 5*app.trackWidth//2, 7*app.height//8 - 10, 
                            text=f"{app.uStatus}", font="Arial 24 bold")
    if app.lStatus != None:
        canvas.create_text(20 + app.trackWidth//2, 7*app.height//8 - 10, 
                            text=f"{app.lStatus}", font="Arial 24 bold")
    if app.rStatus != None:
        canvas.create_text(20 + 7*app.trackWidth//2, 7*app.height//8 - 10, 
                            text=f"{app.rStatus}", font="Arial 24 bold")

def drawAllArrows(app, canvas):
    drawDownArrow(app, canvas)
    drawUpArrow(app, canvas)
    drawLeftArrow(app, canvas)
    drawRightArrow(app, canvas)
    drawFallingArrows(app, canvas)

def drawFallingArrows(app, canvas):
    for i in range(len(app.arrowsPresent)):
        xmid = app.arrowsPresent[i][0]
        ymid = app.arrowsPresent[i][1]
        arrow = app.arrowsPresent[i][2]
        canvas.create_image(xmid, ymid, image=ImageTk.PhotoImage(arrow))

def drawDownArrow(app, canvas):
    if app.dArrowPressed:
        canvas.create_image(20 + 3*app.trackWidth//2, (7*app.height//8 + 
                            app.height - 20)//2, 
                            image=ImageTk.PhotoImage(app.dArrowPress))
    else:
        canvas.create_image(20 + 3*app.trackWidth//2, 
                            (7*app.height//8 + app.height - 20)//2, 
                            image=ImageTk.PhotoImage(app.dArrow))

def drawUpArrow(app, canvas):
    if app.uArrowPressed:
        canvas.create_image(20 + 5*app.trackWidth//2, (7*app.height//8 + 
                            app.height - 20)//2, 
                        image=ImageTk.PhotoImage(app.uArrowPress))
    else:
        canvas.create_image(20 + 5*app.trackWidth//2, (7*app.height//8 + 
        app.height - 20)//2, image=ImageTk.PhotoImage(app.uArrow))

def drawLeftArrow(app, canvas):
    if app.lArrowPressed:
        canvas.create_image(20 + app.trackWidth//2, (7*app.height//8 + 
                            app.height - 20)//2, 
                        image=ImageTk.PhotoImage(app.lArrowPress))
    else:
        canvas.create_image(20 + app.trackWidth//2, (7*app.height//8 + 
                            app.height - 20)//2, 
                            image=ImageTk.PhotoImage(app.lArrow))

def drawRightArrow(app, canvas):
    if app.rArrowPressed:
        canvas.create_image(20 + 7*app.trackWidth//2, (7*app.height//8 + 
                            app.height - 20)//2, 
                        image=ImageTk.PhotoImage(app.rArrowPress))
    else:
        canvas.create_image(20 + 7*app.trackWidth//2, (7*app.height//8 + 
                            app.height - 20)//2, 
                            image=ImageTk.PhotoImage(app.rArrow))

def drawTrack(app, canvas):
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.trackBackground))
    canvas.create_rectangle(20, 7*app.height//8, app.width - 20, 
                            app.height- 20, outline="white")
    canvas.create_rectangle(0, 0, app.width, app.height//16, outline="white")
    canvas.create_rectangle(20, 70, 20 + app.trackWidth, app.height - 20, 
                            outline="white")
    canvas.create_rectangle(20 + app.trackWidth, 70, 20 + 2*app.trackWidth, 
                            app.height - 20, outline="white")
    canvas.create_rectangle(20 + 2*app.trackWidth, 70, 20 + 3*app.trackWidth, 
                            app.height - 20, outline="white")
    canvas.create_rectangle(20 + 3*app.trackWidth, 70, 20 + 4*app.trackWidth, 
                            app.height - 20, outline="white")

def drawScore(app, canvas):
    canvas.create_text(app.width//2, app.height//32, text=f"Score: {app.score}",
                        font="Arial 24", fill="white")
    canvas.create_text(7*app.width//8, app.height//60,
                        text=f"Combo: {app.combo}", font="Arial 16", 
                        fill="white")
    canvas.create_text(7*app.width//8, app.height//24,
                        text=f"Multiplier: {app.multiplier}", 
                        font="Arial 16", fill="white")

def drawPause(app, canvas):
    canvas.create_rectangle(5, 5, app.height//16 - 5, app.height//16 - 5, 
                            fill="white")
    canvas.create_rectangle(11, 11, 21, app.height//16 - 11, fill="black")
    canvas.create_rectangle(27, 11, 37, app.height//16 - 11, fill="black")


def drawEnterName(app, canvas):
    drawScoreboard(app, canvas)
    canvas.create_rectangle(app.width//6, 4*app.height//15,
                            5*app.width//6, 5*app.height//6, fill="white")
    canvas.create_text(app.width//2, 7*app.height//16,
                        text="Enter your name", font="Arial 30 bold")
    canvas.create_rectangle(app.width//4, app.height//2 - 20,
                            3*app.width//4, app.height//2 + 20)
    canvas.create_text(app.width//2, app.height//2,
                        text=f"{app.enteredName}", font="Arial 16")
    canvas.create_text(app.width//2, 9*app.height//16,
                        text="(no spaces)", font="Arial 16")

def drawScoreboard(app, canvas):
    xmid = app.width//2
    canvas.create_image(xmid, app.height//2,
                        image=ImageTk.PhotoImage(app.endBackground))
    canvas.create_text(xmid, app.height//6, 
                        text="Game Over",font="Arial 40 bold", fill="white")
    canvas.create_text(xmid, 4*app.height//18, text=f"Score: {app.score}", 
                        font="Arial 24", fill="white")
    canvas.create_rectangle(app.width//5, 4*app.height//15, 4*app.width//5, 
                            4*app.height//5, fill="white")
    canvas.create_text(xmid, app.height//3,
                        text="Highscores", font="Arial 26 bold")
    canvas.create_text(xmid, 9*app.height//10, text="Press s to start over", 
                        font="Arial 16", fill="white")

    margin = (11*app.height//15 - 6.5*app.height//15) // 5
    for i in range(len(app.highscores)):
        score = app.highscores[i]
        name = app.highscoreNames[i]
        canvas.create_text(3*app.width//8, 6.5*app.height//15 + (margin * i),
                            text=f"{name}", font="Arial 18")
        canvas.create_text(5*app.width//8, 6.5*app.height//15 + (margin * i),
                            text=f"{score}", font="Arial 18")

    

def redrawAll(app, canvas):
    if app.gameStatus == "not started":
        drawStartScreen(app, canvas)
    elif app.gameStatus == "player pick":
        drawPlayerPickScreen(app, canvas)
    elif app.gameStatus == "import song":
        drawImportScreen(app, canvas)
    elif app.gameStatus == "invalid song":
        drawInvalidScreen(app, canvas)
    elif app.gameStatus == "pick song":
        drawPickSongScreen(app, canvas)
    elif app.gameStatus == "playing":
        drawTrack(app, canvas)
        drawAllArrows(app, canvas)
        drawFallingArrows(app, canvas)
        drawStatus(app, canvas)
        drawScore(app, canvas)
        drawPause(app, canvas)
        if app.paused:
            drawPausedScreen(app, canvas)
    elif app.gameStatus == "enter name":
        drawEnterName(app, canvas)
    elif app.gameStatus == "scoreboard":
        drawScoreboard(app, canvas)

runApp(width=500, height=800)
