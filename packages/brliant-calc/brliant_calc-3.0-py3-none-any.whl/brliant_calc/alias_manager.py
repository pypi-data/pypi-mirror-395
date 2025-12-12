import os
import sys
import platform
import json
from pathlib import Path


def get_config_dir():
    
    if platform.system() == "Windows":
        config_dir = Path(os.environ.get("APPDATA", "")) / "brliant_calc"
    else:
        config_dir = Path.home() / ".config" / "brliant_calc"
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_file():
    
    return get_config_dir() / "config.json"


def get_scripts_dir():
    
    import site
    
    if platform.system() == "Windows":
        scripts_dir = None
        
        
        if sys.prefix and sys.prefix != 'None':
            try:
                scripts_dir = Path(sys.prefix) / "Scripts"
                if scripts_dir.exists():
                    return scripts_dir
            except:
                pass
        
        
        try:
            if hasattr(site, 'USER_BASE') and site.USER_BASE:
                user_scripts = Path(site.USER_BASE) / "Scripts"
                if user_scripts.exists():
                    return user_scripts
                # Create if doesn't exist
                user_scripts.mkdir(parents=True, exist_ok=True)
                return user_scripts
        except:
            pass
        
        
        try:
            if sys.executable:
                python_dir = Path(sys.executable).parent
                scripts_dir = python_dir / "Scripts"
                if scripts_dir.exists():
                    return scripts_dir
        except:
            pass
        
        
        try:
            appdata = os.environ.get('APPDATA')
            if appdata:
                python_version = f"Python{sys.version_info.major}{sys.version_info.minor}"
                fallback_scripts = Path(appdata) / "Python" / python_version / "Scripts"
                fallback_scripts.mkdir(parents=True, exist_ok=True)
                return fallback_scripts
        except:
            pass
        
        
        fallback = Path.home() / ".brliant_calc" / "Scripts"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback
        
    else:
        
        if sys.prefix and sys.prefix != 'None':
            try:
                scripts_dir = Path(sys.prefix) / "bin"
                if scripts_dir.exists():
                    return scripts_dir
            except:
                pass
        
        
        try:
            if hasattr(site, 'USER_BASE') and site.USER_BASE:
                user_bin = Path(site.USER_BASE) / "bin"
                if user_bin.exists():
                    return user_bin
                user_bin.mkdir(parents=True, exist_ok=True)
                return user_bin
        except:
            pass
        
        # Fallback
        fallback = Path.home() / ".local" / "bin"
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback



def create_alias(alias_name):
    
    import subprocess
    import ctypes
    
    if platform.system() == "Windows":
        
        scripts_dir = get_scripts_dir()
        alias_path = scripts_dir / f"{alias_name}.bat"
        wrapper_content = f'@echo off\nbrliant_calc %*\n'
        
        
        try:
            
            with open(alias_path, 'w') as f:
                f.write(wrapper_content)
            
            
            config_file = get_config_file()
            config = {}
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
            
            if 'aliases' not in config:
                config['aliases'] = []
            
            if alias_name not in config['aliases']:
                config['aliases'].append(alias_name)
            
            config['scripts_dir'] = str(scripts_dir)
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✓ Alias '{alias_name}' created successfully!")
            print(f"  Location: {alias_path}")
            print(f"✓ You can now use: {alias_name} b add 5 10")
            
            return True
            
        except PermissionError:
           
            print(f"⚠ Creating alias requires administrator privileges.")
            print(f"  Attempting to elevate with sudo...")
            
            try:
                
                temp_script = Path.home() / f".brliant_calc_temp_{alias_name}.py"
                script_content = f'''import sys
from pathlib import Path

alias_path = Path(r"{alias_path}")
wrapper_content = "@echo off\\nbrliant_calc %*\\n"

try:
    with open(alias_path, 'w') as f:
        f.write(wrapper_content)
    print("Alias created successfully!")
except Exception as e:
    print(f"Error: {{e}}")
    sys.exit(1)
'''
                with open(temp_script, 'w', encoding='utf-8') as f:
                    f.write(script_content)
                
                
                result = subprocess.run(
                    ['sudo', 'python', str(temp_script)],
                    capture_output=True,
                    text=True
                )
                
                
                if temp_script.exists():
                    temp_script.unlink()
                
                if result.returncode == 0:
                    
                    config_file = get_config_file()
                    config = {}
                    if config_file.exists():
                        with open(config_file, 'r') as f:
                            config = json.load(f)
                    
                    if 'aliases' not in config:
                        config['aliases'] = []
                    
                    if alias_name not in config['aliases']:
                        config['aliases'].append(alias_name)
                    
                    config['scripts_dir'] = str(scripts_dir)
                    
                    with open(config_file, 'w') as f:
                        json.dump(config, f, indent=2)
                    
                    print(f"✓ Alias '{alias_name}' created successfully with sudo!")
                    print(f"  Location: {alias_path}")
                    print(f"✓ You can now use: {alias_name} b add 5 10")
                    return True
                else:
                    print(f"✗ Failed to create alias with sudo.")
                    print(f"  Error: {result.stderr}")
                    return False
                    
            except FileNotFoundError:
                print("✗ 'sudo' command not found.")
                print("  Please install Windows 11 sudo or run PowerShell as Administrator and try again.")
                return False
            except Exception as e:
                print(f"✗ Error creating alias: {e}")
                return False
        
        except Exception as e:
            print(f"✗ Error creating alias: {e}")
            return False
    
    else:
        
        scripts_dir = get_scripts_dir()
        alias_path = scripts_dir / alias_name
        wrapper_content = f'#!/bin/sh\nbrliant_calc "$@"\n'
        
        try:
            
            with open(alias_path, 'w') as f:
                f.write(wrapper_content)
            os.chmod(alias_path, 0o755)
            
           
            config_file = get_config_file()
            config = {}
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
            
            if 'aliases' not in config:
                config['aliases'] = []
            
            if alias_name not in config['aliases']:
                config['aliases'].append(alias_name)
            
            config['scripts_dir'] = str(scripts_dir)
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✓ Alias '{alias_name}' created successfully!")
            print(f"  Location: {alias_path}")
            print(f"✓ You can now use: {alias_name} b add 5 10")
            
            return True
            
        except PermissionError:
            
            print(f"⚠ Creating alias requires sudo privileges.")
            print(f"  Attempting to elevate with sudo...")
            
            try:
                import subprocess
                
                
                temp_script = Path.home() / f".brliant_calc_temp_{alias_name}.sh"
                script_content = f'''#!/bin/sh
cat > "{alias_path}" << 'EOF'
{wrapper_content}EOF
chmod 755 "{alias_path}"
'''
                with open(temp_script, 'w') as f:
                    f.write(script_content)
                os.chmod(temp_script, 0o755)
                
            
                result = subprocess.run(['sudo', str(temp_script)], capture_output=True, text=True)
                temp_script.unlink()
                
                if result.returncode == 0:
                 
                    config_file = get_config_file()
                    config = {}
                    if config_file.exists():
                        with open(config_file, 'r') as f:
                            config = json.load(f)
                    
                    if 'aliases' not in config:
                        config['aliases'] = []
                    
                    if alias_name not in config['aliases']:
                        config['aliases'].append(alias_name)
                    
                    config['scripts_dir'] = str(scripts_dir)
                    
                    with open(config_file, 'w') as f:
                        json.dump(config, f, indent=2)
                    
                    print(f"✓ Alias '{alias_name}' created successfully with sudo!")
                    print(f"  Location: {alias_path}")
                    print(f"✓ You can now use: {alias_name} b add 5 10")
                    return True
                else:
                    print(f"✗ Failed to create alias with sudo.")
                    return False
                    
            except Exception as e:
                print(f"✗ Error creating alias: {e}")
                return False
        
        except Exception as e:
            print(f"✗ Error creating alias: {e}")
            return False



def remove_alias(alias_name):
  
    import subprocess
    
    config_file = get_config_file()
    
    if not config_file.exists():
        print(f"✗ No aliases found.")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        scripts_dir = Path(config.get('scripts_dir', ''))
        
        if platform.system() == "Windows":
            alias_path = scripts_dir / f"{alias_name}.bat"
        else:
            alias_path = scripts_dir / alias_name
        
        if not alias_path.exists():
            print(f"✗ Alias '{alias_name}' not found.")
            return False
        
        try:
          
            alias_path.unlink()
            
           
            if 'aliases' in config and alias_name in config['aliases']:
                config['aliases'].remove(alias_name)
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"✓ Alias '{alias_name}' removed successfully!")
            return True
            
        except PermissionError:
            # Need sudo
            print(f"⚠ Removing alias requires administrator privileges.")
            print(f"  Attempting to elevate with sudo...")
            
            try:
                if platform.system() == "Windows":
                    result = subprocess.run(['sudo', 'cmd', '/c', 'del', str(alias_path)], capture_output=True)
                else:
                    result = subprocess.run(['sudo', 'rm', str(alias_path)], capture_output=True)
                
                if result.returncode == 0:
                   
                    if 'aliases' in config and alias_name in config['aliases']:
                        config['aliases'].remove(alias_name)
                    
                    with open(config_file, 'w') as f:
                        json.dump(config, f, indent=2)
                    
                    print(f"✓ Alias '{alias_name}' removed successfully with sudo!")
                    return True
                else:
                    print(f"✗ Failed to remove alias with sudo.")
                    return False
                    
            except FileNotFoundError:
                print("✗ 'sudo' command not found.")
                return False
            except Exception as e:
                print(f"✗ Error removing alias: {e}")
                return False
        
    except Exception as e:
        print(f"✗ Error removing alias: {e}")
        return False



def list_aliases():
    """List all created aliases."""
    config_file = get_config_file()
    
    if not config_file.exists():
        print("No aliases created yet.")
        return
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        aliases = config.get('aliases', [])
        
        if not aliases:
            print("No aliases created yet.")
        else:
            print("Created aliases:")
            for alias in aliases:
                print(f"  - {alias}")
    
    except Exception as e:
        print(f"✗ Error reading aliases: {e}")
