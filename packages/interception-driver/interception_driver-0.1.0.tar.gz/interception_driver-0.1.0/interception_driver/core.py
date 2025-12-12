import ctypes
import os
import time
from .structures import Stroke
from .constants import *

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

class Interception:
    def __init__(self):
        
        """
        Initializes the Interception client, loads the DLL, and creates a context.
        """

        base_path = os.path.dirname(os.path.abspath(__file__))
        dll_path = os.path.join(base_path , "interception.dll")

        try:
            self._dll = ctypes.cdll.LoadLibrary(dll_path)
        except OSError:
            raise FileNotFoundError(f"DLL Bulunamadi: {dll_path}")
        
        self._dll.interception_create_context.restype = ctypes.c_void_p
        self._dll.interception_destroy_context.argtypes = [ctypes.c_void_p]
        self._dll.interception_send.argtypes = [ctypes.c_void_p , ctypes.c_int , ctypes.c_void_p, ctypes.c_uint]

        # Create context

        self._context = self._dll.interception_create_context()

        if not self._context:
            raise Exception("Interception context could not be created. Check if the driver is installed!")
        
    def destroy(self):
        
        """
        Destroys the Interception context.
        Should be called when the Interception object is no longer needed.
        """

        if self._context:
           self._dll.interception_destroy_context(self._context)
           self._context = None

    def _send_mouse(self, x, y, state, flags):
        """
        Sends a normalized mouse input event via the low-level API.
        """
        stroke = Stroke()
        nx, ny = self._normalize(x, y)
        
        stroke.mouse.x = nx
        stroke.mouse.y = ny
        stroke.mouse.state = state
        stroke.mouse.flags = flags

        for i in range(11, 21):
            self._dll.interception_send(self._context, i, ctypes.byref(stroke), 1)

    def move_to(self, x, y):
        flags = MOUSE_MOVE_ABSOLUTE | MOUSE_VIRTUAL_DESKTOP
        self._send_mouse(x, y, 0, flags)

    def click(self, x, y):

        """
        Performs a left mouse click at the specified absolute screen coordinates (x, y).
        """

        self.move_to(x, y)
        flags = MOUSE_MOVE_ABSOLUTE | MOUSE_VIRTUAL_DESKTOP
        
        self._send_mouse(x, y, MOUSE_LEFT_BUTTON_DOWN, flags)
        time.sleep(0.05) 
        self._send_mouse(x, y, MOUSE_LEFT_BUTTON_UP, flags)

    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.destroy()
    
    
    def __del__(self):
        self.destroy()

    def _normalize(self, x, y):

        """
        Normalizes absolute pixel coordinates (x, y) to a 0-65535 range
        based on the Windows Virtual Screen size, suitable for hardware mouse input.
        """
        
        SM_XVIRTUALSCREEN, SM_YVIRTUALSCREEN = 76, 77
        SM_CXVIRTUALSCREEN, SM_CYVIRTUALSCREEN = 78, 79
        
        user32 = ctypes.windll.user32
        v_x = user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
        v_y = user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
        v_width = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN)
        v_height = user32.GetSystemMetrics(SM_CYVIRTUALSCREEN)

        print(f"{v_x} , {v_y} , {v_width} , {v_height}")

        norm_x = int(((x - v_x) * 65535) / v_width) + 1
        norm_y = int(((y - v_y) * 65535) / v_height) + 1
        return norm_x, norm_y