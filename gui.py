from dearpygui.core import *
from dearpygui.simple import *
import time

    
def save_settings(sender, data ):
    with window("ZippAuto Configuration"):
        input_value = get_value("Input")

        add_text( input_value + " Saved.", color=[232,163,33])
        time.sleep(1)
        hide_item( input_value + " Saved.")


def directory_picker(sender, data):
    select_directory_dialog(callback=apply_selected_directory)

def directory_picker2(sender, data):
    select_directory_dialog(callback=apply_selected_directory2)

def apply_selected_directory2(sender, data):
    log_debug(data)  # so we can see what is inside of data
    directory = data[0]
    folder = data[1]
    set_value("folder_path2", f"{directory}\\{folder}")
    f = open("backuplocation.txt", "w")
    f.write(f"{directory}\\{folder}")
    f.close()

def apply_selected_directory(sender, data):
    log_debug(data)  # so we can see what is inside of data
    directory = data[0]
    folder = data[1]
    set_value("folder_path", f"{directory}\\{folder}")
    f = open("zipplocation.txt", "w")
    f.write(f"{directory}\\{folder}")
    f.close()


def set_screen():
    set_main_window_size(1000,800)
    set_global_font_scale(1.20)
    set_theme("Dark")
    set_style_window_padding(30,30)

    with window("ZippAuto Configuration", width=980, height=750):
        set_window_pos("ZippAuto Configuration", 0, 0)
        add_text("Welcome to autozipp!")
        add_text("You need to specify which folder to zipp & upload to google drive and backup folder")
        add_spacing(count=12)
        
        add_button("Select Location To Zipp", callback=directory_picker)
        add_spacing(count=6)
        add_text("Selected : ")
        add_same_line()
        add_label_text("##folderpath", source="folder_path", color=[255, 0, 0])

        add_spacing(count=5)
        add_separator()
        add_spacing(count=5)

        add_button("Select Location Of Backup", callback=directory_picker2)
        add_spacing(count=6)
        add_text("Selected : ")
        add_same_line()
        add_label_text("##folderpath2", source="folder_path2", color=[255, 0, 0])

def main():
    set_screen()
    start_dearpygui()


