import glfw

_window_height = None
_keys = set()
_mouse_buttons = set()
_mouse_pos = (0, 0)
_typed_chars = []

def _key_callback(window, key, scancode, action, mods):
    if action == glfw.PRESS:
        _keys.add(key)
    elif action == glfw.RELEASE:
        _keys.discard(key)

def _char_callback(window, codepoint):
    global _typed_chars
    _typed_chars.append(chr(codepoint))

def get_typed_chars():
    global _typed_chars
    chars = _typed_chars
    _typed_chars = []
    return chars

def _mouse_button_callback(window, button, action, mods):
    if action == glfw.PRESS:
        _mouse_buttons.add(button)
    elif action == glfw.RELEASE:
        _mouse_buttons.discard(button)

def _cursor_pos_callback(window, xpos, ypos):
    global _mouse_pos
    _mouse_pos = (xpos, ypos)

def init_input_callbacks(window):
    global _window_height
    glfw.set_key_callback(window, _key_callback)
    glfw.set_mouse_button_callback(window, _mouse_button_callback)
    glfw.set_cursor_pos_callback(window, _cursor_pos_callback)
    glfw.set_char_callback(window, _char_callback)
    width, height = glfw.get_window_size(window)
    _window_height = height

def get_mouse_position():
    x, y = _mouse_pos
    return x, y

def is_key_pressed(key):
    return key in _keys

def is_mouse_button_pressed(button):
    return button in _mouse_buttons

def collide_pos(rect, pos):
    if rect.x+rect.width > pos[0] > rect.x and rect.y+rect.height > pos[1] > rect.y:
        return True
    return False

