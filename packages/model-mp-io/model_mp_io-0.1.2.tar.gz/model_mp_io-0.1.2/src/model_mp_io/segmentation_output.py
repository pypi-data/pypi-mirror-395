import cv2
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import time
import os


class SegmentationOutput:
    """
    Output helper for image segmentation results.

    Responsibilities:
    - Input: image and inference results
    - Output: image annotated with masks, boxes, labels and confidences
    """
    
    def __init__(self, colors=None, alpha=0.5, class_names=None):
        """
        Initialize the segmentation output helper.

        Args:
            colors: optional list of colors used to render different class masks
            alpha: mask overlay transparency (0-1)
            class_names: optional list or dict mapping class IDs to human-friendly names
        """
        self.colors = colors or self._generate_colors(80)  # default 80 different colors
        self.alpha = alpha
        # Default class name mapping, can be adjusted based on actual model
        self.class_names = class_names 
    
    def _generate_colors(self, num_colors: int) -> List[Tuple[int, int, int]]:
        """
        Generate a deterministic list of random RGB colors.

        A fixed seed ensures the same colors every run.
        """
        np.random.seed(42)  # fixed seed to ensure consistent colors
        colors = []
        for _ in range(num_colors):
            colors.append(tuple(np.random.randint(0, 255, 3).tolist()))
        return colors
    
    def get_class_name(self, class_id: int) -> str:
        """
        Resolve a class name from a given class ID.

        Args:
            class_id: integer class identifier

        Returns:
            Human-readable class name as string
        """
        if isinstance(self.class_names, dict):
            return self.class_names.get(class_id, f"Class {class_id}")
        elif isinstance(self.class_names, list) and 0 <= class_id < len(self.class_names):
            return self.class_names[class_id]
        else:
            return f"Class {class_id}"
    
    def draw_segmentation(self, image: np.ndarray, segmentation_results: Dict[str, Any], 
                         draw_boxes: bool = True, draw_masks: bool = True,
                         thickness: int = 2, font_scale: float = 0.6) -> np.ndarray:
        """
        Draw segmentation results on an image.

        Args:
            image: input image as a numpy array (BGR)
            segmentation_results: a dict-like object containing keys 'boxes', 'scores',
                'class_ids', and 'masks'
            draw_boxes: whether to draw bounding boxes
            draw_masks: whether to render segmentation masks as overlays
            thickness: line thickness for boxes and label text stroke
            font_scale: font scale for text labels

        Returns:
            Image with segmentation visualization applied.
        """
        result_image = image.copy()
        
        boxes = segmentation_results.get('boxes', [])
        scores = segmentation_results.get('scores', [])
        class_ids = segmentation_results.get('class_ids', [])
        masks = segmentation_results.get('masks', [])
        
        # Create an overlay for masks
        if draw_masks and masks:
            mask_overlay = np.zeros_like(image, dtype=np.uint8)
            
            for i, mask in enumerate(masks):
                if i < len(class_ids):
                    class_id = class_ids[i]
                    color = self.colors[class_id % len(self.colors)]
                    
                    # Apply the mask to the colored overlay
                    mask_colored = np.zeros_like(image, dtype=np.uint8)
                    mask_colored[mask > 0] = color
                    mask_overlay = cv2.addWeighted(mask_overlay, 1.0, mask_colored, 1.0, 0)
            
            # Blend mask overlay onto the original image with configured alpha
            result_image = cv2.addWeighted(result_image, 1.0, mask_overlay, self.alpha, 0)
        
        # Draw bounding boxes and labels
        if draw_boxes and boxes:
            for i, box in enumerate(boxes):
                if i < len(scores) and i < len(class_ids):
                    x1, y1, x2, y2 = map(int, box)
                    score = scores[i]
                    class_id = class_ids[i]
                    
                    # Choose a color for this class
                    color = self.colors[class_id % len(self.colors)]
                    
                    # Resolve class name for display
                    class_name = self.get_class_name(class_id)
                    
                    # Draw the bounding box
                    cv2.rectangle(result_image, (x1, y1), (x2, y2), color, thickness)
                    
                    # Prepare label text showing class name, id and confidence
                    label = f"{class_name} ({class_id}): {score:.2f}"
                    
                    # Calculate text size for background box
                    (text_width, text_height), baseline = cv2.getTextSize(
                        label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness
                    )
                    
                    # Draw background rectangle for text for readability
                    cv2.rectangle(
                        result_image,
                        (x1, y1 - text_height - baseline - 5),
                        (x1 + text_width, y1),
                        color,
                        -1
                    )
                    
                    # Draw the text label in white on top of the background
                    cv2.putText(
                        result_image,
                        label,
                        (x1, y1 - baseline - 2),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale,
                        (255, 255, 255),
                        thickness
                    )
        
        return result_image
    
    def draw_masks_only(self, image: np.ndarray, masks: List[np.ndarray], 
                       class_ids: Optional[List[int]] = None) -> np.ndarray:
        """
        Render only segmentation masks onto the image (no boxes or labels).

        Args:
            image: input image as numpy array (BGR)
            masks: list of binary mask arrays
            class_ids: optional list of class IDs corresponding to masks

        Returns:
            Image with masks blended on top.
        """
        result_image = image.copy()
        mask_overlay = np.zeros_like(image, dtype=np.uint8)
        
        for i, mask in enumerate(masks):
            if class_ids and i < len(class_ids):
                class_id = class_ids[i]
            else:
                class_id = i
            
            color = self.colors[class_id % len(self.colors)]
            
            # Apply this mask with the chosen color to the overlay
            mask_colored = np.zeros_like(image, dtype=np.uint8)
            mask_colored[mask > 0] = color
            mask_overlay = cv2.addWeighted(mask_overlay, 1.0, mask_colored, 1.0, 0)
        
        # Blend mask overlay onto the original image
        result_image = cv2.addWeighted(result_image, 1.0, mask_overlay, self.alpha, 0)
        
        return result_image
    
    def save_segmentation(self, image: np.ndarray, output_path: str, **kwargs) -> None:
        """
        Save the annotated segmentation image to disk.

        Args:
            image: annotated image to save
            output_path: destination file path
            **kwargs: extra arguments (kept for API compatibility)
        """
        cv2.imwrite(output_path, image)
    
    def save_masks_separately(self, image: np.ndarray, masks: List[np.ndarray], 
                             class_ids: Optional[List[int]] = None,
                             output_dir: str = ".") -> None:
        """
        Save each mask as a separate image file.

        Each saved image contains only the colored region for a single mask.

        Args:
            image: original image to use as a template for mask images
            masks: list of binary mask arrays
            class_ids: optional list of class IDs corresponding to masks
            output_dir: directory where mask images will be written
        """
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for i, mask in enumerate(masks):
            # Create an image that only contains the current mask colored
            mask_image = np.zeros_like(image)
            if class_ids and i < len(class_ids):
                class_id = class_ids[i]
            else:
                class_id = i
            
            color = self.colors[class_id % len(self.colors)]
            mask_image[mask > 0] = color
            
            # Write the mask image to disk and log the location
            class_name = self.get_class_name(class_id)
            output_path = os.path.join(output_dir, f"mask_{i}_{class_name}.png")
            cv2.imwrite(output_path, mask_image)
            print(f"[INFO] Mask {i} ({class_name}) saved to {output_path}")
    
    def print_segmentation_summary(self, segmentation_results: Dict[str, Any]) -> None:
        """
        Print a short human-readable summary of segmentation results.

        Args:
            segmentation_results: dictionary containing boxes, class_ids, scores, etc.
        """
        boxes = segmentation_results.get('boxes', [])
        class_ids = segmentation_results.get('class_ids', [])
        scores = segmentation_results.get('scores', [])
        
        print(f"Detected {len(boxes)} objects:")
        
        # Count occurrences of each class
        class_counts = {}
        for i, box in enumerate(boxes):
            if i < len(class_ids):
                class_id = class_ids[i]
                class_name = self.get_class_name(class_id)
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
        
        # Print class distribution
        for class_name, count in class_counts.items():
            print(f"  {class_name}: {count}")
    
    def get_segmentation_stats(self, segmentation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compute basic statistics from segmentation results.

        Args:
            segmentation_results: dictionary containing 'boxes', 'class_ids', 'scores', 'masks'

        Returns:
            A dictionary with summary statistics such as counts per class,
            average confidence and total mask area.
        """
        boxes = segmentation_results.get('boxes', [])
        class_ids = segmentation_results.get('class_ids', [])
        scores = segmentation_results.get('scores', [])
        masks = segmentation_results.get('masks', [])
        
        # Aggregate statistics
        class_counts = {}
        total_mask_area = 0
        avg_confidence = 0
        
        if scores:
            avg_confidence = sum(scores) / len(scores)
        
        for i, box in enumerate(boxes):
            if i < len(class_ids):
                class_id = class_ids[i]
                class_name = self.get_class_name(class_id)
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
            
            if i < len(masks):
                mask = masks[i]
                total_mask_area += np.sum(mask > 0)
        
        return {
            'total_objects': len(boxes),
            'total_masks': len(masks),
            'class_distribution': class_counts,
            'average_confidence': avg_confidence,
            'total_mask_area': total_mask_area
        }
