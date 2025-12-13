ultimateultimateguitar
======================

This is a CLI client for ultimate-guitar.com.

[Donations](https://liberapay.com/ltworf)

![Screenshot of a terminal showing usage](img/screenshot.png)

Since the website is completely non-functional with js disabled, I wrote this
to access its content anyway.

It has the nice extra that it can transpose.

[Demonstration video](https://youtu.be/Spm1IIaYo8Q)

Usage
=====

It can be called with the URL of a song on the command line.

```bash
# prints the chords
ultimateultimateguitar URL

# prints the same song but transposed
ultimateultimateguitar --transpose 2 URL
```

In alternative, calling it without parameters will enter the interactive mode, where you can search for songs directly.

In interactive mode you want to first `search` for a title or author, and then type `load N`, where N is the index of the wanted result.


Install it
==========

```
apt install ultimateultimateguitar
```

If it's not available, you can use

```
pip install ultimateultimateguitar
```



