# Standard Libraries
import argparse
import time

# Self-made Libraries
import util.app as app

def main(arg):
    # Initialize
    detector = app.VideoDetector()

    # Load Settings
    detector.roadConfigFile(arg)

    # Set up
    detector.setupVideoCapture()
    detector.setupVideoWriter()
    detector.setupModel()

    # Try Detect
    detector.detectHumanBody()

if __name__ == '__main__':
    start = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Load YML')

    args = parser.parse_args()

    main(args.config)
    end = time.perf_counter()

    print(f"実行時間: {end - start:.2f}s")