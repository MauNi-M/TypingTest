import os.path
import random
import time
import tkinter as tk
from tkinter import font
from tkinter import ttk
import bs4
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

import json
import shutil

IMAGE_WIDTH = 300
WINDOW_WIDHT = 1200
WINDOW_HEIGHT = 600
MAIN_TEXT_WRAP = 800
TYPING_BOX_FONT = ("Helvetica 12")
BUTTON_FONT = ("Helvetica 16")
TIMER_FONT = ("Courier 35 bold")
WPM_FONT = ("Helvetica 40 bold")


class TypingTest(tk.Tk):
    classes = ("listicle-slide-hed-number", "listicle-slide-hed-text", "slide-image-wrap",
               "listicle-slide-dek")
    attributes = ("art_number", "art_title", "art_img_url", "art_content_wrapper")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # screen params
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # window configuration
        self.title("Mauni's typing test")
        self.geometry(
            f"{WINDOW_WIDHT}x{WINDOW_HEIGHT}"
            f"+{self.screen_width // 2 - WINDOW_WIDHT // 2}"
            f"+{self.screen_height // 2 - WINDOW_HEIGHT // 2}")


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=2)

        self.data = {}
        self.current_content = None
        self.skills_content = {}
        self.letter_counter = -1
        self.timer_counter = 0
        self.timer = None

        self.check_if_local_data()

        # mainframe CONTENT
        self.mainframe = tk.Frame(self)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=2)
        self.mainframe.grid(row=1, column=0, sticky=tk.N + tk.E + tk.W)

        # secondary frame, IMAGE
        self.secframe = tk.Frame(self, bd=5, bg="dark gray")
        self.secframe.grid(row=1, column=2, rowspan=2, sticky=tk.N)

        # tertiary frame INPUT
        self.tertframe = tk.Frame(self)
        self.tertframe.columnconfigure(0, weight=1)
        self.tertframe.columnconfigure(1, weight=1)
        self.tertframe.grid(row=2, column=0, sticky=tk.S)

        # ##### Initial layout ####

        # artcicle number
        self.article_number = tk.Label(self.mainframe)
        self.article_number.grid(sticky=tk.W + tk.E)

        # article title
        self.title_label = tk.Label(self.mainframe)
        self.title_label.grid(sticky=tk.W + tk.E)

        # article text
        self.main_text_label = tk.Label(self.mainframe, wraplength=MAIN_TEXT_WRAP)
        self.main_text_label.grid(sticky=tk.W + tk.E)

        # article image
        self.cover_image_label = ttk.Label(self.secframe)
        self.photo_image = None
        self.cover_image_label.grid(row=1, column=0, sticky=tk.N)

        # word counter
        self.word_counter_label = ttk.Label(self.secframe, background="dark gray")
        self.word_counter_label.grid(row=2, column=0, sticky=tk.S)

        # timer
        self.timer_label = ttk.Label(self.secframe, font=TIMER_FONT, foreground="white", background="dark gray")
        self.timer_label.grid(row=3, column=0, sticky=tk.S)

        # finished label
        self.finished_label = ttk.Label(self.secframe, font=TIMER_FONT, foreground="white")
        self.timer_label.grid(row=4, column=0, sticky=tk.S)

        # typing box
        self.typing_box = tk.Text(self.tertframe, height=7, font=TYPING_BOX_FONT, )
        self.typing_box.grid(row=1, column=0, sticky=tk.W + tk.E)

        # button frame
        self.btnframe = tk.Frame(self.tertframe, pady=10)
        self.btnframe.columnconfigure(0, weight=1)
        self.btnframe.columnconfigure(1, weight=1)
        self.btnframe.grid(row=2, column=0, sticky=tk.W + tk.E)

        # buttons
        self.start_button = tk.Button(self.btnframe,
                                      text="Start",
                                      command=self.typing_engine,
                                      width=20,
                                      font=BUTTON_FONT)
        self.next_button = tk.Button(self.btnframe,
                                     text="Next",
                                     command=self.next_article,
                                     width=20,
                                     font=BUTTON_FONT)
        self.start_button.grid(row=1, column=0, pady=10)
        self.next_button.grid(row=1, column=1, pady=10)

        self.get_contents()
        self.mainloop()

    def add_one_second(self):
        self.timer_label.config(text=self.timer_counter)
        self.timer_counter += 1
        self.timer = self.after(1000, self.add_one_second)

    def typing_engine(self):
        self.typing_box.focus()
        self.add_one_second()
        self.typing_box.bind("<Key>", self.check_typing)

    def check_typing(self, event):
        # compares the keys pressed against the text from the content
        letters_typed = self.typing_box.get("1.0", tk.END)
        total_letters = len(self.typing_box.get("1.0", tk.END))
        minutes = self.timer_counter / 60
        wpm = (total_letters/5)/minutes
        self.word_counter_label.config(text=f"WPM: {wpm:.2f}", font=WPM_FONT)
        # todo: add error checking to the function

        if event.keysym == "BackSpace":
            self.letter_counter -= 1
            if self.letter_counter < 0:
                self.letter_counter = -1

        elif event.keysym == "space" or event.char != "":
            self.letter_counter += 1
            self.check_letters(event.char, self.letter_counter)
            self.check_words()
        else:
            pass


    def im_finished(self, wpm):
        self.timer_counter = 0
        self.after_cancel(self.timer)
        self.finished_label.config(text=f"Final score: {wpm}", font=TIMER_FONT)

    def check_words(self):
        correct_words = self.current_content["art_content_wrapper"].split()
        typed_words = self.typing_box.get("1.0", tk.END)
        pass

    def check_letters(self, letter, index):
        content = self.current_content["art_content_wrapper"]
        # c stands for chars
        new_index = f"1.0+{index}c"
        self.typing_box.tag_add(f"letter_{index}", new_index)

        if letter == content[index]:
            self.typing_box.tag_config(f"letter_{index}", foreground="green", background="blue")
        else:
            self.typing_box.tag_config(f"letter_{index}", foreground="red", background="orange")
        self.update()
        print(self.typing_box.tag_cget(f"letter_{index}", "foreground"))

    def next_article(self):
        self.letter_counter = -1
        self.typing_box.delete("1.0", tk.END)
        self.timer_counter = 0
        self.get_contents()
        self.after_cancel(self.timer)

    def get_contents(self):
        content_data = random.choice(list(range(len(self.data) + 1)))
        try:
            self.current_content = self.data[str(content_data)]
        except KeyError:
            print(self.current_content)

        try:
            # getting data
            article_number = content_data
            title = self.current_content["art_title"]
            main_text = self.current_content["art_content_wrapper"]  # TODO: change main text name in dictionary
            image_url = self.current_content["art_img_url"]
            self.set_image(image_url=image_url, title=title)

            # setting data
            self.article_number.config(text=article_number, font=("Courier 50 bold"))
            self.title_label.config(text=title, font=("Times 25"))
            self.main_text_label.config(text=main_text, font=("Helvetica 12"))
            self.cover_image_label.config(image=self.photo_image)
        except TypeError:
            print(self.current_content)
            raise ValueError(f"something happened with current data # {content_data}")

    def set_image(self, image_url, title):
        image_path = "./images/" + title + ".png"
        try:
            with open(image_path, "r"):
                pass
        except FileNotFoundError:
            response = requests.get(image_url, stream=True)
            if response.status_code == 200:
                response.raw.decode_content = True
                with open(image_path, "wb") as f:
                    shutil.copyfileobj(response.raw, f)

        cover_image = Image.open(image_path)
        img_w, img_h = cover_image.size
        width = IMAGE_WIDTH
        ratio = img_w / img_h
        calculated_height = width / ratio
        cover_image = cover_image.resize((width, int(calculated_height)), Image.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(image=cover_image)
        return None

    def get_data_again(self, data):
        pass

    # todo create get data again function
    def check_if_local_data(self):
        try:
            with open("content_info.json", "r") as data_file:
                local_data = json.load(data_file)
                self.data = local_data
                print("Local data found")

        except FileNotFoundError:
            print("Getting from web")
            self._get_100_skills_you_should_know()

    def _relevant_content(self, item: bs4.element.Tag):
        image_attributes = ["srcset", "data-srcset"]
        article_number = int(str(item.select_one(f".{TypingTest.classes[0]}").string))
        article_title = str(item.select_one(f".{TypingTest.classes[1]}").string)
        try:
            article_image_url = item.select_one(f".{TypingTest.classes[2]}").picture.source.attrs[image_attributes[0]]
        except KeyError:
            try:
                article_image_url = item.select_one(f".{TypingTest.classes[2]}").picture.source.attrs[
                    image_attributes[1]]
            except KeyError:
                raise KeyError

        all_text = item.select(f".{TypingTest.classes[3]}")
        whole_paragraph = []
        for p_tag in all_text[0].find_all("p"):
            t = " ".join([str(child) for child in p_tag.stripped_strings])
            whole_paragraph.append(t)
        article_content_text = " ".join(whole_paragraph)
        self.skills_content[article_number] = {TypingTest.attributes[1]: article_title,
                                               TypingTest.attributes[2]: article_image_url,
                                               TypingTest.attributes[3]: article_content_text}

    def _get_100_skills_you_should_know(self):
        raw_data_path = "./data/data.txt"
        one_hundred_skills_url = "https://www.popularmechanics.com/home/g87/skills-everyone-should-know/"
        try:
            with open(raw_data_path, "r") as raw_data_file:
                raw_data = raw_data_file.read()
        except FileNotFoundError:
            r = requests.get(one_hundred_skills_url)
            raw_data = r.text
            with open(raw_data_path, "w") as raw_data_file:
                raw_data_file.write(raw_data)

        soup = BeautifulSoup(raw_data, "html5lib")

        content = soup.select("div[class='listicle-body-content']")
        first_child = content[0].div

        self._relevant_content(first_child)

        for sib in content[0].div.find_next_siblings():
            if "class" not in sib.attrs.keys() or "listicle-slide" not in sib.attrs["class"]:
                continue
            self._relevant_content(sib)
        try:
            with open("content_info.json", "x") as content_file:
                json.dump(self.skills_content, content_file)
        except FileExistsError:
            current_size = os.path.getsize("content_info.json")
            if current_size < 52767:
                print("data incomplete")
                self._get_100_skills_you_should_know()
        self.data = self.skills_content


if __name__ == "__main__":
    app = TypingTest()
