#Author: Zachery Uporsky 9/23/22
#main listener for dream script
import argparse
import json
import logging
import math
import os
from random import random
import re
import subprocess
from concurrent.futures import thread
import sys
from threading import Thread

import zmq
import importlib.util


#TODO create Discord bot integration
#TODO HTTP socket communication
#TODO txt document solution
#TODO create alternate listening options



def main():
    print('Initializing dream listener, please be patient.')

    arg_parser = create_cmd_parser()
    opt = arg_parser.parse_args()
    
    try:
        gen = opt.generation_count
        outdir = opt.out_dir
        cfgloc = opt.cfg_location
        with open(cfgloc) as load_file: cfgdata = json.load(load_file)
        promptdir = opt.prompt_dir
        dbg = opt.debug
    except (Exception) as e:
        print(f'{e}. Aborting.')
        sys.exit(-1)
    
    projectid = generate_unique_genid(outdir) #maybe create an application for branching and whatnot
    projectdir = f'{outdir}/id{projectid}'
    outdir += f'/id{projectid}' 
    
    
    #TODO add generation for resuming 

    
    #create new iteration
    #continue with new iteration
    print('Initializing done.')
    

    #finally, start dream
    print(f'Using interface option {opt.interface}.')
    #!remember that if method of nesting dream_listen changes, then so might the PATH
    spec = importlib.util.spec_from_file_location('dreamv2', './scripts/dreamv2.py')
    dreamv2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dreamv2)

    match opt.interface:
        case 'http':
            outparser = create_output_parser()
            fully_constructed = False
            close = False
            while (not close):
                #create local context
                context = zmq.Context()
                socket = context.socket(zmq.REP)
                socket.bind("tcp://*:5555")    
                
                log = open('./dream_listener/log.txt')
                portlog = open('./dream_listener/port_log.txt')
                portlog.write('BEGIN OF PORT ACTIVITY')

                #monitoring = False 
                #if input('Actively monitor the port?: ') == 'Y':
                #    monitoring = True
                
                outdir = f'{outdir}/gen{gen}' 
                os.makedirs(outdir, exist_ok=True)

                #monitor option

                #!start daemon
                print(f'[generation{gen}]Starting dream on current gen in {outdir}...')
                dreamv2.http_main()
                print(f'[generation{gen}]Finished dream on current gen.')
                gen += 1
                
                print(f'[generation{gen}]Interpreting output command from{gen-1}.')
                dream_output_log = open(outdir + "/dream_log.txt")
                dream_output_string = dream_output_log.readline()
                interpreted_output = interpret_output(outparser, dream_output_string)
                
                #create next prompt
                #modify the next prompt location
                
                #modify the next prompt properties 


#generates a unique project id so that we don't have to
def generate_unique_genid(outdir): 
    dirlist = sorted(os.listdir(outdir), reverse=True)
    existing_name = next(
        (f for f in dirlist if re.match('id(\d+)', f)),
        'id00000',
    )
    basecount = int(existing_name.split('id',1)[0]) + 1
    return f'{basecount:06}'


def parse_output(parser, string=str):
    
    #strip input string
    #outputs/img-samples\000001.1957557850.png: "an arm made of synthetic muscles" -s100 -W1024 -H960 -C7.5 -Ak_lms -S1957557850
    input_args = string.split(': ') 
    to_parse = input_args[1].split(' -')[0:-1]
    parse_str = ''
    for partition in to_parse:
        parse_str += partition.strip("\"") + ' '
    return parser.parse_args(parse_str)


def interpret_output(parser, string=str):
    #create new_command -> writes command to file
    #strip input string
    #outputs/img-samples\000001.1957557850.png: "an arm made of synthetic muscles" -s100 -W1024 -H960 -C7.5 -Ak_lms -S1957557850

    input_args = string.split(': ') 
    dream_cmd = input_args[1].split(" -")
    
    path = input_args[0]
    prompt = dream_cmd[0][1:-1]
    
    #create a string that the Dream bot args would be recognizeable
    parse_str = ''
    for part in dream_cmd[1:-1]:
        parse_str += f'-{part} '
    options = parser.parse_args(parse_str)

    return [options, prompt, path]


def construct_new_prompt(args, parser, prompt_dir, cfg, gen, fully_constructed=False, mode=0):
    #0 -> constructive, 1 -> absolute
    #[iterations, steps, width, height, strength, variation, init_img, seed, {variations}]
    s = ['-n', '-s', '-W', '-H', '-f', '-v', '-I', '-S', '-V']
    prompt_str = ' '
    if gen == 1:
        prompt_str = open(prompt_dir).readline()
    elif not fully_constructed and mode==0:
        defaults = cfg['defaults']
        last_prompt = parser.parse(open(prompt_dir).readline())
        prompt_arr = [f'{args[1]} ']
        last_input = args[0]
        #use input for last prompt
        cout = 0
        for setting in defaults:
            if setting == None: prompt_arr.append(f'{s[cout]}{setting}')
            else:
                match s[cout]:
                    case '-n':
                        if last_prompt.iterations == args[0].iterations: prompt_arr.append( f'{s[cout]}{args[0].iterations} ')
                    case '-s':
                        prompt_arr.append(  f'{s[cout]}{args[0].steps} ')
                    case '-W':
                        prompt_arr.append(f'{s[cout]}{args[0].width} ')
                    case '-H':
                        prompt_arr.append(f'{s[cout]}{args[0].height} ')
                    case '-f':
                        prompt_arr.append(f'{s[cout]}{args[0].strength} ')
                    case '-v':
                        prompt_arr.append(f'{s[cout]}{args[0].variation} ')
            cout += 1
            
            #!add method of appending init_img and seed
        #allow us to say this command has been fully constructed
        fully_constructed = True
        prompt_str
        pass
    return prompt_str

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
        type=str,
        dest='interface',
        choices=INTERFACES,
        metavar='INTERFACE_TYPE',
        default='http',
        help='Specifies what method of communication the listener will use.'
    )
    parser.add_argument(
        '-cfg',
        type=str,
        dest='cfg_location',
        metavar='CONFIG_LOCATION',
        default='./cfg/cfg.json',
        help='File location to a JSON config file.'
    )
    parser.add_argument(
        '-dbg',
        action='store_true',
        dest='debug',
        default=False,
        help='Flag to turn on debugging.'
    )
    parser.add_argument(
        '--out_dir',
        type=str,
        dest='out_dir',
        default='./outputs/procedural',
        help='Specifies what location you would like to start the bot in'
    )
    parser.add_argument(
        '--generations',
        '-gen',
        type=int,
        dest='generation_count',
        default=1,
        help='Number of generations to do on modes AUTONOMOUS.'
    )
    parser.add_argument(
        '--prompt_location',
        '-prompt',
        '-p',
        type=str,
        dest='prompt_dir',
        default='./dream_listener/prompts/prompt.txt',
        help='Specifies the file location of the generative prompt'
    )
    return parser

def create_output_parser(): 
    parser = argparse.ArgumentParser(
        description="Parser for dream.py output logs"
    )
    
    parser.add_argument('prompt', dest='prompt')
    parser.add_argument(
    '-s', 
    '--steps', 
    type=int, 
    dest='steps',
    help='Number of steps')
    parser.add_argument(
        '-S',
        '--seed',
        type=int,
        dest='seed',
        help='Image seed; a +ve integer, or use -1 for the previous seed, -2 for the one before that, etc',
    )
    parser.add_argument(
        '-n',
        '--iterations',
        type=int,
        dest='iterations',
        default=1,
        help='Number of samplings to perform (slower, but will provide seeds for individual images)',
    )
    parser.add_argument(
        '-W', '--width', 
        type=int, 
        dest='width',
        help='Image width, multiple of 64'
    )
    parser.add_argument(
        '-H', '--height', 
        type=int, 
        dest='height',
        help='Image height, multiple of 64'
    )
    parser.add_argument(
        '-C',
        '--cfg_scale',
        default=7.5,
        type=float,
        help='Classifier free guidance (CFG) scale - higher numbers cause generator to "try" harder.',
    )
    parser.add_argument(
        '-g', '--grid', action='store_true', help='generate a grid'
    )
    parser.add_argument(
        '--outdir',
        '-o',
        type=str,
        dest='out_dir',
        default=None,
        help='Directory to save generated images and a log of prompts and seeds',
    )
    parser.add_argument(
        '--seamless',
        action='store_true',
        help='Change the model to seamless tiling (circular) mode',
    )
    parser.add_argument(
        '-i',
        '--individual',
        action='store_true',
        help='Generate individual files (default)',
    )
    parser.add_argument(
        '-I',
        '--init_img',
        type=str,
        dest='init_img',
        help='Path to input image for img2img mode (supersedes width and height)',
    )
    parser.add_argument(
        '-M',
        '--init_mask',
        type=str,
        help='Path to input mask for inpainting mode (supersedes width and height)',
    )
    parser.add_argument(
        '-T',
        '-fit',
        '--fit',
        action='store_true',
        help='If specified, will resize the input image to fit within the dimensions of width x height (512x512 default)',
    )
    parser.add_argument(
        '-f',
        '--strength',
        default=0.75,
        type=float,
        dest='strength',
        help='Strength for noising/unnoising. 0.0 preserves image exactly, 1.0 replaces it completely',
    )
    parser.add_argument(
        '-G',
        '--gfpgan_strength',
        default=0,
        type=float,
        help='The strength at which to apply the GFPGAN model to the result, in order to improve faces.',
    )
    parser.add_argument(
        '-U',
        '--upscale',
        nargs='+',
        default=None,
        type=float,
        help='Scale factor (2, 4) for upscaling followed by upscaling strength (0-1.0). If strength not specified, defaults to 0.75'
    )
    parser.add_argument(
        '-save_orig',
        '--save_original',
        action='store_true',
        help='Save original. Use it when upscaling to save both versions.',
    )
    # variants is going to be superseded by a generalized "prompt-morph" function
    #    parser.add_argument('-v','--variants',type=int,help="in img2img mode, the first generated image will get passed back to img2img to generate the requested number of variants")
    parser.add_argument(
        '-x',
        '--skip_normalize',
        action='store_true',
        help='Skip subprompt weight normalization',
    )
    parser.add_argument(
        '-A',
        '-m',
        '--sampler',
        dest='sampler_name',
        default=None,
        type=str,
        choices=SAMPLER_CHOICES,
        metavar='SAMPLER_NAME',
        help=f'Switch to a different sampler. Supported samplers: {", ".join(SAMPLER_CHOICES)}',
    )
    parser.add_argument(
        '-t',
        '--log_tokenization',
        action='store_true',
        help='shows how the prompt is split into tokens'
    )
    parser.add_argument(
        '-v',
        '--variation_amount',
        default=0.0,
        type=float,
        dest='variation',
        help='If > 0, generates variations on the initial seed instead of random seeds per iteration. Must be between 0 and 1. Higher values will be more different.'
    )
    parser.add_argument(
        '-V',
        '--with_variations',
        default=None,
        type=str,
        dest='variation_list',
        help='list of variations to apply, in the format `seed:weight,seed:weight,...'
    )
    return parser


if __name__ == '__main__':
    main()



#for cmd sake
#pew workon stable-diffusion