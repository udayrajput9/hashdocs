# HashDocs - Developer Guide

Welcome to the technical documentation for **HashDocs**. This document explains the architecture, tech stack, and the overall workflow of the project, serving as a guide for developers wanting to contribute to or understand the inner workings of the platform.

## 🏗️ Architecture & Tech Stack

HashDocs is a full-stack Hybrid Web2/Web3 application built utilizing the following technologies:

- **Backend Framework**: Django (Python)
- **Database**: SQLite3 (default for local development, can be migrated to PostgreSQL for production)
- **Frontend**: HTML, CSS, JavaScript (Vanilla JS / jQuery depending on the specific templates)
- **Web3 Integration**: Web3.js / Ethers.js
- **Wallet Provider**: MetaMask
- **Decentralized Storage**: IPFS (InterPlanetary File System) for immutable certificate storage
- **Smart Contracts / Blockchain**: Compatible with EVM-based networks like Ethereum, Polygon, or local testnets (Hardhat/Ganache)

## 📂 Project Structure

- `hashdocs/`: The main Django project configuration directory (contains `settings.py`, `urls.py`).
- `accounts/`: Handles user authentication, registration, user profiles, and wallet address mapping.
- `api/`: REST API endpoints to facilitate frontend-backend communication.
- `builder/`: Contains the logic for the certificate template builder tool (UI rendering and backend payload processing).
- `certificates/`: The core module managing the generation and issuance records of certificates.
- `verification/`: Holds the critical logic used to verify a certificate's authenticity against IPFS and the anchored blockchain hashes.
- `templates/`: HTML files for frontend layout rendering (Dashboard, Application tools, Builder, Verification pages).
- `static/, media/`: CSS, JS, Images, and user-uploaded templates.

## ⚙️ Core Functionality & Workflow

HashDocs combines traditional web forms with Web3 concepts to securely issue and attest generated documents.

### 1. File Generation & IPFS Pinning
When an issuer creates a certificate template and provides recipient data (manual entry or CSV), HashDocs generates the certificate files. To ensure immutability and continuous availability natively suited for block explorers, these images and associated metadata are uploaded to **IPFS**, which returns a unique Content Identifier (CID).

### 2. Blockchain Anchoring
To prove the exact time and authenticity of the document, HashDocs executes a "Certificate Anchoring" transaction:
- The web app interfaces with the user's **MetaMask** wallet.
- The frontend prompts the user to sign and pay for a transaction.
- The transaction anchors the certificate's unique cryptographic hash (often the CID or SHA-256 hash) onto a Smart Contract.
- **Premium Constraint**: Certificates will not be successfully issued unless the user establishes the transaction and has sufficient balance (network gas fees + a specific premium charge of $0.0001 equivalent in the native token).

### 3. Circular Generation Context (QR Codes)
Once the transaction is confirmed, HashDocs creates a QR code natively embedding both:
- The final blockchain Transaction Hash (TxHash).
- The IPFS CID for file retrieval.
This securely embedded QR code provides a direct validation layer directly attached to the final certificate format. 

### 4. Verification Process
When someone scans the QR code or uses the verification link provided:
- The system reads the blockchain transaction corresponding to the hash to verify the timestamp and issuer.
- It fetches the exact unalterable file pinned on the IPFS network via its CID.
- If the retrieved file integrity matches what is anchored, the document is marked as **Verified**.

## 🚀 Setting Up the Development Environment

1. **Clone the repository** and navigate to the project root directory.
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows run: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply Database Migrations**:
   Setup the local SQLite3 database or configure your own.
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```
6. **Frontend/Web3 Setup**: Ensure you have a browser with MetaMask installed and configured to connect to your intended developer network (Localhost 8545, Sepolia, Polygon Amoy, etc.).
