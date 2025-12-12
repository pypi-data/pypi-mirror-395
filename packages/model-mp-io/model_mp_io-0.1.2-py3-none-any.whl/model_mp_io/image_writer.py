import cv2
import os
from typing import Dict, Any, List, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Platform-specific configuration
unihiker_ttf_file_path = '/opt/unihiker/Version'

def windows_get_font():
    """
    Get available font file path on Windows systems.
    
    Searches for commonly available fonts on Windows in order of preference:
    1. SimHei (Chinese font for better Unicode support)
    2. Arial (English fallback font)
    
    Returns:
        str: Path to the first available font file
        
    Raises:
        RuntimeError: If no suitable font files are found
    """
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",  # Chinese Unicode font
        "C:/Windows/Fonts/arial.ttf",   # Standard English font
    ]
    
    for path in font_paths:
        if os.path.exists(path):
            print(f"[INFO] Font file loaded: {path}")
            return path
            
    raise RuntimeError(f"[ERROR] No suitable font files found in: {font_paths}")


def is_unihiker_version(file_path):
    """
    Detect if running on UniHiker platform.
    
    UniHiker is an educational computing platform that requires
    specific font handling for proper text rendering.
    
    Args:
        file_path (str): Path to check for UniHiker version file
        
    Returns:
        bool: True if running on UniHiker platform, False otherwise
    """
    try:
        return os.path.exists(file_path)
    except Exception as e:
        print(f"[ERROR] Platform detection failed: {file_path}, Error: {e}")
        return False


class ImageWriter:
    """
    Professional Image Output and Visualization Engine.
    
    This class provides comprehensive image output capabilities for AI model
    inference results. It supports multiple model types and provides high-quality
    text rendering with automatic platform-specific font selection.
    
    Key Features:
    - Universal model result visualization
    - Cross-platform font support with automatic detection
    - Professional text rendering with background rectangles
    - Customizable styling and positioning
    - High-quality output for production use
    
    Supported Model Types:
    - Image Classification: Class labels with confidence scores
    - Object Detection: Bounding boxes with labels and scores  
    - Image Segmentation: Masks with overlays and labels
    
    Attributes:
        font_file (str): Path to the selected font file for text rendering
    """
    
    def __init__(self):
        """
        Initialize the ImageWriter with appropriate font configuration.
        
        Automatically detects the platform and selects the best available
        font for text rendering. Platform detection includes:
        - UniHiker: Uses embedded HYQiHei_50S.ttf font
        - Windows: Uses system fonts (SimHei, Arial)
        - Other: Uses default system fonts
        
        Raises:
            RuntimeError: If no suitable fonts are found on the system
        """
        self.font_file = None
        
        # Platform-specific font selection
        if is_unihiker_version(unihiker_ttf_file_path):
            # UniHiker platform with embedded fonts
            self.font_file = "HYQiHei_50S.ttf"
            print("[INFO] UniHiker platform detected, using embedded font")
        else:
            # Windows or other platforms
            self.font_file = windows_get_font()

    def draw(self, image, output):
        """
        Render AI model inference results onto an image.
        
        Universal drawing method that automatically detects the model type
        and applies appropriate visualization techniques. Supports all major
        computer vision model types with professional formatting.
        
        Args:
            image (numpy.ndarray): Input image in BGR format with shape (H, W, C)
            output (dict): Model inference results containing:
                         - 'model': Model type identifier string
                         - 'result': List of inference results
                         
        Returns:
            numpy.ndarray: Annotated image with visualization overlays
            
        Raises:
            ValueError: If model type is not supported
            
        Supported Model Types:
            - 'image_classification': Class labels with confidence scores
            - 'object_detection': Bounding boxes with class labels
            - 'segmentation': Instance masks with class information
            
        Example:
            writer = ImageWriter()
            annotated_img = writer.draw(image, detection_results)
        """
        model_type = output['model']
        
        # Route to appropriate visualization method based on model type
        if model_type == 'image_classification':
            return self.draw_classification(image, output)
        elif model_type == 'object_detection':
            return self.draw_detections(image, output)
        elif model_type == 'segmentation':
            return self.draw_segmentation(image, output, self.font_file)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
    def get_masked_image(
        self,
        segmentation_results: Dict[str, Any], 
        original_image: np.ndarray, 
        id: int = -1,
        mode: bool = True,
    ):
        """
        Extract masked image based on segmentation masks.
        
        Args:
            segmentation_results: Dictionary containing 'result' key, where 'result' is a list of instances, each containing 'mask' key.
            original_image: Original image as NumPy array (H, W, 3).
            id: -1 means extract all instances (merge all masks), >=0 means process only the id-th instance.
            mode: Masking mode.
                True: Keep instances (mask regions preserved with transparent background)
                False: Remove instances (mask regions become black, background preserved)
        """
        if 'result' not in segmentation_results:
            raise ValueError("segmentation_results must contain 'result' key")

        results = segmentation_results['result']
        
        if not results:
            print("[WARN] No segmentation results found.")
            return

        # Initialize final mask
        combined_mask = None

        if id == -1:
            # Merge all instance masks
            h, w = original_image.shape[:2]
            combined_mask = np.zeros((h, w), dtype=bool)
            for instance in results:
                mask = instance.get("mask")
                if mask is not None:
                    # Ensure mask shape matches
                    if mask.shape != (h, w):
                        mask = cv2.resize(mask.astype(np.float32), (w, h), interpolation=cv2.INTER_NEAREST)
                    combined_mask |= (mask > 0.5)
        else:
            # Process only the specified id instance
            if id < 0 or id >= len(results):
                raise IndexError(f"Instance id {id} out of range [0, {len(results)-1}]")
            mask = results[id].get("mask")
            if mask is None:
                raise ValueError(f"No mask found for instance id {id}")
            h, w = original_image.shape[:2]
            if mask.shape != (h, w):
                mask = cv2.resize(mask.astype(np.float32), (w, h), interpolation=cv2.INTER_NEAREST)
            combined_mask = (mask > 0.5)

        if combined_mask is None:
            print("[WARN] No valid mask generated.")
            return

        # Expand to 3 channels
        mask_3channel = np.stack([combined_mask] * 3, axis=-1)
        black_background = np.zeros_like(original_image, dtype=original_image.dtype)

        if mode:
            # Keep instances with transparent background
            h, w = original_image.shape[:2]
            # Create RGBA image
            masked_image = np.zeros((h, w, 4), dtype=np.uint8)
            # Copy RGB of instance regions
            masked_image[..., :3][mask_3channel] = original_image[mask_3channel]
            # Instance region alpha=255, other regions alpha=0
            masked_image[..., 3][combined_mask] = 255
            # Non-instance region alpha=0 (already initialized to 0)

        else:
            # Remove instances with black background
            masked_image = np.where(~mask_3channel, original_image, black_background)
        return masked_image


    def draw_text_with_bg(self, img, text, pos=(10, 30), font_file=None, font_size=30,
                          text_color=(255, 255, 255), bg_color=(0, 0, 0), padding=5):
        """
        Render text with background rectangle for improved readability.
        
        This method provides professional text rendering with background
        rectangles to ensure text visibility against any image background.
        Uses Pillow for high-quality font rendering with proper Unicode support.
        
        Args:
            img (numpy.ndarray): Input image in BGR format
            text (str): Text string to render
            pos (tuple): Text position as (x, y) coordinates
            font_file (str, optional): Path to font file. Uses instance font if None
            font_size (int): Font size in pixels (default: 30)
            text_color (tuple): Text color as BGR tuple (default: white)
            bg_color (tuple): Background color as BGR tuple (default: black)
            padding (int): Padding around text in pixels (default: 5)
            
        Returns:
            numpy.ndarray: Image with rendered text in BGR format
            
        Note:
            - Colors are specified in BGR format for OpenCV compatibility
            - Automatically handles font loading and text measurement
            - Provides anti-aliased text rendering for professional quality
            
        Example:
            img_with_text = writer.draw_text_with_bg(
                img, "Detection: Car (0.95)", 
                pos=(10, 30), font_size=24
            )
        """
        # Use instance font if none specified
        if font_file is None:
            font_file = self.font_file
            
        # Convert BGR image to RGB for Pillow processing
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        # Load font with specified size
        try:
            font = ImageFont.truetype(font_file, font_size)
        except (OSError, IOError):
            # Fallback to default font if specified font fails
            font = ImageFont.load_default()
            print(f"[WARN] Failed to load font {font_file}, using default")
        
        # Calculate text bounding box (Pillow 11.3+ compatible)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x, y = pos

        # Calculate background rectangle coordinates
        rect_start = (x - padding, y - padding)
        rect_end = (x + text_width + padding, y + text_height + padding)

        # Convert BGR colors to RGB for Pillow
        bg_color_rgb = (bg_color[2], bg_color[1], bg_color[0])
        text_color_rgb = (text_color[2], text_color[1], text_color[0])

        # Draw background rectangle
        draw.rectangle([rect_start, rect_end], fill=bg_color_rgb)
        
        # Draw text over background
        draw.text((x, y), text, font=font, fill=text_color_rgb)

        # Convert back to BGR format for OpenCV compatibility
        result_image = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        return result_image



    def draw_classification(self, image: np.ndarray, classification_result: Dict[str, Any], 
                           position: Tuple[int, int] = (10, 30),
                           background_color: Tuple[int, int, int] = (0, 0, 0),
                           text_color: Tuple[int, int, int] = (255, 255, 255),
                           show_probability: bool = True,
                           show_class_id: bool = True,
                           position_type: str = "top-left",
                           font_scale: float = 0.6, thickness: int = 2) -> np.ndarray:
        """
        Render image classification results onto an image.
        
        Visualizes the top classification prediction with customizable styling
        and positioning. Provides professional text rendering with background
        rectangles for optimal readability.
        
        Args:
            image (np.ndarray): Input image in BGR format
            classification_result (Dict[str, Any]): Classification results containing:
                                                   - 'result': List of predictions with class info
            position (Tuple[int, int]): Custom text position (x, y) for "custom" position_type
            background_color (Tuple[int, int, int]): Background rectangle color in BGR format
            text_color (Tuple[int, int, int]): Text color in BGR format
            show_probability (bool): Whether to display confidence score
            show_class_id (bool): Whether to display class ID number
            position_type (str): Text positioning mode ("custom", "top-left", etc.)
            font_scale (float): Font scaling factor for text size
            thickness (int): Text stroke thickness
            
        Returns:
            np.ndarray: Annotated image with classification results
            
        Example:
            writer = ImageWriter()
            result_img = writer.draw_classification(
                image, classification_results,
                show_probability=True, position_type="top-left"
            )
        """
        result_image = image.copy()
        
        # Extract top prediction from classification results
        max_classification = classification_result['result'][0]
        class_name = max_classification['class_name']
        probability = max_classification['score']
        class_id = max_classification['class_id']
        
        # Build label text with optional components
        label_parts = [f"{class_name}"]
        if show_probability:
            label_parts.append(f"{probability:.3f}")
        if show_class_id:
            label_parts.append(f"(ID:{class_id})")
        
        label = " ".join(label_parts)

        # Render text with background for better visibility
        result_image = self.draw_text_with_bg(
            result_image, label, position, self.font_file, 
            20, text_color, background_color, 5
        )
        
        return result_image

    def draw_detections(self, image: np.ndarray, detections: Dict[str, Any], 
                       thickness: int = 2, font_size: int = 20) -> np.ndarray:
        """
        Render object detection results onto an image.
        
        Visualizes bounding boxes, class labels, and confidence scores for
        all detected objects. Provides professional formatting with colored
        bounding boxes and readable text labels.
        
        Args:
            image (np.ndarray): Input image in BGR format
            detections (Dict[str, Any]): Detection results containing:
                                       - 'result': List of detections with bbox, class info, scores
            thickness (int): Bounding box line thickness (default: 2)
            font_size (int): Font size for text labels (default: 20)
            
        Returns:
            np.ndarray: Annotated image with detection visualizations
            
        Detection Format:
            Each detection should contain:
            - 'bbox': Bounding box coordinates [x1, y1, x2, y2]
            - 'class_id': Numerical class identifier
            - 'class_name': Human-readable class name
            - 'score': Detection confidence score [0, 1]
            
        Example:
            writer = ImageWriter()
            result_img = writer.draw_detections(image, detection_results, thickness=3)
        """
        result_image = image.copy()
        
        # Process each detection in the results
        for detection in detections["result"]:
            bbox = detection['bbox']  # [x1, y1, x2, y2]
            class_id = detection['class_id']
            class_name = detection['class_name']
            score = detection['score']
            
            # Use green color for bounding boxes (can be made configurable)
            color = (0, 255, 0)
            
            # Draw bounding box rectangle
            cv2.rectangle(result_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, thickness)
            
            # Prepare label text with class name and confidence
            label = f"{class_name}: {score:.2f}"
            
            # Position text above the bounding box
            text_x = bbox[0]
            text_y = max(0, bbox[1] - font_size - 5)

            # Render label with background for readability
            result_image = self.draw_text_with_bg(
                result_image, 
                label, 
                (text_x, text_y), 
                self.font_file, 
                font_size, 
                (255, 255, 255),   # White text
                (0, 0, 0),         # Black background
                5                  # Padding around text
            )

        return result_image


    def draw_segmentation(self, image: np.ndarray, segmentation_results: Dict[str, Any], 
                         font_file: str = None, conf_threshold: float = 0.5, 
                         draw_boxes: bool = True, draw_masks: bool = True, 
                         thickness: int = 2, font_size: int = 20, alpha: float = 0.5) -> np.ndarray:
        """
        Render image segmentation results onto an image.
        
        Visualizes instance segmentation with colored masks, bounding boxes,
        and class labels. Provides configurable transparency for mask overlays
        and professional text rendering for object identification.
        
        Args:
            image (np.ndarray): Input image in BGR format
            segmentation_results (Dict[str, Any]): Segmentation results containing:
                                                  - 'result': List of segmented instances
            font_file (str, optional): Font file path. Uses instance font if None
            conf_threshold (float): Confidence threshold for mask binarization (default: 0.5)
            draw_boxes (bool): Whether to draw bounding boxes around segments
            draw_masks (bool): Whether to draw colored mask overlays
            thickness (int): Bounding box line thickness (default: 2)
            font_size (int): Font size for text labels (default: 20)
            alpha (float): Mask overlay transparency [0, 1] (default: 0.5)
            
        Returns:
            np.ndarray: Annotated image with segmentation visualizations
            
        Segmentation Format:
            Each segmentation should contain:
            - 'mask': Segmentation mask array (H, W) with probability values
            - 'bbox': Bounding box coordinates [x1, y1, x2, y2]
            - 'class_name': Human-readable class name
            - 'score': Segmentation confidence score [0, 1]
            
        Example:
            writer = ImageWriter()
            result_img = writer.draw_segmentation(
                image, segmentation_results, 
                draw_masks=True, alpha=0.6
            )
        """
        result_image = image.copy()

        # Process each segmented instance
        for item in segmentation_results['result']:
            mask = item['mask']  # Shape: (H, W), float32 probability values
            
            # Binarize mask using confidence threshold
            mask_bin = (mask > conf_threshold).astype(np.uint8)
            
            # Use green color for mask overlay (can be made configurable)
            color = (0, 200, 0)  # Green in BGR format

            # Apply mask overlay if enabled
            if draw_masks:
                # Convert color to same data type as result_image
                overlay_color = np.array(color, dtype=np.uint8)
                
                # Create 3-channel version of binary mask
                mask_3ch = np.stack([mask_bin] * 3, axis=-1)  # Shape: (H, W, 3)
                
                # Apply alpha blending for transparent overlay
                result_image = np.where(
                    mask_3ch,
                    (alpha * overlay_color + (1 - alpha) * result_image).astype(np.uint8),
                    result_image
                )

            # Draw bounding box if enabled
            if draw_boxes:
                bbox = item['bbox']
                # Draw bounding box rectangle
                cv2.rectangle(result_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, thickness)
                
                # Calculate text position above bounding box
                text_x = bbox[0]
                text_y = max(0, bbox[1] - font_size - 5)
            else:
                # Position text at top-left if no bounding box
                text_x, text_y = 10, 30

            # Prepare label text with class name and confidence
            label = f"{item['class_name']}: {item['score']:.2f}"
            
            # Render label with background for readability
            result_image = self.draw_text_with_bg(
                result_image, 
                label, 
                (text_x, text_y), 
                self.font_file, 
                font_size, 
                (255, 255, 255),   # White text
                (0, 0, 0),         # Black background
                5                  # Padding around text
            )

        return result_image

    def save(self, image: np.ndarray, path: str):
        """
        Save image to specified file path with automatic directory creation.
        
        Provides convenient image saving with automatic directory structure
        creation if the target directory doesn't exist. Supports all common
        image formats based on file extension.
        
        Args:
            image (numpy.ndarray): Image data in BGR format to save
            path (str): Output file path including filename and extension
                       Supports formats: .jpg, .png, .bmp, .tiff, etc.
            
        Note:
            - Automatically creates parent directories if they don't exist
            - File format is determined by the file extension
            - Prints confirmation message upon successful save
            
        Example:
            writer = ImageWriter()
            writer.save(processed_image, "outputs/results/annotated_image.jpg")
        """
        # Create directory structure if it doesn't exist
        dir_name = os.path.dirname(path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
            
        # Save image using OpenCV
        success = cv2.imwrite(path, image)
        
        if success:
            print(f"[INFO] Image saved successfully to: {path}")
        else:
            print(f"[ERROR] Failed to save image to: {path}")
