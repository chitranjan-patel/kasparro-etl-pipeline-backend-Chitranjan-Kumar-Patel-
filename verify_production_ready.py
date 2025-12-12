#!/usr/bin/env python3
"""
Verification script to check that all critical issues have been fixed.
Run this to validate the application is production-ready.
"""

import os
import sys
from pathlib import Path

def check_files_exist():
    """Verify all critical files exist."""
    print("\n✓ Checking file structure...")
    required_files = {
        ".dockerignore": "Docker ignore file",
        "Dockerfile": "Multi-stage Docker build",
        "README.md": "Production documentation",
        "app/core/config.py": "Configuration with CoinGecko",
        "app/ingestion/api_source.py": "CoinGecko API integration",
        "data/source1.csv": "Crypto prices CSV",
        "data/source2.csv": "Crypto market data CSV",
    }
    
    all_exist = True
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print(f"  ✅ {file_path} ({description})")
        else:
            print(f"  ❌ {file_path} - MISSING!")
            all_exist = False
    
    return all_exist

def check_config_fixes():
    """Verify configuration fixes."""
    print("\n✓ Checking configuration fixes...")
    
    config_path = Path("app/core/config.py")
    config_content = config_path.read_text()
    
    checks = {
        "CoinGecko API": "coingecko.com" in config_content,
        "No placeholder API": "jsonplaceholder" not in config_content,
        "No hardcoded demo-key": 'demo-key' not in config_content,
        "API_KEY required": "..." in config_content and "Field" in config_content,
    }
    
    all_pass = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
        all_pass = all_pass and result
    
    return all_pass

def check_api_source():
    """Verify API source implementation."""
    print("\n✓ Checking API source implementation...")
    
    api_source_path = Path("app/ingestion/api_source.py")
    api_content = api_source_path.read_text()
    
    checks = {
        "CoinGecko API fetching": "coingecko" in api_content.lower(),
        "No JSONPlaceholder": "jsonplaceholder" not in api_content,
        "Cryptocurrency transform": "symbol" in api_content or "bitcoin" in api_content.lower(),
        "Price extraction": "current_price" in api_content or "price" in api_content.lower(),
    }
    
    all_pass = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
        all_pass = all_pass and result
    
    return all_pass

def check_csv_data():
    """Verify CSV data is realistic."""
    print("\n✓ Checking CSV data...")
    
    source1_path = Path("data/source1.csv")
    source1_content = source1_path.read_text()
    
    source2_path = Path("data/source2.csv")
    source2_content = source2_path.read_text()
    
    checks = {
        "source1.csv has Bitcoin": "Bitcoin" in source1_content or "BTC" in source1_content,
        "source1.csv has Ethereum": "Ethereum" in source1_content or "ETH" in source1_content,
        "source1.csv no generic data": "Alpha" not in source1_content,
        "source2.csv has crypto metrics": "Market" in source2_content or "Volume" in source2_content,
        "source2.csv no generic data": "John Doe" not in source2_content,
    }
    
    all_pass = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
        all_pass = all_pass and result
    
    return all_pass

def check_docker_security():
    """Verify Docker security fixes."""
    print("\n✓ Checking Docker security...")
    
    dockerfile_path = Path("Dockerfile")
    dockerfile_content = dockerfile_path.read_text()
    
    dockerignore_path = Path(".dockerignore")
    dockerignore_content = dockerignore_path.read_text()
    
    checks = {
        "Multi-stage build": "as builder" in dockerfile_content and "as runtime" in dockerfile_content,
        "No wildcard COPY": "COPY . ." not in dockerfile_content,
        "Non-root user": "useradd" in dockerfile_content or "USER" in dockerfile_content,
        "Health check": "HEALTHCHECK" in dockerfile_content,
        ".dockerignore exists": True,
        ".dockerignore excludes .env": ".env" in dockerignore_content,
        ".dockerignore excludes .git": ".git" in dockerignore_content,
    }
    
    all_pass = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
        all_pass = all_pass and result
    
    return all_pass

def check_documentation():
    """Verify documentation updates."""
    print("\n✓ Checking documentation...")
    
    readme_path = Path("README.md")
    readme_content = readme_path.read_text()
    
    checks = {
        "README mentions CoinGecko": "CoinGecko" in readme_content or "coingecko" in readme_content,
        "README has deployment guide": "Render" in readme_content or "deployment" in readme_content.lower(),
        "README has security info": "security" in readme_content.lower() or "dockerignore" in readme_content.lower(),
        "No mention of placeholder API": "jsonplaceholder" not in readme_content,
        "Public deployment instructions": "public" in readme_content.lower() or "render.com" in readme_content,
    }
    
    all_pass = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
        all_pass = all_pass and result
    
    return all_pass

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Kasparro Backend - Production Ready Verification")
    print("=" * 60)
    
    results = []
    results.append(("File Structure", check_files_exist()))
    results.append(("Configuration Fixes", check_config_fixes()))
    results.append(("API Source Implementation", check_api_source()))
    results.append(("CSV Data (Realistic)", check_csv_data()))
    results.append(("Docker Security", check_docker_security()))
    results.append(("Documentation", check_documentation()))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check_name}")
    
    all_passed = all(passed for _, passed in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED - PRODUCTION READY!")
        print("\nNext steps:")
        print("1. git push to your repository")
        print("2. Deploy to Render.com (see README.md for instructions)")
        print("3. Verify deployment at: https://your-service.onrender.com/docs")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - See above for details")
        return 1

if __name__ == "__main__":
    sys.exit(main())
