# Sync soundfiles with my mp3 player

August 2021

Python script to sync the files on my mp3 player (the "target") which is essentially an external storage with the files on my computer (the "source"). New or updated files on source are copied to target, files that have been removed from source are deleted from target. - And yes, I have heard about Spotify, but no, I am no friend of streaming, haha.

All that is needed to run this script, is **Python 3.6** or higher and the rich package (pip install rich) for some nice console output. Then navigate to the main project folder in a CLI and start the process with `python sync`. Source and target paths and the directories you want to sync can be specified in the config.yaml file.
