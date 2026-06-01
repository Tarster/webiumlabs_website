import re
import requests
import subprocess

def get_desec_info():
    try:
        # Use sudo to read the config
        result = subprocess.run(['sudo', 'cat', '/etc/ddclient.conf'], capture_output=True, text=True, check=True)
        config = result.stdout
        
        token_match = re.search(r'password=(.+)', config)
        domain_match = re.search(r'tarster.com,(.+)', config)
        
        token = token_match.group(1).strip() if token_match else None
        # In the specific config we saw: tarster.com,webiumlabs.com
        domains = ["webiumlabs.com"] # Defaulting to the target domain
        
        return token, domains
    except Exception as e:
        print(f"Error reading ddclient config: {e}")
        return None, None

def update_desec(token, domain):
    if not token or not domain:
        print("Missing token or domain.")
        return

    # deSEC API endpoint for updating IPv4
    # Note: ddclient already does this, but the user specifically asked for a script.
    url = f"https://update.dedyn.io/nic/update?hostname={domain}"
    headers = {
        'Authorization': f'Token {token}'
    }
    
    try:
        # deSEC uses dyndns2 protocol which can be updated via simple GET or Basic Auth
        # But for 'Token' auth we use the deSEC specific API if needed, 
        # however the update.dedyn.io usually expects Basic Auth with the token as password.
        
        response = requests.get(url, auth=(domain, token))
        print(f"Update for {domain}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error updating deSEC: {e}")

if __name__ == "__main__":
    token, domains = get_desec_info()
    if token:
        for dom in domains:
            update_desec(token, dom)
