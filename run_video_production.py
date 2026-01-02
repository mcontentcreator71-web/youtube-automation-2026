#!/usr/bin/env python3
"""
Wrapper script for video production that handles input from command line or stdin
This makes it easier to call from n8n Execute Command nodes
"""

import json
import sys
import os
from pathlib import Path

# Add current directory to path to import video_production
sys.path.insert(0, str(Path(__file__).parent))

try:
    from video_production import VideoProducer
except ImportError:
    print(json.dumps({
        'error': 'Could not import video_production module. Make sure video_production.py is in the same directory.',
        'status': 'failed'
    }))
    sys.exit(1)

def main():
    """Main entry point for video production"""
    try:
        # Try to read from stdin first (n8n will pass JSON here)
        input_data = None
        
        # First try command line argument (for execSync compatibility)
        if len(sys.argv) > 1:
            try:
                input_data = json.loads(sys.argv[1])
            except (json.JSONDecodeError, ValueError):
                # If not JSON, might be a file path
                if os.path.exists(sys.argv[1]):
                    with open(sys.argv[1], 'r', encoding='utf-8') as f:
                        input_data = json.load(f)
        
        # If no command line arg, try stdin
        if not input_data and not sys.stdin.isatty():
            # Data is being piped in
            input_str = sys.stdin.read()
            if input_str.strip():
                input_data = json.loads(input_str)
        
        if not input_data:
            # Use default test data
            input_data = {
                'title': 'AI News Update',
                'videoType': 'shorts',
                'shortScript': 'AI technology is rapidly evolving. Stay tuned for updates.',
                'longScript': 'AI technology continues to advance.',
                'imagePrompts': ['AI technology', 'Machine learning']
            }
        
        # Create video producer
        output_dir = os.getenv('VIDEO_OUTPUT_DIR', './videos')
        producer = VideoProducer(output_dir=output_dir)
        
        # Process video request
        result = producer.process_video_request(input_data)
        
        # Output result as JSON
        print(json.dumps(result))
        
        # Exit with error code if failed
        if result.get('status') != 'success':
            sys.exit(1)
            
    except json.JSONDecodeError as e:
        print(json.dumps({
            'error': f'Invalid JSON input: {str(e)}',
            'status': 'failed'
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            'error': str(e),
            'status': 'failed'
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()

