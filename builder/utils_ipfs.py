import hashlib
import time

def upload_to_ipfs(file_bytes, filename="cert.png"):
    """
    Mock IPFS upload for local development (no API keys required).
    In production, replace this with Pinata or Web3.Storage HTTP API calls.
    Returns a deterministic IPFS CID (Qm...) representing the content hash.
    """
    # Simulate network delay for realism
    time.sleep(0.5) 
    
    # Generate a real SHA-256 hash of the content to mimic IPFS CIDv0
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()
    
    # IPFS CIDv0 typically starts with Qm and is 46 chars long (base58)
    mock_cid = "Qm" + sha256_hash[:44]
    
    return mock_cid, f"https://ipfs.io/ipfs/{mock_cid}"
