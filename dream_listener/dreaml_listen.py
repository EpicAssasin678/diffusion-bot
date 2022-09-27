#Author: Zachery Uporsky 9/23/22
#main listener for dream script
import argparse
from concurrent.futures import thread
from threading import Thread 
import zmq
import scripts.dreamv2 as dreamv2



#TODO create Discord bot integration
#TODO HTTP socket communication
#TODO txt document solution

def main():
    arg_parser = create_argv_parser()
    opt = arg_parser.parse_args()
    #create our listener
    thread1 = Thread(name="dream_listener", target=watch_dream())



    #http option 

    #create local context
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")    
    #create listening context on dreamv2

    #create new iteration
    #continue with new iteration

    



def watch_dream():
    #listen for the object 
    pass


#parser for command call 

INTERFACES = [
    'discord',
    'http',
    'text'
]

def create_cmd_parser():
    parser = argparse.ArgumentParser(
        description="""Create a daemon for stable diffusion.
        Use --discord_bot to launch discord bot alongside dream.py
        Use --log for logging input of the daemon
        By default new thread will launch without notifying a discord bot.

        """
    ) 
    parser.add_argument(
        '--interface_type',
        '-i',
        dest='interface',
        choices=INTERFACES,
        metavar='INTERFACE_TYPE',
        default='http'
    )
    parser.add_argument(
        '-cfg',
        dest=cfg_location,
        metavar='CONFIG_LOCATION',
        default='./cfg/cfg.json'
    )
    return parser





if __name__ == '__main__':
    main()
