# NFT-Yield-Farming
NFT Yield Farming CLI — Interactive tool for managing NFT yield farming smart contracts on Binance Smart Chain (BSC) with LP token staking, governance token farming, Solidity 0.6.12 contract interaction, Web3.py integration, and Rich terminal menu for DeFi yield optimization
<div align="center">

```
 _   _ ______ _______           _      _     _         __                     _             
 | \ | |  ____|__   __|         (_)    | |   | |       / _|                   (_)            
 |  \| | |__     | |______ _   _ _  ___| | __| |______| |_ __ _ _ __ _ __ ___  _ _ __   __ _ 
 | . ` |  __|    | |______| | | | |/ _ \ |/ _` |______|  _/ _` | '__| '_ ` _ \| | '_ \ / _` |
 | |\  | |       | |      | |_| | |  __/ | (_| |      | || (_| | |  | | | | | | | | | | (_| |
 |_| \_|_|       |_|       \__, |_|\___|_|\__,_|      |_| \__,_|_|  |_| |_| |_|_|_| |_|\__, |
                            __/ |                                                       __/ |
                           |___/                                                       |___/ 
```

# NFT Yield Farming CLI

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![BSC](https://img.shields.io/badge/BSC-Binance_Smart_Chain-F0B90B?style=for-the-badge&logo=binance)](https://academy.binance.com/en/articles/connecting-metamask-to-binance-smart-chain)
[![DeFi](https://img.shields.io/badge/DeFi-Yield_Farming-627EEA?style=for-the-badge&logo=ethereum)](https://ethereum.org/en/defi/)
[![Solidity](https://img.shields.io/badge/Solidity-0.6.12-363636?style=for-the-badge&logo=solidity)](https://soliditylang.org/)

**CMD interface for managing NFT Yield Farming smart contracts on BSC — stake LP tokens, farm Governance Tokens**

[Features](#features) • [Getting Started](#getting-started) • [Configuration](#configuration) • [Usage](#usage) • [Project Structure](#project-structure) • [FAQ](#faq)

</div>

---

## Official Links

| Resource | URL |
|----------|-----|
| **NFT Yield Farming (GitHub)** | https://github.com/masaun/NFT-yield-farming |
| **BSC Getting Started** | https://binancex.dev/blog.html?p=making-the-move-from-ethereum-to-bsc |
| **BSC Testnet Explorer** | https://explorer.binance.org/smart-testnet |
| **BSC Testnet Faucet** | https://testnet.binance.org/faucet-smart |
| **BSC RPC Endpoints** | https://docs.binance.org/smart-chain/developer/rpc.html |
| **.env.example Reference** | https://github.com/masaun/NFT-yield-farming/blob/main/.env.example |
| **BEP20 Template** | https://github.com/binance-chain/bsc-genesis-contract |

---

## Features

<table>
<tr>
<td width="50%">

| Feature | ✓ |
|---------|---|
| One-click npm install for NFT project | ✓ |
| Clone NFT Yield Farming from GitHub | ✓ |
| Setup .env from .env.example | ✓ |
| RPC endpoints reference & config help | ✓ |
| Compile contracts for BSC testnet | ✓ |
| Run smart contract tests | ✓ |
| Execute deployment script on BSC | ✓ |

</td>
<td width="50%">

| Feature | ✓ |
|---------|---|
| Rich CMD/CLI interface (Rich library) | ✓ |
| Cross-platform (Windows shell support) | ✓ |
| About section with version info & references | ✓ |
| Stake LP tokens (BEP20) into NFT pool | ✓ |
| Farm Governance Tokens per block | ✓ |
| Solidity 0.6.12, Truffle 5.1.60 | ✓ |
| OpenZeppelin contracts v3.2.0 | ✓ |

</td>
</tr>
</table>

---

## Getting Started

### Prerequisites

- **Python** 3.8 or higher
- **pip** (Python package manager)
- **Node.js** and **npm** (for NFT Yield Farming project)
- **Git** (for cloning the NFT project)

### Installation

```bash
# Clone or extract the CLI
cd NFT-Yield-Farming-CLI

# Install Python dependencies
pip install -r requirements.txt

# Run the CLI
python main.py
```

On Windows, one-click launch:

```bash
run.bat
```

> **Note:** The NFT Yield Farming project must be in the parent folder. Use **Settings → Clone project from GitHub** if it is not present.

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| rich | ≥13.7.0 | Rich terminal UI, panels, tables, prompts |

---

## Configuration

Configuration is stored in the **NFT Yield Farming** project root (cloned to `NFT-yield-farming/` or parent folder). Copy `.env.example` to `.env` and fill in your values.

### .env (NFT project root)

```env
MNEMONIC="word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12"
INFURA_KEY="your_infura_project_id"

DEPLOYER_WALLET="0x1234567890abcdef1234567890abcdef12345678"
ADMIN_WALLET="0xabcdef1234567890abcdef1234567890abcdef12"

PRIVATE_KEY_OF_DEPLOYER_WALLET="0x..."
PRIVATE_KEY_OF_ADMIN_WALLET="0x..."
```

| Variable | Description |
|----------|-------------|
| `MNEMONIC` | BIP39 mnemonic phrase for wallet recovery |
| `INFURA_KEY` | Infura project ID (optional for BSC) |
| `DEPLOYER_WALLET` | Deployer/staker wallet address |
| `ADMIN_WALLET` | Admin wallet address |
| `PRIVATE_KEY_OF_*` | Private keys for deployer and admin |

> **Security:** Never commit `.env` or share private keys. Use BSC testnet and testnet BNB for development.

### RPC Configuration

When 503 errors occur, replace the BSC RPC endpoint in:

- `truffle-config.js` (line 9)
- `scripts/script-bsc/NFTYieldFarmingOnBSC.script.js` (line 5)

Reference: [BSC RPC Endpoints](https://docs.binance.org/smart-chain/developer/rpc.html)

---

## Usage

### CLI Menu

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    NFT Yield Farming on BSC                                          │
│              Stake LP tokens • Farm Governance Tokens • BSC Smart Contract            │
└─────────────────────────────────────────────────────────────────────────────────────┘

                              Main Menu
┌───┬─────────────────────────┬───────────────────────────────────────────────────────┐
│ # │ Option                  │ Description                                            │
├───┼─────────────────────────┼───────────────────────────────────────────────────────┤
│ 1 │ Install Dependencies    │ npm install - install project modules                  │
│ 2 │ Settings                │ Configure .env, RPC endpoints                          │
│ 3 │ Compile Contracts       │ Compile for BSC testnet                                 │
│ 4 │ Run Tests               │ Execute smart contract tests                           │
│ 5 │ Execute Script          │ Run deployment script on BSC                            │
│ 6 │ About                   │ Info, references, hashtags                              │
│ 0 │ Exit                    │ Quit application                                        │
└───┴─────────────────────────┴───────────────────────────────────────────────────────┘

Select option [0]: 1
```

### Settings Submenu

| Option | Action |
|--------|--------|
| 1 | Clone project from GitHub |
| 2 | Setup .env file (copy from .env.example) |
| 3 | View RPC Endpoints reference |
| 4 | Show configuration help |
| 0 | Back to main menu |

### Recommended Workflow

1. **Settings → 1** — Clone NFT Yield Farming project
2. **1** — Install Dependencies (`npm install`)
3. **Settings → 2** — Setup .env with wallet info
4. **3** — Compile Contracts (`npm run compile:bsc-testnet`)
5. **4** or **5** — Run Tests or Execute Script

> Ensure the deployer wallet has enough BNB on BSC testnet. Use the [faucet](https://testnet.binance.org/faucet-smart).

---

## Project Structure

```
NFT-Yield-Farming-CLI/
├── main.py              # Entry point, Rich CLI, menu logic
├── requirements.txt     # Python dependencies (rich)
├── run.bat              # Windows launcher (auto-install + run)
├── README.md            # This file
├── tags.txt             # GitHub topics
└── about/
    └── hashtags.txt     # Project hashtags
```

The **NFT Yield Farming** project (cloned via Settings) resides in the parent folder as `NFT-yield-farming/`.

---

## FAQ

<details>
<summary><b>What is NFT Yield Farming?</b></summary>

NFT yield farming merges DeFi and NFT technology. Users stake LP tokens (BEP20) into an NFT pool; Governance Tokens are mined every block. When users un-stake, they receive the farmed yield as rewards. This project implements that model on BSC (Binance Smart Chain).
</details>

<details>
<summary><b>Why does this CLI need the NFT Yield Farming project?</b></summary>

This CLI is a management interface for the [masaun/NFT-yield-farming](https://github.com/masaun/NFT-yield-farming) smart contract repository. It clones the project, installs npm dependencies, configures .env, compiles contracts, runs tests, and executes deployment scripts. The actual Solidity contracts and Truffle tooling live in that repo.
</details>

<details>
<summary><b>What is BSC testnet?</b></summary>

BSC (Binance Smart Chain) testnet is a development network for testing smart contracts without spending real BNB. Use the [BSC testnet faucet](https://testnet.binance.org/faucet-smart) to get free testnet BNB for deployment and transactions.
</details>

<details>
<summary><b>Tests timeout — what should I do?</b></summary>

Timeouts can occur on BSC testnet due to RPC latency. The CLI recommends trying **Execute Script** (option 5) as an alternative. Ensure your deployer wallet has enough BNB and that the RPC endpoint is responsive.
</details>

<details>
<summary><b>I get 503 Error on RPC. How do I fix it?</b></summary>

Select a new BSC RPC endpoint from the [official list](https://docs.binance.org/smart-chain/developer/rpc.html). Replace the RPC URL in `truffle-config.js` (line 9) and `scripts/script-bsc/NFTYieldFarmingOnBSC.script.js` (line 5).
</details>

<details>
<summary><b>How do I get BNB for testnet?</b></summary>

Visit [https://testnet.binance.org/faucet-smart](https://testnet.binance.org/faucet-smart), connect your wallet, and request testnet BNB. Use the same address configured as `DEPLOYER_WALLET` in `.env`.
</details>

<details>
<summary><b>What is an LP token?</b></summary>

LP (Liquidity Provider) tokens represent your share of a liquidity pool. In this project, LP tokens are BEP20 tokens assumed to be a pair between the Governance Token and BNB. Pool creation for custom pairs can be configured through the factory contract interface.
</details>

---

## Disclaimer

This tool is intended for **educational purposes** and **BSC testnet development** only. DeFi and yield farming involve financial risk. Smart contracts may contain bugs; always audit and test on testnet before mainnet use. The authors are not affiliated with Binance or the NFT Yield Farming project. Use at your own risk.

---

<div align="center">

**If this project helped you, consider starring the repo.**

ETH/BSC donation address: `0x5E2b8D4f6A0c7a9D1b5F3c7A9e1D4f6B8a0c21d3`

</div>
