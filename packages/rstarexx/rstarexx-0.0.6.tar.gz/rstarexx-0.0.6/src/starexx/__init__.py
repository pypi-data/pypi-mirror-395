# __init__.py
import sys, subprocess, os

def main():
    if len(sys.argv) < 2:
        return
    
    command = sys.argv[1]
    
    if command == "allow":
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_py = os.path.join(current_dir, "__main__.py")
            
            if os.path.exists(main_py):
                subprocess.run([sys.executable, main_py], check=True)
            else:
                print("Error: __main__.py not found")
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