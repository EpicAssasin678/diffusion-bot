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
    arg_parser = create_cmd_parser()
    opt = arg_parser.parse_args()
    
    #create our listener
    thread1 = Thread(name="dream_listener", target=watch_dream())

    import scripts.dreamv2 as dreamv2
    #http option 

    #create local context
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")    
    #create listening context on dreamv2

    #create new iteration
    #continue with new iteration
    print('Welcome to Dream Listener, this is currently running')
    



def watch_dream(debug=False):
    #listen for the object 
    if debug: print('Running watch_dream()')
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
    parser.add_argument(
        'dbg',
        dest='debug',
        metavar='DEBUG',
        action='store_true',
        default=False
    )
    return parser

def create_argv_parser():
    pass





if __name__ == '__main__':
    main()
