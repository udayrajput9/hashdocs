# HashDocs - User & Testing Guide

Welcome to **HashDocs**, a Web3-based decentralized platform for generating, storing, and verifying certificates using blockchain technology.

This document serves as a comprehensive guide for users and testers to understand how to interact with the platform.

## 🚀 Prerequisites for Testing

Before you begin testing the platform, ensure you have the following set up:

1. **MetaMask Extension**: Install the [MetaMask browser extension](https://metamask.io/).
2. **Create a Wallet**: Set up a new wallet or import an existing one.
3. **Network Configuration**: Ensure you are connected to the correct testnet (e.g., Sepolia or Polygon Amoy) as specified by the platform.
4. **Testnet Funds**: **IMPORTANT:** HashDocs is a premium service. You will need at least **$0.0001** worth of cryptocurrency (e.g., MATIC or ETH depending on the chain) in your connected MetaMask wallet to successfully issue a certificate. You can obtain testnet funds from various online faucets if testing on a testnet.

## 🧪 Testing Workflow

Follow these steps to thoroughly test the functionality of HashDocs:

### 1. Connecting Your Wallet
- Go to the HashDocs homepage or dashboard.
- Click on the **"Connect Wallet"** button.
- MetaMask will prompt you to authorize the connection to the site.
- Once connected, your wallet address should be visible on the dashboard, confirming the integration is working.

### 2. Creating a Certificate Batch
- Navigate to the **Builder / Templates** section.
- Design your certificate using the provided builder tools.
- Go to the **Certificates** generation page.
- Enter the required student/recipient details (or upload a CSV file with details).

### 3. Issuing Certificates (Web3 Transaction)
- Click on **Generate / Issue Certificates**.
- MetaMask will pop up, asking you to confirm a blockchain transaction.
- **Note:** This step involves anchoring the certificates on the blockchain and pinning the data securely to IPFS (InterPlanetary File System).
- Review the gas fees and the premium charge. **Confirm** the transaction.
- Wait for the transaction to be mined and confirmed. Once successful, the certificate hashes are permanently stored on the blockchain!

### 4. Viewing and Verifying Certificates
- After successful issuance, a unique **QR Code** will be generated for each certificate.
- Scan the QR code or click the verification link on the certificate.
- The verification page will fetch the data from the decentralized IPFS storage and check the transaction hash on the blockchain.
- It will display the certificate details and confirm its authenticity with a *Verified* status.

## 🛑 Troubleshooting

- **MetaMask doesn't pop up:** Ensure your browser is not blocking pop-ups and that the MetaMask extension is unlocked.
- **Transaction Failed:** You might not have enough funds to cover the $0.0001 premium charge + network gas fees. Check your wallet balance.
- **Certificate not showing as verified instantly:** Blockchain transactions take a few seconds to process. Please wait a moment and refresh the verification page.
