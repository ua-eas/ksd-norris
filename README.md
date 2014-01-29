# osg-norris

Norris issue workflow statistical chainsaw.

## Mike's really quick notes on development setup.

Tried to go complicated (see below), things blew up, got tired.

Went with 64-bit Cygwin, with the Cygwin-supplied system Python package, chucked
the whole Pyenv/Virtualenv thing out the window.  So:

*   Installed 64-bit Cygwin under 64-bit Windows 7.

*   Added some developer-ish packages: openssh, git-*, wget, curl, autoconf,
    automake, libtool, make, gcc-*, flex, bison, pkg-config.

*   Added libuuid-devel to resolve a problem with Pip installation on
    64-bit Cygwin, see:
    
        https://github.com/kennethreitz/requests/issues/1547
    
*   Installed Pip, then used it to install the JIRA Python API:

        $ wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py 
        $ python get-pip.py
        $ pip install jira-python
        
*   Cloned from GitHub:

		[ TBD ]
		
*   Changed to root directory of repository, and set PYTHONPATH:

		$ export PYTHONPATH=./src
		
    Then set NRSCONFIG to the location of the config file:
    
        $ export NRSCONFIG=./config/norris.json



## (THIS DIDN'T WORK, PRESERVED FOR LATER REVIEW) Mike's quick notes on development setup.

Using Eclipse Kepler running on 64-bit Windows 7.

Norris is python-based, so eventually I gave up trying to do UNIXy things from inside Eclipse,
and tried to install 64-bit Cygwin.  Then I banged my head against a wall for about a day 
trying to get Python to compile under 64-bit Cygwin (google "cygwin python libffi" if you 
want the sad story) before I gave up and switched back to 32-bit Cygwin.

I added a bunch of developer-ish packages, plus some stuff to support Python compilation:

    openssh, openssl[-devel], git, git-*, wget, curl, autoconf, automake,
    make, gcc-*, zlib[-devel], ncurses, libncurses[-devel], readline, libffi[-devel],
    sqlite3, libsqlite3[-devel], pkg-config

Note that I also got some weird and intermittent fork()-related errors.  The recommended
solution was to temporarily disable on-access scanning in Sophos Endpoint Security, and
then run the Cygwin "rebaseall" procedure, as detailed here:

    http://cygwin.com/faq-nochunks.html#faq.using.bloda
    http://cygwin.wikia.com/wiki/Rebaseall

[ That didn't help either, so I gave up.  I include the intended procedure below, 
  marking the the point of the compile failure, for popular edification: ]

So after all of that, here's the actual CLI procedure for building up a pyenv/virtualenv 
environment inside Cygwin on Windows 7 (whew):

    $ git clone git://github.com/yyuu/pyenv.git ~/.pyenv
	$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
	$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
	$ echo 'eval "$(pyenv init -)"' >> ~/.bash_profile

[ restart terminal to pick up changes ]

	$ pyenv install 2.7.6
	$ pyenv local 2.7.6
	$ git clone git://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
	$ pyenv virtualenv 2.7.5 norris
	$ pyenv shell norris
	$ pip install jira-python


