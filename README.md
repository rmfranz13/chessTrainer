# Chess Trainer 

Train yourself in chess the same way super-human AI (LeelaChessZero) is trained, but in a much more sample-efficient manner. Your opponent starts off knowing nothing, and as you continue to defeat it, it will start learning and begin to piece together the rules of chess, from the ground up. Eventually (guaranteed if you're a human in less than 100 games), you'll face an opponent that is stronger than you. At this point we've found your sweet spot: you'll become the student and start learning. Each game is played against a unique randomly-generated opponent that will, on average, be slightly stronger than you. This will guide you in the direction of stronger play. Once you've found your sweet spot, your opponents will continue to vary in strength. They won't always be stronger than you, and even your stronger opponents aren't likely to be completely indesctructable. You always have a fighting chance, which is important. There are no time settings, no take-backs, no analysis (although the games will be saved), and no wrong way to play. Play as fast as you want, as slow as you want, try crazy things and see what happens... if you want to improve, there's no better way than simply playing chess, start to end, against these unique randomly-generated opponents who will tend to be slightly stronger than you.

This is to address some of the problems I see as being introduced by standard chess engines like Stock Fish. In the grand scheme of the history of Chess, super-human chess engines are a relatively recent invention. The ability to pull out the super-human chess engine in your phone and analyze your games is at best going to help you realize you aren't superhuman, and at worst teach you strategies that you aren't ready for. Practicing against traditional chess engines like Stock Fish will punish risk taking and exploration and beat you into a pattern of being as conservative as possible, trying to last as long as possible without making a mistake. There isn't a good way to make a traditional chess engine play to your level except for handicapping it materially, or by having it make intentionally bad moves. These approaches put you in unnatural positions that aren't going to teach you much.

This approach is fundamentally different, and teaches you chess the same way as a neural network like Leela Chess Zero (and hey, neural network? you have one of those: your brain).

# How does it work?

I start off with a fully-trained network from leelaChess, this is called the "master" network. It's not literally a perfect chess-playing agent, but you can bet it's much stronger than you. I add a lot of noise to it so that it plays randomly, and then as you keep playing... winning and losing, the amount of noise gets adjusted each game, giving you players that are always unique and always about as far from perfect as you are. It will aim to win 2/3 of the games against you, and push you towards strategy more like that of the master network over time. That is... we are distilling the chess knowledge gained by leelaChess over millions of games into you the human. It just so happens that as you become more master-like in chess, you will become... more master-like in chess. This approach doesn't teach you what's good or bad chess strategy, it just pits you against an infinite number of unique opponents that drive you in the direction of being more like the master network.

You start off on level 0 representing pure random play. Winning a game moves you up 2 levels, losing a game moves you down 1 level, a draw moves you up 1 level. Each level up reduces the amount of noise added to the training network you'll play against in the next round, bringing that agent closer to the master network, causing feature's of master's playing style to become ever-more apparent. By the time you get to level 100, you're playing the un-altered master network and defeating it means you're likely superhuman at chess (there's some hardware dependence though). The agent playing against you is generated prior to each chess game, persists for the duration of the game, then disappears forever. In other words, whatever strategies you encounter as you play, you'll likely never see those exact strategies ever again, even if you keep playing around the same level. You're being exposed to all possible chess strategies that are roughly as far from master as you are. Some agents randomly like bishops better than rooks, or randomly prefer the left side of the board vs the right, or really like moving one particular piece a lot. It doesn't know what the relative worth of pieces are, it doesn't know the value of controlling the center or having rooks on open files or knights on outposts. These aspects of the strategy change with each new opponent, but as you get closer to level 100, getting to ever-increasing levels of play, you'll start to notice patterns in the noise, strategies that are successful, and these turn out to be what we might recognize as strategy. Because winning moves you up 2 levels, but losing moves you down 1 level, you will on average be playing against a slightly stronger opponent than yourself, which is how you improve. Unlike far-superhuman chess engines that tend to beat you into a risk-averse strategy where you're just trying to last as long as possible, the opponents you face here will not be indestructable, you'll always have a fighting chance. Additionally, it will not make intentionally stupid moves which is a common strategy to get standard chess engines to play at a certain level. It's always trying to win, even when the amount of noise added is such that it appears to be playing terribly. 

The first 10 to 20 games might feel absurdly easy, and you might question whether it's improving at all. Rest assured it is getting better with each level (on average), and rest assured you will not make it to level 100. You might see sparks of good strategy appear around level 20-30 only to then witness a needless queen sacrifice. The reason I included so many levels where it appears to be playing terribly is because there is signal in the noise on these levels... it may not be particularly good at the early levels but it isn't random. Perhaps the earliest improvement you'll notice is that it will start avoiding check mate for longer, rather than walking straight into it (even at the cost of random queen sacrifices)... it will make you chase the king around a little longer before you're able to ultimately check mate. It will also improve at putting pressure on your king and specifically directly attacks at your king, even though it may do a terrible job of this and end up throwing away the pieces it was attempting to attack your king with. Somewhere in the level 30 range, it'll start to become more adept at tactics, and understand that it ought to protect it's pieces and re-capture. It appears to start to care more about material, but this is only as a means of achieving the king-directed strategies it had come across earlier. This progression of skills isn't an accident, it's building up chess skills in a very logical way. The most important aspect of chess is to protect the king and attack your opponents king, and you'll notice the AI doing a better job of this even before it understands that a queen is more valuable than a pawn. By the time you get to level 70 (way above my level) it's playing recognizable openings to a deep level, not because it's memorized those openings but because it's good enough to "understand". The engine will teach you what's important for you to understand at your skill level, often through humiliating defeat and putting you in the weirdest positions you could never have dreamed of. If your head hurts, that means you're learning, and I have never met human opponents who could make my head hurt so much.


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
