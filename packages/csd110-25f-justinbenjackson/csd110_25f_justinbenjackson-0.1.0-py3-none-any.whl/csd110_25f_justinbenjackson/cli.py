## This is where we do most of the work.
import sys
import os

def main():
     # " 'I only have a brain part time' - Justin Mcintomney" 
    invalid_msg: str = "INVALID - Type --help to see instructions."
    help_msg: str = "1st arg is the shape, 2nd is the character for blank space, 3rd is the character for filled in space, 4th is folder destination (MUST EXIST)... \n   Valid shapes: 'square' 'triangle' 'triangle_l' 'triangle_r' 'circle' 'heart' 'hourglass' \n    Example call: poetry run justinbenjackson square - ! C:/Users/Bob/Downloads"
    args = sys.argv 

    if "--help" in args:
        print(help_msg)
    elif len(args) != 5:
        print(invalid_msg)
    else:
        valid = True

        output_str: str

        shape_input: str = args[1]
        white_space: str = args[2]
        black_space: str = args[3]
        fourth_arg: str = args[4]
        
        if len(white_space) != 1 or len(black_space) != 1:
            valid = False

        if not os.path.exists(fourth_arg):
            valid = False

        if shape_input == "square":
            output_str = get_square(white_space, black_space) 
        elif shape_input == "triangle_l":
            output_str = get_triangle_l(white_space, black_space)
        elif shape_input == "triangle_r":
            output_str = get_triangle_r(white_space, black_space)
        elif shape_input == "triangle":
            output_str = get_triangle(white_space, black_space)
        elif shape_input == "hourglass":
            output_str = get_hourglass(white_space, black_space)
        elif shape_input == "circle":
            output_str = get_circle(white_space, black_space)
        elif shape_input == "heart":
            output_str = get_heart(white_space, black_space)
        else:
            valid = False

        if valid:
            r = 1 # Dec
            file_name: str = f"output_{shape_input}{r}.txt"
            output_path: str = fourth_arg + os.sep + file_name 
            while(True):
                if os.path.exists(fourth_arg + os.sep + file_name):
                    r += 1
                    file_name = f"output_{shape_input}{r}.txt"
                    output_path = fourth_arg + os.sep + file_name 
                else:
                    break
            file = open(output_path, "a")
            with open(output_path, "w") as file:
                file.write(output_str)
            file.close()
        else:
            print(invalid_msg)


def get_square(w: str, b: str): 
    """ w means white space, b means black space. black space is foreground, white space is background. """
    s: str = ""
    s += f"{b} {b} {b} {b} {b} {b} {b}\n"
    s += f"{b} {w} {w} {w} {w} {w} {b}\n"
    s += f"{b} {w} {w} {w} {w} {w} {b}\n"
    s += f"{b} {w} {w} {w} {w} {w} {b}\n"
    s += f"{b} {w} {w} {w} {w} {w} {b}\n"
    s += f"{b} {w} {w} {w} {w} {w} {b}\n"
    s += f"{b} {b} {b} {b} {b} {b} {b}\n"
    return s

def get_triangle_l(w: str, b: str): 
    """ w means white space, b means black space. black space is foreground, white space is background. """
    s: str = ""
    s += f"{b} {w} {w} {w} {w} {w} {w}\n" 
    s += f"{b} {b} {w} {w} {w} {w} {w}\n"
    s += f"{b} {w} {b} {w} {w} {w} {w}\n"
    s += f"{b} {w} {w} {b} {w} {w} {w}\n"
    s += f"{b} {w} {w} {w} {b} {w} {w}\n"
    s += f"{b} {w} {w} {w} {w} {b} {w}\n"
    s += f"{b} {b} {b} {b} {b} {b} {b}\n"
    return s

def get_triangle_r(w: str, b: str): 
    """ w means white space, b means black space. black space is foreground, white space is background. """
    s: str = ""
    s += f"{w} {w} {w} {w} {w} {w} {b}\n" 
    s += f"{w} {w} {w} {w} {w} {b} {b}\n"
    s += f"{w} {w} {w} {w} {b} {w} {b}\n"
    s += f"{w} {w} {w} {b} {w} {w} {b}\n"
    s += f"{w} {w} {b} {w} {w} {w} {b}\n"
    s += f"{w} {b} {w} {w} {w} {w} {b}\n"
    s += f"{b} {b} {b} {b} {b} {b} {b}\n"
    return s

def get_triangle(w: str, b: str): 
    """ w means white space, b means black space. black space is foreground, white space is background. """
    s: str = ""
    s += f"{w} {w} {w} {w} {w} {w} {w}\n" 
    s += f"{w} {w} {w} {w} {w} {w} {w}\n"
    s += f"{w} {w} {w} {w} {w} {w} {w}\n"
    s += f"{w} {w} {w} {b} {w} {w} {w}\n"
    s += f"{w} {w} {b} {w} {b} {w} {w}\n"
    s += f"{w} {b} {w} {w} {w} {b} {w}\n"
    s += f"{b} {b} {b} {b} {b} {b} {b}\n"
    return s

def get_hourglass(w: str, b: str): 
    """ w means white space, b means black space. black space is foreground, white space is background. """
    s: str = ""
    s += f"{b} {b} {b} {b} {b} {b} {b}\n" 
    s += f"{w} {b} {w} {w} {w} {b} {w}\n"
    s += f"{w} {w} {b} {w} {b} {w} {w}\n"
    s += f"{w} {w} {w} {b} {w} {w} {w}\n"
    s += f"{w} {w} {b} {w} {b} {w} {w}\n"
    s += f"{w} {b} {w} {w} {w} {b} {w}\n"
    s += f"{b} {b} {b} {b} {b} {b} {b}\n"
    return s

def get_circle(w: str, b: str): 
    """ w means white space, b means black space. black space is foreground, white space is background. """
    s: str = ""
    s += f"{w} {w} {b} {b} {b} {w} {w}\n"
    s += f"{w} {b} {w} {w} {w} {b} {w}\n"
    s += f"{b} {w} {w} {w} {w} {w} {b}\n"
    s += f"{b} {w} {w} {w} {w} {w} {b}\n"
    s += f"{b} {w} {w} {w} {w} {w} {b}\n"
    s += f"{w} {b} {w} {w} {w} {b} {w}\n"
    s += f"{w} {w} {b} {b} {b} {w} {w}\n"
    return s

def get_heart(w: str, b: str): 
    """ w means white space, b means black space. black space is foreground, white space is background. """
    s: str = ""
    s += f"{w} {b} {w} {w} {w} {b} {w}\n"
    s += f"{b} {w} {b} {w} {b} {w} {b}\n"
    s += f"{b} {w} {w} {b} {w} {w} {b}\n"
    s += f"{b} {w} {w} {w} {w} {w} {b}\n"
    s += f"{w} {b} {w} {w} {w} {b} {w}\n"
    s += f"{w} {w} {b} {w} {b} {w} {w}\n"
    s += f"{w} {w} {w} {b} {w} {w} {w}\n"
    return s
