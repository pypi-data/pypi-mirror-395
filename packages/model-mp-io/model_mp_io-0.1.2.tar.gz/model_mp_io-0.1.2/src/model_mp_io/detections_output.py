import cv2
import numpy as np
from typing import List, Dict, Any, Tuple

class DetectionOutput:

    def __init__(self, colors=None):
        """
        Initialize the detection output visualization engine.
        
        Args:
            colors (List[Tuple[int, int, int]], optional): Custom color palette for classes.
                                                          If None, generates 80 random colors.
                                                          Each color is a BGR tuple (B, G, R).
        """
        # Use provided colors or generate default palette
        self.colors = colors or self._generate_colors(80)  # Default: 80 distinct colors
    
    def _generate_colors(self, num_colors: int) -> List[Tuple[int, int, int]]:
        """
        Generate a diverse color palette for object class visualization.
        
        Creates visually distinct colors using random generation with a fixed
        seed to ensure consistent color assignment across runs.
        
        Args:
            num_colors (int): Number of distinct colors to generate
            
        Returns:
            List[Tuple[int, int, int]]: List of BGR color tuples for OpenCV
            
        Note:
            Uses a fixed random seed (42) to ensure reproducible color assignment
            for consistent visualization across different runs.
        """
        np.random.seed(42)  # Fixed seed for consistent color generation
        colors = []
        
        for _ in range(num_colors):
            # Generate random BGR color tuple
            color = tuple(np.random.randint(0, 255, 3).tolist())
            colors.append(color)
            
        return colors
    
    def draw_detections(self, image: np.ndarray, detections: Dict[str, Any], 
                       thickness: int = 2, font_scale: float = 0.6) -> np.ndarray:
        """
        Render object detection results onto an image with professional formatting.
        
        Visualizes all detected objects with colored bounding boxes, class labels,
        and confidence scores. Each object class is assigned a unique color for
        easy visual distinction.
        
        Args:
            image (np.ndarray): Input image in BGR format with shape (H, W, C)
            detections (Dict[str, Any]): Detection results containing:
                                       - 'result': List of detection objects
            thickness (int): Bounding box line thickness (default: 2)
            font_scale (float): Text scaling factor for labels (default: 0.6)
            
        Returns:
            np.ndarray: Annotated image with detection visualizations in BGR format
            
        Detection Format:
            Each detection in the 'result' list should contain:
            - 'bbox': Bounding box coordinates [x1, y1, x2, y2]
            - 'class_id': Numerical class identifier for color selection
            - 'class_name': Human-readable class name
            - 'score': Detection confidence score [0, 1]
            
        Example:
            detector_viz = DetectionOutput()
            result_img = detector_viz.draw_detections(
                image, detection_results, thickness=3, font_scale=0.8
            )
        """
        result_image = image.copy()
        
        # Process each detection in the results
        for detection in detections['result']:
            bbox = detection['bbox']  # [x1, y1, x2, y2]
            class_id = detection['class_id']
            class_name = detection['class_name']
            score = detection['score']
            
            # Select color based on class ID (cyclic selection if more classes than colors)
            color = self.colors[class_id % len(self.colors)]
            
            # Draw bounding box rectangle
            cv2.rectangle(result_image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, thickness)
            
            # Prepare label text with class name and confidence
            label = f"{class_name}: {score:.2f}"
            
            # Calculate text dimensions for background rectangle
            (text_width, text_height), baseline = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
            )
            
            # Draw background rectangle for text (using same color as bounding box)
            cv2.rectangle(
                result_image,
                (bbox[0], bbox[1] - text_height - baseline - 5),
                (bbox[0] + text_width, bbox[1]),
                color,
                -1  # Filled rectangle
            )
            
            # Draw text label on background
            cv2.putText(
                result_image,
                label,
                (bbox[0], bbox[1] - baseline - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_scale,
                (255, 255, 255),  # White text for contrast
                thickness
            )
        
        return result_image
    
    def save_detections(self, image: np.ndarray, detections: Dict[str, Any], 
                       output_path: str, **kwargs) -> None:
        """
        Save image with rendered detection results to file.
        
        Convenience method that combines detection visualization and file saving
        in a single operation. Supports all the same styling options as draw_detections.
        
        Args:
            image (np.ndarray): Input image in BGR format
            detections (Dict[str, Any]): Detection results to visualize
            output_path (str): File path for saving the annotated image
            **kwargs: Additional arguments passed to draw_detections method
            
        Example:
            detector_viz.save_detections(
                image, detection_results, "output/detections.jpg",
                thickness=3, font_scale=0.8
            )
        """
        result_image = self.draw_detections(image, detections, **kwargs)
        cv2.imwrite(output_path, result_image)
        print(f"[INFO] Detection results saved to: {output_path}")
    
    def print_detections(self, detections: Dict[str, Any]) -> None:
        """
        Print detection results in a formatted table.
        
        Displays detection information including object count, class names,
        confidence scores, and bounding box coordinates in a readable format.
        
        Args:
            detections (Dict[str, Any]): Detection results containing 'result' list
            
        Example:
            detector_viz.print_detections(detection_results)
            # Output:
            # Detected 3 objects:
            #   1. car (confidence: 0.892) - position: [120, 50, 300, 200]
            #   2. person (confidence: 0.756) - position: [400, 100, 480, 350]
        """
        results = detections.get('result', [])
        print(f"Detected {len(results)} objects:")
        
        for i, detection in enumerate(results):
            bbox = detection['bbox']
            class_name = detection['class_name']
            score = detection['score']
            print(f"  {i+1}. {class_name} (confidence: {score:.3f}) - "
                  f"position: [{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}]")
    
    def get_detection_summary(self, detections: Dict[str, Any]) -> Dict[str, int]:
        """
        Generate a summary of detection results by object class.
        
        Counts the number of detections for each object class, providing
        a statistical overview of the detection results.
        
        Args:
            detections (Dict[str, Any]): Detection results containing 'result' list
            
        Returns:
            Dict[str, int]: Dictionary mapping class names to detection counts
            
        Example:
            summary = detector_viz.get_detection_summary(detection_results)
            # Returns: {'car': 2, 'person': 1, 'bicycle': 1}
        """
        summary = {}
        results = detections.get('result', [])
        
        for detection in results:
            class_name = detection['class_name']
            summary[class_name] = summary.get(class_name, 0) + 1
            
        return summary
    
    def get_detection_by_index(self, detections: Dict[str, Any], index: int) -> Dict[str, Any]:
        """
        Retrieve detection information for a specific object by index.
        
        Extracts detailed information for a specific detection including
        confidence score, bounding box in XYWH format, and class label.
        
        Args:
            detections (Dict[str, Any]): Detection results containing 'result' list
            index (int): Zero-based index of the target detection
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                          - 'confidence': Detection confidence score [0, 1]
                          - 'xywh': Bounding box in [x, y, width, height] format
                          - 'label': Human-readable class name
                          Returns default values if index is invalid
                          
        Example:
            obj_info = detector_viz.get_detection_by_index(results, 0)
            print(f"First object: {obj_info['label']} at {obj_info['xywh']}")
        """
        results = detections.get('result', [])
        
        if not results or index < 0 or index >= len(results):
            return {
                'confidence': 0.0,
                'xywh': [0, 0, 0, 0],
                'label': 'Unknown'
            }
        
        detection = results[index]
        bbox = detection.get('bbox', [0, 0, 0, 0])
        
        # Convert from XYXY to XYWH format
        x1, y1, x2, y2 = bbox
        w = x2 - x1
        h = y2 - y1
        
        return {
            'confidence': detection.get('score', 0.0),
            'xywh': [x1, y1, w, h],
            'label': detection.get('class_name', 'Unknown')
        }
    
    def get_detection_stats(self, detections: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics from detection results.
        
        Analyzes detection results to extract key statistics including
        total object count and the index of the highest confidence detection.
        
        Args:
            detections (Dict[str, Any]): Detection results containing 'result' list
            
        Returns:
            Dict[str, Any]: Statistics dictionary containing:
                          - 'total_objects': Total number of detected objects
                          - 'max_confidence_id': Index of highest confidence detection
                          - 'max_confidence': Highest confidence score [0, 1]
                          
        Example:
            stats = detector_viz.get_detection_stats(detection_results)
            print(f"Found {stats['total_objects']} objects, "
                  f"best detection has confidence {stats['max_confidence']:.3f}")
        """
        results = detections.get('result', [])
        
        if not results:
            return {
                'total_objects': 0,
                'max_confidence_id': -1,
                'max_confidence': 0.0
            }
        
        # Calculate total number of objects
        total_objects = len(results)
        
        # Find detection with highest confidence
        max_confidence = -1
        max_confidence_id = -1
        
        for i, detection in enumerate(results):
            confidence = detection.get('score', 0.0)
            if confidence > max_confidence:
                max_confidence = confidence
                max_confidence_id = i
        
        return {
            'total_objects': total_objects,
            'max_confidence_id': max_confidence_id,
            'max_confidence': max_confidence
        }
