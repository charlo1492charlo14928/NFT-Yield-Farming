"""
NFT Yield Farming - Interactive Interface
Smart contract CLI for farming yield by staking LP tokens on BSC
"""

import os
import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from rich import box
from utils import ensure_env

# CLI root (folder containing main.py)
CLI_ROOT = Path(__file__).resolve().parent
# Project root (parent of CLI - NFT Yield Farming folder)
PROJECT_ROOT = CLI_ROOT.parent


def get_nft_project_root() -> Path:
    """Find NFT Yield Farming project root (with package.json)."""
    candidates = [
        PROJECT_ROOT / "NFT-yield-farming",  # Cloned repo
        PROJECT_ROOT,  # Current folder
    ]
    for path in candidates:
        if (path / "package.json").exists():
            return path
    return PROJECT_ROOT

LOGO = r"""
 _   _ ______ _______           _      _     _         __                     _             
 | \ | |  ____|__   __|         (_)    | |   | |       / _|                   (_)            
 |  \| | |__     | |______ _   _ _  ___| | __| |______| |_ __ _ _ __ _ __ ___  _ _ __   __ _ 
 | . ` |  __|    | |______| | | | |/ _ \ |/ _` |______|  _/ _` | '__| '_ ` _ \| | '_ \ / _` |
 | |\  | |       | |      | |_| | |  __/ | (_| |      | || (_| | |  | | | | | | | | | | (_| |
 |_| \_|_|       |_|       \__, |_|\___|_|\__,_|      |_| \__,_|_|  |_| |_| |_|_|_| |_|\__, |
                            __/ |                                                       __/ |
                           |___/                                                       |___/ 
"""


def clear_screen(console: Console):
    """Clear the console screen."""
    console.clear()


def show_logo(console: Console):
    """Display the NFT Yield Farming logo."""
    console.print(Panel(
        Text(LOGO, style="bold cyan"),
        title="[bold yellow]NFT Yield Farming on BSC[/bold yellow]",
        subtitle="[dim]Stake LP tokens • Farm Governance Tokens • BSC Smart Contract[/dim]",
        border_style="cyan",
        box=box.DOUBLE,
        padding=(0, 2),
    ))
    console.print()


def run_command(cmd: list[str], console: Console, cwd: Path = None) -> bool:
    """Run a command and display output. Returns True if successful."""
    work_dir = cwd or PROJECT_ROOT
    try:
        # Use shell on Windows for proper npm resolution
        if sys.platform == "win32":
            result = subprocess.run(
                " ".join(cmd),
                cwd=work_dir,
                shell=True,
            )
        else:
            result = subprocess.run(cmd, cwd=work_dir)
        return result.returncode == 0
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return False


def install_dependencies(console: Console):
    """Install npm modules in the root directory."""
    console.print(Panel(
        "[bold]Installing npm modules...[/bold]\n"
        "Executing: [cyan]npm install[/cyan]\n\n"
        "This installs dependencies for the NFT Yield Farming project.",
        title="[yellow]Install Dependencies[/yellow]",
        border_style="yellow",
    ))
    console.print()
    
    success = run_command(["npm", "install"], console, get_nft_project_root())
    
    if success:
        console.print("[green]✓ Dependencies installed successfully![/green]")
    else:
        console.print("[red]✗ Failed to install dependencies. Make sure Node.js and npm are installed.[/red]")
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def settings_menu(console: Console):
    """Settings - configure .env and RPC endpoints."""
    while True:
        clear_screen(console)
        show_logo(console)
        
        table = Table(title="[bold yellow]Settings[/bold yellow]", show_header=True, header_style="cyan")
        table.add_column("Option", style="white")
        table.add_column("Description", style="dim")
        table.add_row("1", "Clone project from GitHub")
        table.add_row("2", "Setup .env file (copy from .env.example)")
        table.add_row("3", "View RPC Endpoints reference")
        table.add_row("4", "Show configuration help")
        table.add_row("0", "Back to main menu")
        console.print(table)
        console.print()
        
        choice = Prompt.ask("[cyan]Select option[/cyan]", choices=["0", "1", "2", "3", "4"], default="0")
        
        if choice == "0":
            break
        elif choice == "1":
            clone_project(console)
        elif choice == "2":
            setup_env(console)
        elif choice == "3":
            show_rpc_reference(console)
        elif choice == "4":
            show_config_help(console)


def clone_project(console: Console):
    """Clone NFT Yield Farming project from GitHub."""
    repo_url = "https://github.com/masaun/NFT-yield-farming.git"
    target = PROJECT_ROOT / "NFT-yield-farming"
    
    if target.exists() and any(target.iterdir()):
        console.print("[yellow]⚠ Project folder already exists.[/yellow]")
        if not Confirm.ask("Clone anyway? (may overwrite)", default=False):
            return
    
    console.print(f"[cyan]Cloning from {repo_url}...[/cyan]")
    success = run_command(["git", "clone", repo_url], console, PROJECT_ROOT)
    
    if success:
        console.print("[green]✓ Project cloned successfully![/green]")
        console.print("[dim]Run 'Install Dependencies' and configure .env[/dim]")
    else:
        console.print("[red]✗ Clone failed. Ensure git is installed.[/red]")
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def setup_env(console: Console):
    """Setup .env file from .env.example."""
    nft_root = get_nft_project_root()
    env_example = nft_root / ".env.example"
    env_file = nft_root / ".env"
    
    if env_file.exists():
        if Confirm.ask("[yellow].env already exists. Overwrite?[/yellow]", default=False):
            pass
        else:
            return
    
    if env_example.exists():
        try:
            content = env_example.read_text(encoding="utf-8")
            env_file.write_text(content, encoding="utf-8")
            console.print("[green]✓ Created .env from .env.example[/green]")
            console.print("[dim]Please edit .env and add your wallet info, private keys, etc.[/dim]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
    else:
        console.print("[yellow]⚠ .env.example not found in project root.[/yellow]")
        console.print("[dim]Create .env manually. Reference: https://github.com/masaun/NFT-yield-farming/blob/main/.env.example[/dim]")
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def show_rpc_reference(console: Console):
    """Show BSC RPC endpoints reference."""
    console.print(Panel(
        "[bold]BSC RPC Endpoints[/bold]\n\n"
        "When 503 Error happens, select a new BSC RPC Endpoint.\n\n"
        "Reference: [link=https://docs.binance.org/smart-chain/developer/rpc.html]"
        "https://docs.binance.org/smart-chain/developer/rpc.html[/link]\n\n"
        "Replace RPC in these files:\n"
        "  • truffle-config.js (line 9)\n"
        "  • scripts/script-bsc/NFTYieldFarmingOnBSC.script.js (line 5)",
        title="[yellow]RPC Configuration[/yellow]",
        border_style="yellow",
    ))
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def show_config_help(console: Console):
    """Show configuration help."""
    console.print(Panel(
        "[bold]Setup Steps[/bold]\n\n"
        "① Install modules: npm install\n"
        "② Add .env with wallet/private key info (see .env.example)\n"
        "③ Compile: npm run compile:bsc-testnet\n"
        "④ Test: npm run test:nft-yield-farming_bsc-testnet\n"
        "⑤ Script: npm run script:nft-yield-farming_bsc-testnet\n\n"
        "[dim]Note: Ensure deployer wallet has enough BNB on BSC testnet.[/dim]",
        title="[yellow]Configuration Help[/yellow]",
        border_style="yellow",
    ))
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def compile_contracts(console: Console):
    """Compile contracts on BSC testnet."""
    console.print(Panel(
        "[bold]Compiling smart contracts...[/bold]\n"
        "Executing: [cyan]npm run compile:bsc-testnet[/cyan]\n\n"
        "Compiles contracts for BSC testnet.",
        title="[yellow]Compile Contracts[/yellow]",
        border_style="yellow",
    ))
    console.print()
    
    success = run_command(["npm", "run", "compile:bsc-testnet"], console, get_nft_project_root())
    
    if success:
        console.print("[green]✓ Contracts compiled successfully![/green]")
    else:
        console.print("[red]✗ Compilation failed. Check that dependencies are installed and truffle-config is correct.[/red]")
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def run_tests(console: Console):
    """Run smart contract tests."""
    console.print(Panel(
        "[bold]Running smart contract tests...[/bold]\n"
        "Executing: [cyan]npm run test:nft-yield-farming_bsc-testnet[/cyan]\n\n"
        "[dim]Note: Timeouts may occur. Try 'Execute Script' if tests fail.[/dim]",
        title="[yellow]Run Tests[/yellow]",
        border_style="yellow",
    ))
    console.print()
    
    success = run_command(["npm", "run", "test:nft-yield-farming_bsc-testnet"], console, get_nft_project_root())
    
    if success:
        console.print("[green]✓ All tests passed![/green]")
    else:
        console.print("[yellow]⚠ Tests failed or timed out. Try 'Execute Script' as an alternative.[/yellow]")
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def execute_script(console: Console):
    """Execute smart contract script on BSC testnet."""
    console.print(Panel(
        "[bold]Executing smart contract script...[/bold]\n"
        "Executing: [cyan]npm run script:nft-yield-farming_bsc-testnet[/cyan]\n\n"
        "[yellow]⚠ Ensure deployer wallet has enough BNB on BSC testnet![/yellow]\n"
        "Faucet: https://testnet.binance.org/faucet-smart",
        title="[yellow]Execute Script[/yellow]",
        border_style="yellow",
    ))
    console.print()
    
    if not Confirm.ask("Proceed with script execution?", default=True):
        return
    
    success = run_command(["npm", "run", "script:nft-yield-farming_bsc-testnet"], console, get_nft_project_root())
    
    if success:
        console.print("[green]✓ Script executed successfully![/green]")
    else:
        console.print("[red]✗ Script execution failed. Check BNB balance and configuration.[/red]")
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def about_section(console: Console):
    """Show about information and references."""
    clear_screen(console)
    
    # Load hashtags
    hashtags_path = CLI_ROOT / "about" / "hashtags.txt"
    hashtags = ""
    if hashtags_path.exists():
        hashtags = hashtags_path.read_text(encoding="utf-8").strip()
    
    content = """[bold cyan]Introduction[/bold cyan]
This is a smart contract that enables users to farm yield by staking LP tokens (BEP20) 
into an NFT pool. Once staked, Governance Tokens are mined every block. Users receive 
rewards when they un-stake. Works on BSC (Binance Smart Chain).

[bold cyan]Version Info[/bold cyan]
• Solidity (Solc): v0.6.12
• Truffle: v5.1.60
• web3.js: v1.2.9
• openzeppelin-solidity: v3.2.0

[bold cyan]References[/bold cyan]
• Getting Started: https://binancex.dev/blog.html?p=making-the-move-from-ethereum-to-bsc
• BSC Explorer: https://explorer.binance.org/smart-testnet
• Testnet Faucet: https://testnet.binance.org/faucet-smart
• BEP20 Template: https://github.com/binance-chain/bsc-genesis-contract
• RPC Endpoints: https://docs.binance.org/smart-chain/developer/rpc.html
"""
    
    console.print(Panel(
        content,
        title="[bold yellow]About NFT Yield Farming[/bold yellow]",
        border_style="cyan",
    ))
    
    if hashtags:
        console.print()
        console.print(Panel(
            hashtags,
            title="[bold cyan]Hashtags[/bold cyan]",
            border_style="dim",
        ))
    
    Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")


def main_menu(console: Console):
    """Main menu loop."""
    while True:
        clear_screen(console)
        show_logo(console)
        
        table = Table(
            title="[bold yellow]Main Menu[/bold yellow]",
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED,
        )
        table.add_column("#", style="cyan", width=3)
        table.add_column("Option", style="white")
        table.add_column("Description", style="dim")
        
        table.add_row("1", "Install Dependencies", "npm install - install project modules")
        table.add_row("2", "Settings", "Configure .env, RPC endpoints")
        table.add_row("3", "Compile Contracts", "Compile for BSC testnet")
        table.add_row("4", "Run Tests", "Execute smart contract tests")
        table.add_row("5", "Execute Script", "Run deployment script on BSC")
        table.add_row("6", "About", "Info, references, hashtags")
        table.add_row("0", "Exit", "Quit application")
        
        console.print(table)
        console.print()
        
        choice = Prompt.ask(
            "[bold cyan]Select option[/bold cyan]",
            choices=["0", "1", "2", "3", "4", "5", "6"],
            default="0",
        )
        
        if choice == "0":
            console.print("[green]Goodbye![/green]")
            break
        elif choice == "1":
            clear_screen(console)
            show_logo(console)
            install_dependencies(console)
        elif choice == "2":
            settings_menu(console)
        elif choice == "3":
            clear_screen(console)
            show_logo(console)
            compile_contracts(console)
        elif choice == "4":
            clear_screen(console)
            show_logo(console)
            run_tests(console)
        elif choice == "5":
            clear_screen(console)
            show_logo(console)
            execute_script(console)
        elif choice == "6":
            about_section(console)


@ensure_env
def main():
    """Entry point."""
    console = Console()
    
    try:
        main_menu(console)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted. Goodbye![/yellow]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise


if __name__ == "__main__":
    main()
