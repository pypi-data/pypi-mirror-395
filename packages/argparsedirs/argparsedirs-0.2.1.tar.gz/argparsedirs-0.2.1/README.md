This is a very simple action for argparse that allows
you to specify a readable or a writeable directory as an `argparse` action.
I found it on StackOverflow years ago and used it since then,
unfortunately I cannot find the original source now.

I guess it would be best to have this added directly into `argparse` anyway.

### Usage
Just import and use as an action:

    import argparse
    import argparsedirs

    argparser = argparse.ArgumentParser()

    argparser.add_argument('indir', type=argparsedirs.ReadableDirType)
    argparser.add_argument('outdir', type=argparsedirs.WriteableDirType)

    args = argparser.parse_args()
