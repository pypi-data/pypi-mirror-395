import cv2
import os


class ImageReader:

    def __init__(self, source=0):
        """
        Initialize image source and configure capture method.
        
        Automatically detects the input type and sets up appropriate
        capture mechanisms. Supports cameras, video files, image files,
        and RTSP streams.
        
        Args:
            source: Input source - can be:
                   - int: Camera device ID (0 for default camera)
                   - str: File path or RTSP URL
                   
        Raises:
            FileNotFoundError: If specified file doesn't exist
            ValueError: If file format is unsupported or stream cannot be opened
        """
        self.source = source
        self.cap = None
        self.is_image = False
        self.is_camera = False
        self.is_rtsp = False
        self.is_video_file = False
        self.image_data = None
        self.set_width = None    
        self.set_height = None
        self.open_source()

    def open_source(self):
        """
        Open and configure the specified input source.
        
        Analyzes the source type and initializes appropriate capture method:
        - Integer sources: Camera devices
        - RTSP URLs: Network video streams
        - File paths: Video or image files based on extension
        
        For image files, data is loaded into memory immediately.
        For video sources, a VideoCapture object is created.
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If source cannot be opened or format is unsupported
        """
        if isinstance(self.source, int):
            # Camera device initialization
            self.cap = cv2.VideoCapture(self.source)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            if self.cap.isOpened():
                print(f"[INFO] Camera {self.source} opened successfully")
                self.is_image = False
                self.is_camera = True
                self.is_rtsp = False
                self.is_video_file = False
            else:
                print(f"[WARN] Failed to open camera {self.source}")
        else:
            # RTSP stream handling
            if self.source.lower().startswith("rtsp://"):
                self.cap = cv2.VideoCapture(self.source, cv2.CAP_FFMPEG)
                if self.cap.isOpened():
                    print(f"[INFO] RTSP stream {self.source} opened successfully")
                    self.is_image = False
                    self.is_camera = False
                    self.is_rtsp = True
                    self.is_video_file = False
                else:
                    raise ValueError(f"Failed to open RTSP stream: {self.source}")
                return

            # Local file validation
            if not os.path.exists(self.source):
                raise FileNotFoundError(f"File does not exist: {self.source}")

            # Image file detection and loading
            image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
            _, ext = os.path.splitext(self.source.lower())
            
            if ext in image_extensions:
                # Load static image into memory
                self.image_data = cv2.imread(self.source)
                if self.image_data is None:
                    raise ValueError(f"Failed to read image: {self.source}")
                self.is_image = True
                self.is_camera = False
                self.is_rtsp = False
                self.is_video_file = False
                self.cap = None
                print(f"[INFO] Image file {self.source} loaded successfully")
            else:
                # Video file initialization
                self.cap = cv2.VideoCapture(self.source, cv2.CAP_FFMPEG)
                if self.cap.isOpened():
                    total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    fps = self.cap.get(cv2.CAP_PROP_FPS)
                    width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    print(f"[INFO] Video file {self.source}: {total_frames} frames at {fps} FPS, resolution {width}x{height}")
                    self.is_image = False
                    self.is_camera = False
                    self.is_rtsp = False
                    self.is_video_file = True
                else:
                    raise ValueError(f"Failed to open file: {self.source} - not a valid video or image file")

    def set_resolution(self, width, height):
        """
        Configure video capture resolution.
        
        Sets the resolution for camera and video file sources.
        Args:
            width (int): Target frame width in pixels
            height (int): Target frame height in pixels
            
        Note:
            - Camera devices may not support all resolutions
            - Video files will be scaled to the requested resolution
            - Static images are not affected by this setting
        """
        
        self.set_width = width
        self.set_height = height

    def release(self):
        """
        Release video capture resources.
        
        Properly closes video capture objects and frees associated resources.
        Should be called when the ImageReader is no longer needed to prevent
        resource leaks.
        
        Note:
            Only applies to video sources (camera, video files, RTSP streams).
            Static images don't require explicit resource release.
        """
        if self.cap is not None:
            self.cap.release()
            print("[INFO] Video capture resources released")

    def read_frame(self):
        """
        Capture or retrieve the current frame.
        
        Behavior depends on the input source type:
        - Static images: Returns a copy of the loaded image data
        - Video sources: Captures the next frame from the stream
        
        Returns:
            numpy.ndarray: Frame data in BGR format with shape (H, W, C)
                          Returns a copy to prevent external modifications
                          
        Raises:
            RuntimeError: If frame capture fails or image data is not available
            
        Example:
            frame = reader.read_frame()
            cv2.imshow('Frame', frame)
        """
        # Handle static image sources
        if hasattr(self, 'is_image') and self.is_image:
            if hasattr(self, 'image_data') and self.image_data is not None:
                # Return a copy to prevent external modification of internal data
                if self.set_width and self.set_height:
                    img = cv2.resize(self.image_data, (self.set_width, self.set_height))
                    return img
                return self.image_data.copy()
            else:
                raise RuntimeError("Image data not loaded")
        
        # Handle video sources (camera, video file, RTSP stream)
        if self.cap is None:
            raise RuntimeError("Video source not initialized")
            
        ret, frame = self.cap.read()
        if not ret:
            if self.is_video_file:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
                if not ret:
                    raise RuntimeError("Failed to read frame after rewind")
                return frame
            if self.is_camera:
                raise RuntimeError("Failed to capture frame from camera")
            if self.is_rtsp:
                raise RuntimeError("Failed to capture frame from RTSP stream")
            raise RuntimeError("Failed to capture frame")
        
        if self.set_width and self.set_height:
            if self.is_camera:
                h, w, c = frame.shape
                w1 = int(h*self.set_width//self.set_height)
                x1 = (w-w1)//2
                frame = frame[:, x1:x1+w1] 
                frame = cv2.resize(frame, (self.set_width, self.set_height))
            if self.is_video_file or self.is_rtsp:
                frame = cv2.resize(frame, (self.set_width, self.set_height))
        return frame







