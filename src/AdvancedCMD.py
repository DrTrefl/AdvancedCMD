import os
import sys
import subprocess
import platform
import socket
import datetime
import time
import random
import threading
import json
import hashlib
import zipfile
import difflib
import math
import re
import base64
import calendar
import urllib.parse
import urllib.request
import getpass
from pathlib import Path
from collections import deque

try:
    import colorama
    from colorama import Fore, Back, Style
    import psutil
    import requests
    import pyfiglet
    from cryptography.fernet import Fernet
    from PIL import Image
    colorama.init()
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Install with: pip install colorama psutil requests pyfiglet pillow cryptography")
    sys.exit(1)

class AdvancedCMD:
    def __init__(self):
        self.history = deque(maxlen=100)
        self.current_dir = os.getcwd()
        self.notes_file = "notes.txt"
        self.todo_file = "todo.json"
        self.agenda_file = "agenda.json"
        self.running = True
        self.load_todo_list()
        self.load_agenda()
        
    def load_todo_list(self):
        try:
            with open(self.todo_file, 'r') as f:
                self.todo_list = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.todo_list = []
    
    def save_todo_list(self):
        with open(self.todo_file, 'w') as f:
            json.dump(self.todo_list, f, indent=2)

    def load_agenda(self):
        try:
            with open(self.agenda_file, 'r') as f:
                self.agenda = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.agenda = []

    def save_agenda(self):
        with open(self.agenda_file, 'w') as f:
            json.dump(self.agenda, f, indent=2)
    
    def print_banner(self):
        banner = pyfiglet.figlet_format("Advanced CMD", font="slant")
        print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Welcome to Advanced CMD{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type 'help' for available commands or 'exit' to quit{Style.RESET_ALL}")
        print()
    
    def print_error(self, message):
        print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")
    
    def print_success(self, message):
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
    
    def print_info(self, message):
        print(f"{Fore.BLUE}{message}{Style.RESET_ALL}")
    
    def print_warning(self, message):
        print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")
    
    def get_prompt(self):
        return f"{Fore.MAGENTA}Advanced CMD{Fore.CYAN} > {Style.RESET_ALL}"
    
    def execute_system_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                self.print_error(result.stderr)
            return result.returncode == 0
        except Exception as e:
            self.print_error(f"Failed to execute command: {e}")
            return False
    
    def cmd_help(self, args):
        commands = {
            "System Commands": [
                "'dir' - list directory contents",
                "'cd' - change directory", 
                "'cls' - clear screen", 
                "'copy' - copy file from source to destination", 
                "'move' - move/rename file", 
                "'del' - delete file", 
                "'exit' - quit Advanced CMD"],
            "System Info": [
                "'sysinfo' - display comprehensive system information (CPU, RAM, OS)", 
                "'netinfo' - show network interfaces, IP addresses, subnet masks", 
                "'ps' - list all running processes with PID, CPU and memory usage", 
                "'diskinfo' - display disk usage for all drives and partitions", 
                "'uptime' - show system boot time and uptime duration", 
                "'temp' - show CPU and GPU temperatures in real-time", 
                "'whoami_plus' - extended user info with groups and permissions"],
            "Network Tools": [
                "'ping' [host] - send ICMP ping packets to host", 
                "'ports' - scan and list all open local network ports", 
                "'http' [url] - fetch HTTP headers and status code from URL", 
                "'whois' [domain] - perform WHOIS lookup for domain information", 
                "'geoip' [IP] - get geolocation info for IP address (country, city, ISP)", 
                "'mailcheck' [email] - verify if email address exists using MX lookup", 
                "'nettest' - perform internet speed test (download, upload, ping)"],
            "Utilities & Tools": [
                "'calc' [expression] - evaluate mathematical expression (e.g. calc 2+2*3)", 
                "'timer' [seconds] - countdown timer with beep sound at end", 
                "'note' [text] - append timestamped text to notes.txt file", 
                "'todo' - task manager - add, list, mark done, remove tasks", 
                "'find' [file name] - searches for a file by its name", 
                "'recent' - show recently accessed/modified files", 
                "'tree' - display directory structure as tree", 
                "'du' [folder] - show disk usage and size of folder", 
                "'backup' [source] [dest] - create compressed backup of folder", 
                "'diff' [file1] [file2] - compare two files and show differences",
                "'weather' [city] - fetch current weather information for city"],
            "Fun & Games": [
                "'ascii' [text] - generate ASCII art from input text",
                "'asciiart' [image.jpg] - convert image file to ASCII art representation",  
                "'matrix' - display falling green Matrix-style text effect", 
                "'snake' - play classic Snake game in console", 
                "'rps' [choice] - play Rock-Paper-Scissors (rock/paper/scissors)", 
                "'mindmap' [topic] - generate simple ASCII mind map structure"],
            "Advanced": [
                "'encrypt' [file] - encrypt file with password protection", 
                "'decrypt' [file] - decrypt encrypted file with password", 
                "'pwgen' [length]/[nosymbols] - generate secure random password", 
                "'translate' [text] [lang] - translate text to specified language", 
                "'agenda' - calendar and appointment manager"],
            "System Management": [
                "'kill' [PID] - terminate process by Process ID", 
                "'syslog' - display system logs and recent events"]
        }
        
        print(f"{Fore.CYAN}Advanced CMD - Available Commands:{Style.RESET_ALL}\n")
        for category, cmds in commands.items():
            print(f"{Fore.GREEN}{category}:{Style.RESET_ALL}")
            for cmd in cmds:
                print(f"  {Fore.YELLOW}{cmd}{Style.RESET_ALL}")
            print()
    
    def format_bytes(self, bytes_count):
        if bytes_count == 0:
            return "0 B"
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_count < 1024:
                return f"{bytes_count:.1f} {unit}"
            bytes_count /= 1024
        return f"{bytes_count:.1f} PB"

    def cmd_dir(self, args):
        path = args[0] if args else '.'
        try:
            items = os.listdir(path)
            total_size = 0
            file_count = 0
            dir_count = 0
            
            print(f"{Fore.CYAN}Directory of {os.path.abspath(path)}{Style.RESET_ALL}\n")
            
            for item in sorted(items):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    print(f"{Fore.BLUE}<DIR>     {item}{Style.RESET_ALL}")
                    dir_count += 1
                else:
                    size = os.path.getsize(item_path)
                    total_size += size
                    file_count += 1
                    print(f"{size:>10} {item}")
            
            print(f"\n{Fore.GREEN}{file_count} File(s)  {total_size:,} bytes")
            print(f"{dir_count} Dir(s){Style.RESET_ALL}")
            
        except Exception as e:
            self.print_error(f"Cannot access directory: {e}")
    
    def cmd_cd(self, args):
        if not args:
            print(os.getcwd())
            return
            
        path = args[0]
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()
            self.print_success(f"Changed to: {self.current_dir}")
        except Exception as e:
            self.print_error(f"Cannot change directory: {e}")

    def cmd_cls(self, args):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def cmd_copy(self, args):
        if len(args) < 2:
            self.print_error("Usage: copy <source> <destination>")
            return
        
        try:
            import shutil
            shutil.copy2(args[0], args[1])
            self.print_success(f"Copied {args[0]} to {args[1]}")
        except Exception as e:
            self.print_error(f"Copy failed: {e}")
    
    def cmd_move(self, args):
        if len(args) < 2:
            self.print_error("Usage: move <source> <destination>")
            return
        
        try:
            import shutil
            shutil.move(args[0], args[1])
            self.print_success(f"Moved {args[0]} to {args[1]}")
        except Exception as e:
            self.print_error(f"Move failed: {e}")
    
    def cmd_del(self, args):
        if not args:
            self.print_error("Usage: del <filename>")
            return
        
        try:
            os.remove(args[0])
            self.print_success(f"Deleted {args[0]}")
        except Exception as e:
            self.print_error(f"Delete failed: {e}")

#SYSTEM INFO:

    def cmd_sysinfo(self, args):
        print(f"{Fore.CYAN}System Information:{Style.RESET_ALL}")
        print(f"OS: {platform.system()} {platform.release()}")
        print(f"Architecture: {platform.architecture()[0]}")
        print(f"Processor: {platform.processor()}")
        print(f"Machine: {platform.machine()}")
        print(f"Node: {platform.node()}")
        
        memory = psutil.virtual_memory()
        print(f"Total RAM: {memory.total / (1024**3):.2f} GB")
        print(f"Available RAM: {memory.available / (1024**3):.2f} GB")
        print(f"Used RAM: {(memory.total - memory.available) / (1024**3):.2f} GB")
        
        print(f"CPU Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
        print(f"CPU Usage: {psutil.cpu_percent(interval=1):.1f}%")
        
        disk = psutil.disk_usage('/')
        print(f"Disk Total: {disk.total / (1024**3):.2f} GB")
        print(f"Disk Free: {disk.free / (1024**3):.2f} GB")

    def cmd_netinfo(self, args):
        print(f"{Fore.CYAN}Network Information:{Style.RESET_ALL}")
        
        interfaces = psutil.net_if_addrs()
        for interface_name, addresses in interfaces.items():
            print(f"\n{Fore.YELLOW}{interface_name}:{Style.RESET_ALL}")
            for addr in addresses:
                if addr.family == socket.AF_INET:
                    print(f"  IPv4: {addr.address}")
                    print(f"  Netmask: {addr.netmask}")
                elif addr.family == socket.AF_INET6:
                    print(f"  IPv6: {addr.address}")
        
        try:
            gateways = psutil.net_if_stats()
            print(f"\n{Fore.GREEN}Interface Statistics:{Style.RESET_ALL}")
            for interface, stats in gateways.items():
                if stats.isup:
                    print(f"  {interface}: UP, Speed: {stats.speed} Mbps")
        except Exception as e:
            self.print_error(f"Could not get network stats: {e}")

    def cmd_ps(self, args):
        print(f"{Fore.CYAN}Running Processes:{Style.RESET_ALL}")
        print(f"{'PID':<8} {'Name':<25} {'CPU%':<8} {'Memory%':<10}")
        print("-" * 60)
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                print(f"{info['pid']:<8} {info['name'][:24]:<25} {info['cpu_percent']:<8.1f} {info['memory_percent']:<10.1f}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def cmd_diskinfo(self, args):
        print(f"{Fore.CYAN}Disk Usage Information:{Style.RESET_ALL}")
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total_gb = usage.total / (1024**3)
                used_gb = usage.used / (1024**3)
                free_gb = usage.free / (1024**3)
                percent = (usage.used / usage.total) * 100
                
                print(f"\n{Fore.YELLOW}{partition.device}{Style.RESET_ALL} ({partition.fstype})")
                print(f"  Total: {total_gb:.2f} GB")
                print(f"  Used:  {used_gb:.2f} GB ({percent:.1f}%)")
                print(f"  Free:  {free_gb:.2f} GB")
                
            except PermissionError:
                print(f"\n{Fore.YELLOW}{partition.device}{Style.RESET_ALL} - Access Denied")

    def cmd_uptime(self, args):
        boot_time = psutil.boot_time()
        current_time = time.time()
        uptime_seconds = current_time - boot_time
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        boot_time_str = datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"{Fore.GREEN}System Uptime:{Style.RESET_ALL}")
        print(f"Boot time: {boot_time_str}")
        print(f"Uptime: {days} days, {hours} hours, {minutes} minutes")

    def cmd_temp(self, args):
        print(f"{Fore.CYAN}System Temperature Monitor{Style.RESET_ALL}")
        
        try:
            if hasattr(psutil, 'sensors_temperatures'):
                temps = psutil.sensors_temperatures()
                
                if not temps:
                    print(f"{Fore.YELLOW}No temperature sensors found on this system{Style.RESET_ALL}")
                    
                    print(f"\n{Fore.BLUE}CPU Usage as thermal indicator:{Style.RESET_ALL}")
                    for i in range(5):
                        cpu_percent = psutil.cpu_percent(interval=1)
                        thermal_estimate = "Cold" if cpu_percent < 30 else "Warm" if cpu_percent < 70 else "Hot"
                        print(f"  CPU Usage: {cpu_percent:5.1f}% {thermal_estimate}")
                    return
                
                for name, entries in temps.items():
                    print(f"\n{Fore.YELLOW}{name.title()} Sensors:{Style.RESET_ALL}")
                    for entry in entries:
                        label = entry.label or "Unknown"
                        temp = entry.current
                        
                        if temp < 50:
                            color = Fore.GREEN
                            status = "cold"
                        elif temp < 70:
                            color = Fore.YELLOW
                            status = "warm"
                        else:
                            color = Fore.RED
                            status = "hot"
                        
                        print(f"  {status} {label}: {color}{temp:.1f}°C{Style.RESET_ALL}")
            
            else:
                print(f"{Fore.YELLOW}Temperature monitoring not supported on this system{Style.RESET_ALL}")
                
                print(f"\n{Fore.BLUE}CPU Usage (thermal indicator):{Style.RESET_ALL}")
                cpu_percent = psutil.cpu_percent(interval=1)
                print(f"Current CPU Usage: {cpu_percent:.1f}%")
                
        except Exception as e:
            self.print_error(f"Temperature monitoring failed: {e}")

    def cmd_whoami_plus(self, args):
        print(f"{Fore.CYAN}Extended User Information:{Style.RESET_ALL}")
        
        try:
            username = getpass.getuser()
            
            print(f"\n{Fore.YELLOW}User Identity:{Style.RESET_ALL}")
            print(f"  Username: {username}")
            print(f"  User ID: {os.getuid() if hasattr(os, 'getuid') else 'N/A (Windows)'}")
            print(f"  Home Directory: {os.path.expanduser('~')}")
            print(f"  Current Directory: {os.getcwd()}")
            
            print(f"\n{Fore.YELLOW}System Context:{Style.RESET_ALL}")
            print(f"  Computer Name: {platform.node()}")
            print(f"  Operating System: {platform.system()} {platform.release()}")
            print(f"  Architecture: {platform.machine()}")
            
            current_process = psutil.Process()
            print(f"\n{Fore.YELLOW}Process Information:{Style.RESET_ALL}")
            print(f"  Process ID: {current_process.pid}")
            print(f"  Parent PID: {current_process.ppid()}")
            print(f"  CPU Usage: {current_process.cpu_percent():.1f}%")
            print(f"  Memory Usage: {current_process.memory_info().rss / (1024*1024):.1f} MB")
            
            print(f"\n{Fore.YELLOW}Environment:{Style.RESET_ALL}")
            important_vars = ['PATH', 'PYTHON_PATH', 'TEMP', 'TMP', 'USERPROFILE', 'HOME']
            for var in important_vars:
                value = os.environ.get(var, 'Not set')
                if len(value) > 50:
                    value = value[:50] + "..."
                print(f"  {var}: {value}")
            
        except Exception as e:
            self.print_error(f"Could not retrieve user information: {e}")

#NETWORK TOOLS:

    def cmd_ping(self, args):
        if not args:
            self.print_error("Usage: ping <hostname_or_ip>")
            return
        
        host = args[0]
        count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 4
        
        print(f"{Fore.CYAN}Pinging {host} with {count} packets...{Style.RESET_ALL}")
        
        try:
            if os.name == 'nt':
                result = subprocess.run(['ping', '-n', str(count), host], 
                                      capture_output=True, text=True)
            else:
                result = subprocess.run(['ping', '-c', str(count), host], 
                                      capture_output=True, text=True)
            
            if result.returncode == 0:
                print(result.stdout)
            else:
                print(f"{Fore.RED}Ping failed:{Style.RESET_ALL}")
                print(result.stderr if result.stderr else result.stdout)
                
        except Exception as e:
            self.print_error(f"Ping command failed: {e}")

    def cmd_ports(self, args):
        print(f"{Fore.CYAN}Open Network Connections:{Style.RESET_ALL}")
        print(f"{'Protocol':<8} {'Local Address':<22} {'Remote Address':<22} {'Status':<12} {'PID':<8}")
        print("-" * 80)
        
        for conn in psutil.net_connections():
            if conn.status == 'LISTEN':
                local = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
                remote = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else ""
                protocol = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
                pid = conn.pid if conn.pid else ""
                
                print(f"{protocol:<8} {local:<22} {remote:<22} {conn.status:<12} {pid:<8}")

    def cmd_http(self, args):
        if not args:
            self.print_error("Usage: http <url>")
            return
        
        url = args[0]
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"{Fore.CYAN}Fetching HTTP info for: {url}{Style.RESET_ALL}")
        
        try:
            response = requests.get(url, timeout=10, allow_redirects=True)
            
            print(f"\n{Fore.GREEN}HTTP Response:{Style.RESET_ALL}")
            print(f"Status Code: {response.status_code} {response.reason}")
            print(f"Final URL: {response.url}")
            
            print(f"\n{Fore.YELLOW}Headers:{Style.RESET_ALL}")
            for header, value in response.headers.items():
                print(f"  {header}: {value}")
            
            print(f"\n{Fore.BLUE}Response Info:{Style.RESET_ALL}")
            print(f"Content Length: {len(response.content)} bytes")
            print(f"Content Type: {response.headers.get('content-type', 'Unknown')}")
            print(f"Server: {response.headers.get('server', 'Unknown')}")
            print(f"Response Time: {response.elapsed.total_seconds():.3f} seconds")
            
            if response.history:
                print(f"\n{Fore.MAGENTA}Redirects:{Style.RESET_ALL}")
                for i, resp in enumerate(response.history):
                    print(f"  {i+1}. {resp.status_code} -> {resp.url}")
            
        except requests.RequestException as e:
            self.print_error(f"HTTP request failed: {e}")

    def cmd_whois(self, args):
        if not args:
            self.print_error("Usage: whois <domain>")
            return
        
        domain = args[0].lower().strip()
        
        print(f"{Fore.CYAN}WHOIS lookup for: {domain}{Style.RESET_ALL}")
        
        try:
            try:
                ip = socket.gethostbyname(domain)
                print(f"IP Address: {ip}")
                
                hostname = socket.gethostbyaddr(ip)[0]
                print(f"Hostname: {hostname}")
                
            except Exception as e:
                self.print_error(f"Domain lookup failed: {e}")
                
        except Exception as e:
            self.print_error(f"WHOIS lookup failed: {e}")

    def cmd_geoip(self, args):
        if not args:
            self.print_error("Usage: geoip <ip_address>")
            return
        
        ip = args[0]
        
        print(f"{Fore.CYAN}GeoIP lookup for: {ip}{Style.RESET_ALL}")
        
        try:
            url = f"http://ip-api.com/json/{ip}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['status'] == 'success':
                    print(f"\n{Fore.GREEN}Location Information:{Style.RESET_ALL}")
                    print(f"  IP Address: {data.get('query', ip)}")
                    print(f"  Country: {data.get('country', 'Unknown')} ({data.get('countryCode', '')})")
                    print(f"  Region: {data.get('regionName', 'Unknown')} ({data.get('region', '')})")
                    print(f"  City: {data.get('city', 'Unknown')}")
                    print(f"  ZIP Code: {data.get('zip', 'Unknown')}")
                    print(f"  Latitude: {data.get('lat', 'Unknown')}")
                    print(f"  Longitude: {data.get('lon', 'Unknown')}")
                    print(f"  Timezone: {data.get('timezone', 'Unknown')}")
                    print(f"  ISP: {data.get('isp', 'Unknown')}")
                    print(f"  Organization: {data.get('org', 'Unknown')}")
                else:
                    self.print_error(f"GeoIP lookup failed: {data.get('message', 'Unknown error')}")
            else:
                self.print_error("GeoIP service unavailable")
                
        except Exception as e:
            self.print_error(f"GeoIP lookup failed: {e}")

    def cmd_mailcheck(self, args):
        if not args:
            self.print_error("Usage: mailcheck <email_address>")
            return
        
        email = args[0]
        
        if '@' not in email:
            self.print_error("Invalid email format")
            return
        
        domain = email.split('@')[1]
        print(f"{Fore.CYAN}Checking email: {email}{Style.RESET_ALL}")
        
        try:
            socket.gethostbyname(domain)
            print(f"{Fore.GREEN}Email domain appears to be valid{Style.RESET_ALL}")
            print("Note: This checks domain validity, not if the specific email address exists")
            
        except Exception as e:
            self.print_error(f"Email check failed: {e}")

    def cmd_nettest(self, args):
        print(f"{Fore.CYAN}Internet Speed Test Starting...{Style.RESET_ALL}")
        
        try:
            print(f"\n{Fore.YELLOW}Ping Test:{Style.RESET_ALL}")
            ping_hosts = ["8.8.8.8", "1.1.1.1", "google.com"]
            
            for host in ping_hosts:
                try:
                    if os.name == 'nt':
                        result = subprocess.run(['ping', '-n', '4', host], 
                                              capture_output=True, text=True)
                    else:
                        result = subprocess.run(['ping', '-c', '4', host], 
                                              capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        print(f"  {host}: Connected")
                    else:
                        print(f"  {host}: Failed")
                except:
                    print(f"  {host}: Error")
            
            print(f"\n{Fore.YELLOW}Connection Test:{Style.RESET_ALL}")
            
            start_time = time.time()
            try:
                response = requests.get("http://www.google.com", timeout=10)
                end_time = time.time()
                print(f"  Basic connectivity: {(end_time - start_time)*1000:.0f}ms")
            except:
                print("  Connection test failed")
            
            print(f"\n{Fore.GREEN}Speed test completed{Style.RESET_ALL}")
            print("Note: For accurate speed tests, use dedicated tools like speedtest-cli")
            
        except Exception as e:
            self.print_error(f"Network speed test failed: {e}")

#UTILITIES & TOOLS:

    def cmd_calc(self, args):
        if not args:
            self.print_error("Usage: calc <expression>")
            return
        
        expression = " ".join(args)
        try:
            allowed_chars = set("0123456789+-*/.() ")
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                print(f"{Fore.GREEN}{expression} = {result}{Style.RESET_ALL}")
            else:
                self.print_error("Invalid characters in expression")
        except Exception as e:
            self.print_error(f"Calculation error: {e}")

    def cmd_timer(self, args):
        if not args:
            self.print_error("Usage: timer <seconds>")
            return
        
        try:
            seconds = int(args[0])
            print(f"{Fore.YELLOW}Timer started for {seconds} seconds...{Style.RESET_ALL}")
            
            for i in range(seconds, 0, -1):
                print(f"\r{Fore.RED}{i:02d}{Style.RESET_ALL}", end="", flush=True)
                time.sleep(1)
            
            print(f"\r{Fore.GREEN}Time's up!{Style.RESET_ALL}")
            if os.name == 'nt':
                import winsound
                winsound.Beep(1000, 1000)
            else:
                print("\a")
                
        except ValueError:
            self.print_error("Please enter a valid number of seconds")

    def cmd_note(self, args):
        if not args:
            self.print_error("Usage: note <text>")
            return
        
        note_text = " ".join(args)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.notes_file, 'a') as f:
            f.write(f"[{timestamp}] {note_text}\n")
        
        self.print_success(f"Note added to {self.notes_file}")

    def cmd_todo(self, args):
        if not args:
            if not self.todo_list:
                print("No tasks found.")
                return
            
            print(f"{Fore.CYAN}TODO List:{Style.RESET_ALL}")
            for i, task in enumerate(self.todo_list, 1):
                status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if task.get('done', False) else f"{Fore.RED}✗{Style.RESET_ALL}"
                print(f"{i}. {status} {task['text']}")
            return
        
        action = args[0].lower()
        
        if action == "add" and len(args) > 1:
            task_text = " ".join(args[1:])
            self.todo_list.append({"text": task_text, "done": False, "created": datetime.datetime.now().isoformat()})
            self.save_todo_list()
            self.print_success("Task added")
            
        elif action == "done" and len(args) > 1:
            try:
                task_num = int(args[1]) - 1
                if 0 <= task_num < len(self.todo_list):
                    self.todo_list[task_num]['done'] = True
                    self.save_todo_list()
                    self.print_success("Task marked as done")
                else:
                    self.print_error("Invalid task number")
            except ValueError:
                self.print_error("Please enter a valid task number")
                
        elif action == "remove" and len(args) > 1:
            try:
                task_num = int(args[1]) - 1
                if 0 <= task_num < len(self.todo_list):
                    removed_task = self.todo_list.pop(task_num)
                    self.save_todo_list()
                    self.print_success(f"Removed task: {removed_task['text']}")
                else:
                    self.print_error("Invalid task number")
            except ValueError:
                self.print_error("Please enter a valid task number")
        else:
            print("Usage: todo [add <text> | done <number> | remove <number>]")

    def cmd_find(self, args):
        if not args:
            self.print_error("Usage: find <search_string>")
            return
        
        search_string = " ".join(args)
        found_files = []
        
        for root, dirs, files in os.walk('.'):
            for file in files:
                if search_string.lower() in file.lower():
                    found_files.append(os.path.join(root, file))
        
        if found_files:
            print(f"{Fore.GREEN}Found {len(found_files)} matching files:{Style.RESET_ALL}")
            for file in found_files[:20]:
                print(f"  {file}")
            if len(found_files) > 20:
                print(f"  ... and {len(found_files) - 20} more files")
        else:
            print("No matching files found.")

    def cmd_recent(self, args):
        search_path = args[0] if args else '.'
        days_back = int(args[1]) if len(args) > 1 and args[1].isdigit() else 7
        
        print(f"{Fore.CYAN}Files modified in the last {days_back} days:{Style.RESET_ALL}")
        
        cutoff_time = time.time() - (days_back * 24 * 60 * 60)
        recent_files = []
        
        for root, dirs, files in os.walk(search_path):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    stat = os.stat(file_path)
                    if stat.st_mtime > cutoff_time:
                        recent_files.append({
                            'path': os.path.relpath(file_path),
                            'mtime': stat.st_mtime,
                            'size': stat.st_size,
                            'type': 'file'
                        })
                except OSError:
                    continue
        
        recent_files.sort(key=lambda x: x['mtime'], reverse=True)
        
        if not recent_files:
            print(f"{Fore.YELLOW}No recently modified files found{Style.RESET_ALL}")
            return
        
        print(f"{'Modified':<20} {'Size':<12} {'File'}")
        print("-" * 60)
        
        for item in recent_files[:25]:
            mod_time = datetime.datetime.fromtimestamp(item['mtime']).strftime("%Y-%m-%d %H:%M")
            size_str = self.format_bytes(item['size'])
            path = item['path']
            
            age_hours = (time.time() - item['mtime']) / 3600
            if age_hours < 1:
                color = Fore.GREEN
            elif age_hours < 24:
                color = Fore.YELLOW
            else:
                color = Style.RESET_ALL
            
            print(f"{color}{mod_time:<20} {size_str:>12} {path}{Style.RESET_ALL}")
        
        if len(recent_files) > 25:
            print(f"\n{Fore.BLUE}... and {len(recent_files) - 25} more files{Style.RESET_ALL}")

    def cmd_tree(self, args):
        path = args[0] if args else '.'

    def cmd_du(self, args):
        folder = args[0] if args else '.'
        
        if not os.path.exists(folder):
            self.print_error(f"Folder not found: {folder}")
            return
        
        print(f"{Fore.CYAN}Analyzing disk usage for: {os.path.abspath(folder)}{Style.RESET_ALL}")
        
        folder_sizes = {}
        total_size = 0
        file_count = 0
        
        try:
            for root, dirs, files in os.walk(folder):
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                folder_size = 0
                for file in files:
                    if file.startswith('.'):
                        continue
                    try:
                        file_path = os.path.join(root, file)
                        size = os.path.getsize(file_path)
                        folder_size += size
                        total_size += size
                        file_count += 1
                    except OSError:
                        continue
                
                if folder_size > 0:
                    rel_path = os.path.relpath(root, folder)
                    if rel_path == '.':
                        rel_path = os.path.basename(os.path.abspath(folder))
                    folder_sizes[rel_path] = folder_size
            
            sorted_folders = sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)
            
            print(f"\n{Fore.YELLOW}Disk Usage Analysis:{Style.RESET_ALL}")
            print(f"{'Size':<12} {'Percentage':<12} {'Folder'}")
            print("-" * 50)
            
            for folder_path, size in sorted_folders[:15]:
                percentage = (size / total_size) * 100 if total_size > 0 else 0
                size_str = self.format_bytes(size)
                
                if percentage > 20:
                    color = Fore.RED
                elif percentage > 10:
                    color = Fore.YELLOW
                else:
                    color = Fore.GREEN
                
                print(f"{color}{size_str:>12} {percentage:>10.1f}% {folder_path}{Style.RESET_ALL}")
            
            print(f"\n{Fore.GREEN}Summary:{Style.RESET_ALL}")
            print(f"Total Size: {self.format_bytes(total_size)}")
            print(f"Total Files: {file_count:,}")
            print(f"Total Folders: {len(folder_sizes)}")
            
        except Exception as e:
            self.print_error(f"Disk usage analysis failed: {e}")

    def cmd_backup(self, args):
        if len(args) < 2:
            self.print_error("Usage: backup <source_folder> <destination>")
            return
        
        source = args[0]
        destination = args[1]
        
        if not os.path.exists(source):
            self.print_error(f"Source folder not found: {source}")
            return
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{os.path.basename(source)}_backup_{timestamp}.zip"
        backup_path = os.path.join(destination, backup_name)
        
        print(f"{Fore.CYAN}Creating backup: {source} -> {backup_path}{Style.RESET_ALL}")
        
        try:
            os.makedirs(destination, exist_ok=True)
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                file_count = 0
                total_size = 0
                
                for root, dirs, files in os.walk(source):
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                    
                    for file in files:
                        if file.startswith('.'):
                            continue
                            
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source)
                        
                        try:
                            zipf.write(file_path, arcname)
                            file_count += 1
                            total_size += os.path.getsize(file_path)
                            
                            if file_count % 100 == 0:
                                print(f"  Processed {file_count} files...")
                        except Exception as e:
                            print(f"  Warning: Could not backup {file_path}: {e}")
            
            backup_size = os.path.getsize(backup_path)
            compression_ratio = (1 - backup_size / total_size) * 100 if total_size > 0 else 0
            
            self.print_success(f"Backup created successfully!")
            print(f"  Files backed up: {file_count}")
            print(f"  Original size: {self.format_bytes(total_size)}")
            print(f"  Backup size: {self.format_bytes(backup_size)}")
            print(f"  Compression: {compression_ratio:.1f}%")
            print(f"  Location: {backup_path}")
            
        except Exception as e:
            self.print_error(f"Backup failed: {e}")

    def cmd_diff(self, args):
        if len(args) < 2:
            self.print_error("Usage: diff <file1> <file2>")
            return
        
        file1, file2 = args[0], args[1]
        
        if not os.path.exists(file1):
            self.print_error(f"File not found: {file1}")
            return
        if not os.path.exists(file2):
            self.print_error(f"File not found: {file2}")
            return
        
        print(f"{Fore.CYAN}Comparing files: {file1} <-> {file2}{Style.RESET_ALL}")
        
        try:
            with open(file1, 'r', encoding='utf-8', errors='ignore') as f1:
                lines1 = f1.readlines()
            with open(file2, 'r', encoding='utf-8', errors='ignore') as f2:
                lines2 = f2.readlines()
            
            diff = list(difflib.unified_diff(lines1, lines2, 
                                           fromfile=file1, tofile=file2, lineterm=''))
            
            if not diff:
                self.print_success("Files are identical")
                return
            
            print(f"\n{Fore.YELLOW}Differences found:{Style.RESET_ALL}")
            
            for line in diff:
                if line.startswith('---') or line.startswith('+++'):
                    print(f"{Fore.BLUE}{line}{Style.RESET_ALL}")
                elif line.startswith('@@'):
                    print(f"{Fore.MAGENTA}{line}{Style.RESET_ALL}")
                elif line.startswith('+'):
                    print(f"{Fore.GREEN}{line}{Style.RESET_ALL}")
                elif line.startswith('-'):
                    print(f"{Fore.RED}{line}{Style.RESET_ALL}")
                else:
                    print(line, end='')
            
            added = len([line for line in diff if line.startswith('+')])
            removed = len([line for line in diff if line.startswith('-')])
            
            print(f"\n{Fore.CYAN}Statistics:{Style.RESET_ALL}")
            print(f"  Lines added: {Fore.GREEN}{added}{Style.RESET_ALL}")
            print(f"  Lines removed: {Fore.RED}{removed}{Style.RESET_ALL}")
            
        except Exception as e:
            self.print_error(f"File comparison failed: {e}")

    def cmd_weather(self, args):
        if not args:
            city = "London"
        else:
            city = " ".join(args)
        
        try:
            url = f"http://wttr.in/{city}?format=3"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"{Fore.CYAN}Weather for {city}:{Style.RESET_ALL}")
                print(response.text.strip())
            else:
                self.print_error("Could not fetch weather data")
        except Exception as e:
            self.print_error(f"Weather fetch failed: {e}")            

#FUN & GAMES:

    def cmd_ascii(self, args):
        if not args:
            self.print_error("Usage: ascii <text>")
            return
        
        text = " ".join(args)
        try:
            ascii_art = pyfiglet.figlet_format(text)
            print(f"{Fore.CYAN}{ascii_art}{Style.RESET_ALL}")
        except Exception as e:
            self.print_error(f"ASCII art generation failed: {e}")

    def cmd_asciiart(self, args):
        if not args:
            self.print_error("Usage: asciiart <image_file>")
            return
        
        image_path = args[0]
        if not os.path.exists(image_path):
            self.print_error(f"Image file not found: {image_path}")
            return
        
        try:
            ascii_chars = "@%#*+=-:. "
            
            with Image.open(image_path) as img:
                img = img.convert('L')
                
                width = 80
                height = int(width * img.height / img.width * 0.5)
                img = img.resize((width, height))
                
                pixels = img.getdata()
                ascii_img = ""
                
                for i, pixel in enumerate(pixels):
                    ascii_img += ascii_chars[pixel // 32]
                    if (i + 1) % width == 0:
                        ascii_img += '\n'
                
                print(f"{Fore.CYAN}ASCII Art from {image_path}:{Style.RESET_ALL}")
                print(ascii_img)
                
                save = input("Save ASCII art to file? (y/N): ").lower()
                if save == 'y':
                    output_file = f"{os.path.splitext(image_path)[0]}_ascii.txt"
                    with open(output_file, 'w') as f:
                        f.write(ascii_img)
                    self.print_success(f"ASCII art saved to {output_file}")
                
        except ImportError:
            self.print_error("PIL (Pillow) library required: pip install pillow")
        except Exception as e:
            self.print_error(f"ASCII art conversion failed: {e}")

    def cmd_matrix(self, args):
        print(f"{Fore.GREEN}Press Ctrl+C to stop the Matrix effect...{Style.RESET_ALL}")
        
        try:
            width = 80
            height = 24
            matrix = [[' ' for _ in range(width)] for _ in range(height)]
            
            while True:
                for col in range(width):
                    if random.random() < 0.1:
                        matrix[0][col] = random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZあいうえおかきくけこ")
                
                for row in range(height - 1, 0, -1):
                    for col in range(width):
                        matrix[row][col] = matrix[row - 1][col]
                        matrix[row - 1][col] = ' '
                
                os.system('cls' if os.name == 'nt' else 'clear')
                for row in matrix:
                    print(f"{Fore.GREEN}{''.join(row)}{Style.RESET_ALL}")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}Matrix effect stopped.{Style.RESET_ALL}")

    def cmd_snake(self, args):
        print(f"{Fore.GREEN} Snake Game - Use WASD keys, Q to quit{Style.RESET_ALL}")
        print("This is a simplified version. Press Enter to continue...")
        input()
        
        width, height = 20, 10
        snake = [(width//2, height//2)]
        direction = (1, 0)
        food = (random.randint(1, width-2), random.randint(1, height-2))
        score = 0
        
        def draw_game():
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.GREEN}Snake Game - Score: {score} - WASD to move, Q to quit{Style.RESET_ALL}")
            
            print("┌" + "─" * width + "┐")
            for y in range(height):
                line = "│"
                for x in range(width):
                    if (x, y) in snake:
                        if (x, y) == snake[0]:
                            line += f"{Fore.GREEN}●{Style.RESET_ALL}"
                        else:
                            line += f"{Fore.GREEN}○{Style.RESET_ALL}"
                    elif (x, y) == food:
                        line += f"{Fore.RED}♦{Style.RESET_ALL}"
                    else:
                        line += " "
                line += "│"
                print(line)
            print("└" + "─" * width + "┘")
        
        try:
            for _ in range(10):
                draw_game()
                
                move = input("Move (w/a/s/d/q): ").lower()
                if move == 'q':
                    break
                elif move == 'w' and direction != (0, 1):
                    direction = (0, -1)
                elif move == 's' and direction != (0, -1):
                    direction = (0, 1)
                elif move == 'a' and direction != (1, 0):
                    direction = (-1, 0)
                elif move == 'd' and direction != (-1, 0):
                    direction = (1, 0)
                
                head_x, head_y = snake[0]
                new_head = (head_x + direction[0], head_y + direction[1])
                
                if (new_head[0] < 0 or new_head[0] >= width or 
                    new_head[1] < 0 or new_head[1] >= height or 
                    new_head in snake):
                    print(f"{Fore.RED}Game Over! Final Score: {score}{Style.RESET_ALL}")
                    break
                
                snake.insert(0, new_head)
                
                if new_head == food:
                    score += 10
                    food = (random.randint(0, width-1), random.randint(0, height-1))
                    while food in snake:
                        food = (random.randint(0, width-1), random.randint(0, height-1))
                else:
                    snake.pop()
        
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Game interrupted{Style.RESET_ALL}")

    def cmd_rps(self, args):
        if not args:
            self.print_error("Usage: rps <rock|paper|scissors>")
            return
        
        user_choice = args[0].lower()
        valid_choices = ['rock', 'paper', 'scissors']
        
        if user_choice not in valid_choices:
            self.print_error("Choose rock, paper, or scissors")
            return
        
        computer_choice = random.choice(valid_choices)
        
        print(f"You chose: {Fore.YELLOW}{user_choice}{Style.RESET_ALL}")
        print(f"Computer chose: {Fore.YELLOW}{computer_choice}{Style.RESET_ALL}")
        
        if user_choice == computer_choice:
            print(f"{Fore.BLUE}It's a tie!{Style.RESET_ALL}")
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'paper' and computer_choice == 'rock') or \
             (user_choice == 'scissors' and computer_choice == 'paper'):
            print(f"{Fore.GREEN}You win!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Computer wins!{Style.RESET_ALL}")

    def cmd_mindmap(self, args):
        if not args:
            self.print_error("Usage: mindmap <central_topic>")
            return
        
        topic = " ".join(args)
        
        print(f"{Fore.CYAN}Mind Map for: {topic}{Style.RESET_ALL}")
        
        mindmaps = {
            'programming': {
                'Languages': ['Python', 'JavaScript', 'Java', 'C++'],
                'Concepts': ['OOP', 'Algorithms', 'Data Structures'],
                'Tools': ['IDE', 'Git', 'Debugger', 'Testing'],
                'Domains': ['Web Dev', 'Mobile', 'AI/ML', 'Systems']
            },
            'project': {
                'Planning': ['Goals', 'Timeline', 'Resources', 'Risks'],
                'Development': ['Design', 'Code', 'Test', 'Deploy'],
                'Management': ['Team', 'Budget', 'Quality', 'Communication'],
                'Success': ['Metrics', 'Feedback', 'Iteration', 'Documentation']
            },
            'business': {
                'Strategy': ['Vision', 'Mission', 'Goals', 'Competition'],
                'Operations': ['Processes', 'Systems', 'Quality', 'Efficiency'],
                'Finance': ['Revenue', 'Costs', 'Profit', 'Investment'],
                'People': ['Team', 'Culture', 'Skills', 'Growth']
            }
        }
        
        map_data = mindmaps.get(topic.lower())
        
        if not map_data:
            map_data = {
                'Key Aspects': ['Aspect 1', 'Aspect 2', 'Aspect 3'],
                'Benefits': ['Benefit 1', 'Benefit 2', 'Benefit 3'],
                'Challenges': ['Challenge 1', 'Challenge 2', 'Challenge 3'],
                'Next Steps': ['Step 1', 'Step 2', 'Step 3']
            }
        
        print(f"\n{' ' * 20}{Fore.YELLOW}┌─────────────────┐{Style.RESET_ALL}")
        print(f"{' ' * 20}{Fore.YELLOW}│{Style.RESET_ALL} {topic.center(15)} {Fore.YELLOW}│{Style.RESET_ALL}")
        print(f"{' ' * 20}{Fore.YELLOW}└─────────────────┘{Style.RESET_ALL}")
        
        branches = list(map_data.keys())
        for i, (branch, items) in enumerate(map_data.items()):
            if i == 0:
                print(f"{' ' * 28}{Fore.BLUE}│{Style.RESET_ALL}")
            else:
                print(f"{' ' * 28}{Fore.BLUE}│{Style.RESET_ALL}")
            
            print(f"{Fore.BLUE}{'─' * 15}┼─────────────┤{Style.RESET_ALL} {Fore.GREEN}{branch}{Style.RESET_ALL}")
            
            for j, item in enumerate(items):
                connector = "├─" if j < len(items) - 1 else "└─"
                print(f"{' ' * 29}{Fore.BLUE}{connector}{Style.RESET_ALL} {item}")
        
        print(f"\n{Fore.BLUE}Tip: Use 'mindmap programming', 'mindmap project', or 'mindmap business' for detailed templates{Style.RESET_ALL}")

#ADVANCED:

    def cmd_encrypt(self, args):
        if not args:
            self.print_error("Usage: encrypt <filename>")
            return
        
        filename = args[0]
        if not os.path.exists(filename):
            self.print_error(f"File not found: {filename}")
            return
        
        password = getpass.getpass("Enter encryption password: ")
        if not password:
            self.print_error("Password cannot be empty")
            return
        
        try:
            key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
            fernet = Fernet(key)
            
            with open(filename, 'rb') as file:
                file_data = file.read()
            
            encrypted_data = fernet.encrypt(file_data)
            
            encrypted_filename = filename + '.encrypted'
            with open(encrypted_filename, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)
            
            self.print_success(f"File encrypted: {encrypted_filename}")
            
            remove_original = input("Remove original file? (y/N): ").lower()
            if remove_original == 'y':
                os.remove(filename)
                print("Original file removed")
                
        except Exception as e:
            self.print_error(f"Encryption failed: {e}")

    def cmd_decrypt(self, args):
        if not args:
            self.print_error("Usage: decrypt <encrypted_filename>")
            return
        
        filename = args[0]
        if not os.path.exists(filename):
            self.print_error(f"File not found: {filename}")
            return
        
        password = getpass.getpass("Enter decryption password: ")
        if not password:
            self.print_error("Password cannot be empty")
            return
        
        try:
            key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
            fernet = Fernet(key)
            
            with open(filename, 'rb') as encrypted_file:
                encrypted_data = encrypted_file.read()
            
            decrypted_data = fernet.decrypt(encrypted_data)
            
            if filename.endswith('.encrypted'):
                decrypted_filename = filename[:-10]
            else:
                decrypted_filename = filename + '.decrypted'
            
            with open(decrypted_filename, 'wb') as decrypted_file:
                decrypted_file.write(decrypted_data)
            
            self.print_success(f"File decrypted: {decrypted_filename}")
            
        except Exception as e:
            self.print_error(f"Decryption failed: {e}")

    def cmd_pwgen(self, args):
        length = 16
        include_symbols = True
        
        if args:
            try:
                length = int(args[0])
                if length < 4:
                    length = 4
                elif length > 128:
                    length = 128
            except ValueError:
                self.print_error("Invalid length, using default (16)")
        
        if len(args) > 1:
            if 'nosymbols' in args[1:]:
                include_symbols = False
        
        lowercase = "abcdefghijklmnopqrstuvwxyz"
        uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers = "0123456789"
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        chars = lowercase + uppercase + numbers
        if include_symbols:
            chars += symbols
        
        print(f"{Fore.GREEN}Generated passwords ({length} characters):{Style.RESET_ALL}")
        
        for i in range(5):
            password = ''.join(random.choice(chars) for _ in range(length))
            
            strength = self.calculate_password_strength(password)
            strength_color = Fore.GREEN if strength > 80 else Fore.YELLOW if strength > 60 else Fore.RED
            
            print(f"{i+1}. {Fore.CYAN}{password}{Style.RESET_ALL} {strength_color}[{strength}%]{Style.RESET_ALL}")
        
        print(f"\n{Fore.BLUE}Security Tips:{Style.RESET_ALL}")
        print("  - Use different passwords for different accounts")
        print("  - Store passwords in a password manager")
        print("  - Enable two-factor authentication when available")

    def calculate_password_strength(self, password):
        score = 0
        
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
        
        if any(c.islower() for c in password):
            score += 15
        if any(c.isupper() for c in password):
            score += 15
        if any(c.isdigit() for c in password):
            score += 15
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 20
        
        if not any(password[i:i+3].isdigit() for i in range(len(password)-2)):
            score += 10
        
        return min(score, 100)

    def cmd_translate(self, args):
        if len(args) < 2:
            self.print_error("Usage: translate <text> <target_language>")
            print("Example: translate 'Hello world' spanish")
            print("Languages: spanish, french, german, polish, italian, portuguese, russian, japanese, chinese")
            return
        
        text = args[0]
        target_lang = args[1].lower()
        
        lang_codes = {
            'spanish': 'es', 'french': 'fr', 'german': 'de', 'polish': 'pl',
            'italian': 'it', 'portuguese': 'pt', 'russian': 'ru', 
            'japanese': 'ja', 'chinese': 'zh', 'korean': 'ko',
            'arabic': 'ar', 'hindi': 'hi', 'dutch': 'nl'
        }
        
        target_code = lang_codes.get(target_lang, target_lang)
        
        print(f"{Fore.CYAN}Translating '{text}' to {target_lang.title()}...{Style.RESET_ALL}")
        
        try:
            translations = {
                'hello': {'es': 'hola', 'fr': 'bonjour', 'de': 'hallo', 'pl': 'cześć'},
                'world': {'es': 'mundo', 'fr': 'monde', 'de': 'welt', 'pl': 'świat'},
                'good morning': {'es': 'buenos días', 'fr': 'bonjour', 'de': 'guten morgen', 'pl': 'dzień dobry'},
                'thank you': {'es': 'gracias', 'fr': 'merci', 'de': 'danke', 'pl': 'dziękuję'},
                'goodbye': {'es': 'adiós', 'fr': 'au revoir', 'de': 'auf wiedersehen', 'pl': 'do widzenia'}
            }
            
            text_lower = text.lower()
            if text_lower in translations and target_code in translations[text_lower]:
                result = translations[text_lower][target_code]
                print(f"{Fore.GREEN}Translation: {result}{Style.RESET_ALL}")
                
                if target_code == 'pl':
                    pronunciations = {
                        'cześć': 'chesh-ch', 'świat': 'shvyat', 
                        'dzień dobry': 'jen dob-ri', 'dziękuję': 'jen-koo-yeh'
                    }
                    if result in pronunciations:
                        print(f"{Fore.BLUE}Pronunciation: [{pronunciations[result]}]{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}Translation not available for '{text}' to {target_lang}{Style.RESET_ALL}")
                print("This is a demo implementation.")
                
        except Exception as e:
            self.print_error(f"Translation failed: {e}")

    def cmd_agenda(self, args):
        if not args:
            today = datetime.date.today()
            print(f"{Fore.CYAN}Agenda for {today.strftime('%A, %B %d, %Y')}:{Style.RESET_ALL}")
            
            today_events = [event for event in self.agenda if event['date'] == today.isoformat()]
            
            if today_events:
                for event in sorted(today_events, key=lambda x: x.get('time', '00:00')):
                    time_str = event.get('time', 'All day')
                    print(f"  {time_str} - {event['title']}")
            else:
                print("  No events scheduled for today")
            
            print(f"\n{Fore.YELLOW}Upcoming events (next 7 days):{Style.RESET_ALL}")
            upcoming = []
            for i in range(1, 8):
                future_date = today + datetime.timedelta(days=i)
                future_events = [event for event in self.agenda if event['date'] == future_date.isoformat()]
                for event in future_events:
                    event['display_date'] = future_date
                    upcoming.append(event)
            
            if upcoming:
                for event in sorted(upcoming, key=lambda x: (x['date'], x.get('time', '00:00'))):
                    date_str = event['display_date'].strftime('%a %b %d')
                    time_str = event.get('time', 'All day')
                    print(f"  {date_str} {time_str} - {event['title']}")
            else:
                print("  No upcoming events")
                
            print(f"\nUsage: agenda add <date> <time> <title> | agenda list | agenda remove <id>")
            return
        
        action = args[0].lower()
        
        if action == 'add' and len(args) >= 4:
            date_str = args[1]
            time_str = args[2]
            title = ' '.join(args[3:])
            
            try:
                datetime.datetime.strptime(date_str, '%Y-%m-%d')
                if time_str != 'allday':
                    datetime.datetime.strptime(time_str, '%H:%M')
                
                event = {
                    'id': len(self.agenda) + 1,
                    'date': date_str,
                    'time': time_str if time_str != 'allday' else None,
                    'title': title,
                    'created': datetime.datetime.now().isoformat()
                }
                
                self.agenda.append(event)
                self.save_agenda()
                self.print_success(f"Event added: {title} on {date_str}")
                
            except ValueError:
                self.print_error("Invalid date/time format. Use YYYY-MM-DD HH:MM")
                
        elif action == 'list':
            if not self.agenda:
                print("No events in agenda")
                return
                
            print(f"{Fore.CYAN}All Events:{Style.RESET_ALL}")
            for event in sorted(self.agenda, key=lambda x: (x['date'], x.get('time', '00:00'))):
                date_obj = datetime.datetime.strptime(event['date'], '%Y-%m-%d')
                date_str = date_obj.strftime('%a %b %d, %Y')
                time_str = event.get('time', 'All day')
                print(f"  [{event['id']:2d}] {date_str} {time_str} - {event['title']}")
                
        elif action == 'remove' and len(args) > 1:
            try:
                event_id = int(args[1])
                self.agenda = [event for event in self.agenda if event['id'] != event_id]
                self.save_agenda()
                self.print_success(f"Event {event_id} removed")
            except ValueError:
                self.print_error("Invalid event ID")
        else:
            print("Usage: agenda [add <YYYY-MM-DD> <HH:MM|allday> <title> | list | remove <id>]")

#SYSTEM MANAGEMENT:

    def cmd_kill(self, args):
        if not args:
            self.print_error("Usage: kill <PID>")
            return
        
        try:
            pid = int(args[0])
            process = psutil.Process(pid)
            process_name = process.name()
            
            if process_name.lower() in ['explorer.exe', 'winlogon.exe', 'csrss.exe', 'system']:
                confirm = input(f"{Fore.YELLOW}Warning: {process_name} is a system process. Continue? (y/N): {Style.RESET_ALL}")
                if confirm.lower() != 'y':
                    print("Operation cancelled.")
                    return
            
            process.terminate()
            process.wait(timeout=3)
            self.print_success(f"Process {pid} ({process_name}) terminated")
            
        except ValueError:
            self.print_error("Please enter a valid PID number")
        except psutil.NoSuchProcess:
            self.print_error(f"Process with PID {args[0]} not found")
        except psutil.AccessDenied:
            self.print_error("Access denied - insufficient permissions or protected process")
        except psutil.TimeoutExpired:
            try:
                process.kill()
                self.print_warning(f"Process {pid} force killed")
            except:
                self.print_error("Failed to force kill process")
        except Exception as e:
            self.print_error(f"Failed to kill process: {e}")

    def cmd_syslog(self, args):
        print(f"{Fore.CYAN}System Logs and Events{Style.RESET_ALL}")
        
        try:
            if os.name == 'nt':
                print(f"\n{Fore.YELLOW}Recent Windows Events:{Style.RESET_ALL}")
                try:
                    result = subprocess.run(['wevtutil', 'qe', 'System', '/c:10', '/rd:true', '/f:text'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        events = result.stdout.split('\n\n')
                        for i, event in enumerate(events[:5]):
                            if event.strip():
                                print(f"{Fore.GREEN}Event {i+1}:{Style.RESET_ALL}")
                                lines = event.split('\n')[:10]
                                for line in lines:
                                    if line.strip():
                                        print(f"  {line.strip()}")
                                print()
                    else:
                        print("Could not access Windows Event Log")
                except:
                    print("Event log access failed")
                    
                print(f"\n{Fore.YELLOW}System Information:{Style.RESET_ALL}")
                boot_time = psutil.boot_time()
                boot_date = datetime.datetime.fromtimestamp(boot_time)
                print(f"  Last boot: {boot_date.strftime('%Y-%m-%d %H:%M:%S')}")
                
            else:
                print(f"\n{Fore.YELLOW}System Information:{Style.RESET_ALL}")
            boot_time = psutil.boot_time()
            boot_date = datetime.datetime.fromtimestamp(boot_time)
            print(f"  Last boot: {boot_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            print(f"\n{Fore.YELLOW}System Process Summary:{Style.RESET_ALL}")
            process_count = len(psutil.pids())
            print(f"  Total processes: {process_count}")
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except:
                    continue
            
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            print(f"  Top CPU processes:")
            for proc in processes[:5]:
                name = proc.get('name', 'Unknown')[:20]
                cpu = proc.get('cpu_percent', 0)
                print(f"    {name}: {cpu:.1f}%")
            
            memory = psutil.virtual_memory()
            print(f"\n{Fore.YELLOW}Memory Status:{Style.RESET_ALL}")
            print(f"  Total: {memory.total / (1024**3):.2f} GB")
            print(f"  Available: {memory.available / (1024**3):.2f} GB")
            print(f"  Usage: {memory.percent:.1f}%")
            
        except Exception as e:
            self.print_error(f"System log access failed: {e}")

    def run(self):
        self.print_banner()
        
        while self.running:
            try:
                command = input(self.get_prompt()).strip()
                
                if not command:
                    continue
                
                if command != "exit":
                    self.history.append(command)
                
                parts = command.split()
                cmd_name = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []
                
                method_name = f"cmd_{cmd_name}"
                if hasattr(self, method_name):
                    getattr(self, method_name)(args)
                elif cmd_name == "exit":
                    self.print_success("Goodbye!")
                    self.running = False
                else:
                    if not self.execute_system_command(command):
                        self.print_error(f"Unknown command: {cmd_name}")
                        
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' to quit.{Style.RESET_ALL}")
            except EOFError:
                print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                self.print_error(f"Unexpected error: {e}")

def main():
    try:
        cmd = AdvancedCMD()
        cmd.run()
    except Exception as e:
        print(f"Failed to start Advanced CMD: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()