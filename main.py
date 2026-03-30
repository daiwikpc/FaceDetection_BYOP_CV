"""
Face Detection using OpenCV and Haar Cascades
A beginner-friendly Computer Vision project that detects faces in images and webcam feeds.

Author: Your Name
Date: 2026
"""

import cv2
import os
import sys
from pathlib import Path


class FaceDetector:
    """
    A simple face detection class using OpenCV's Haar Cascade Classifier.
    
    Haar Cascades are pre-trained classifiers that use machine learning
    to detect objects (in this case, faces) in images.
    """
    
    def __init__(self):
        """
        Initialize the Face Detector with Haar Cascade classifier.
        """
        # Load the pre-trained Haar Cascade for face detection
        # This XML file contains the trained cascade classifier
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Verify if the cascade was loaded successfully
        if self.face_cascade.empty():
            raise Exception("Error: Could not load Haar Cascade classifier!")
        
        print("✓ Haar Cascade classifier loaded successfully!")
    
    def detect_faces_in_image(self, image_path, output_path=None):
        """
        Detect faces in a single image file.
        
        Args:
            image_path (str): Path to the input image
            output_path (str): Optional path to save the output image with detected faces
            
        Returns:
            dict: Contains detected faces count and face coordinates
        """
        # Check if the image file exists
        if not os.path.exists(image_path):
            print(f"✗ Error: Image file '{image_path}' not found!")
            return None
        
        # Read the image from the specified path
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"✗ Error: Could not read image '{image_path}'!")
            return None
        
        # Convert image to grayscale (Haar Cascades work better on grayscale images)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces using the Haar Cascade classifier
        # Parameters:
        # - scaleFactor: How much the image size is reduced at each image pyramid level
        # - minNeighbors: How many neighbors each candidate rectangle should have
        # - minSize: Minimum face size
        # - maxSize: Maximum face size
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            maxSize=(500, 500)
        )
        
        # Prepare results
        results = {
            'image_path': image_path,
            'faces_detected': len(faces),
            'face_coordinates': faces.tolist()
        }
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            # Draw a blue rectangle around each detected face
            # Color format is BGR (Blue, Green, Red) in OpenCV
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Add text above each detected face
            cv2.putText(image, 'Face', (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Save the output image if path is provided
        if output_path:
            cv2.imwrite(output_path, image)
            print(f"✓ Output image saved to: {output_path}")
        
        return results
    
    def detect_faces_in_video(self, video_path, output_path=None):
        """
        Detect faces in a video file.
        
        Args:
            video_path (str): Path to the input video
            output_path (str): Optional path to save the output video with detected faces
            
        Returns:
            dict: Contains detection statistics
        """
        # Check if the video file exists
        if not os.path.exists(video_path):
            print(f"✗ Error: Video file '{video_path}' not found!")
            return None
        
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"✗ Error: Could not open video '{video_path}'!")
            return None
        
        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Initialize video writer if output path is provided
        out = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        
        frame_count = 0
        total_faces_detected = 0
        
        print(f"Processing video: {total_frames} frames at {fps} FPS...")
        
        # Process each frame in the video
        while True:
            ret, frame = cap.read()
            
            # Break if no more frames
            if not ret:
                break
            
            frame_count += 1
            
            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces in the frame
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            total_faces_detected += len(faces)
            
            # Draw rectangles around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, 'Face', (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Write frame to output video if writer is initialized
            if out:
                out.write(frame)
            
            # Print progress every 30 frames
            if frame_count % 30 == 0:
                print(f"  Processed {frame_count}/{total_frames} frames...")
        
        # Release resources
        cap.release()
        if out:
            out.release()
            print(f"✓ Output video saved to: {output_path}")
        
        results = {
            'video_path': video_path,
            'total_frames': total_frames,
            'total_faces_detected': total_faces_detected,
            'average_faces_per_frame': total_faces_detected / total_frames if total_frames > 0 else 0
        }
        
        return results
    
    def detect_faces_webcam(self, duration_seconds=10):
        """
        Real-time face detection using webcam.
        
        Args:
            duration_seconds (int): Duration to run the webcam (in seconds)
            
        Returns:
            dict: Contains detection statistics
        """
        # Open the default webcam (index 0)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("✗ Error: Could not access webcam!")
            return None
        
        print(f"✓ Webcam opened successfully!")
        print(f"Press 'q' to quit or wait for {duration_seconds} seconds...")
        
        frame_count = 0
        total_faces = 0
        
        import time
        start_time = time.time()
        
        # Capture frames from webcam
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("✗ Error: Could not read frame from webcam!")
                break
            
            frame_count += 1
            
            # Convert frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces in the frame
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            total_faces += len(faces)
            
            # Draw rectangles around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, 'Face', (x, y - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display face count on frame
            cv2.putText(frame, f'Faces: {len(faces)}', (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display the frame
            cv2.imshow('Face Detection - Webcam', frame)
            
            # Check for quit condition
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("✓ Webcam stream stopped by user.")
                break
            
            # Check if duration exceeded
            if time.time() - start_time > duration_seconds:
                print(f"✓ Duration of {duration_seconds} seconds reached.")
                break
        
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        
        results = {
            'total_frames': frame_count,
            'total_faces_detected': total_faces,
            'average_faces_per_frame': total_faces / frame_count if frame_count > 0 else 0,
            'duration_seconds': time.time() - start_time
        }
        
        return results


def create_sample_data():
    """Create the data directory if it doesn't exist."""
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    return data_dir


def print_results(results, mode='image'):
    """
    Pretty-print the detection results.
    
    Args:
        results (dict): Detection results
        mode (str): Type of detection ('image', 'video', or 'webcam')
    """
    print("\n" + "="*60)
    print("FACE DETECTION RESULTS")
    print("="*60)
    
    if mode == 'image':
        print(f"Image: {results['image_path']}")
        print(f"Faces Detected: {results['faces_detected']}")
        if results['faces_detected'] > 0:
            print(f"Face Coordinates (x, y, width, height):")
            for i, face in enumerate(results['face_coordinates'], 1):
                print(f"  Face {i}: {face}")
    
    elif mode == 'video':
        print(f"Video: {results['video_path']}")
        print(f"Total Frames: {results['total_frames']}")
        print(f"Total Faces Detected: {results['total_faces_detected']}")
        print(f"Average Faces per Frame: {results['average_faces_per_frame']:.2f}")
    
    elif mode == 'webcam':
        print(f"Total Frames Processed: {results['total_frames']}")
        print(f"Total Faces Detected: {results['total_faces_detected']}")
        print(f"Average Faces per Frame: {results['average_faces_per_frame']:.2f}")
        print(f"Duration: {results['duration_seconds']:.2f} seconds")
    
    print("="*60 + "\n")


def main():
    """Main function to demonstrate face detection capabilities."""
    
    print("\n" + "="*60)
    print("FACE DETECTION SYSTEM")
    print("="*60 + "\n")
    
    # Initialize the Face Detector
    detector = FaceDetector()
    
    # Create data directory
    data_dir = create_sample_data()
    
    # Example 1: Detect faces in an image (if image exists in data folder)
    print("\n[MODE 1] IMAGE DETECTION")
    print("-" * 60)
    
    image_path = 'data/sample_image.jpg'
    if os.path.exists(image_path):
        output_image = 'data/output_image.jpg'
        results = detector.detect_faces_in_image(image_path, output_image)
        if results:
            print_results(results, mode='image')
    else:
        print(f"ℹ No sample image found at '{image_path}'")
        print("  To test image detection:")
        print("  1. Place an image file named 'sample_image.jpg' in the 'data' folder")
        print("  2. Run the script again")
    
    # Example 2: Detect faces in a video (if video exists in data folder)
    print("\n[MODE 2] VIDEO DETECTION")
    print("-" * 60)
    
    video_path = 'data/sample_video.mp4'
    if os.path.exists(video_path):
        output_video = 'data/output_video.mp4'
        results = detector.detect_faces_in_video(video_path, output_video)
        if results:
            print_results(results, mode='video')
    else:
        print(f"ℹ No sample video found at '{video_path}'")
        print("  To test video detection:")
        print("  1. Place a video file named 'sample_video.mp4' in the 'data' folder")
        print("  2. Run the script again")
    
    # Example 3: Real-time webcam detection
    print("\n[MODE 3] WEBCAM DETECTION")
    print("-" * 60)
    print("Starting real-time face detection with your webcam...")
    print("(Press 'q' in the webcam window to stop, or wait 15 seconds)")
    
    results = detector.detect_faces_webcam(duration_seconds=15)
    if results:
        print_results(results, mode='webcam')
    
    print("\n✓ Face Detection System completed!")
    print("="*60 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Program interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)
