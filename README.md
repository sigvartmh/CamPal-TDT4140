# CamPal-TDT4140
Repository for TDT4140 course where we are making a video tracking bot

# Installation



##OSX:
###Install openCV3

```
brew tap homebrew/science
brew install opencv3 --with-contrib --with-python3 --HEAD
```

###Fetch packages
```
pip install -r requirements.txt
```

###Make sure python search openCV directory
PYTHONPATH should point to where the openCV installation is. It's also set in the script in this line

```python
import sys
sys.path.append('/usr/local/Cellar/opencv3/3.2.0/lib/python2.7/site-packages')
```
modify the PATH to suit your environment
