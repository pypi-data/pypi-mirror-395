#!/usr/bin/env python3
"""
NeuroShard CLI - Main entry point for running a node

Usage:
    neuroshard-node --port 8000 --token YOUR_TOKEN
    neuroshard-node --help

This starts a NeuroShard node that:
1. Participates in distributed LLM training
2. Earns NEURO tokens via Proof of Neural Work
3. Serves a web dashboard at http://localhost:PORT/
"""

import argparse
import sys
import os
import webbrowser
import threading
import time

from neuroshard.version import __version__


def open_dashboard_delayed(port: int, delay: float = 3.0):
    """Open the dashboard in browser after a delay (to let server start)."""
    def opener():
        time.sleep(delay)
        url = f"http://localhost:{port}/"
        print(f"\n[NODE] Opening dashboard: {url}")
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"[NODE] Could not open browser: {e}")
            print(f"[NODE] Please manually open: {url}")
    
    thread = threading.Thread(target=opener, daemon=True)
    thread.start()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="NeuroShard Node - Decentralized AI Training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start a node with default settings
  neuroshard-node --token YOUR_WALLET_TOKEN

  # Start on a custom port
  neuroshard-node --port 9000 --token YOUR_WALLET_TOKEN

  # Start without auto-opening browser
  neuroshard-node --token YOUR_WALLET_TOKEN --no-browser

  # Start inference-only node (no training)
  neuroshard-node --token YOUR_WALLET_TOKEN --no-training

  # Run with resource limits
  neuroshard-node --token YOUR_TOKEN --memory 4096 --cpu-threads 4

Get your wallet token at: https://neuroshard.com/wallet
        """
    )
    
    # Core options
    parser.add_argument(
        "--port", type=int, default=8000,
        help="HTTP port for the node (default: 8000)"
    )
    parser.add_argument(
        "--token", type=str, default=None,
        help="Wallet token (64-char hex) or 12-word mnemonic phrase"
    )
    parser.add_argument(
        "--tracker", type=str, default="https://neuroshard.com/api/tracker",
        help="Tracker URL for peer discovery"
    )
    
    # Network options
    parser.add_argument(
        "--announce-ip", type=str, default=None,
        help="Force this IP address for peer announcements"
    )
    parser.add_argument(
        "--announce-port", type=int, default=None,
        help="Force this port for peer announcements"
    )
    
    # Training options
    parser.add_argument(
        "--no-training", action="store_true",
        help="Disable training (inference only)"
    )
    parser.add_argument(
        "--diloco-steps", type=int, default=500,
        help="DiLoCo inner steps before gradient sync (default: 500)"
    )
    
    # Resource limits
    parser.add_argument(
        "--memory", type=int, default=None,
        help="Max memory in MB (default: auto-detect 70%% of system RAM)"
    )
    parser.add_argument(
        "--cpu-threads", type=int, default=None,
        help="Max CPU threads to use (default: all cores)"
    )
    parser.add_argument(
        "--max-storage", type=int, default=100,
        help="Max disk space for training data in MB (default: 100)"
    )
    
    # UI options
    parser.add_argument(
        "--no-browser", action="store_true",
        help="Don't auto-open dashboard in browser"
    )
    parser.add_argument(
        "--headless", action="store_true",
        help="Run without any UI (server mode)"
    )
    
    # Info options
    parser.add_argument(
        "--version", action="version",
        version=f"NeuroShard {__version__}"
    )
    
    args = parser.parse_args()
    
    # Detect GPU before printing banner
    gpu_status = "CPU"
    gpu_color = ""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_status = f"CUDA ({gpu_name})"
            gpu_color = "\033[92m"  # Green
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            gpu_status = "Apple Metal (MPS)"
            gpu_color = "\033[92m"  # Green
        else:
            gpu_status = "CPU (no GPU detected)"
            gpu_color = "\033[93m"  # Yellow
    except ImportError:
        gpu_status = "PyTorch not installed"
        gpu_color = "\033[91m"  # Red
    
    reset_color = "\033[0m"
    
    # Print banner
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███╗   ██╗███████╗██╗   ██╗██████╗  ██████╗               ║
║   ████╗  ██║██╔════╝██║   ██║██╔══██╗██╔═══██╗              ║
║   ██╔██╗ ██║█████╗  ██║   ██║██████╔╝██║   ██║              ║
║   ██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║   ██║              ║
║   ██║ ╚████║███████╗╚██████╔╝██║  ██║╚██████╔╝              ║
║   ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝              ║
║                                                              ║
║   ███████╗██╗  ██╗ █████╗ ██████╗ ██████╗                   ║
║   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔══██╗                  ║
║   ███████╗███████║███████║██████╔╝██║  ██║                  ║
║   ╚════██║██╔══██║██╔══██║██╔══██╗██║  ██║                  ║
║   ███████║██║  ██║██║  ██║██║  ██║██████╔╝                  ║
║   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝                  ║
║                                                              ║
║            Decentralized AI Training Network                 ║
║                     v{__version__:<10}                            ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Print GPU status
    print(f"  {gpu_color}🖥️  Device: {gpu_status}{reset_color}")
    print()
    
    # Validate token
    if not args.token:
        print("[ERROR] Wallet token required!")
        print()
        print("Get your token at: https://neuroshard.com/wallet")
        print("Or generate a new wallet with: neuroshard-node --help")
        print()
        print("Usage: neuroshard-node --token YOUR_TOKEN")
        sys.exit(1)
    
    # Auto-open browser (unless disabled)
    if not args.no_browser and not args.headless:
        open_dashboard_delayed(args.port)
    
    # Import runner from the package
    from neuroshard.runner import run_node
    
    # Handle mnemonic input
    node_token = args.token
    if node_token:
        words = node_token.strip().split()
        if len(words) == 12:
            try:
                from mnemonic import Mnemonic
                mnemo = Mnemonic("english")
                if mnemo.check(node_token):
                    seed = mnemo.to_seed(node_token, passphrase="")
                    node_token = seed[:32].hex()
                    print("[NODE] ✅ Wallet recovered from mnemonic")
                else:
                    print("[WARNING] Invalid mnemonic - treating as raw token")
            except ImportError:
                print("[WARNING] 'mnemonic' package not installed")
            except Exception as e:
                print(f"[WARNING] Mnemonic error: {e}")
    
    # Run the node
    print(f"[NODE] Starting on port {args.port}...")
    print(f"[NODE] Dashboard: http://localhost:{args.port}/")
    print()
    
    run_node(
        port=args.port,
        tracker=args.tracker,
        node_token=node_token,
        announce_ip=args.announce_ip,
        announce_port=args.announce_port,
        enable_training=not args.no_training,
        available_memory_mb=args.memory,
        max_storage_mb=args.max_storage,
        max_cpu_threads=args.cpu_threads,
        diloco_inner_steps=args.diloco_steps,
    )


if __name__ == "__main__":
    main()

