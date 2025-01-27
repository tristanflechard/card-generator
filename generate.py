import json
import hashlib
import colorsys

def generate_color_from_string(s):
    """Generate a pleasing color from a string."""
    hash_object = hashlib.md5(s.encode())
    hash_hex = hash_object.hexdigest()
    
    h = int(hash_hex[:2], 16) / 255.0
    s = 0.6
    v = 0.8
    
    rgb = colorsys.hsv_to_rgb(h, s, v)
    
    return '#{:02x}{:02x}{:02x}'.format(
        int(rgb[0] * 255),
        int(rgb[1] * 255),
        int(rgb[2] * 255)
    )

def get_options_html(card):
    """Generate HTML for options based on card type."""
    if card['type'] == 'QCM':
        return '\n'.join(f'<div class="qcm-option">{option}</div>' for option in card['options'])
    elif card['type'] == 'Vrai ou Faux':
        return '''
        <div class="vrai-faux-container">
            <div class="vf-option vrai-option">VRAI</div>
            <div class="vf-option faux-option">FAUX</div>
        </div>
        '''
    return ''

def create_card_html(card):
    """Create HTML for a single card."""
    options_html = get_options_html(card)
    
    return f'''
    <div class="card theme-{card['theme'].lower().replace(' ', '-')}">
        <div class="question">{card['question']}</div>
        <div class="options">
            {options_html}
        </div>
        <div class="answer-section">
            <div class="answer">Réponse: {card['answer']}</div>
            <div class="explanation">{card['explanation']}</div>
            <div class="sources">
                {', '.join([f"{source['name']} [{source['ref']}]" for source in card['sources']])}
            </div>
        </div>
    </div>
    '''

def generate_theme_styles(theme_colors):
    """Generate CSS for predefined theme colors."""
    styles = []
    for theme, color in theme_colors.items():
        theme_class = f'.theme-{theme.lower().replace(" ", "-")}'
        styles.append(f'''
        {theme_class} {{
            background-color: {color};
            color: #fff; /* Ensure text is readable */
        }}
        ''')
    return '\n'.join(styles)

def generate_cards_page(json_file, template_file, output_file):
    """Generate the complete HTML page with all cards."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Predefined themes and colors
    theme_colors = {
        "RGPD": "#7DA661",  # Green
        "qualite-annotation": "#D08C66",  # Orange-brown
        "droits-auteur": "#6689B2",  # Blue
        "impact_humain": "#D1B56C",  # Beige-gold
        "ethique": "#D27E38",  # Orange
        "big-data": "#4B944B",  # Dark green
    }


    # Generate theme styles
    theme_styles = generate_theme_styles(theme_colors)

    # Generate cards HTML
    cards_html = '\n'.join(create_card_html(card) for card in data['cards'])

    # Read the template
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace placeholders in the template
    final_html = template.replace('{theme_styles}', theme_styles).replace('{cards}', cards_html)
    
    # Write the final HTML to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)

def create_card_back_html(card, theme_colors, theme_logos):
    """Create HTML for the back of a single card."""
    theme_class = f"theme-{card['theme'].lower().replace(' ', '-')}"
    logo = theme_logos.get(card['theme'], "default-logo.png")  # Default logo if not found
    
    return f'''
    <div class="card {theme_class}">
        <div class="theme-name">{card['theme']}</div>
        <div class="theme-logo">
            <img src="{logo}" alt="Logo de {card['theme']}" />
        </div>
    </div>
    '''

def generate_card_backs_page(json_file, template_file, output_file):
    """Generate the HTML page for all card backs."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Predefined themes and colors
    theme_colors = {
        "RGPD": "#7DA661",  # Green
        "qualite-annotation": "#D08C66",  # Orange-brown
        "droits-auteur": "#6689B2",  # Blue
        "impact_humain": "#D1B56C",  # Beige-gold
        "ethique": "#D27E38",  # Orange
        "big-data": "#4B944B",  # Dark green
    }

    # Generate styles using theme_colors (dictionary)
    theme_styles = generate_theme_styles(theme_colors)
    
    # Predefined logos for themes
    theme_logos = {
        "RGPD": "logos/rgpd.png",
        "qualite-annotation": "logos/qualite-annotation.png",
        "droits-auteur": "logos/droits-auteur.png",
        "impact_humain": "logos/impact-humain.png",
        "ethique": "logos/ethique.png",
        "big-data": "logos/big-data.png",
    }

    # Generate HTML for all card backs
    cards_html = '\n'.join(
        create_card_back_html(card, theme_colors, theme_logos) for card in data['cards']
    )

    # Read the template file
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace placeholders in the template
    final_html = template.replace('{theme_styles}', theme_styles).replace('{cards}', cards_html)

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)


if __name__ == '__main__':
    generate_cards_page('cards.json', 'template.html', 'carte_front.html')
    generate_card_backs_page('cards.json', 'template_back.html', 'carte_back.html')