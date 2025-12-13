"""
NetShare - Secure Network File Sharing Tool

A secure, Python-based network file sharing tool that allows you to share
folders over your local WiFi network with any device (Android, iOS, PC).
"""

__version__ = "1.0.4"
__author__ = "NetShare Contributors"
__license__ = "GPL-3.0"

from netshare.app import main

__all__ = ['main', '__version__']
