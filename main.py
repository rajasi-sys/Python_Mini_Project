import subprocess
import sys
import os

def main():
    """
    Entry point for the Expense Tracker application.
    This script acts as a launcher that automatically boots up the Streamlit dashboard.
    """
    print("🚀 Starting the Expense Tracker Dashboard...")
    
    # Get the absolute path to the dashboard file to prevent folder structure errors
    project_root = os.path.dirname(__file__)
    dashboard_path = os.path.join(project_root, "ui", "dashboard.py")
    
    # Check if the dashboard file actually exists before trying to run it
    if not os.path.exists(dashboard_path):
        print(f"❌ Error: Could not find the dashboard file at {dashboard_path}")
        print("Make sure you are running this from the root 'Python_Mini_Project' folder.")
        return

    # Run the Streamlit app using the current Python environment
    try:
        # This is the Python equivalent of typing `python -m streamlit run ui/dashboard.py` in the terminal
        subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])
    
    except KeyboardInterrupt:
        # Handles the user pressing Ctrl+C gracefully
        print("\n🛑 Shutting down the Expense Tracker. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred while starting the application: {e}")

if __name__ == "__main__":
    main()

