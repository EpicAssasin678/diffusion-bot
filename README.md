# diffusion-bot
Discord bot for remote use of stable-diffusion with python scripts for automating and refining prompting and img2img generation




## Installation 
---
This repository serves for both the modification and standalone application of this concept. For corresponding versions, please check below.


### Modification instillation:

For those with lstein/stabel-diffusion fork:
    
1) Copy the dreamv2.py into ./stable-diffusion/scripts
2) Copy the dream_listener folder into the root of stable-diffusion
    * Note: Path should look something like <i>~/stable-diffusion/dream_listener</i>
3) Once you have started your environment for stable diffusion, install required dependencies for the script. This instillation assumes pew, conda environments is a use at your own risk environment for running this.

Dependencies:


    pip install pyzmq

    pip install -U py-cord


## Usage
---
To invoke the bot within pew environment, call dream_listener:
    
    python ./dream_listener/dream_listen.py -n2



