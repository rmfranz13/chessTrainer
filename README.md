# Chess Trainer 

You start off on level 0 representing pure random play. Winning a game moves you up 2 levels, losing a game moves you down 1 level, a draw moves you up 1 level. By the time you get to level 100, you're superhuman at chess. The agent playing against you is generated prior to each chess game, persists for the duration of the game, then disappears forever. In other words, whatever strategies you encounter as you play, you'll never see those strategies again. Some agents randomly like bishops better than rooks, or randomly prefer the left side of the board vs the right, or really like moving one particular piece a lot. These aspects of the strategy change, but as you get closer to level 100, getting to ever-increasing levels of play, you'll start to notice patterns in the noise, strategies that are successful. Because winning moves you up 2 levels, but losing moves you down 1 level, you will on average be playing against a slightly stronger opponent than yourself, which is how you improve. Unlike far-superhuman chess engines that tend to beat you into a risk-averse strategy where you're just trying to last as long as possible, the opponents you face here will not be indestructable, you'll always have a fighting chance. Additionally, it will not make intentionally stupid moves. It's always trying to win, even when the amount of noise added is such that it appears to be playing terribly. 

The first 10 to 20 games might feel absurdly easy, and you might question whether it's improving at all. Rest assured it is getting better with each level (on average), and rest assured you will not make it to level 100. You might see sparks of good strategy appear around level 20-30 only to then witness a needless queen sacrifice. The reason I included so many random-like levels is because there is signal in the noise on these levels... perhaps the first improvement you'll notice is that it will start avoiding check mate for longer, rather than walking straight into it (even at the cost of random queen sacrifices). It will also improve at putting pressure on your king and attacking, even though it will do a terrible job of this and often throw away the pieces it was attempting to attack your king with. Then somewhere in the level 30 range, it'll start to become more adept at tactics, and understand that it ought to protect it's pieces and re-capture. This progression of skills isn't an accident, it's building up chess skills in a very logical way. The most important aspect of chess is to protect the king and attack your opponents king, and you'll notice the AI doing a better job of this even before it understands that a queen is more valuable than a pawn. By the time you get to level 70 (way above my level) it's playing recognizable openings to a deep level, not because it's memorized those openings but because it's good enough to "understand". The engine will teach you what's important for you to understand at your skill level, often through humiliating defeat. It'll also excel at making your head hurt by putting you in bizarre situations you have never encountered. 

While most chess engines are effectively "perfect" for practical purposes, this engine will expose you to *all possible chess players* that are roughly the same distance from "perfect" as you are. It's hard to imagine a more effective method of learning.

I have been playing chess for years, and this engine is teaching me the following lessons in a way I was not getting elsewhere:
1. Respect for the game, and not playing poorly against what appears to be a weak opponent.
1. The value of king safety.
1. The value, or lack thereof, of material -- it's only valuable as a means of attacking or protecting the king.
1. How to build up pressure in the opening and middle game.
1. Tactics. The engine will be surprisingly good at tactics compared to it's apparent strategic understanding.
1. Balance and pacing... when sometimes a slow pace is a good idea, especially in complex situations, and when to take a break from the main battle and play or react to pressures elsewhere.
1. Risk taking. The now-rewardable practice of saying "you know what I'm just gonna do some bat sh*t crazy thing here and see how that goes." The engine will do this against you and succeed, and you'll learn to return the favor.
1. Most importantly, the engine shows you what you don't know about chess. It is excellent at finding your misconceptions and presenting them to you on a silver platter.


# Requirements: 

For now, this requires you have Python3 and git on a Windows machine. Typing "python" at the windows terminal should put you in an interactive python 3 session (powershell or cmd or 3rd party terminal such as might come with python or anaconda). Similarly "git" should be an accessible command from the same terminal.

# Initial setup:
Simply clone this repo and pip install the dependencies (there's only 2: python-chess for the chess-playing logic and certain aspects of the chess GUI, and protobuf which is needed to read and apply noise to the network weights for each game).
```
git clone https://github.com/rmfranz13/chessTrainer.git
pip install -r requirements.txt
```

# How to run:
Now each game will be kicked off simply by calling do_chess.py:
```
python do_chess.py
```

If all goes according to plan, you should be greeted with a welcome message (mostly the same info in this readme), clicking OK, you should see in the terminal the 13 layers of the neural network having noise applied, this may take a few seconds, then a GUI will pop up that randomly selects you to either play black or white. If black, the engine will immediately start playing (might take a minute to load the engine and calculate the move, but shouldn't take more than 10 seconds for subsequent moves). There is no timer and the only options you have besides playing chess moves is to resign or force the engine to resign. This is intended to remove unneeded complixity with options around search depth and thinking time. There are no take-backs, no analysis, no time limit for you. The point is simply to play chess. The games are saved, and you'll see a message indicating where, and you can look at them manually if desired, but the spirit of this trainer is simply to pit you against as many interesting opponents as possible, each opponent (once you find your approximate skill range) having something unique to teach you.

Once the game is over, either by checkmate, resignation, or one of the many possible draw conditions, it will automatically be saved and the window will close.

To play the next game simply re-run 
```
python do_chess.py
```

This time, the level of noise added to the network will be adjusted based on the result of your previous game, making for a better opponent if you won, or a worse opponent if you lost. This cycle repeats indefinitely, and a plot will open with each new game showing the progress you've made.