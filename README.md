# conway-test: test an interactive ncurses program
Bart Massey

This is a test harness for the interactive Game of Life
program `conway` that was presented in my CS 300 class as a
homework problem. The program uses the most excellent
[`pyte`](https://pypi.org/project/pyte/) Python package to
drive `conway` and check that it is rendering properly. The
code is derived from the `pyte`
[`nanoterm.py`](https://github.com/selectel/pyte/blob/master/examples/nanoterm.py)
example.

## Running

Right now, this harness executes only one test: it edits a
flasher onto the screen and then checks that it flashes
once. If you have a working `conway` you can say

    python3 conway-test.py ./conway

and you should see successful execution of all three states
of the flasher test.

## License and Acknowledgements

This work is made available under the "LGPL v3"
license. Please see the file `LICENSE` in this distribution
for license terms.

Thanks much to the authors of `pyte`, who did most of the
work here.
