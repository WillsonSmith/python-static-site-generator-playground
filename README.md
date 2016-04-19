## Python static site generator playgroup

The testing ground for a static site generator build in python. Just the basics right now.

As of now, if you run `python main.py`, it will:

1. take all the source files in `sources` folder
2. if those sources are `.md` or `.markdown` files, compile them
3. inject the source into the `templates/articles`
4. create a new file in the `output` folder with the generated page
