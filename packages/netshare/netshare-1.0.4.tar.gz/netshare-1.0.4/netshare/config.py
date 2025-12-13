"""
NetShare Configuration
Security and application settings
"""

import os

class SecurityConfig:
    """Security-related configuration"""
    
    # Maximum file size to serve (in bytes) - 10GB default
    MAX_FILE_SIZE = 20 * 1024 * 1024 * 1024
    
    # Allowed file extensions (empty list = allow all)
    # Uncomment and populate to restrict file types
    ALLOWED_EXTENSIONS = []
    # ALLOWED_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.png', '.mp4']
    
    # Blocked file extensions (security-sensitive files)
    BLOCKED_EXTENSIONS = [
        '.exe', '.bat', '.cmd', '.sh', '.ps1', '.vbs', '.msi',
        '.scr', '.com', '.pif', '.reg', '.dll', '.sys'
    ]
    
    # Enable/disable directory listing
    ALLOW_DIRECTORY_LISTING = True
    
    # Enable/disable file downloads
    ALLOW_FILE_DOWNLOAD = True
    
    # Maximum path depth from shared folder root
    MAX_PATH_DEPTH = 20
    
    # Rate limiting (requests per minute per IP)
    RATE_LIMIT = 100
    
    # Enable detailed error messages (disable in production)
    DEBUG_ERRORS = False


class AppConfig:
    """Application configuration"""
    
    # Default server settings
    DEFAULT_PORT = 5000
    DEFAULT_HOST = '0.0.0.0'
    
    # Server identification
    SERVER_NAME = "NetShare"
    VERSION = "1.0.0"
    
    # QR Code settings
    QR_BOX_SIZE = 10
    QR_BORDER = 4
    
    # UI settings
    ITEMS_PER_PAGE = 100
    
    # Logging
    ENABLE_ACCESS_LOG = True
    LOG_FILE = "netshare.log"

    # Folder management settings
    FOLDERS_CONFIG_FILE = "shared_folders.json"
    MAX_SHARED_FOLDERS = 20


# Validate configuration on import
def validate_config():
    """Validate configuration settings"""
    if SecurityConfig.MAX_FILE_SIZE <= 0:
        raise ValueError("MAX_FILE_SIZE must be positive")
    
    if SecurityConfig.MAX_PATH_DEPTH <= 0:
        raise ValueError("MAX_PATH_DEPTH must be positive")
    
    if SecurityConfig.RATE_LIMIT <= 0:
        raise ValueError("RATE_LIMIT must be positive")
    
    # Ensure blocked extensions are lowercase
    SecurityConfig.BLOCKED_EXTENSIONS = [
        ext.lower() if ext.startswith('.') else f'.{ext.lower()}'
        for ext in SecurityConfig.BLOCKED_EXTENSIONS
    ]
    
    # Ensure allowed extensions are lowercase
    if SecurityConfig.ALLOWED_EXTENSIONS:
        SecurityConfig.ALLOWED_EXTENSIONS = [
            ext.lower() if ext.startswith('.') else f'.{ext.lower()}'
            for ext in SecurityConfig.ALLOWED_EXTENSIONS
        ]


# Run validation
validate_config()
