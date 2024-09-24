# Chess Trainer 

You start off on level 0 representing pure random play. Winning a game moves you up 2 levels, losing a game moves you down 1 level, a draw moves you up 1 level. By the time you get to level 100, you're superhuman at chess. The agent playing against you is generated prior to each chess game, persists for the duration of the game, then disappears forever. In other words, whatever strategies you encounter as you play, you'll never see those strategies again. Some agents randomly like bishops better than rooks, or randomly prefer the left side of the board vs the right, or really like moving one particular piece a lot. These aspects of the strategy change, but as you get closer to level 100, getting to ever-increasing levels of play, you'll start to notice patterns in the noise, strategies that are successful. For instance, by the time you get to around level, 40 the engine consistently understands that it's a good idea to protect and re-capture pieces (sometimes it won't because it thinks it sees something more important, but in general). By the time you get to level 70 (way above my level) it's playing recognizable openings to a deep level, not because it's memorized those openings but because it's good enough to undersand. The engine will teach you what's important for you to understand at your skill level... it'll teach you this often through humiliating defeat at times when you stuck to your guns and played what you thought you knew was right, and suddenly you're in checkmate. 

I have been playing chess for years, and this has engine has taught me the following valuable lessons, most of which I was not getting elsewhere:
1. Respect for the game. The AI seeming to play terribly is not an invitation for you to play terribly. It'll teach you this.
1. I don't value king safety enough. I can be blind to pressure building up on my king.
1. I often don't go after the opponent's king aggressively enough when an opportunity opens up.
1. I value material too much.
1. Tactics.
1. End game strategy.
1. Balance and pacing (when sometimes a slow pace is a good idea), especially in complex situations.
1. Chess is a much more open-ended and freely-flowing game than I thought. Playing against standard engines, you'll quickly get stuck playing a strategy you're not good enough to play. This engine has taught me to be comfortable saying "ehh... I'm just gonna do some bat sh*t crazy thing and go off the rails here"... but to actually understand when's a good time, for me personally, to do something like.
1. Most importantly, the engine shows you what you don't know about chess. It is the most excellent teacher I've seen at finding your misconceptions and presenting them to you on a silver platter. Think you should win because you castled and your opponent did not? Well, sure, if you're good enough to take advantage of something like that. This engine will precisely answer for you what strategies you're good enough to take advantage of.


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

At the start, you're likely to face at least 10, if not more, random-like opponents in a row before the engine starts showing any signs of what we might consider "thinking". Don't get thrown off by this however. Your first loss is likely to be against an opponent you consider to still be playing terribly, but will catch you making the natural human mistake of playing down to your opponent. That's why the first lesson I listed is respect for the game which we inevitably lack in human games. The reason it will catch you off guard is because it seems to become proficient at chess tactics and check mates far before it arrives at more standard looking strategies like controlling the center and castling (this should make sense if you think about it... it's piecing together good chess play from the ground up, starting with obvious things like looking for check mates and big tactics).
