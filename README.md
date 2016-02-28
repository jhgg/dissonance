# HEAVY IN WIP.

# Dissonance

Dissonance is a simple, idiomatic python framework for building Discord bots of all shapes and sizes.

# Status
In it's infancy

# Installing Dissonance

You will need Python 2.7, 3.4 or 3.5 and setuptools. If you want, you can install Dissonance in a virtual environment.

Install dissonance (and his built in modules) with pip:

    $ pip install dissonance dissonance-modules

This will install dissonance, and his dependencies. It will also give you the `dissonance` command which can be used to create
an initial dissonance configuration, and run the bot. Let's create an instance of dissonance in the folder "mydissonance":

    $ dissonance init mydissonance

If you want to use dissonance with heroku, or just have your Dissonance instance inside of a git repository, the newly created
directory has everything you need: the configuration file, a few sample modules, a .gitignore file (so that you can safely add
everything to git).

    $ cd mydissonance
    $ git init
    $ git add .
    $ git commit -m "Dissonance's initial commit."

Next, open up the `config.py` file and add your Discord credentials to `dissonance_opts`.

Now you can run Dissonance by simply calling:

    $ dissonance run


# License

The MIT License (MIT)

Copyright (c) 2016 Jake Heinz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.