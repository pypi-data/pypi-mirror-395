import cv2

class IO_Windows:

    def __init__(self):

        self.windows = {}
    
    def open_window(self, window_name):
        """
        Create and configure a new display window.
        
        Opens a resizable window with full-screen capability and registers
        it in the window management system for proper lifecycle tracking.
        
        Args:
            window_name (str): Unique identifier for the window
            
        Returns:
            bool: True if window was successfully created and registered
            
        Example:
            window_mgr = IO_Windows()
            success = window_mgr.open_window("Camera Feed")
        """
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        self.windows[window_name] = True
        return True

    def close_window(self, window_name):
        """
        Close a specific display window and clean up resources.
        
        Safely destroys the specified window and removes it from the
        window registry to prevent resource leaks.
        
        Args:
            window_name (str): Name of the window to close
            
        Returns:
            bool: True if window was found and closed, False if not found
            
        Example:
            closed = window_mgr.close_window("Camera Feed")
        """
        if window_name in self.windows:
            cv2.destroyWindow(window_name)
            del self.windows[window_name]
            return True
        else:
            return False

    def close_all_windows(self):
        """
        Close all managed windows and perform complete cleanup.
        
        Destroys all active windows tracked by this manager and clears
        the window registry. Useful for application shutdown or reset.
        
        Returns:
            bool: True if windows were closed, False if no windows were open
            
        Example:
            window_mgr.close_all_windows()  # Clean shutdown
        """
        if self.windows:
            cv2.destroyAllWindows()
            self.windows.clear()
            return True
        else:
            return False

    def show(self, frame, window_name=None):
        """
        Display an image frame in the specified window.
        
        Renders the provided image data in the target window with error handling.
        Supports various image formats compatible with OpenCV display functions.
        
        Args:
            frame (np.ndarray): Image data to display (BGR format recommended)
            window_name (str, optional): Target window name. If None, uses default.
            
        Returns:
            bool: True if image was successfully displayed, False on error
            
        Example:
            success = window_mgr.show(camera_frame, "Live Feed")
        """
        # Display image with error checking
        if window_name not in self.windows:
            return False
        if frame is None:
            return False
        if cv2.imshow(window_name, frame) == -1:
            return False
        return True

    def wait_key(self, stop_key: int = None, delay: int = 1) -> bool:
        """
        Handle keyboard input detection with configurable timing and key filtering.
        
        Monitors for keyboard input within a specified time window. Can detect
        any key press or wait for a specific key code.
        
        Args:
            stop_key (int, optional): Specific key code to wait for. If None, any key triggers return.
            delay (int): Wait time in milliseconds for key detection (default: 1)
            
        Returns:
            bool: True if target key was pressed (or any key if stop_key is None), False if timeout
            
        Example:
            # Wait for ESC key (code 27)
            if window_mgr.wait_key(stop_key=27, delay=30):
                print("ESC pressed, exiting...")
                
            # Check for any key press
            if window_mgr.wait_key():
                print("Key detected!")
        """
        key = cv2.waitKey(delay) & 0xFF
        if stop_key is None:
            # No specific key specified, return True for any key press
            return key != 255  # 255 indicates no key was pressed
        else:
            return key == stop_key

    def set_size(self, window_name, width, height):
        """
        Resize a specific window to the given dimensions.
        
        Programmatically adjusts window size for better visualization control.
        Only works with windows created with WINDOW_NORMAL flag.
        
        Args:
            window_name (str): Name of the window to resize
            width (int): New window width in pixels
            height (int): New window height in pixels
            
        Example:
            window_mgr.set_size("Main View", 1280, 720)  # Set to 720p
        """
        if window_name not in self.windows:
            return False
        cv2.resizeWindow(window_name, width, height)
        return True

