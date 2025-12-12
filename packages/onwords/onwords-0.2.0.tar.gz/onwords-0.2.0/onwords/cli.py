"""
Onwords CLI - Command line interface for gate control

Commands:
    onwords-config  - Configure API key
    onwords-list    - List all products
    onwords-control - Control a gate device
"""

import argparse
import sys
from . import __version__
from .api import configure, get_products, load_config, OnwordsAPI


# ANSI colors for terminal output
class Colors:
    RED = '\033[91m'
    WHITE = '\033[97m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


def print_banner():
    """Print Onwords branded banner."""
    print(f"""
{Colors.BOLD}{Colors.RED}On{Colors.WHITE}words{Colors.RESET} - Gate Control
Version {__version__}
    """)


def cli_config():
    """CLI command: onwords-config"""
    parser = argparse.ArgumentParser(
        prog='onwords-config',
        description=f'{Colors.RED}On{Colors.WHITE}words{Colors.RESET} - Configure your API key'
    )
    parser.add_argument('--api-key', '-k', required=True, help='Your Onwords API key')
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    print_banner()
    
    try:
        configure(args.api_key)
        print(f"{Colors.GREEN}✓ API key configured successfully!{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.RESET}")
        sys.exit(1)


def cli_list():
    """CLI command: onwords-list"""
    parser = argparse.ArgumentParser(
        prog='onwords-list',
        description=f'{Colors.RED}On{Colors.WHITE}words{Colors.RESET} - List all your products'
    )
    parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    # Check if API key is configured
    config = load_config()
    if not config.get("api_key"):
        if not args.json:
            print_banner()
        print(f"{Colors.RED}✗ Error: API key not configured{Colors.RESET}")
        print(f"\nGet your API key:")
        print(f"  1. Visit {Colors.CYAN}https://ostapi.onwords.in{Colors.RESET}")
        print(f"  2. Click 'Get API Key' and login")
        print(f"  3. Select devices and generate key")
        print(f"\nThen run: {Colors.BOLD}onwords-config --api-key YOUR_KEY{Colors.RESET}")
        sys.exit(1)
    
    try:
        product_ids = get_products()
        
        if args.json:
            import json
            print(json.dumps({"product_ids": product_ids}, indent=2))
            return
        
        print_banner()
        
        if not product_ids:
            print(f"{Colors.YELLOW}No products found for your API key.{Colors.RESET}")
            print(f"\nGenerate a new API key with devices at:")
            print(f"  {Colors.CYAN}https://ostapi.onwords.in{Colors.RESET}")
            return
        
        print(f"{Colors.BOLD}Your Products ({len(product_ids)}):{Colors.RESET}\n")
        
        for i, product_id in enumerate(product_ids, 1):
            print(f"  {Colors.BLUE}{i}.{Colors.RESET} {Colors.BOLD}{product_id}{Colors.RESET}")
        
        print(f"\n{Colors.DIM}Control with: onwords-control <product_id> <action>{Colors.RESET}")
            
    except ValueError as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.RESET}")
        sys.exit(1)
    except ConnectionError as e:
        print(f"{Colors.RED}✗ Connection Error: {e}{Colors.RESET}")
        sys.exit(1)


def cli_control():
    """CLI command: onwords-control"""
    # Valid actions by gate type
    sliding_actions = ['open', 'close', 'pause', 'partial_open']
    arm_single_actions = ['open_single_gate', 'close_single_gate', 'pause_single_gate']
    arm_double_actions = ['open_double_gate', 'close_double_gate', 'pause_double_gate']
    all_actions = sliding_actions + arm_single_actions + arm_double_actions
    
    parser = argparse.ArgumentParser(
        prog='onwords-control',
        description=f'{Colors.RED}On{Colors.WHITE}words{Colors.RESET} - Control a gate device',
        epilog=f'''
Actions:
  Sliding Gate: {', '.join(sliding_actions)}
  Arm Gate (Single): {', '.join(arm_single_actions)}
  Arm Gate (Double): {', '.join(arm_double_actions)}
        '''
    )
    parser.add_argument('product_id', help='Product ID to control')
    parser.add_argument('action', choices=all_actions, help='Action to perform')
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    # Check if API key is configured
    config = load_config()
    if not config.get("api_key"):
        print_banner()
        print(f"{Colors.RED}✗ Error: API key not configured{Colors.RESET}")
        print(f"\nRun: {Colors.BOLD}onwords-config --api-key YOUR_KEY{Colors.RESET}")
        sys.exit(1)
    
    print_banner()
    
    try:
        from .controller import control
        gate = control(args.product_id)
        
        print(f"Sending: {Colors.BOLD}{args.action}{Colors.RESET} → {args.product_id}")
        result = gate.action(args.action)
        
        if result.get("status") == "success":
            print(f"{Colors.GREEN}✓ Command sent successfully!{Colors.RESET}")
            if result.get("gate_type"):
                print(f"  Gate Type: {result['gate_type']}")
        else:
            print(f"{Colors.YELLOW}Response: {result}{Colors.RESET}")
            
    except ValueError as e:
        print(f"{Colors.RED}✗ Error: {e}{Colors.RESET}")
        sys.exit(1)
    except ConnectionError as e:
        print(f"{Colors.RED}✗ Connection Error: {e}{Colors.RESET}")
        sys.exit(1)


def main():
    """Main CLI entry point: onwords"""
    parser = argparse.ArgumentParser(
        prog='onwords',
        description=f'{Colors.RED}On{Colors.WHITE}words{Colors.RESET} - Gate Control Package',
        epilog='''
Commands:
  onwords-config   Configure your API key
  onwords-list     List all your products  
  onwords-control  Control a gate device
        '''
    )
    parser.add_argument('--version', '-v', action='version', 
                       version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    print_banner()
    
    # Check config status
    config = load_config()
    if config.get("api_key"):
        key_preview = config["api_key"][:8] + "..." if len(config["api_key"]) > 8 else "***"
        print(f"  {Colors.GREEN}✓{Colors.RESET} API Key: {key_preview}")
    else:
        print(f"  {Colors.RED}✗{Colors.RESET} API Key: Not configured")
        print(f"\n{Colors.BOLD}Get your API key:{Colors.RESET}")
        print(f"  1. Visit {Colors.CYAN}https://ostapi.onwords.in{Colors.RESET}")
        print(f"  2. Click 'Get API Key' and login")
        print(f"  3. Select devices and generate key")
        print(f"  4. Run: {Colors.BOLD}onwords-config --api-key YOUR_KEY{Colors.RESET}")
    
    print(f"\n{Colors.BOLD}Commands:{Colors.RESET}")
    print(f"  {Colors.BOLD}onwords-config{Colors.RESET}   Configure your API key")
    print(f"  {Colors.BOLD}onwords-list{Colors.RESET}     List all your products")
    print(f"  {Colors.BOLD}onwords-control{Colors.RESET}  Control a gate device")
    print()
    print(f"API Docs: {Colors.CYAN}https://ostapi.onwords.in/api-documentation{Colors.RESET}")


if __name__ == '__main__':
    main()
