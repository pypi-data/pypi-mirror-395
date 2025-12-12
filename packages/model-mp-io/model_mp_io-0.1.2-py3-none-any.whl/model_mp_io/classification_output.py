import cv2
import numpy as np
from typing import Dict, Any, Tuple, Optional, List

class ClassificationOutput:

    def __init__(self, font_scale=1.0, thickness=2):
        """
        Initialize the classification output visualization engine.
        
        Args:
            font_scale (float): Font scaling factor (default: 1.0)
                              Higher values = larger text
            thickness (int): Text line thickness (default: 2)
                            Higher values = bolder text
        """
        self.font_scale = font_scale
        self.thickness = thickness
    
    def draw_classification(self, image: np.ndarray, classification_result: Dict[str, Any], 
                           position: Tuple[int, int] = (10, 30),
                           background_color: Tuple[int, int, int] = (0, 0, 0),
                           text_color: Tuple[int, int, int] = (255, 255, 255),
                           show_probability: bool = True,
                           show_class_id: bool = True,
                           position_type: str = "top-left") -> np.ndarray:
        """
        Render classification results onto an image with professional formatting.
        
        Draws the highest-confidence classification result on the image with
        customizable positioning and styling. Supports multiple layout options
        and configurable display elements.
        
        Args:
            image (np.ndarray): Input image in BGR format with shape (H, W, C)
            classification_result (Dict[str, Any]): Classification results containing:
                                                   - 'result': List of classification predictions
                                                   Each prediction should have:
                                                   - 'class_name': Human-readable class name
                                                   - 'score': Confidence probability [0, 1]
                                                   - 'class_id': Numerical class identifier
            position (Tuple[int, int]): Custom text position (x, y) when position_type is "custom"
            background_color (Tuple[int, int, int]): Background rectangle color in BGR format
            text_color (Tuple[int, int, int]): Text color in BGR format
            show_probability (bool): Whether to display confidence score
            show_class_id (bool): Whether to display class ID number
            position_type (str): Text positioning mode:
                               - "custom": Use provided position coordinates
                               - "top-left": Upper left corner of image
                               - "top-right": Upper right corner of image  
                               - "bottom-left": Lower left corner of image
                               - "bottom-right": Lower right corner of image
            
        Returns:
            np.ndarray: Annotated image with classification results in BGR format
            
        Example:
            classifier_viz = ClassificationOutput()
            result_img = classifier_viz.draw_classification(
                image, classification_results,
                position_type="top-right",
                show_probability=True
            )
        """
        result_image = image.copy()
        
        # Extract statistics from classification results
        max_classification_stats = self.get_classification_stats(classification_result)
        class_name = max_classification_stats['max_confidence_classname']
        probability = max_classification_stats['max_confidence']
        class_id = max_classification_stats['max_confidence_id']
        
        # Build label text with optional components
        label_parts = [f"{class_name}"]
        if show_probability:
            label_parts.append(f"{probability:.3f}")
        if show_class_id:
            label_parts.append(f"(ID:{class_id})")
        
        label = " ".join(label_parts)
        
        # Calculate text dimensions for positioning
        (text_width, text_height), baseline = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, self.thickness
        )
        
        # Determine text position based on positioning mode
        if position_type == "top-right":
            # Upper right corner with margin
            x = image.shape[1] - text_width - 10
            y = 30
        elif position_type == "bottom-left":
            # Lower left corner with margin
            x = 10
            y = image.shape[0] - 30
        elif position_type == "bottom-right":
            # Lower right corner with margin
            x = image.shape[1] - text_width - 10
            y = image.shape[0] - 30
        else:
            # Custom position or default top-left
            x, y = position
        
        # Draw background rectangle for text readability
        padding = 5
        cv2.rectangle(
            result_image,
            (x - padding, y - text_height - baseline - padding),
            (x + text_width + padding, y + baseline + padding),
            background_color,
            -1  # Filled rectangle
        )
        
        # Draw classification text over background
        cv2.putText(
            result_image,
            label,
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            self.font_scale,
            text_color,
            self.thickness
        )
        
        return result_image
    
    def save_classification(self, image: np.ndarray, classification_result: Dict[str, Any], 
                           output_path: str, **kwargs) -> None:
        """
        Save image with rendered classification results to file.
        
        Convenience method that combines classification visualization and file saving
        in a single operation. Supports all the same styling options as draw_classification.
        
        Args:
            image (np.ndarray): Input image in BGR format
            classification_result (Dict[str, Any]): Classification results to visualize
            output_path (str): File path for saving the annotated image
            **kwargs: Additional arguments passed to draw_classification method
            
        Example:
            classifier_viz.save_classification(
                image, results, "output/classified_image.jpg",
                position_type="bottom-right", show_probability=True
            )
        """
        result_image = self.draw_classification(image, classification_result, **kwargs)
        cv2.imwrite(output_path, result_image)
        print(f"[INFO] Classification result saved to: {output_path}")
    
    def get_classification_by_id(self, classification_results: List[Dict[str, Any]], class_id: int = 0) -> Dict[str, Any]:
        """
        Retrieve classification information for a specific class ID.
        
        Searches through classification results to find information for a specific
        class identifier. Useful for extracting specific class confidence scores
        and labels from multi-class results.
        
        Args:
            classification_results (List[Dict[str, Any]]): List of classification results
            class_id (int): Target class ID to search for (default: 0)
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                          - 'confidence': Confidence score for the specified class [0, 1]
                          - 'label': Human-readable class name
                          Returns default values if class ID not found
                          
        Example:
            class_info = classifier_viz.get_classification_by_id(results, class_id=2)
            print(f"Class 2 confidence: {class_info['confidence']}")
        """
        for result in classification_results:
            if result.get('class_id') == class_id:
                return {
                    'confidence': result.get('score', 0.0),  # Updated to use 'score' key
                    'label': result.get('class_name', 'Unknown')
                }
        
        # Return default values if specified class ID not found
        return {
            'confidence': 0.0,
            'label': 'Unknown'
        }
    
    def get_classification_stats(self, classification_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics from classification results.
        
        Analyzes classification results to extract key statistics including
        total number of classes, highest confidence prediction, and associated
        metadata. Useful for result analysis and visualization decisions.
        
        Args:
            classification_result (Dict[str, Any]): Classification result containing:
                                                   - 'result': List of class predictions
                                                   
        Returns:
            Dict[str, Any]: Statistics dictionary containing:
                          - 'total_labels': Total number of classified labels
                          - 'max_confidence_id': Class ID with highest confidence  
                          - 'max_confidence_classname': Name of highest confidence class
                          - 'max_confidence': Highest confidence score [0, 1]
                          
        Example:
            stats = classifier_viz.get_classification_stats(classification_result)
            print(f"Best prediction: {stats['max_confidence_classname']} "
                  f"({stats['max_confidence']:.3f})")
        """
        results = classification_result.get('result', [])
        
        if not results:
            return {
                'total_labels': 0,
                'max_confidence_id': -1,
                'max_confidence_classname': 'Unknown',
                'max_confidence': 0.0
            }
        
        # Calculate total number of labels
        total_labels = len(results)
        
        # Find prediction with highest confidence
        max_confidence = -1
        max_confidence_id = -1
        max_confidence_classname = 'Unknown'
        
        for result in results:
            confidence = result.get('score', 0.0)  # Updated to use 'score' key
            if confidence > max_confidence:
                max_confidence = confidence
                max_confidence_id = result.get('class_id', -1)
                max_confidence_classname = result.get('class_name', 'Unknown')
        
        return {
            'total_labels': total_labels,
            'max_confidence_id': max_confidence_id,
            'max_confidence_classname': max_confidence_classname,
            'max_confidence': max_confidence
        }
    
