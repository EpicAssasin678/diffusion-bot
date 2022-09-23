#Author: Zachery Uporsky 9/23/22
#main listener for dream script
import argparse
from concurrent.futures import thread
from threading import Thread 
import zmq


#TODO create Discord bot integration
#TODO HTTP socket communication
#TODO txt document solution

def main():
    arg_parser = create_argv_parser()
    opt = arg_parser.parse_args()
    #create our listener
    thread1 = Thread(name="dream_listener", target=watch_dream())

    #create local context
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    



def watch_dream():
    #listen for the object 
    pass


#parser for command call 

def create_argv_parser():
    parser = argparse.ArgumentParser(
        description="""Create a daemon for stable diffusion.
        Use --discord_bot to launch discord bot alongside dream.py
        Use --log for logging input of the daemon
        By default new thread will launch without notifying a discord bot.
        
        """
    ) 
    parser.add_argument("discord"
    )
    return parser




if __name__ == '__main__':
    main()
    