#!/usr/bin/env python3
"""
NetShare - Simple Network File Sharing Tool
Share Windows folders with Android devices over WiFi
"""

import os
import socket
import sys
import threading
import webbrowser
import logging
from pathlib import Path
from urllib.parse import quote, unquote
from functools import wraps
from collections import defaultdict
from time import time

import qrcode
from flask import Flask, render_template, send_from_directory, abort, request, jsonify

# Import configuration
try:
    from netshare.config import SecurityConfig, AppConfig
except ImportError:
    # Fallback if config.py is not available
    class SecurityConfig:
        MAX_FILE_SIZE = 20 * 1024 * 1024 * 1024
        BLOCKED_EXTENSIONS = ['.exe', '.bat', '.cmd', '.sh', '.ps1']
        ALLOW_DIRECTORY_LISTING = True
        ALLOW_FILE_DOWNLOAD = True
        MAX_PATH_DEPTH = 20
        RATE_LIMIT = 100
        DEBUG_ERRORS = False
        ALLOWED_EXTENSIONS = []
    
    class AppConfig:
        DEFAULT_PORT = 5000
        DEFAULT_HOST = '0.0.0.0'
        SERVER_NAME = "NetShare"
        VERSION = "1.0.0"
        ENABLE_ACCESS_LOG = True

# Try to import tkinter for GUI (optional on some systems)
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    HAS_GUI = True
except ImportError:
    HAS_GUI = False
    print("Warning: tkinter not available. GUI folder selection disabled.")

app = Flask(__name__)

# Configure logging
if AppConfig.ENABLE_ACCESS_LOG:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
else:
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())

# Rate limiting storage
rate_limit_storage = defaultdict(list)


def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not SecurityConfig.RATE_LIMIT:
            return f(*args, **kwargs)
        
        ip = request.remote_addr
        now = time()
        
        # Clean old requests
        rate_limit_storage[ip] = [
            req_time for req_time in rate_limit_storage[ip]
            if now - req_time < 60
        ]
        
        # Check rate limit
        if len(rate_limit_storage[ip]) >= SecurityConfig.RATE_LIMIT:
            logger.warning(f"Rate limit exceeded for {ip}")
            abort(429)  # Too Many Requests
        
        rate_limit_storage[ip].append(now)
        return f(*args, **kwargs)
    
    return decorated_function


def is_safe_path(base_path, target_path):
    """Verify that target_path is within base_path (prevents path traversal)"""
    base_path = os.path.abspath(base_path)
    target_path = os.path.abspath(target_path)
    
    # Check if target is within base
    if not target_path.startswith(base_path):
        return False
    
    # Check path depth
    relative_path = os.path.relpath(target_path, base_path)
    depth = len(Path(relative_path).parts)
    if depth > SecurityConfig.MAX_PATH_DEPTH:
        logger.warning(f"Path depth exceeded: {relative_path}")
        return False
    
    return True


def is_allowed_file(filename):
    """Check if file extension is allowed"""
    ext = os.path.splitext(filename)[1].lower()
    
    # Check blocked extensions first
    if ext in SecurityConfig.BLOCKED_EXTENSIONS:
        logger.warning(f"Blocked file extension: {ext}")
        return False
    
    # If allowed list is specified, check it
    if SecurityConfig.ALLOWED_EXTENSIONS:
        return ext in SecurityConfig.ALLOWED_EXTENSIONS
    
    return True


def get_system_drives():
    """Get list of available drives (Windows) or root directories (Unix)"""
    import platform

    if platform.system() == 'Windows':
        # Windows: Get available drives
        import string
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                try:
                    # Try to access to verify it's available
                    os.listdir(drive)
                    drives.append({
                        'name': f"{letter}: Drive",
                        'path': drive,
                        'accessible': True
                    })
                except (PermissionError, OSError):
                    drives.append({
                        'name': f"{letter}: Drive",
                        'path': drive,
                        'accessible': False
                    })
        return drives
    else:
        # Unix/Linux/Mac: Start from home directory or root
        home = os.path.expanduser("~")
        return [{
            'name': 'Home',
            'path': home,
            'accessible': True
        }, {
            'name': 'Root',
            'path': '/',
            'accessible': os.access('/', os.R_OK)
        }]


def list_directories(path):
    """List subdirectories in the given path"""
    directories = []

    try:
        # Normalize path
        path = os.path.abspath(path)

        if not os.path.exists(path):
            return None, "Path does not exist"

        if not os.path.isdir(path):
            return None, "Path is not a directory"

        # Get parent directory
        parent = os.path.dirname(path) if path != os.path.dirname(path) else None

        # List all items in directory
        try:
            items = os.listdir(path)
        except PermissionError:
            return None, "Permission denied"

        # Filter to only directories
        for item in sorted(items):
            item_path = os.path.join(path, item)
            try:
                if os.path.isdir(item_path):
                    accessible = os.access(item_path, os.R_OK)
                    directories.append({
                        'name': item,
                        'path': item_path,
                        'accessible': accessible
                    })
            except (OSError, PermissionError):
                # Skip items we can't access
                continue

        return {
            'current_path': path,
            'parent': parent,
            'directories': directories
        }, None

    except Exception as e:
        logger.error(f"Error listing directories in {path}: {str(e)}")
        return None, str(e)


def validate_folder_path(path):
    """Validate folder path for security and accessibility"""
    import json

    # Normalize path
    path = os.path.abspath(path)

    # Check if exists
    if not os.path.exists(path):
        return False, "Path does not exist"

    # Check if directory
    if not os.path.isdir(path):
        return False, "Path is not a directory"

    # Check read permissions
    if not os.access(path, os.R_OK):
        return False, "No read permission for this directory"

    # Check if already shared
    if path in config.shared_folders:
        return False, "Folder is already shared"

    # Check for parent-child conflicts
    for existing in config.shared_folders:
        if path.startswith(existing + os.sep):
            return False, f"This folder is inside already shared folder: {os.path.basename(existing)}"
        if existing.startswith(path + os.sep):
            return False, f"Shared folder '{os.path.basename(existing)}' is inside this folder"

    # Check max folders limit
    if len(config.shared_folders) >= AppConfig.MAX_SHARED_FOLDERS:
        return False, f"Maximum of {AppConfig.MAX_SHARED_FOLDERS} folders allowed"

    return True, "Valid"


def save_folders_to_file():
    """Save shared folders list to JSON file"""
    import json

    try:
        config_path = os.path.join(os.path.dirname(__file__), AppConfig.FOLDERS_CONFIG_FILE)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config.shared_folders, f, indent=2)
        logger.info(f"Saved {len(config.shared_folders)} folders to {config_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save folders: {e}")
        return False


def load_folders_from_file():
    """Load shared folders list from JSON file"""
    import json

    try:
        config_path = os.path.join(os.path.dirname(__file__), AppConfig.FOLDERS_CONFIG_FILE)
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                folders = json.load(f)

            # Validate each folder still exists
            valid_folders = []
            for folder in folders:
                if os.path.isdir(folder):
                    valid_folders.append(folder)
                else:
                    logger.warning(f"Skipping non-existent folder from config: {folder}")

            config.shared_folders = valid_folders
            logger.info(f"Loaded {len(valid_folders)} folders from {config_path}")
            return True
    except Exception as e:
        logger.error(f"Failed to load folders: {e}")

    return False


# Global configuration
class Config:
    """Application configuration"""
    shared_folders = []
    server_port = 5000
    host = '0.0.0.0'
    
config = Config()


def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def generate_qr_code(url, output_path=None):
    """Generate QR code for the given URL

    Args:
        url: The URL to encode in the QR code
        output_path: Optional custom output path (if None, uses default netshare_qr.png in module directory)

    Returns:
        str: Path to the generated QR code PNG file
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Determine output path
    if output_path is None:
        qr_path = os.path.join(os.path.dirname(__file__), 'netshare_qr.png')
    else:
        # Convert relative paths to absolute based on current working directory
        qr_path = output_path if os.path.isabs(output_path) else os.path.abspath(output_path)

    # Ensure directory exists
    qr_dir = os.path.dirname(qr_path)
    if qr_dir:  # Only create directory if path has a directory component
        os.makedirs(qr_dir, exist_ok=True)

    # Save as PNG
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_path)

    # Print to terminal
    print("\n" + "="*50)
    print("Scan this QR code with your mobile device:")
    print("="*50)
    qr.print_ascii(invert=True)
    print("="*50)
    print(f"QR code saved to: {qr_path}")

    return qr_path


def format_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def get_file_info(filepath):
    """Get file information including size and type"""
    stat_info = os.stat(filepath)
    return {
        'size': format_size(stat_info.st_size),
        'size_bytes': stat_info.st_size,
        'is_dir': os.path.isdir(filepath)
    }


@app.route('/')
@rate_limit
def index():
    """Home page showing all shared folders"""
    folders = []
    for folder_path in config.shared_folders:
        if os.path.exists(folder_path):
            folders.append({
                'name': os.path.basename(folder_path),
                'path': folder_path,
                'full_path': folder_path
            })
    
    return render_template('index.html', 
                         folders=folders,
                         server_url=f"http://{get_local_ip()}:{config.server_port}")


@app.route('/browse/<int:folder_index>')
@app.route('/browse/<int:folder_index>/<path:subpath>')
@rate_limit
def browse(folder_index, subpath=''):
    """Browse files in a shared folder"""
    if folder_index >= len(config.shared_folders):
        logger.warning(f"Invalid folder index: {folder_index}")
        abort(404)
    
    base_folder = config.shared_folders[folder_index]
    target_path = os.path.join(base_folder, subpath)
    
    # Security: ensure we're still within the shared folder
    if not is_safe_path(base_folder, target_path):
        logger.warning(f"Path traversal attempt: {target_path}")
        abort(403)
    
    if not os.path.exists(target_path):
        abort(404)
    
    # If it's a file, serve it
    if os.path.isfile(target_path):
        # Check if file download is allowed
        if not SecurityConfig.ALLOW_FILE_DOWNLOAD:
            logger.warning(f"File download disabled: {target_path}")
            abort(403)
        
        # Check file extension
        if not is_allowed_file(target_path):
            logger.warning(f"Blocked file access: {target_path}")
            abort(403)
        
        # Check file size
        file_size = os.path.getsize(target_path)
        if file_size > SecurityConfig.MAX_FILE_SIZE:
            logger.warning(f"File too large: {target_path} ({file_size} bytes)")
            abort(413)  # Request Entity Too Large
        
        logger.info(f"Serving file: {target_path} to {request.remote_addr}")
        
        return send_from_directory(
            os.path.dirname(target_path),
            os.path.basename(target_path),
            as_attachment=True
        )
    
    # If it's a directory, list contents
    if not SecurityConfig.ALLOW_DIRECTORY_LISTING:
        logger.warning(f"Directory listing disabled: {target_path}")
        abort(403)
    
    items = []
    try:
        for item_name in sorted(os.listdir(target_path)):
            item_path = os.path.join(target_path, item_name)
            try:
                # Skip if file extension is blocked
                if os.path.isfile(item_path) and not is_allowed_file(item_path):
                    continue
                
                info = get_file_info(item_path)
                items.append({
                    'name': item_name,
                    'is_dir': info['is_dir'],
                    'size': info['size'],
                    'size_bytes': info['size_bytes']
                })
            except (OSError, PermissionError):
                # Skip files we can't access
                continue
    except (OSError, PermissionError) as e:
        error_msg = "Cannot access folder" if not SecurityConfig.DEBUG_ERRORS else str(e)
        return render_template('error.html', error=error_msg), 403
    
    # Build breadcrumb navigation
    breadcrumbs = []
    if subpath:
        parts = subpath.split(os.sep)
        current_path = ''
        for part in parts:
            current_path = os.path.join(current_path, part) if current_path else part
            breadcrumbs.append({
                'name': part,
                'path': current_path
            })
    
    return render_template('browse.html',
                         folder_index=folder_index,
                         folder_name=os.path.basename(base_folder),
                         current_path=subpath,
                         breadcrumbs=breadcrumbs,
                         items=items)


@app.route('/upload/<int:folder_index>', methods=['POST'])
@app.route('/upload/<int:folder_index>/<path:subpath>', methods=['POST'])
@rate_limit
def upload_file(folder_index, subpath=''):
    """Handle file upload to a shared folder"""
    try:
        # Validate folder index
        if folder_index >= len(config.shared_folders):
            logger.warning(f"Invalid folder index: {folder_index}")
            return jsonify({
                'success': False,
                'message': 'Invalid folder index'
            }), 404

        base_folder = config.shared_folders[folder_index]
        target_dir = os.path.join(base_folder, subpath)

        # Security: ensure we're still within the shared folder
        if not is_safe_path(base_folder, target_dir):
            logger.warning(f"Path traversal attempt in upload: {target_dir}")
            return jsonify({
                'success': False,
                'message': 'Invalid path'
            }), 403

        # Verify target directory exists
        if not os.path.exists(target_dir) or not os.path.isdir(target_dir):
            return jsonify({
                'success': False,
                'message': 'Target directory does not exist'
            }), 404

        # Check if file was included in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file provided'
            }), 400

        file = request.files['file']

        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400

        # Sanitize filename to prevent path traversal
        filename = os.path.basename(file.filename)
        if not filename or filename.startswith('.'):
            return jsonify({
                'success': False,
                'message': 'Invalid filename'
            }), 400

        # Build target file path
        target_file_path = os.path.join(target_dir, filename)

        # Final safety check
        if not is_safe_path(base_folder, target_file_path):
            logger.warning(f"Path traversal attempt via filename: {filename}")
            return jsonify({
                'success': False,
                'message': 'Invalid filename'
            }), 403

        # Check if file already exists
        if os.path.exists(target_file_path):
            return jsonify({
                'success': False,
                'message': f'File "{filename}" already exists'
            }), 409  # Conflict

        # Check file size (read from content-length header if available)
        content_length = request.content_length
        if content_length and content_length > SecurityConfig.MAX_FILE_SIZE:
            logger.warning(f"Upload too large: {content_length} bytes")
            return jsonify({
                'success': False,
                'message': f'File too large. Maximum size is {format_size(SecurityConfig.MAX_FILE_SIZE)}'
            }), 413  # Request Entity Too Large

        # Save the file
        try:
            file.save(target_file_path)
            file_size = os.path.getsize(target_file_path)

            # Double-check size after saving
            if file_size > SecurityConfig.MAX_FILE_SIZE:
                os.remove(target_file_path)
                logger.warning(f"Upload exceeded size limit: {file_size} bytes")
                return jsonify({
                    'success': False,
                    'message': f'File too large. Maximum size is {format_size(SecurityConfig.MAX_FILE_SIZE)}'
                }), 413

            logger.info(f"File uploaded: {target_file_path} ({format_size(file_size)}) from {request.remote_addr}")

            return jsonify({
                'success': True,
                'message': f'Successfully uploaded "{filename}"',
                'filename': filename,
                'size': format_size(file_size)
            }), 200

        except Exception as e:
            logger.error(f"Error saving uploaded file: {str(e)}")
            # Clean up if file was partially created
            if os.path.exists(target_file_path):
                try:
                    os.remove(target_file_path)
                except:
                    pass
            return jsonify({
                'success': False,
                'message': 'Failed to save file'
            }), 500

    except Exception as e:
        logger.error(f"Error in upload handler: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@app.route('/api/folders', methods=['GET'])
@rate_limit
def api_folders():
    """API endpoint to get list of shared folders"""
    folders = []
    for idx, folder_path in enumerate(config.shared_folders):
        if os.path.exists(folder_path):
            folders.append({
                'index': idx,
                'name': os.path.basename(folder_path),
                'path': folder_path
            })
    return jsonify(folders)


@app.route('/qr-code')
@rate_limit
def get_qr_code():
    """Serve the QR code image"""
    qr_path = os.path.join(os.path.dirname(__file__), 'netshare_qr.png')

    if not os.path.exists(qr_path):
        # Regenerate if missing
        local_ip = get_local_ip()
        url = f"http://{local_ip}:{config.server_port}"
        qr_path = generate_qr_code(url)

    return send_from_directory(
        os.path.dirname(qr_path),
        os.path.basename(qr_path),
        mimetype='image/png'
    )


@app.route('/api/browse-filesystem')
@rate_limit
def api_browse_filesystem():
    """Browse server filesystem for folder selection"""
    try:
        path = request.args.get('path', '').strip()

        # If no path specified, return drives/roots
        if not path:
            drives = get_system_drives()
            return jsonify({
                'success': True,
                'drives': drives,
                'current_path': None,
                'parent': None,
                'directories': []
            }), 200

        # List directories in the specified path
        result, error = list_directories(path)

        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 400

        return jsonify({
            'success': True,
            'current_path': result['current_path'],
            'parent': result['parent'],
            'directories': result['directories'],
            'drives': []
        }), 200

    except Exception as e:
        logger.error(f"Error browsing filesystem: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@app.route('/api/folders', methods=['POST'])
@rate_limit
def api_add_folder():
    """Add a new shared folder"""
    try:
        data = request.get_json()

        if not data or 'path' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing path parameter'
            }), 400

        folder_path = data['path'].strip()

        # Validate path
        is_valid, message = validate_folder_path(folder_path)

        if not is_valid:
            logger.warning(f"Invalid folder add attempt: {folder_path} - {message} from {request.remote_addr}")
            return jsonify({
                'success': False,
                'message': message
            }), 400

        # Add to shared folders
        config.shared_folders.append(folder_path)

        # Save to file for persistence
        save_folders_to_file()

        logger.info(f"Folder added: {folder_path} from {request.remote_addr}")

        return jsonify({
            'success': True,
            'message': f'Successfully added folder: {os.path.basename(folder_path)}',
            'folders': [
                {'index': idx, 'name': os.path.basename(p), 'path': p}
                for idx, p in enumerate(config.shared_folders)
            ]
        }), 200

    except Exception as e:
        logger.error(f"Error adding folder: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


@app.route('/api/folders/<int:folder_index>', methods=['DELETE'])
@rate_limit
def api_remove_folder(folder_index):
    """Remove a shared folder by index"""
    try:
        if folder_index < 0 or folder_index >= len(config.shared_folders):
            return jsonify({
                'success': False,
                'message': 'Invalid folder index'
            }), 400

        removed_path = config.shared_folders.pop(folder_index)

        # Save to file for persistence
        save_folders_to_file()

        logger.info(f"Folder removed: {removed_path} from {request.remote_addr}")

        return jsonify({
            'success': True,
            'message': f'Successfully removed folder: {os.path.basename(removed_path)}',
            'folders': [
                {'index': idx, 'name': os.path.basename(p), 'path': p}
                for idx, p in enumerate(config.shared_folders)
            ]
        }), 200

    except Exception as e:
        logger.error(f"Error removing folder: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500


def select_folders_gui():
    """GUI for selecting folders to share"""
    if not HAS_GUI:
        print("Error: GUI not available. Please use command-line mode.")
        return []
    
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    folders = []
    while True:
        folder = filedialog.askdirectory(
            title="Select a folder to share (Cancel to finish)"
        )
        if not folder:
            break
        folders.append(folder)
        
        result = messagebox.askyesno(
            "Add More?",
            f"Added: {folder}\n\nDo you want to add another folder?"
        )
        if not result:
            break
    
    root.destroy()
    return folders


def start_server(port=5000):
    """Start the Flask server"""
    local_ip = get_local_ip()
    url = f"http://{local_ip}:{port}"
    
    print("\n" + "="*60)
    print(f"NetShare Server Started!")
    print("="*60)
    print(f"Local URL: {url}")
    print(f"Sharing {len(config.shared_folders)} folder(s)")
    for idx, folder in enumerate(config.shared_folders):
        print(f"  [{idx}] {folder}")
    print("="*60)
    
    # Generate QR code
    generate_qr_code(url)
    
    print("\nTo stop the server, press Ctrl+C")
    print("="*60 + "\n")
    
    # Try to open browser
    try:
        threading.Timer(1.5, lambda: webbrowser.open(url)).start()
    except:
        pass
    
    # Start Flask server
    app.run(host=config.host, port=port, debug=False, threaded=True)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='NetShare - Share folders over local network',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  netshare --gui                    # Use GUI to select folders
  netshare --folder /path/to/share  # Share specific folder
  netshare --folder "C:\\Users\\Documents" --port 8000
  netshare --url https://example.com                    # Generate QR code for URL
  netshare --url https://example.com --output qr.png   # Generate QR with custom filename
        """
    )
    
    parser.add_argument('--gui', action='store_true',
                       help='Use GUI to select folders')
    parser.add_argument('--folder', '-f', action='append',
                       help='Folder to share (can be specified multiple times)')
    parser.add_argument('--port', '-p', type=int, default=5000,
                       help='Port to run server on (default: 5000)')
    parser.add_argument('--url', '-u', type=str, default=None,
                       help='Generate QR code for the given URL (standalone mode)')
    parser.add_argument('--output', '-o', type=str, default=None,
                       help='Output path for QR code PNG file (default: netshare_qr.png)')

    args = parser.parse_args()

    # Validate --output requires --url
    if args.output and not args.url:
        print("Error: --output flag requires --url flag")
        print("Use: netshare --url <URL> --output <filename>")
        sys.exit(1)

    # Handle URL-only mode (standalone QR generation)
    if args.url:
        # Validate that no conflicting flags were specified
        if args.gui or args.folder or args.port != 5000:
            print("Error: --url flag cannot be combined with --folder, --gui, or --port")
            print("Use --url only for standalone QR code generation.")
            sys.exit(1)

        # Generate QR code for the provided URL
        try:
            output_path = args.output if args.output else 'netshare_qr.png'
            qr_path = generate_qr_code(args.url, output_path=output_path)
            print(f"\nQR code generated successfully!")
            print(f"URL: {args.url}")
            print(f"Saved to: {qr_path}")
            sys.exit(0)
        except Exception as e:
            print(f"Error generating QR code: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    # Try to load folders from saved config first
    load_folders_from_file()

    # Determine folders to share
    if args.gui:
        if not HAS_GUI:
            print("Error: GUI not available on this system.")
            print("Please use --folder option instead.")
            sys.exit(1)
        config.shared_folders = select_folders_gui()
        # Save GUI-selected folders
        if config.shared_folders:
            save_folders_to_file()
    elif args.folder:
        config.shared_folders = [os.path.abspath(f) for f in args.folder]
        # Save command-line folders
        save_folders_to_file()
    elif not config.shared_folders:
        # Interactive mode (only if no saved folders)
        print("NetShare - Network File Sharing Tool")
        print("="*50)
        print("Enter folders to share (one per line, empty line to finish):")

        while True:
            folder = input("Folder path: ").strip()
            if not folder:
                break
            if os.path.isdir(folder):
                config.shared_folders.append(os.path.abspath(folder))
                print(f"  ✓ Added: {folder}")
            else:
                print(f"  ✗ Not a valid folder: {folder}")

        # Save interactively-selected folders
        if config.shared_folders:
            save_folders_to_file()
    else:
        # Using saved folders from config file
        print(f"Loaded {len(config.shared_folders)} folder(s) from saved configuration")

    if not config.shared_folders:
        print("\nNo folders selected. Exiting.")
        sys.exit(0)
    
    # Validate all folders exist
    valid_folders = []
    for folder in config.shared_folders:
        if os.path.isdir(folder):
            valid_folders.append(folder)
        else:
            print(f"Warning: Skipping non-existent folder: {folder}")
    
    config.shared_folders = valid_folders
    
    if not config.shared_folders:
        print("\nNo valid folders to share. Exiting.")
        sys.exit(0)
    
    config.server_port = args.port
    
    # Start the server
    try:
        start_server(config.server_port)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
