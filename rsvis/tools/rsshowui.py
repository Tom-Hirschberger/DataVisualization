# ===========================================================================
#   rsshowui.py -------------------------------------------------------------
# ===========================================================================

#   import ------------------------------------------------------------------
# ---------------------------------------------------------------------------
import rsvis.tools.index

from tkinter import *
from PIL import Image, ImageTk

#   class -------------------------------------------------------------------
# ---------------------------------------------------------------------------
class RSShowUI():

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def __init__(self, data, keys=dict()):
        self._data = data
        self.set_keys(keys)
        self._index = rsvis.tools.index.Index(len(self._data))
        self._index_spec = rsvis.tools.index.Index(len(self._data[0]))
        self.clear()
 
    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def clear(self):
        self._mouse_area = None
        self._mouse_point = None
   
    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def set_keys(self, keys):
        if isinstance(keys, dict):
            self._keys = keys
        else:
            self._keys = dict()

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def imshow(self, wait=False):
        self.window = Tk()
        self.window.title("HURRA")
        self.window.geometry("1000x850")
        self.initialize_window()
        self.window.mainloop()

    def initialize_window(self):
        self.scrollbar = Scrollbar(self.window, orient="vertical")
        self.lists = Listbox(self.window, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lists.yview)
        self.scrollbar.pack(side="left", fill="y")
        self.lists.pack(side="left", fill="y")
        for i in range(len(self._data)):
            self.lists.insert(END, i)

        
        self.set_img_from_index()
        self.img_width, self.img_height , _ = self._data[0][0].data.shape

        # https://solarianprogrammer.com/2018/04/20/python-opencv-show-image-tkinter-window/
        self.bg_img = ImageTk.PhotoImage(image = self.img)
        self.bg = Label(self.window, image=self.bg_img)

        self.bg.pack(side="right", fill="both", expand="y")
        self.bg.bind("<Configure>", self.resize_image)
        self.window.bind("<Key>", self.key_event)
        self.bg.bind("<Button-1>", self.mouse_button_pressed)
        self.bg.bind("<ButtonRelease-1>", self.mouse_button_released)
        # https://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
        self.lists.bind("<<ListboxSelect>>", self.listbox_event)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def resize_image(self,event):
        self.get_geometry(event.width, event.height)
        self.img = self.img_copy.resize((self.width, self.height))
        self.bg_img = ImageTk.PhotoImage(self.img)
        self.bg.configure(image = self.bg_img)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def get_geometry(self, width, height):
        if height < width:
            self.height = height
            self.width = int(float(self.img_width)/float(self.img_height)*float(self.height))
        else:
            self.width = width
            self.height = int(float(self.width)*float(self.img_height)/float(self.img_width))

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def get_img(self, index=None):
        index = self._index() if not index else index
        return self._data[index][self._index_spec()].data

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def get_img_from_spec(self, spec):
        if spec:
            index_spec = self._data[self._index()].index(spec)
            return self._data[self._index()][index_spec].data
        else:
            raise ValueError("Spec is none.")
        
    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def set_img_from_index(self, index=None, show=False):
        self.set_img(self.get_img(index=index), show=show)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def set_img(self, img, show=False):
        self.img = Image.fromarray(img)
        self.img_copy= self.img.copy()
        if show:
            self.show_image_in_window()

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def listbox_event(self,event):
        self._index(index=self.lists.curselection()[0])
        self.set_img_from_index(show=True)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def show_image_in_window(self):
        self.img = self.img_copy.resize((self.width, self.height))
        self.bg_img = ImageTk.PhotoImage(self.img)
        self.bg.configure(image = self.bg_img)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def get_key_event_name(self, arg):
        return 'key_' + str(arg)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def has_key(self, arg):
        return hasattr(self, self.get_key_event_name(arg)) or arg in self._keys 

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def key_event(self, event):
        # Get the method from 'self'. Default to a lambda.
        key_event_name = self.get_key_event_name(event.char)

        if hasattr(self, key_event_name):
            method = getattr(self, key_event_name, lambda: "Invalid key")
            # Call the method as we return it
            return method()
        elif key_event_name in self._keys:
            # param = [self.show(index=p) for p in self._keys[key_event_name]["param"]]
            return self._keys[key_event_name](self) 

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def key_d(self, **kwargs):
        self._index.next()
        self.set_img_from_index(show=True)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def key_a(self, **kwargs):
        self._index.last()
        self.set_img_from_index(show=True)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def key_w(self, **kwargs):
        self._index_spec.next()
        self.set_img_from_index(show=True)

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def key_s(self, **kwargs):
        self._index_spec.last()
        self.set_img_from_index(show=True)     

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def key_q(self, **kwargs):
        self.window.destroy()

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def mouse_button_pressed(self, event):
        self.bg.focus_set()
        self._mouse_area = [(event.x, event.y)]

    #   method --------------------------------------------------------------
    # -----------------------------------------------------------------------
    def mouse_button_released(self, event):
        self.bg.focus_set()
        self._mouse_area.append((event.x, event.y))
        self._mouse_point = (event.x, event.y)
        print("point: {}, area: {}".format(self._mouse_point, self._mouse_area))