"""
Payment module for IntelliComm Protocol with x402 integration.

This module provides payment configuration and utilities for integrating
x402 payment protocol with FastAPI-based HTTP servers.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class PaymentConfig:
    """Configuration for agent payment requirements."""
    required: bool = False
    price: Optional[str] = None  # e.g., "$0.001"
    pay_to_address: Optional[str] = None  # Wallet address to receive payment
    network: Optional[str] = None  # e.g., "base-sepolia", "base-mainnet"
    facilitator_url: Optional[str] = None  # X402 facilitator URL

    def __post_init__(self):
        """Validate payment configuration."""
        if self.required:
            if not self.price:
                raise ValueError("Price must be specified when payment is required")
            if not self.pay_to_address:
                raise ValueError("Payment address must be specified when payment is required")
            if not self.network:
                # Use default network from environment or base-sepolia
                self.network = os.getenv("NETWORK", "base-sepolia")
            if not self.facilitator_url:
                # Use default facilitator URL
                self.facilitator_url = os.getenv(
                    "FACILITATOR_URL", 
                    "https://x402.org/facilitator"
                )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "required": self.required,
            "price": self.price,
            "pay_to_address": self.pay_to_address,
            "network": self.network,
            "facilitator_url": self.facilitator_url
        }


def load_wallet_config() -> Dict[str, str]:
    """
    Load wallet configuration from environment variables.
    
    Returns:
        Dictionary with wallet configuration
        
    Raises:
        ValueError: If required environment variables are missing
    """
    private_key = os.getenv("CLIENT_PRIVATE_KEY") or os.getenv("WALLET_PRIVATE_KEY")
    if not private_key:
        raise ValueError(
            "CLIENT_PRIVATE_KEY or WALLET_PRIVATE_KEY environment variable is required for payment client"
        )
    
    return {
        "private_key": private_key,
        "network": os.getenv("NETWORK", "base-sepolia"),
        "facilitator_url": os.getenv("FACILITATOR_URL", "https://x402.org/facilitator")
    }


def get_payment_address() -> str:
    """
    Get the payment receiving address from environment variables.
    
    Returns:
        Payment receiving wallet address
        
    Raises:
        ValueError: If PAYMENT_ADDRESS is not set
    """
    address = os.getenv("SERVER_WALLET_ADDRESS") or os.getenv("PAYMENT_ADDRESS")
    if not address:
        raise ValueError(
            "SERVER_WALLET_ADDRESS or PAYMENT_ADDRESS environment variable is required for payment server"
        )
    return address


def validate_payment_config(config: PaymentConfig) -> bool:
    """
    Validate a payment configuration.
    
    Args:
        config: PaymentConfig to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    if not config.required:
        return True
        
    if not config.price:
        raise ValueError("Price is required when payment is enabled")
        
    if not config.pay_to_address:
        raise ValueError("Payment address is required when payment is enabled")
        
    # Validate address format (basic check for Ethereum address)
    if not config.pay_to_address.startswith("0x") or len(config.pay_to_address) != 42:
        raise ValueError(
            f"Invalid payment address format: {config.pay_to_address}. "
            "Must be a valid Ethereum address (0x...)"
        )
        
    # Validate network
    valid_networks = [
        "base-sepolia", "base-mainnet", 
        "ethereum-mainnet", "ethereum-sepolia",
        "solana-devnet", "solana-mainnet"
    ]
    if config.network not in valid_networks:
        raise ValueError(
            f"Invalid network: {config.network}. "
            f"Must be one of: {', '.join(valid_networks)}"
        )
        
    # Validate price format
    if not config.price.startswith("$"):
        raise ValueError(
            f"Invalid price format: {config.price}. "
            "Must start with $ (e.g., '$0.001')"
        )
        
    try:
        price_value = float(config.price[1:])
        if price_value <= 0:
            raise ValueError("Price must be greater than 0")
    except ValueError:
        raise ValueError(
            f"Invalid price value: {config.price}. "
            "Must be a valid number (e.g., '$0.001')"
        )
        
    return True


def create_payment_middleware_config(config: PaymentConfig, path: str) -> Dict[str, Any]:
    """
    Create configuration for x402 FastAPI middleware.
    
    Args:
        config: PaymentConfig object
        path: API path to protect
        
    Returns:
        Dictionary with middleware configuration
    """
    if not config.required:
        return None
        
    return {
        "path": path,
        "price": config.price,
        "pay_to_address": config.pay_to_address,
        "network": config.network,
        "facilitator_url": config.facilitator_url
    }

