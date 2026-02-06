"""
Generate Secure Secret Keys for ORBIT
Creates cryptographically secure random keys for production use
"""

import secrets
import sys

def generate_secret_key(length=32):
    """Generate a URL-safe secret key"""
    return secrets.token_urlsafe(length)

def generate_hex_key(length=32):
    """Generate a hexadecimal secret key"""
    return secrets.token_hex(length)

def main():
    print("=" * 70)
    print("🔐 ORBIT SECRET KEY GENERATOR")
    print("=" * 70)
    print()
    print("Generating cryptographically secure secret keys...")
    print()
    
    # Generate keys
    secret_key = generate_secret_key(32)
    jwt_secret = generate_secret_key(32)
    encryption_key = generate_secret_key(32)
    
    # Display keys
    print("📋 COPY THESE TO YOUR .env FILE:")
    print("-" * 70)
    print()
    print(f"SECRET_KEY={secret_key}")
    print(f"JWT_SECRET_KEY={jwt_secret}")
    print(f"ENCRYPTION_KEY={encryption_key}")
    print()
    print("-" * 70)
    print()
    
    # Additional keys for other services
    print("🔧 ADDITIONAL KEYS (Optional):")
    print("-" * 70)
    print()
    print(f"N8N_ENCRYPTION_KEY={generate_secret_key(32)}")
    print(f"N8N_JWT_SECRET={generate_secret_key(32)}")
    print(f"BACKUP_ENCRYPTION_KEY={generate_secret_key(32)}")
    print(f"GRAFANA_SECRET_KEY={generate_secret_key(32)}")
    print()
    print("-" * 70)
    print()
    
    # Security notes
    print("🔒 SECURITY NOTES:")
    print("-" * 70)
    print("✅ All keys are cryptographically secure (256-bit)")
    print("✅ Keys are URL-safe (can be used in URLs/headers)")
    print("✅ Keys are unique and randomly generated")
    print()
    print("⚠️  IMPORTANT:")
    print("   • Never commit these keys to version control")
    print("   • Use different keys for dev/staging/production")
    print("   • Rotate keys periodically (every 90 days)")
    print("   • Store production keys in secure vault (AWS Secrets Manager, etc.)")
    print()
    print("=" * 70)
    print()
    
    # Save to file option
    if len(sys.argv) > 1 and sys.argv[1] == "--save":
        filename = ".env.secrets"
        with open(filename, "w") as f:
            f.write("# Generated Secret Keys - DO NOT COMMIT TO GIT\n")
            f.write(f"SECRET_KEY={secret_key}\n")
            f.write(f"JWT_SECRET_KEY={jwt_secret}\n")
            f.write(f"ENCRYPTION_KEY={encryption_key}\n")
            f.write(f"N8N_ENCRYPTION_KEY={generate_secret_key(32)}\n")
            f.write(f"N8N_JWT_SECRET={generate_secret_key(32)}\n")
            f.write(f"BACKUP_ENCRYPTION_KEY={generate_secret_key(32)}\n")
            f.write(f"GRAFANA_SECRET_KEY={generate_secret_key(32)}\n")
        
        print(f"💾 Keys saved to: {filename}")
        print(f"⚠️  Remember to add {filename} to .gitignore!")
        print()

if __name__ == "__main__":
    main()
