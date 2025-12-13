"""Setup script for vizu package with proper .pth file installation."""

from setuptools import setup
from setuptools.command.install import install
import os
import shutil


class PostInstallCommand(install):
    """Post-installation hook to install .pth file to site-packages."""
    
    def run(self):
        install.run(self)
        
        # Find site-packages directory
        for path in self.get_outputs():
            if 'site-packages' in path and '__init__.py' in path:
                site_packages = os.path.dirname(os.path.dirname(path))
                break
        else:
            print("Warning: Could not find site-packages directory")
            return
        
        # Copy .pth file to site-packages
        pth_source = os.path.join(os.path.dirname(__file__), 'vizu-init.pth')
        pth_dest = os.path.join(site_packages, 'vizu-init.pth')
        
        try:
            shutil.copy2(pth_source, pth_dest)
            print(f"✅ Installed {pth_dest}")
        except Exception as e:
            print(f"⚠️  Failed to install .pth file: {e}")


setup(
    cmdclass={
        'install': PostInstallCommand,
    }
)
