# Chess Trainer 

You start off on level 0 representing pure random play. Winning a game moves you up 2 levels, losing a game moves you down 1 level, a draw moves you up 1 level. By the time you get to level 100, you're superhuman at chess. The agent playing against you is generated prior to each chess game, persists for the duration of the game, then disappears forever. In other words, whatever strategies you encounter as you play, you'll never see those strategies again. Some agents randomly like bishops better than rooks, or randomly prefer the left side of the board vs the right, or really like moving one particular piece a lot. These aspects of the strategy change, but as you get closer to level 100, getting to ever-increasing levels of play, you'll start to notice patterns in the noise, strategies that are successful. Because winning moves you up 2 levels, but losing moves you down 1 level, you will on average be playing against a slightly stronger opponent than yourself, which is how you improve. Unlike far-superhuman chess engines that tend to beat you into a risk-averse strategy where you're just trying to last as long as possible, the opponents you face here will not be indestructable, you'll always have a fighting chance. Additionally, it will not make intentionally stupid moves. It's always trying to win, even when the amount of noise added is such that it appears to be playing terribly. 

The first 10 to 20 games might feel absurdly easy, and you might question whether it's improving at all. Rest assured it is getting better with each level (on average), and rest assured you will not make it to level 100. You might see sparks of good strategy appear around level 20-30 only to then witness a needless queen sacrifice. The reason I included so many random-like levels is because there is signal in the noise on these levels... perhaps the first improvement you'll notice is that it will start avoiding check mate for longer, rather than walking straight into it (even at the cost of random queen sacrifices). It will also improve at putting pressure on your king and attacking, even though it will do a terrible job of this and often throw away the pieces it was attempting to attack your king with. Then somewhere in the level 30 range, it'll start to become more adept at tactics, and understand that it ought to protect it's pieces and re-capture. This progression of skills isn't an accident, it's building up chess skills in a very logical way. The most important aspect of chess is to protect the king and attack your opponents king, and you'll notice the AI doing a better job of this even before it understands that a queen is more valuable than a pawn. By the time you get to level 70 (way above my level) it's playing recognizable openings to a deep level, not because it's memorized those openings but because it's good enough to "understand". The engine will teach you what's important for you to understand at your skill level, often through humiliating defeat. It'll also excel at making your head hurt by putting you in bizarre situations you have never encountered. 

While most chess engines are effectively "perfect" for practical purposes, this engine will expose you to *all possible chess players* that are roughly the same distance from "perfect" as you are. It's hard to imagine a more effective method of learning.

I have been playing chess for years, and this has engine has taught me the following valuable lessons, in the following order
1. The real value of king safety.
1. The value of material -- only as a means of attacking or protecting the king.
1. How to build up pressure on the enemy king in the opening and middle game.
1. Common shapes and structures: multi-piece arrangements that act together in a reliable way, such as a bishop and pawn co-protecting eachother, or battering ram with queen and rook.
1. Tactics and end game strategy.
1. Opening mistakes (and traps).
1. Building up pressure in the opening that isn't obviously king-focussed.
1. Balance and pacing (when sometimes a slow pace is a good idea), especially in complex situations. When to play elsewhere.
1. Risk taking. The now-rewardable practice of saying "you know what I'm just gonna do some bat sh*t crazy thing here and see how that goes."
1. Most importantly, the engine shows you what you don't know about chess. It is excellent at finding your misconceptions and presenting them to you on a silver platter.


# Requirements: 

For now, this requires you have Python3 on a Windows machine. Typing "python" at the windows terminal should put you in an interactive python 3 session (powershell or cmd or 3rd party terminal such as might come with python or anaconda)

# How to run:
From a windows terminal where python and pip is accessible
```
pip install -r requirements.txt
python do_chess.py
```
If all goes according to plan, you should be greeted with a welcome message (mostly the same info in this readme), clicking OK, you should see in the terminal the 13 layers of the neural network having noise applied, then a GUI will pop up that randomly selects you to either play black or white. If black, the engine will immediately start playing (might take a minute... while the engine is thinking you can't move or edit the GUI window, a known limitation). There is no timer and the only options you have besides playing chess moves is to resign or force the engine to resign. This is intended to remove unneeded complixity with options around search depth and thinking time. Making the engine resign is an honesty-policy thing or could be used to see what the engine is like on much stronger levels... using the engine resign to amass fake wins to put you at a too-strong of a level, I would adivse against using the button at all however. The engine should move within 10 seconds or less. It goes to a search depth of 6 moves, which when playing against the unaltered network is enough to be superhuman (and hopefully fast enough to be usalbe on most modern hardware).

Once the game is over, either by checkmate, resignation, or one of the many possible draw conditions, it will automatically be saved. 

To play the next game simply re-run 
```
python do_chess.py
```

(assuming you win the first game because it will be playing quite terribly), you will now be greeted with a plot showing your progress over time. This behavior will continue from hence forth. You can restart by deleting all the games (you'll get a message indicating which folder they're saved in, and you can't save more than 1000 games simply from the naming format... this shouldn't be a blocker, simply delete the games and start again if you manage to play 1000 games). 