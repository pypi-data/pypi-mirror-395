# __init__.py
import sys, subprocess, os

def main():
    if len(sys.argv) < 2:
        return
    
    command = sys.argv[1]
    
    if command == "allow":
        try:
            module_dir = os.path.dirname(os.path.abspath(__file__))
            server_script = os.path.join(module_dir, "starexx.py")
            
            if os.path.exists(server_script):
                subprocess.run([sys.executable, server_script], check=True)
            else:
                print("starexx.py not found")
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error: {e}")
    
    elif command == "exit":
        try:
            subprocess.run(["pkill", "-f", "python.*starexx.py"])
        except:
            pass

if __name__ == "__main__":
    main()