from modules.frame_selector import select_frame
from modules.light_color_simulator import simulate_lighting
from modules.lens_renderer import render_lens_effect
from modules.camera_movement import suggest_camera_movement
from modules.texture_generator import generate_visual_texture
from utils.script_parser import parse_script

def main():
    script_text = parse_script("sample_script.txt")
    
    print("[1] Selecting Frame...")
    frame = select_frame(script_text)
    
    print("[2] Simulating Light and Color...")
    lighting, color = simulate_lighting(script_text)
    
    print("[3] Rendering Lens Effects...")
    lens = render_lens_effect(script_text)
    
    print("[4] Suggesting Camera Movement...")
    movement = suggest_camera_movement(script_text)
    
    print("[5] Generating Visual Texture...")
    texture = generate_visual_texture(script_text)
    
    visual_world = {
        "Frame": frame,
        "Lighting": lighting,
        "Color": color,
        "Lens": lens,
        "Movement": movement,
        "Texture": texture,
    }

    print("\n--- Visual World Constructed ---")
    for key, value in visual_world.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
