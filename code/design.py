import json, keyboard, webbrowser, run_inputs
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from threading import Thread
from pyautogui import position
from pynput.keyboard import Listener


if __name__ == "__main__":
    bg_col = "#2f2f2f"
    frame_col = "#383838"
    text_col = "#a0a0ad"
    action_frame_col = "#534C5A"

    start_keybind = "f5"
    stop_keybind = "f5"
    add_keybind = "enter"

    i__ = 0
    has_booted = False
    has_cursor_movement = True
    is_done = False
    on_cooldown = False
    previous_x, previous_y, previous_key = 0, 0, "left_click"


    def refresh_settings():
        global bg_col, frame_col, text_col, action_frame_col, has_booted, stop_keybind, start_keybind, add_keybind
        settings_file = open("settings.txt", "r")
        settings = settings_file.readlines()

        for line in settings:
            try:
                setting, value = line.replace("\n", "").split('=')
            except:
                continue
            if setting == "bg_color":
                bg_col = value
            elif setting == "frame_color":
                frame_col = value
            elif setting == "text_color":
                text_col = value
            elif setting == "action_frame_color":
                action_frame_col = value
            elif setting == "start_keybind":
                start_keybind = value
            elif setting == "stop_keybind":
                stop_keybind = value
            elif setting == "add_keybind":
                add_keybind = value
            elif setting == "open_with_new_save" and value.lower() == "true" and not has_booted:
                cur_save = open("current_save.aki", "w")
                cur_save.write("")
                cur_save.close()
                has_booted = True
        settings_file.close()
    refresh_settings()


    def clear_file(file):
        f = open(file, "w")
        f.write("")
        f.close()
        refresh_settings()
        refresh()


    def read_line(line):
        line = json.loads(line)
        return line["time"], line["x"], line["y"], line["move"], line["type"], line["key"]


    def run_script():
        global on_cooldown, start_button, stop_button, is_done
        if on_cooldown:
            return
        cur_save = open("current_save.aki", "r")

        Thread(target=run_inputs.start, args=(cur_save.readlines(), start_loop_type.get(),
                                              start_loop_count.get(), stop_script)).start()

        cur_save.close()
        start_button.configure(state="disabled")
        stop_button.configure(state="normal")
        on_cooldown = True


    def stop_script():
        global on_cooldown, start_button, stop_button
        run_inputs.count__ += 1
        on_cooldown = False
        start_button.configure(state="normal")
        stop_button.configure(state="disabled")


    def on_press(key):
        global start_button, stop_button
        key = str(key).replace("'", "").replace("Key.", "")

        if key == start_keybind.lower() and start_button['state'] == NORMAL:
            run_script()
        elif key == stop_keybind.lower() and stop_button['state'] == NORMAL:
            stop_script()

    def root_key_press(key):
        global add_keybind
        to_press_key = add_keybind.lower()

        if key.char == to_press_key and not on_cooldown:
            add_new_action(cursor_movement_type, is_key_to_press_none, press_type, False, 0)
            return

        key = str(key.keysym).lower().split("_")[0]
        key = key.replace("return", "enter").replace("control", "ctrl").replace("return", "enter")

        if key == to_press_key and not on_cooldown:
            add_new_action(cursor_movement_type, is_key_to_press_none, press_type, False, 0)
            return



    listener = Listener(on_press=on_press)
    listener.start()


    def entry_settings(text, character_limit, is_numeric):
        text.set(text.get().replace(" ", ""))
        if len(text.get()) > character_limit:
            text.set(text.get()[0:character_limit])
        if is_numeric and len(text.get()) >= 1:
            try:
                int(text.get())
            except ValueError:
                text.set(text.get()[0:len(text.get()) - 1])
                entry_settings(text, character_limit, is_numeric)


    # HEADER AND ROOT START ---------------------------------------------------vvvvvvvvvvvvvvvvvvvvvvvvvv
    #                                                                                   vvvvvvvvvvvvvvvvv
    #                                                                                              vvvvvv
    root = Tk()
    root.iconbitmap("icon.ico")
    root.title("Auto key inputer")
    root.geometry("510x500")
    root.resizable(0, 0)
    root.configure(background=bg_col)
    root.attributes('-topmost', True)

    cursor_movement_type = StringVar()
    press_type = StringVar()
    start_loop_type = IntVar()
    start_loop_count = StringVar()
    start_loop_count.set("3")
    time_value = StringVar()
    pos_x_value = StringVar()
    pos_y_value = StringVar()
    key_combination_entry_value = StringVar()
    is_key_to_press_none = IntVar()

    start_loop_count.trace("w", lambda *args: entry_settings(start_loop_count, 7, True))
    time_value.trace("w", lambda *args: entry_settings(time_value, 6, True))
    pos_x_value.trace("w", lambda *args: entry_settings(pos_x_value, 4, True))
    pos_y_value.trace("w", lambda *args: entry_settings(pos_y_value, 4, True))
    key_combination_entry_value.trace("w", lambda *args: entry_settings(key_combination_entry_value, 17, False))


    def browse_files():
        file_name = filedialog.askopenfilename(initialdir="..\\saves",
                                              title="Select a file",
                                              filetypes=((".aki files", "*.aki"), ("All files", "*.*")))
        try:
            f2 = open(file_name, "r")
            f = open("current_save.aki", "w")
            f.write(f2.read())
            f.close()
            f2.close()
            refresh()
        except:
            print("no file to browse!")


    def save_fie():
        files = [('.aki files', '*.aki'),
                 ('All files', '*.*')]
        try:
            file_name = filedialog.asksaveasfile(filetypes=files, defaultextension=files).name
            f2 = open("current_save.aki", "r")
            f = open(file_name, "w")
            f.write(f2.read())
            f.close()
            f2.close()
        except:
            print("no file to browse!")


    menubar = Menu(root)
    file_menu = Menu(menubar, tearoff=0, activeborderwidth=2)
    file_menu.add_command(label="New", command=lambda: clear_file("current_save.aki"))
    file_menu.add_command(label="Open", command=browse_files)
    file_menu.add_command(label="Save as...       ", command=save_fie)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label="GitHub page", command=lambda: webbrowser.open('https://github.com/02-t/AutoKeyInputer'))
    # help_menu.add_command(label="YouTube tutorial") TODO: ADD YOUTUBE LINK IN THE FUTURE
    help_menu.add_separator()
    help_menu.add_command(label="Key inputs you can use", command=lambda: webbrowser.open('scancodes.txt'))
    menubar.add_cascade(label="Help", menu=help_menu)

    credits_menu = Menu(menubar, tearoff=0)
    credits_menu.add_command(label="made with love by 02_t")
    credits_menu.add_separator()
    credits_menu.add_command(label="Github", command=lambda: webbrowser.open('https://github.com/02-t'))
    menubar.add_cascade(label="Credits", menu=credits_menu)

    root.config(menu=menubar)

    Label(root, text="made by 02_t", font=("Arial", 16), bg=bg_col, fg="#a0a0ad").pack()
    Label(root,
          text="Simulate mouse/keyboard inputs while being afk. Press '+' to start!",
          font=("Calibri", 12), bg=bg_col, fg="#6e6e7d").pack()


    #                                                                                              ^^^^^^
    #                                                                                 ^^^^^^^^^^^^^^^^^^^
    # HEADER AND ROOT FINISH -------------------------------------------------^^^^^^^^^^^^^^^^^^^^^^^^^^^


    # SCROLL FRAME START ------------------------------------------------------vvvvvvvvvvvvvvvvvvvvvvvvvv
    #                                                                                   vvvvvvvvvvvvvvvvv
    #                                                                                              vvvvvv


    def scroll_scale(event):
        canvas.configure(scrollregion=canvas.bbox("all"), height="312", width="460")


    frame_bg = Frame(root, bg=frame_col, height="312", width="460")
    frame_bg.place(x=15, y=55)
    canvas = Canvas(frame_bg, bg=frame_col, height="312", width="460", bd=0, highlightthickness=0, relief='ridge')
    canvas.place(x=15, y=55)
    frame = Frame(canvas, bg=frame_col)
    scrollbar = Scrollbar(frame_bg, orient="vertical", command=canvas.yview, bg=frame_col, elementborderwidth=0)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left")
    canvas.create_window((0, 0), window=frame, anchor='nw')
    frame.bind("<Configure>", scroll_scale)


    def delete_value(i):
        global on_cooldown
        if on_cooldown:
            messagebox.showerror("Can't delete entry", "Please disable the script or stop editing and try again!")
            return
        with open('current_save.aki', 'r') as fr:
            lines = fr.readlines()
            ptr = 1
            fr.close()

            with open('current_save.aki', 'w') as fw:
                for line in lines:
                    if ptr != i + 1:
                        fw.write(line)
                    ptr += 1
                fw.close()

        refresh()


    def add_value(line):
        global i__
        a = i__
        time_, x_, y_, move_, type_, key_ = read_line(line)

        if move_ == "none":
            x_ = "--"
            y_ = "--"

        if key_ == "none":
            type_ = "---"

        frame_ = Frame(frame, width=460, height=44, bg=frame_col)
        frame_.pack()
        Label(frame_, text="wait " + str(time_) + " ms", bg=frame_col, fg=text_col).place(x=2, y=12)
        Label(frame_, text="x: " + str(x_) + "\ny: " + str(y_), bg=frame_col, fg=text_col, justify=LEFT).place(x=110,
                                                                                                               y=4)
        Label(frame_, text="cursor movement:\n" + move_, bg=frame_col, fg=text_col).place(x=274, y=4)
        Label(frame_, text=key_ + "\n" + type_, bg=frame_col, fg=text_col, width=17).place(x=150, y=4)
        Button(frame_, text="X", font=("Terminal", 8), bg="#FA6161", activebackground="#FA6161",
               command=lambda: delete_value(a)).place(x=440, y=15)
        Button(frame_, text="edit", font=("Terminal", 10), bg="#77DAEF", activebackground="#77DAEF",
               command=lambda: add_new_action(cursor_movement_type, is_key_to_press_none, press_type, True, a)).place(
            x=386, y=12)
        Frame(frame_, width=430, height=1, bg=text_col).place(x=15, y=43)


    def refresh():
        global frame
        for widget in frame.winfo_children():
            widget.destroy()
        f = open("current_save.aki", "r")
        lines = f.readlines()
        global i__
        i__ = 0

        for line in lines:
            add_value(line)
            i__ = i__ + 1

        f.close()
        if i__ > 0:
            start_button.configure(state=NORMAL)
        else:
            start_button.configure(state=DISABLED)


    #                                                                                              ^^^^^^
    #                                                                                 ^^^^^^^^^^^^^^^^^^^
    # SCROLL FRAME FINISH ----------------------------------------------------^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # FOOTER FRAME START ------------------------------------------------------vvvvvvvvvvvvvvvvvvvvvvvvvv
    #                                                                                   vvvvvvvvvvvvvvvvv
    #                                                                                              vvvvvv
    def put_on_top():
        if on_top.get() == 1:
            root.attributes('-topmost', True)
        else:
            root.attributes('-topmost', False)


    def add_new_action(cursor_movement_type, is_key_to_press_none, press_type, is_in_edit_mode, pos_):
        global previous_x, previous_y, on_cooldown, has_cursor_movement
        global time_value, pos_x_value, pos_y_value, key_combination_entry_value
        has_cursor_movement = True
        previous_x = 0
        previous_y = 0
        previous_key = "left_click"
        if on_cooldown:
            messagebox.showerror("Can't delete entry", "Please disable the script or stop editing and try again!")
            return
        on_cooldown = True
        new_frame = Frame(root, height=100, width=400, bg=action_frame_col)
        new_frame.place(x=55, y=200)

        def cursor_movement_radio_click(is_none):
            global has_cursor_movement, previous_x, previous_y
            if is_none and has_cursor_movement:
                has_cursor_movement = False
                previous_x = pos_x_value.get()
                previous_y = pos_y_value.get()
                pos_x_value.set(0)
                pos_y_value.set(0)
                x_entry.configure(state=DISABLED)
                y_entry.configure(state=DISABLED)
            elif not is_none:
                has_cursor_movement = True
                x_entry.configure(state=NORMAL)
                y_entry.configure(state=NORMAL)
                pos_x_value.set(previous_x)
                pos_y_value.set(previous_y)

        def key_change_radio_click(is_none):
            global previous_key
            if is_none:
                previous_key = key_combination_entry_value.get()
                key_combination_entry_value.set("none")
                key_entry.configure(state=DISABLED)
                click_radio.configure(state=DISABLED)
                hold_radio.configure(state=DISABLED)
                release_radio.configure(state=DISABLED)
            else:
                key_entry.configure(state=NORMAL)
                key_combination_entry_value.set(previous_key)
                click_radio.configure(state=NORMAL)
                hold_radio.configure(state=NORMAL)
                release_radio.configure(state=NORMAL)

        def close_window():
            global on_cooldown
            new_frame.pack_forget()
            new_frame.destroy()
            on_cooldown = False

        def add_action(is_in_edit_mode, pos_):
            if not is_in_edit_mode:
                f = open("current_save.aki", "a")
                f.write('{ "time":' + time_value.get().strip() + ', "x":' + pos_x_value.get().strip() + ', "y":' +
                        pos_y_value.get().strip() + ', "move":"' + cursor_movement_type.get().strip() + '", "type":"' +
                        press_type.get().strip() + '", "key":"' + key_combination_entry_value.get().strip() + '"}\n')
                f.close()
                refresh()
                close_window()
            else:
                count, count2 = 0, 0
                str_ = ["", ""]
                f = open("current_save.aki", "r")
                for line in f:
                    if count == pos_:
                        count2 += 1
                        count += 1
                        continue
                    str_[count2] = str_[count2] + line
                    count += 1
                f.close()

                f = open("current_save.aki", "w")
                f.write(str_[0])
                f.write('{ "time":' + time_value.get().strip() + ', "x":' + pos_x_value.get().strip() + ', "y":' +
                        pos_y_value.get().strip() + ', "move":"' + cursor_movement_type.get().strip() + '", "type":"' +
                        press_type.get().strip() + '", "key":"' + key_combination_entry_value.get().strip() + '"}\n')
                f.write(str_[1])
                f.close()
                refresh()
                close_window()

        close_button = Button(new_frame, text="cancel", command=close_window, bg="#FA6161", activebackground="#FA6161")
        close_button.place(x=5, y=70)

        add_button_text = "add"
        add_button_bg_col = "#7FDB97"
        add_button_pos_x = 365
        time_pos_x = 0
        if is_in_edit_mode:
            add_button_text = "update"
            add_button_bg_col = "#77DAEF"
            add_button_pos_x = 349
            time_pos_x = -3

        add_button = Button(new_frame, text=add_button_text, command=lambda: add_action(is_in_edit_mode, pos_),
                            bg=add_button_bg_col, activebackground="#7FDB97")
        add_button.place(x=add_button_pos_x, y=70)

        time_value.set("1000")
        Entry(new_frame, bd=2, width=7, textvariable=time_value).place(x=300 + time_pos_x, y=73)
        Label(new_frame, text="time (ms)", bg=action_frame_col).place(x=240 + time_pos_x, y=73)

        pos_x_value.set("0")
        x_entry = Entry(new_frame, bd=2, width=5, textvariable=pos_x_value)
        x_entry.place(x=25, y=7)
        Label(new_frame, text="x:", bg=action_frame_col).place(x=5, y=7)

        pos_y_value.set("0")
        y_entry = Entry(new_frame, bd=2, width=5, textvariable=pos_y_value)
        y_entry.place(x=25, y=39)
        Label(new_frame, text="y:", bg=action_frame_col).place(x=5, y=39)

        Label(new_frame, text="Press the SpaceBar to get the\ncoordinates of your mouse's position!",
              bg=action_frame_col, fg=text_col, font=("Arial", 8)).place(x=53, y=68)

        cursor_movement_type.set("teleport")
        Radiobutton(new_frame, text="Teleport", variable=cursor_movement_type, bg=action_frame_col,
                    activebackground=action_frame_col,
                    value="teleport", command=lambda: cursor_movement_radio_click(False)).place(x=310, y=0)
        Radiobutton(new_frame, text="None", variable=cursor_movement_type, bg=action_frame_col,
                    activebackground=action_frame_col,
                    value="none", command=lambda: cursor_movement_radio_click(True)).place(x=310, y=40)
        Radiobutton(new_frame, text="Move/Drag", variable=cursor_movement_type, bg=action_frame_col,
                    activebackground=action_frame_col,
                    value="move", command=lambda: cursor_movement_radio_click(False)).place(x=310, y=20)

        is_key_to_press_none.set(0)
        Radiobutton(new_frame, variable=is_key_to_press_none, value=0, bg=action_frame_col,
                    activebackground=action_frame_col, command=lambda: key_change_radio_click(False)).place(x=156, y=11)
        Radiobutton(new_frame, text="None", variable=is_key_to_press_none, value=1, bg=action_frame_col,
                    activebackground=action_frame_col, command=lambda: key_change_radio_click(True)).place(x=156, y=36)

        key_combination_entry_value.set("left_click")
        key_entry = Entry(new_frame, bd=2, width=18, textvariable=key_combination_entry_value)
        key_entry.place(x=180, y=11)

        press_type.set("click")
        click_radio = Radiobutton(new_frame, text="Click", variable=press_type, value="click", bg=action_frame_col,
                                  activebackground=action_frame_col)
        click_radio.place(x=80, y=0)
        hold_radio = Radiobutton(new_frame, text="Hold", variable=press_type, value="hold", bg=action_frame_col,
                                 activebackground=action_frame_col)
        hold_radio.place(x=80, y=20)
        release_radio = Radiobutton(new_frame, text="Release", variable=press_type, value="release",
                                    bg=action_frame_col,
                                    activebackground=action_frame_col)
        release_radio.place(x=80, y=40)

        if is_in_edit_mode:
            f = open("current_save.aki", 'r')
            lines = f.readlines()

            time_, x_, y_, move_, type_, key_ = read_line(lines[pos_])
            f.close()

            key_combination_entry_value.set(key_)
            time_value.set(time_)
            pos_x_value.set(x_)
            pos_y_value.set(y_)
            cursor_movement_type.set(move_)
            press_type.set(type_)

            if key_ == "none":
                is_key_to_press_none.set(1)
                key_change_radio_click(True)
            if move_ == "none":
                cursor_movement_radio_click(True)


        def clicked_space():
            global previous_x, previous_y, cursor_movement_type
            if cursor_movement_type.get() == "none":
                return

            try:
                pos_x_value.set(str(position().x))
                pos_y_value.set(str(position().y))
                previous_x = pos_x_value.get()
                previous_y = pos_y_value.get()
            except:
                return

        keyboard.on_press_key("space", lambda _: clicked_space())


    footer = Frame(root, bg=frame_col, height="80", width="480")
    footer.place(x=10, y=388)

    on_top = IntVar()  # <------- "always on top" button
    on_top.set(1)
    always_on_top_check = Checkbutton(footer, text='always on top', font=("Arial", 14), bg=frame_col, fg=text_col,
                                      variable=on_top, onvalue=1, offvalue=0, command=put_on_top,
                                      activeforeground=text_col,activebackground=frame_col)
    always_on_top_check.place(x=0, y=0)

    add_button = Button(footer, text='+', bg=bg_col, font=("Arial", 18), width=3, fg="#FFFFFF",
                        activebackground=frame_col, activeforeground="#FFFFFF",
                        command=lambda: add_new_action(cursor_movement_type, is_key_to_press_none, press_type, False,
                                                       0))
    add_button.place(x=410, y=15)

    start_button = Button(footer, text='START', bg=bg_col, font=("Arial", 12), width=6, fg="#FFFFFF", state=DISABLED,
                          activebackground=frame_col, activeforeground="#FFFFFF", command=run_script)
    start_button.place(x=325, y=6)

    stop_button = Button(footer, text='STOP', bg=bg_col, font=("Arial", 12), width=6, fg="#FFFFFF", state=DISABLED,
                         activebackground=frame_col, activeforeground="#FFFFFF", command=stop_script)
    stop_button.place(x=325, y=43)

    Radiobutton(footer, text="Run once", bg=frame_col, font=("Arial", 11), fg=text_col, variable=start_loop_type,
                value=0, activebackground=frame_col, activeforeground=text_col).place(x=155, y=0)

    Radiobutton(footer, text="Run infinitely", bg=frame_col, font=("Arial", 11), fg=text_col, variable=start_loop_type,
                value=1, activebackground=frame_col, activeforeground=text_col).place(x=155, y=26)

    Radiobutton(footer, text="Run                 times", bg=frame_col, font=("Arial", 11), fg=text_col,
                variable=start_loop_type, value=2, activebackground=frame_col, activeforeground=text_col).place(x=155,
                                                                                                                y=52)
    repeat_times_entry = Entry(footer, font=("Arial", 10), width=8, textvariable=start_loop_count)
    repeat_times_entry.place(x=211, y=55)

    change_keybind = Button(footer, text="Edit\nkeybinds", bg="#8EEE9C", activebackground="#8EEE9C",
                            font=("Arial", 9), command=lambda: webbrowser.open("settings.txt"))
    change_keybind.place(x=10, y=32)


    def refresh_keybinds():
        global start_keybind, stop_keybind, add_keybind
        start_keybind1, stop_keybind1, add_keybind1 = start_keybind, stop_keybind, add_keybind
        bool_ = False
        refresh_settings()

        if start_keybind1 != start_keybind or stop_keybind1 != stop_keybind or add_keybind1 != add_keybind:
            bool_ = True

        if bool_:
            messagebox.showinfo(title="Changes detected!", message="Changes detected!\n\nThe keybinds are:\nStart - " +
                                start_keybind + "\nStop - " + stop_keybind + "\nAdd - "+add_keybind)
        else:
            messagebox.showerror(title="No Changes detected!", message="No changes detected! Maybe you forgot to save" +
                                " the file?\n\nThe keybinds are:\nStart - " +
                                start_keybind + "\nStop - " + stop_keybind + "\nAdd - "+add_keybind)


    refresh_keybind = Button(footer, text="Refresh\nkeybinds", bg="#BB90D6", activebackground="#BB90D6",
                             font=("Arial", 9), command=refresh_keybinds)
    refresh_keybind.place(x=79, y=32)
    #                                                                                              ^^^^^^
    #                                                                                 ^^^^^^^^^^^^^^^^^^^
    # FOOTER FRAME FINISH ----------------------------------------------------^^^^^^^^^^^^^^^^^^^^^^^^^^^

    refresh()
    root.bind('<KeyPress>', root_key_press)
    root.mainloop()
