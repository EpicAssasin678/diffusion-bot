## Documentation
***
Ideas for application sturcture. Overview of calls.
    
    dream_listener.py -> calls dreamv2.py -> posts to discord bot 
    dream_listener.py -> dreamv2.py -> 


Main problems for discord bot:


⪢ Creating a new script through dream_listener

⪢ How to sync between bot and active task

⪢ Creating a non-multithreaded synced process (because of python)

⪢ Wrapping stable_diffusion in a process/thread wrapper in the first place 

⪢ 

***
### Intended Use 
Call dream_listener with kwargs --interface_type \<type> -cfg \<file_location> -m \<mode> 

Args:

* --interface_type = the type of communication to use with dreamv2.py, type = discord, http, txt, thread
* -cfg = the location of an alternative config file
* -m = mode for running dream (NOTE: not all modes are possible with all interface_type options)

Modes



***
Main loop 
1 - use the dream_listener as a complete wrapper, only interacting with the dream script by using dream.py 
2 - use the dream_listener in conjunction with dreamv2.py as a better method for communicating, mostly with the http and discord bot options 
3 - 

Notes
- possible to use use cfg.json to also preload stdin for dreamv2's main_loop 




    