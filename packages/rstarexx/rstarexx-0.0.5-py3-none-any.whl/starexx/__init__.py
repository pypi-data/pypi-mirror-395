# __init__.py
import sys, subprocess, os

def main():
    if len(sys.argv) < 2:
        return
    
    command = sys.argv[1]
    
    if command == "allow":
        try:
            subprocess.run(["python3", "-m", "starexx"], check=True)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error: {e}")
    
    elif command == "exit":
        try:
            subprocess.run(["pkill", "-f", "starexx"])
        except:
            pass

if __name__ == "__main__":
    main()