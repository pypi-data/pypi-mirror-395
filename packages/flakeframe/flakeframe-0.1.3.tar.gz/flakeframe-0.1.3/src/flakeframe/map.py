# Actual map rendering

import staticmaps # py-staticmaps
from img2unicode import FastGenericDualOptimizer, FastQuadDualOptimizer, HalfBlockDualOptimizer, Renderer
from PIL import Image, ImageDraw
from io import BytesIO, StringIO
import sys
import shutil
import time
import re
import select

def textsize(self, text, font=None): # fixes a bug in PIL lol
    bbox = self.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]
    
ImageDraw.ImageDraw.textsize = textsize

def get_terminal_pixels(): # doesn't work :(
    if not sys.stdout.isatty():
        return 1920, 1080
    
    old_settings = None
    fd = sys.stdin.fileno()
    if sys.platform != "win32":
        import termios
        old_settings = termios.tcgetattr(fd)
        
    try:
        if sys.platform != "win32":
            import tty
            tty.setraw(fd)
        
        sys.stdout.write("\x1b[14t")
        sys.stdout.flush()
        
        response = b""
        start = time.time()
        print("sent")
        
        while time.time() - start < 0.5: # this is broken
            print("reading")
            ready, _, _ = select.select([sys.stdin], [], [], 0.5)
            if ready:
                chunk = sys.stdin.buffer.read(32)
                if not chunk:
                    break
                response += chunk
                if b't' in response:
                    break
            else:
                break  # Timeout
        
        match = re.search(r'\x1b\[4;(\d+);(\d+)t', response)
        if match:
            height_px = int(match.group(1))
            width_px  = int(match.group(2))
            return width_px, height_px
    
    except Exception:
        pass
    finally:
        if old_settings and sys.platform != "win32":
            import termios
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old_settings)
    
    return 1920, 1080 # fallback

def render_map(lat, lon, zoom=14, debug = False, fast = False): # TODO: make dynamic/configurable later - Q/E keys?
    start_time = time.perf_counter()
    
    context = staticmaps.Context()
    context.set_tile_provider(staticmaps.tile_provider_ArcGISWorldImagery) # make configurable
    center = staticmaps.create_latlng(lat, lon)
    
    context.set_center(center)
    context.set_zoom(zoom)
    setup_time = time.perf_counter()
    
    cols, rows = shutil.get_terminal_size()
    max_w = cols - 2
    reserve_lines = 2
    available_lines = max(10, rows - reserve_lines)
    
    char_aspect = 2.1
    target_aspect = max_w / (available_lines * char_aspect)
    
    base_max = 380
    if target_aspect > 1:
        base_w = base_max
        base_h = max(100, int(base_max / target_aspect))
    else:
        base_h = base_max
        base_w = max(150, int(base_max / target_aspect))
    
    image = context.render_pillow(base_w, base_h)
    maprend_time = time.perf_counter()
    # term_w_px, term_h_px = get_terminal_pixels()
    
    final_w = max_w * 9
    final_h = available_lines * 19
    
    image = image.resize((final_w, final_h), resample = Image.LANCZOS)
    resize_time = time.perf_counter()

    columns, rows = shutil.get_terminal_size()
    max_w = columns - 2
    
    if fast:
        optimizer = FastQuadDualOptimizer()           # quad block chars
    else:
        optimizer = FastGenericDualOptimizer("block") # all block chars
    
    renderer = Renderer(default_optimizer = optimizer, max_w = max_w)
    setrend_time = time.perf_counter()
    
    out = StringIO()
    renderer.render_terminal(image, out, optimizer = optimizer)
    final_time = time.perf_counter()
    
    data = out.getvalue()
    lines = data.splitlines()
    data = "\n".join(lines[:-4]) # trim last 4 lines (provider watermark)
    
    # print("\x1b[H\x1b[2J")
    
    if debug:
        print("\x1b[H\x1b[2J")
        print(data)
        print("lat/long: ", lat, lon, "\nzoom: ", zoom)
        print("Setup:       ", setup_time - start_time)
        print("Map render:  ", maprend_time - setup_time)
        print("Resizing:    ", resize_time - maprend_time)
        print("Rend setup:  ", setrend_time - resize_time)
        print("img2unicode: ", final_time - setrend_time)
        print("Elapsed:     ", final_time - start_time)
    
    return data