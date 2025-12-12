from aj090_hw_tools import hw_tools

def script_ep():
    """
    Entry point for running the aj090_hw_tools script.
    """
    try:
        hw_tools()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    script_ep()