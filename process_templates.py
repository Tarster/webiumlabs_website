import os
import re

def process_html():
    template_dir = r"webium_template\automatix.framer.website"
    output_dir = r"templates\jinja2"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    # --- Process index.html -> home.html ---
    index_path = os.path.join(template_dir, "index.html")
    home_path = os.path.join(output_dir, "home.html")
    
    print(f"Processing {index_path} -> {home_path}")
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Perform asset and link replacements
    html = html.replace("../framerusercontent.com/images/", "/static/images/")
    html = html.replace("href=\"contact.html\"", "href=\"/contact/\"")
    html = html.replace("href=\"index.html\"", "href=\"/\"")
    html = html.replace("index.html#", "/#")
    
    # Save processed home.html
    with open(home_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("home.html written successfully")
    
    # --- Process contact.html -> contact.html ---
    contact_path = os.path.join(template_dir, "contact.html")
    contact_out_path = os.path.join(output_dir, "contact.html")
    
    print(f"Processing {contact_path} -> {contact_out_path}")
    with open(contact_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    # Perform asset and link replacements
    html = html.replace("../framerusercontent.com/images/", "/static/images/")
    html = html.replace("href=\"contact.html\"", "href=\"/contact/\"")
    html = html.replace("href=\"index.html\"", "href=\"/\"")
    html = html.replace("index.html#", "/#")
    
    # Fix the textarea name attribute from duplicate "Name" to "message"
    # The textarea looks like: name="Name" and placeholder="Tell us more about your project"
    # Let's use regex or string replace to find it and change name="Name" to name="message"
    # Let's check what the string is:
    # <textarea type=None name=Name id=None placeholder='Tell us more about your project' ...>
    # Since Framer generates it, we can replace placeholder='Tell us more about your project' with name change.
    # Actually, let's search for name="Name" inside textarea
    # We can replace: name="Name" placeholder="Tell us more about your project" with name="message" placeholder="..."
    # In our contact detail parser, the attributes printed:
    # {'required': None, 'name': 'Name', 'placeholder': 'Tell us more about your project', 'class': 'framer-form-input'}
    # This means the attribute was name="Name"
    
    # Let's replace the name attribute of the textarea:
    html = html.replace('name="Name" placeholder="Tell us more about your project"', 'name="message" placeholder="Tell us more about your project"')
    html = html.replace('name=\'Name\' placeholder=\'Tell us more about your project\'', 'name=\'message\' placeholder=\'Tell us more about your project\'')
    # Just in case, let's also do a search and replace for any textarea with name="Name" and replace it:
    # We can find <textarea ... name="Name" ...> and replace name="Name" with name="message"
    html = re.sub(r'(<textarea[^>]*\bname=)"Name"([^>]*>)', r'\1"message"\2', html)
    html = re.sub(r'(<textarea[^>]*\bname=)\'Name\'([^>]*>)', r'\1\'message\'\2', html)
    
    # Also inject the custom AJAX Javascript handler at the end of the file, just before </body>
    form_handler_script = '<script src="/static/js/form_handler.js" defer></script>'
    if "</body>" in html:
        html = html.replace("</body>", f"{form_handler_script}</body>")
    else:
        html += form_handler_script
        
    with open(contact_out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("contact.html written successfully")

if __name__ == "__main__":
    process_html()
