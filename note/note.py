"""
    Simple script for making quick timestamped notes.
"""
from sys import argv
from datetime import datetime

def main(args):
    
    if len(args) > 1:
        f = open("notes.log", 'a')

        del args[0]
        d = datetime.now()
        ds = datetime.strftime(d, "[%Y-%m-%d %H:%M:%S]")
        f.write(ds + " ")

        for word in args:
            f.write(word + ' ')
        
        f.write("\r\n")
        f.close
        
        print(ds + " Wrote stuff down")
    
    else:
        print("Give something to write down")

if __name__ == "__main__":
    main(argv)
