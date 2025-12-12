#!/usr/bin/env python3
"""
CLI Entry Points for the SDK
"""

import sys
import argparse
from .deploy import deploy
from .interact import interact


def deploy_command():
    """CLI command for deploying contracts"""
    parser = argparse.ArgumentParser(
        description='Deploy a Python file as a smart contract',
        prog='sdk-deploy-contract'
    )
    parser.add_argument(
        'python_file',
        help='Path to the Python file to deploy (e.g., main.py)'
    )
    parser.add_argument(
        '-o', '--output',
        default='deployment.json',
        help='Output file for deployment information (default: deployment.json)'
    )
    parser.add_argument(
        '-r', '--rpc',
        default=None,
        help='RPC URL for the network (default: Moonbase Alpha)'
    )
    
    args = parser.parse_args()
    
    try:
        deploy(args.python_file, args.output, args.rpc)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def interact_command():
    """CLI command for interacting with contracts"""
    parser = argparse.ArgumentParser(
        description='Interact with a deployed smart contract',
        prog='sdk-interact'
    )
    parser.add_argument(
        'contract_address',
        nargs='?',
        default=None,
        help='Contract address (if not provided, loads from deployment.json)'
    )
    parser.add_argument(
        '-p', '--python-file',
        default='main.py',
        help='Path to the original Python file (default: main.py)'
    )
    parser.add_argument(
        '-d', '--deployment',
        default='deployment.json',
        help='Path to deployment.json file (default: deployment.json)'
    )
    parser.add_argument(
        '-r', '--rpc',
        default=None,
        help='RPC URL for the network (default: Moonbase Alpha)'
    )
    
    args = parser.parse_args()
    
    try:
        interact(
            contract_address=args.contract_address,
            python_file_path=args.python_file,
            deployment_file=args.deployment,
            rpc_url=args.rpc
        )
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

