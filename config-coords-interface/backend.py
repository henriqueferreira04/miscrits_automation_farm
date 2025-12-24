import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import ast

app = Flask(__name__)
app.secret_key = 'miscrits_secret'  # Needed for flash messages

# Save config changes endpoint
@app.route('/save_config', methods=['POST'])
def save_config():
    data = request.get_json()
    changes = data.get('changes', [])
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config.py'))
    # Read all lines from config.py
    with open(config_path, 'r') as f:
        lines = f.readlines()
    # Build a dict of changes for quick lookup
    change_dict = {c['key']: tuple(map(int, c['coords'])) for c in changes}
    # Update lines in config.py
    for i, line in enumerate(lines):
        for key, coords in change_dict.items():
            if line.strip().startswith(f'{key} ='):
                lines[i] = f"{key} = {coords}\n"
    # Write back to config.py
    with open(config_path, 'w') as f:
        f.writelines(lines)
    return jsonify({'success': True})
import importlib.util
import mouse
import sys
import importlib

# Import find_coords.py as a module
find_coords_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../find_coords.py'))
spec_fc = importlib.util.spec_from_file_location("find_coords", find_coords_path)
find_coords = importlib.util.module_from_spec(spec_fc)
spec_fc.loader.exec_module(find_coords)





# Dynamically load config.py as a module
def load_config():
    spec = importlib.util.spec_from_file_location("config", os.path.abspath("../config.py"))
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return config

@app.route('/')
def index():
    config = load_config()
    descriptions = {
        'first_attack': 'The coordinate for the first attack option in a battle.',
        'second_attack': 'The coordinate for the second attack option in a battle.',
        'third_attack': 'The coordinate for the third attack option in a battle.',
        'forth_attack': 'The coordinate for the fourth attack option in a battle.',
        'move_right_attack_page_coord': 'Clicks to navigate to the next page of attacks.',
        'exit_fight_coord': 'The button to exit a completed or unsuccessful battle.',
        'confirm_fight_coord': 'Confirms the action to leave the current battle.',
        'close_fight_coord': 'Closes the battle summary window.',
        'capture_action_coord': 'The button to initiate capturing a Miscrit.',
        'okay_action_coord': 'A general "Okay" button for various pop-ups.',
        'keep_action_coord': 'The button to keep a captured Miscrit.',
        'release_action_coord': 'The button to release a captured Miscrit.',
        'confirm_action_coord': 'Confirms a chosen action, like keeping or releasing a Miscrit.',
        'heal_action_coord': 'The button to heal your Miscrits.',
        'get_clear_view_coord': 'A coordinate to click to dismiss UI elements that may be blocking the view.',
        'okay_success_coord': 'The "Okay" button on a success message pop-up.',
        'okay_rank_up_coord': 'The "Okay" button on a Miscrit rank-up notification.',
        'train_miscrit2_coord': 'Selects the second Miscrit in your team for training.',
        'train_miscrit3_coord': 'Selects the third Miscrit in your team for training.',
        'train_miscrit4_coord': 'Selects the fourth Miscrit in your team for training.',
        'train_now_coord': 'The button to start a training session.',
        'platinum_action_coord': 'A button related to platinum currency actions, likely for purchases or premium training.',
        'continue_action_coord': 'A general "Continue" button for progressing through dialogues or sequences.',
        'continue_plat_train_action_coord': 'The "Continue" button for platinum-based training.',
        'new_attack_continue_coord': 'The "Continue" button when a Miscrit learns a new attack.',
        'close_train_page_coord': 'Closes the training selection page.',
        'okay_evolve_miscrit_coord': 'The "Okay" button to confirm a Miscrit\'s evolution.'
    }
    variables = []
    for k in dir(config):
        v = getattr(config, k)
        if not k.startswith('__') and isinstance(v, tuple):
            variables.append({
                'key': k,
                'label': k.replace('_', ' ').title(),
                'coords': v,
                'image': f'/images/{k}.png',  # Assumes images are served from /images
                'description': descriptions.get(k, 'No description available.')
            })
    return render_template('config_interface.html', variables=variables)

@app.route('/move_click', methods=['POST'])
def move_click_route():
    var_name = request.form.get('var_name')
    if not var_name:
        return jsonify({'success': False, 'error': 'Missing variable name'})

    # Call find_coordinates interactively
    coords = find_coords.find_coordinates()

    if coords:
        return jsonify({'success': True, 'var_name': var_name, 'coords': coords})
    else:
        return jsonify({'success': False, 'error': 'Coordinate selection cancelled or failed.'})

# Serve images from the images/ directory
@app.route('/images/<path:filename>')
def images(filename):
    return app.send_static_file(f'../images/{filename}')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
