"""Install the vizu-init.pth file to site-packages for auto-initialization.

This script copies the .pth file that enables zero-code auto-instrumentation.
Run after pip install: python -m vizu.install_pth

Or use the CLI command: vizu-install
"""

import os
import site
import sys


PTH_CONTENT = """import vizu.bootstrap; vizu.bootstrap._auto_init()
"""

PTH_FILENAME = "vizu-init.pth"


def get_site_packages():
    """Get the user's site-packages directory."""
    # Try user site first, then system site
    paths = []
    
    # User site-packages
    user_site = site.getusersitepackages()
    if user_site:
        paths.append(user_site)
    
    # System site-packages
    for path in site.getsitepackages():
        paths.append(path)
    
    # Also check where vizu itself is installed
    try:
        import vizu
        vizu_dir = os.path.dirname(vizu.__file__)
        site_packages = os.path.dirname(vizu_dir)
        if site_packages not in paths:
            paths.insert(0, site_packages)
    except ImportError:
        pass
    
    return paths


def install():
    """Install the .pth file to site-packages."""
    paths = get_site_packages()
    
    installed = False
    for site_packages in paths:
        if not os.path.isdir(site_packages):
            continue
            
        pth_path = os.path.join(site_packages, PTH_FILENAME)
        
        try:
            with open(pth_path, 'w') as f:
                f.write(PTH_CONTENT)
            print(f"✅ Installed {pth_path}")
            installed = True
            break
        except PermissionError:
            print(f"⚠️  Permission denied: {pth_path}")
            continue
        except Exception as e:
            print(f"⚠️  Failed to write {pth_path}: {e}")
            continue
    
    if not installed:
        print("❌ Could not install .pth file to any site-packages directory.")
        print("   Try running with sudo or in a virtual environment.")
        return False
    
    print("\n🎉 Vizu auto-instrumentation is now enabled!")
    print("   Set VIZU_ENABLED=true to activate tracing.")
    print("   Set VIZU_PROJECT_ID=<id> to specify your project.")
    return True


def uninstall():
    """Remove the .pth file from site-packages."""
    paths = get_site_packages()
    
    removed = False
    for site_packages in paths:
        pth_path = os.path.join(site_packages, PTH_FILENAME)
        if os.path.exists(pth_path):
            try:
                os.remove(pth_path)
                print(f"✅ Removed {pth_path}")
                removed = True
            except Exception as e:
                print(f"⚠️  Failed to remove {pth_path}: {e}")
    
    if not removed:
        print("ℹ️  No .pth file found to remove.")
    
    return removed


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Install Vizu auto-instrumentation .pth file"
    )
    parser.add_argument(
        "--uninstall", "-u",
        action="store_true",
        help="Uninstall the .pth file"
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true", 
        help="Check if .pth file is installed"
    )
    
    args = parser.parse_args()
    
    if args.check:
        paths = get_site_packages()
        found = False
        for site_packages in paths:
            pth_path = os.path.join(site_packages, PTH_FILENAME)
            if os.path.exists(pth_path):
                print(f"✅ Found: {pth_path}")
                found = True
        if not found:
            print("❌ .pth file not installed")
            print("   Run: vizu-install")
        return 0 if found else 1
    
    if args.uninstall:
        success = uninstall()
        return 0 if success else 1
    
    success = install()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
