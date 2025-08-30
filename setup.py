"""
Quick Setup Script for FastAPI Professional Project

This script helps set up the project quickly for development or demonstration.
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and print the result."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"   Error: {e.stderr.strip()}")
        return False
    return True

def main():
    """Main setup function."""
    print("🚀 FastAPI Professional Project Setup")
    print("="*50)
    
    # Check if we're in the right directory
    if not os.path.exists("app/main.py"):
        print("❌ Please run this script from the project root directory")
        return
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 10):
        print("❌ Python 3.10+ is required")
        return
    
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")
    
    # Create .env if it doesn't exist
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            run_command("copy .env.example .env", "Creating .env file")
        else:
            print("⚠️  No .env file found. Please create one based on .env.example")
    
    print("\n🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Start the server: python run.py")
    print("2. View API docs: http://127.0.0.1:8000/docs")
    print("3. Test the API: python test_api.py")
    print("4. Run tests: pytest tests/ -v")
    
    print("\n📖 Key Files:")
    print("   app/main.py          - Main FastAPI application")
    print("   app/core/config.py   - Configuration management")
    print("   app/api/routes/      - API endpoint definitions")
    print("   tests/               - Test suite")
    print("   README.md            - Complete documentation")
    print("   DEPLOYMENT.md        - Production deployment guide")

if __name__ == "__main__":
    main()
