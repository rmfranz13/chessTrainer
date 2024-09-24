import pdb
import matplotlib.pyplot as plt
import os
import numpy as np
import random
# pdb.set_trace()
import net_pb2
import tkinter as tk
from tkinter import messagebox

# Adds a a particular amount of noise to the weights of an otherwise super-human-level chess playing neural network (Leela Chess),
# for an experiment in training humans in chess.
#
# The "levels" are tuned such that there are 100 levels, or difficulties, with the assumption the computer is
# set to a fixed search limit of 500 nodes (the constraining factor is that's small enough for slow computers to run in a reasonable time,
# but deep enough (for this type of engine) that a good network won't make a stupid mistake).
# The 500 node limit isn't strict, it should still generate opponents in your strenght range as long as you stick to a standard
# time limit or search depth, but increasing the search depth might "un-tune" it a bit, such that level 0 isn't guaranteed to be totally random, etc.
#
# Every time this program is run, a random opponent is generated, which will seemingly have random strategies and 
# thus the actual difficulty, at a particular level, is also random (approximately in a gaussian fashion).
#
# Level 0 is basically guranteed to play a random/terrible game and level 100 is pretty much going to be unbeatable.
# 
# The level adjusts itself such that you can expect to win 1/3 of the games, if you played infinitely many games 
# (unless you become stronger than the super-human engine). So you're usually playing an opponent that's stronger than you 
# which is beneficial to improving.
#
# The beauty in this approach is that it exposes you, over time, to all possible players that are roughly "as far 
# away as you are" from a superhuman chess player. And as you improve and the level of noise added is reduced, it'll
# show you your weaknesses and concepts you've taken for granted, as it hones you in on how a super-human player values 
# a chess position. This is also, btw, how neural network based engines train themselves. Noise is added to the "best" neural 
# network available which then plays itself to generate a training set. The experiment here is whether this approach is also 
# effective in training the chess-playing neural network... that's in *your* head. 
#
# To test this experiment effectively, I recommend you don't analyze your games with another computer, to show you what
# opportunities you may have missed. This is not how the neural networks are trained, and also not how anyone studied in 
# the vast history of chess (when there were no superhuman computers). You learn by playing and being constantly 
# put in new and challenging situations. The opponents generated by this program, you will find, are quite good at putting you in such situations.
#
# Starts you off at level 50.
# Adds or subtracts 25 based off first result.
# Adds or subtracts 12 based off second result.
# Adds or subtracts 6 based off third result.
# Adds or subtracts 3 based off fourth result.
# Then:
# A win adds 2
# A loss subtracts 1
# A draw adds 1

level = 0

master_weights_file = 'masterWeights/128x14-2020_1226_0035_49_187.pb'
trainer_weights_file = "RyanTrainer/weights.pb"
saved_games_folder = "RyanTrainer/games/"
arena_path = "arena/arena_3.5.1/Arena.exe"
engine_name = "Engine"

max_val = 2**16

net = net_pb2.Net()

#saved_games = os.listdir(saved_games_folder)
# if games folder doesn't exist, create it. Else, get the list of saved games.
if not os.path.exists(saved_games_folder):
    os.makedirs(saved_games_folder)
saved_games = os.listdir(saved_games_folder)


index = 0
indices = [0]
level_progression = [0]
for saved_game in saved_games:
    with open(saved_games_folder + saved_game, "r") as game_file:
        lines = game_file.readlines()
        for line in lines:
            if(engine_name in line):
                if("White" in line):
                    computer_color = 'w'
                    player_color = 'b'
                elif("Black" in line):
                    computer_color = 'b'
                    player_color = 'w'
                else:
                    print("Player and computer are of unknown colors. What a time we live in.")
                    exit(1)
            elif("Result" in line):
                if("1-0" in line):
                    if(computer_color == 'w'):
                        winner = "computer"
                    else:
                        winner = "player"
                elif("0-1" in line):
                    if(computer_color == 'w'):
                        winner = "player"
                    else:
                        winner = "computer"
                elif("*" in line):
                    # Game isn't done. Finish the game.
                    os.system('start ./' + arena_path + " " + saved_game)
                    exit(1)
                else:
                    winner = "tie"
    '''if(index == 0):
        if(winner == "player"):
            level += 25
            index += 1
        elif(winner == "computer"):
            level -= 25
            index += 1
        else:
            pass
    elif(index == 1):
        if(winner == "player"):
            level += 12
            index += 1
        elif(winner == "computer"):
            level -= 12
            index += 1
        else:
            pass
    elif(index == 2):
        if(winner == "player"):
            level += 6
            index += 1
        elif(winner == "computer"):
            level -= 6
            index += 1
        else:
            pass
    elif(index == 3):
        if(winner == "player"):
            level += 3
            index += 1
        elif(winner == "computer"):
            level -= 3
            index += 1
        else:
            pass
    else:'''
    if(winner == "player"):
        level += 2
        index += 1
    elif(winner == "computer"):
        level -= 1
        index += 1
    else:
        level += 1
        index += 1
    level_progression.append(level)
    indices.append(index)


# plot your progress:
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("Your Progress: \nMake it to level 100 and you're the strongest chess player on Earth.")
#Remove y-axis labels
#ax.yaxis.set_ticklabels([])

ax.set_ylabel("Level")
ax.scatter(indices, level_progression)
plt.xlabel("Game Number")
plt.savefig("progression.png")
plt.close()

# If there's less than 5 games, show warning message box indicating you're presently in the calibration rounds.
if(len(indices) == 1):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Welcome", """Welcome to the chess trainer! There are 100 levels and you start off on level 0, which effectively represents 
pure random play. Winning a game moves you up 2 levels, losing a game moves you down 1 level, a draw moves you up 1 level. Level 100 is an unaltered version 
of LeelaZero Chess engine, which is far superhuman. Each "level" represents an amount of noise added to this super human network such that it roughly achieves 
a particular level of play (for instance, pure random play at level 0). Every opponent is generated uniquely for the game at hand, so there are no guarantees 
about the sort of opponent you'll be facing, and that's the point. Because you move up 2 points for a win and down 1 point for a loss, you'll on average face off 
against slightly stronger opponents than you, which is good incentive for practice: you have a shot of winning, your opponents won't be indestructable, but they'll
tend to be a step ahead on the average. 

Since you're starting off on level 0, you'll start off with some very easy games. You'll notice it improving skill level however as you move up the ladder, eventually 
putting you in a realm where you're roughly winning 1/3 of the time.

I decided to start off easy and make it harder because it's good to get a few wins under your belt and get a feel for how the strength progresses.
    
You are certain to play games that you've never dreamed of, and as your skills progress
the trianer will highlight your misconceptions... often in the form of humiliating, annoying, and sometimes even shocking fashion. That's okay though because that's how you learn.

For instance, most folks castle because they're taught it's the right thing to do to protect your king. While this works effectively in human game play, it doesn't give you the visceral feeling of why it's so important to protect the king,
because by the time you're good enough that you're habitually castling, you're never going to find a decent human player who marches their king out into the center of the board and still beats you. It's possible to find such players here. Playing against 
such opponents exposes you to realms that no human player would (or even could). Now anyone can experience what it must've feel like to be a top player, playing against an ever-improving machine, all the while trianing yourself to be more superhuman at chess.

That is why this training program is designed as it is. There is no time limit for you, there are no take-backs, no analysis. There's just playing chess against interesting opponents that are around your strength to make you better. 
    
    Good luck!""")
    root.destroy()
else:
    # Os call to show the plot:
    os.system('start progression.png')

def noise_converter(level_in):
    return(np.exp((-level_in * 0.1535056728662697) - 3.8376418216567423))


global_noise = noise_converter(level)


def unpack_layer(layer_in):
    bytes_array = layer_in.params
    max_weight = layer_in.max_val
    min_weight = layer_in.min_val
    layer_range = max_weight - min_weight
    msbs = bytes_array[::2]
    lsbs = bytes_array[1::2]
    floats = []
    for lsb, msb in zip(msbs, lsbs):
        raw_int = 256 * int(msb) + int(lsb)
        to_float = raw_int / (max_val * layer_range) + min_weight
        floats.append(to_float)
    return(floats)


def repack_layer(floats_in, layer_in):
    max_weight = layer_in.max_val
    min_weight = layer_in.min_val
    layer_range = max_weight - min_weight
    bytes_array = []
    index = 0
    for weight_val in floats_in:
        try:
            raw_int = int((weight_val - min_weight) * (max_val * layer_range))
            binary_val = bin(raw_int)[2:].zfill(16)
            if(int(binary_val[8:], 2) < 255):
                msb = int(binary_val[8:], 2)
                bytes_array.append(msb)
            else:
                bytes_array.append(layer_in.params[index])

            if(int(binary_val[:8], 2) < 255):
                lsb = int(binary_val[:8], 2)
                bytes_array.append(lsb)
            else:
                bytes_array.append(layer_in.params[index + 1])
        # If it didn't work, set back to original.
        except ValueError:
            bytes_array.append(layer_in.params[index])
            bytes_array.append(layer_in.params[index + 1])
        index += 2

    layer_in.params = bytes(bytes_array)


def add_noise_to_layer(noise_level, layer_in):
    try:
        floats = unpack_layer(layer_in)
        for ii in range(len(floats)):
            floats[ii] *= (1.0 + random.gauss(0, noise_level))
        repack_layer(floats, layer_in)
    except ZeroDivisionError:
        pass


with open(master_weights_file, 'rb') as f:
    net.ParseFromString(f.read())


loop_number = 0
for residual_layer in net.weights.residual:
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv1.weights")
    add_noise_to_layer(global_noise, residual_layer.conv1.weights)
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv1.biases")
    add_noise_to_layer(global_noise, residual_layer.conv1.biases)
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv1.bn_means")
    add_noise_to_layer(global_noise, residual_layer.conv1.bn_means)
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv1.bn_stddivs")
    add_noise_to_layer(global_noise, residual_layer.conv1.bn_stddivs)
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv1.bn_gammas")
    add_noise_to_layer(global_noise, residual_layer.conv1.bn_gammas)
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv1.bn_betas")
    add_noise_to_layer(global_noise, residual_layer.conv1.bn_betas)

    print("=================================")
    print("Block number: " + str(loop_number) + ": conv2.weights")
    add_noise_to_layer(global_noise, residual_layer.conv2.weights)
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv2.biases")
    add_noise_to_layer(global_noise, residual_layer.conv2.biases)
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv2.bn_means")
    add_noise_to_layer(global_noise, residual_layer.conv2.bn_means)
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv2.bn_stddivs")
    add_noise_to_layer(global_noise, residual_layer.conv2.bn_stddivs)
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv2.bn_gammas")
    add_noise_to_layer(global_noise, residual_layer.conv2.bn_gammas)
    print("=================================")
    print("Block number: " + str(loop_number) + ": conv2.bn_betas")
    add_noise_to_layer(global_noise, residual_layer.conv2.bn_betas)

    print("Block number: " + str(loop_number) + ": se.w1")
    add_noise_to_layer(global_noise, residual_layer.se.w1)
    print("=================================")
    print("Block number: " + str(loop_number) + ": se.b1")
    add_noise_to_layer(global_noise, residual_layer.se.b1)
    print("=================================")
    print("Block number: " + str(loop_number) + ": se.w2")
    add_noise_to_layer(global_noise, residual_layer.se.w2)
    print("=================================")
    print("Block number: " + str(loop_number) + ": se.b2")
    add_noise_to_layer(global_noise, residual_layer.se.b2)

    loop_number += 1


protobuf_string = net.SerializeToString()

with open(trainer_weights_file, "wb") as outfile:
    outfile.write(protobuf_string)


color = random.sample(['black', 'white'], 1)
print("your color: " + color[0])


os.system('python ./chess_gui.py ' + color[0])
