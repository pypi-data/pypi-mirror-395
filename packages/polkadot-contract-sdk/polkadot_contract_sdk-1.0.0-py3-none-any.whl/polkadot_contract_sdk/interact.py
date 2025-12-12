#!/usr/bin/env python3
"""
Smart Contract Interaction Module
Interact with deployed smart contracts
"""

import ast
import json
import os
from web3 import Web3

# Try to load from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, continue without it

# Moonbase Alpha RPC (Kusama testnet)
MOONBASE_ALPHA_RPC = "https://rpc.api.moonbase.moonbeam.network"


def extract_functions_from_python(file_path):
    """Extract function definitions from Python file"""
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r') as f:
        source = f.read()
    
    tree = ast.parse(source)
    functions = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Get function signature
            args = [arg.arg for arg in node.args.args]
            functions[node.name] = {
                'args': args,
                'source': ast.get_source_segment(source, node)
            }
    
    return functions


def load_deployment(deployment_file='deployment.json'):
    """Load deployment information"""
    if not os.path.exists(deployment_file):
        raise FileNotFoundError(
            f"Error: {deployment_file} not found!\n"
            "Deploy the contract first using: sdk-deploy-contract"
        )
    
    with open(deployment_file, 'r') as f:
        deployment = json.load(f)
    
    return deployment['contract_address'], deployment['abi'], deployment.get('rpc_url', MOONBASE_ALPHA_RPC)


def interact(contract_address=None, python_file_path='main.py', deployment_file='deployment.json', rpc_url=None):
    """
    Interact with a deployed smart contract
    
    Args:
        contract_address: Contract address (if None, loads from deployment_file)
        python_file_path: Path to the original Python file (for function discovery)
        deployment_file: Path to deployment.json file
        rpc_url: RPC URL for the network (default: Moonbase Alpha)
    """
    print("=" * 60)
    print("🔌 Smart Contract Interaction")
    print("=" * 60)
    print()
    
    # Load contract address and ABI
    if contract_address:
        # If contract address is provided, try to load ABI from deployment file
        # If not found, we'll need to handle it differently
        if os.path.exists(deployment_file):
            _, abi, rpc_url_from_file = load_deployment(deployment_file)
            if rpc_url is None:
                rpc_url = rpc_url_from_file
        else:
            raise FileNotFoundError(
                f"Error: {deployment_file} not found!\n"
                "Cannot load ABI without deployment file."
            )
    else:
        contract_address, abi, rpc_url_from_file = load_deployment(deployment_file)
        if rpc_url is None:
            rpc_url = rpc_url_from_file
    
    # Read Python file to get available functions
    print(f"📖 Reading {python_file_path} to discover functions...")
    python_functions = extract_functions_from_python(python_file_path)
    
    # Filter out main and __main__ functions
    contract_functions = {
        name: info for name, info in python_functions.items() 
        if name not in ['main', '__main__']
    }
    
    if not contract_functions:
        print("⚠️  No functions found in Python file (excluding main())")
        print("   Make sure the file has functions to interact with!")
        return
    
    print(f"✅ Found {len(contract_functions)} function(s) from {python_file_path}:")
    for func_name in contract_functions.keys():
        print(f"   - {func_name}")
    print()
    
    # Connect to network
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise ConnectionError("Failed to connect to network!")
    
    print(f"✅ Connected to network")
    print(f"📍 Contract Address: {contract_address}\n")
    
    # Create contract instance
    contract = web3.eth.contract(address=contract_address, abi=abi)
    
    # Get account
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        raise ValueError(
            "PRIVATE_KEY environment variable not set\n"
            "Set it with: export PRIVATE_KEY='your_private_key'"
        )
    
    account = web3.eth.account.from_key(private_key)
    
    # Build dynamic menu based on Python functions
    menu_items = []
    menu_index = 1
    
    # Add functions from Python file
    for func_name, func_info in contract_functions.items():
        args = func_info['args']
        if len(args) == 2:
            menu_items.append({
                'type': 'function',
                'name': func_name,
                'args': args,
                'index': menu_index
            })
            menu_index += 1
    
    # Add helper functions
    helper_functions = [
        {'name': 'getLastResult', 'type': 'view', 'description': 'Get last result'},
        {'name': 'getCalculationCount', 'type': 'view', 'description': 'Get calculation count'}
    ]
    
    for helper in helper_functions:
        menu_items.append({
            'type': 'helper',
            'name': helper['name'],
            'description': helper['description'],
            'index': menu_index
        })
        menu_index += 1
    
    # Add exit option
    exit_index = menu_index
    
    # Interactive menu
    while True:
        print("\n" + "-" * 60)
        print("Available actions (from Python file):")
        
        # Display functions from Python file
        for item in menu_items:
            if item['type'] == 'function':
                args_str = ', '.join(item['args'])
                print(f"{item['index']}. Call {item['name']}({args_str})")
            elif item['type'] == 'helper':
                print(f"{item['index']}. {item['description']}")
        
        print(f"{exit_index}. Exit")
        print("-" * 60)
        
        choice = input(f"\nSelect an action (1-{exit_index}): ").strip()
        
        # Handle exit
        if choice == str(exit_index):
            print("\n👋 Goodbye!")
            break
        
        # Handle function calls from Python file
        selected_item = None
        for item in menu_items:
            if str(item['index']) == choice:
                selected_item = item
                break
        
        if not selected_item:
            print(f"❌ Invalid choice. Please select 1-{exit_index}.")
            continue
        
        try:
            if selected_item['type'] == 'function':
                # Call function from Python file
                func_name = selected_item['name']
                args = selected_item['args']
                
                # Get parameters from user
                params = []
                for arg in args:
                    value = input(f"Enter {arg}: ")
                    try:
                        params.append(int(value))
                    except ValueError:
                        print(f"❌ Invalid number: {value}")
                        break
                else:
                    # All parameters collected successfully
                    params_str = ', '.join(map(str, params))
                    print(f"\n📤 Calling {func_name}({params_str})...")
                    
                    # Get fresh nonce right before building transaction
                    nonce = web3.eth.get_transaction_count(account.address, 'pending')
                    
                    # Build the transaction
                    txn = getattr(contract.functions, func_name)(*params).build_transaction({
                        'from': account.address,
                        'nonce': nonce,
                        'gas': 100000,
                        'gasPrice': web3.eth.gas_price,
                        'chainId': web3.eth.chain_id
                    })
                    
                    # Sign the transaction
                    signed_txn = account.sign_transaction(txn)
                    
                    # Send the signed transaction
                    tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
                    print(f"⏳ Transaction hash: {tx_hash.hex()}")
                    
                    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
                    print(f"✅ Transaction confirmed!")
                    
                    # Get the result
                    result = contract.functions.getLastResult().call()
                    print(f"📊 Result: {result}")
            
            elif selected_item['type'] == 'helper':
                # Call helper function (view function, no transaction needed)
                func_name = selected_item['name']
                result = getattr(contract.functions, func_name)().call()
                print(f"\n📊 {selected_item['description']}: {result}")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

