# Ollama GUI
The source code for a GUI application I wrote using python and its ollama library. This application has options to attach images to image processing models, and also to attach text files as context for non-image generating models. This distinction is important, as image models will not detect text files, and vice-versa.

The location where you place the EXE will determine where the logs and icon are stored.

This was made for personal use, but can be used as long as you have the correct python packages and ollama models installed. 
- window.py can be ran directly, but will create a directory on the E: drive under my name, you can configure this
- main.py is meant for exe building, and should be used with pyinstaller as it deals with the location of key files

I will work on more complex features and style as time goes on, but this is it in terms of raw functionality.
- While this is more of a 'works on my machine' type of project, I hope to make more general implementations of what I made here in the future