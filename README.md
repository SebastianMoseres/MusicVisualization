# Music Visualizer Application (Winner of Best Art Project at McGill AI Society Winter 2025 Hackathon)

This application is a Flask-based web service that generates dynamic music visualizations from uploaded audio files. It analyzes the audio, extracts key features, detects the mood of the song, and creates a video with a dynamic visual representation.

## Overview

The application takes an uploaded audio file (MP3), processes it to extract tempo, beat times, chroma, and spectral contrast. It then uses the song name to fetch lyrics and analyzes those lyrics to determine the mood of the song. Finally, it generates a video visualization based on the audio features and mood. The generated video is returned to the user for download.

## Key Features

*   **Audio Analysis:** Uses `librosa` to analyze audio files, extracting tempo, beat times, chroma, and spectral contrast.
*   **Lyrics and Mood Detection:** Uses `lyricsgenius` to fetch song lyrics and a `transformers` pipeline to analyze the mood of the lyrics.
*   **Dynamic Visualizations**: Generates dynamic visualizations based on the analyzed audio and mood, using `matplotlib` to create animated visuals.
*   **Multiple Visualization Styles:** Offers three different visualization styles that are chosen randomly.
*   **File Handling:** Manages file uploads and temporary file storage.
*   **User Interface:** Provides a simple web interface for uploading files and downloading the generated videos.
*   **Configuration:** Uses a configuration system for setting parameters such as upload folder, output folder, Genius API access token, max duration, and file retention.
*   **Error Handling:** Logs errors and handles exceptions during file processing.
*   **Temporary File Cleanup**: Cleans up temporary files after processing.

## Technologies Used

*   **Flask:** Web framework.
*   **Librosa:** Audio analysis library.
*   **Transformers:** For mood classification.
*   **MoviePy:** Video editing library.
*   **LyricsGenius:** Library to fetch lyrics.
*   **Matplotlib**: Library for creating visualizations.
*   **Numpy**: Library for numerical operations.

## File Structure
The application is primarily contained within the `app.py` file.
* `app.py`: Contains the main Flask application logic, including audio processing, visualization generation, and route handling.
* `index.html` (not directly included in the provided sources): Serves as the template for the upload page and download page.

## Configuration
The application uses the following configuration variables:
*   `UPLOAD_FOLDER`:  Directory where uploaded files are stored.
*   `OUTPUT_FOLDER`: Directory where generated videos are stored.
*   `GENIUS_ACCESS_TOKEN`:  API token for the LyricsGenius service.
*   `MAX_DURATION`: Maximum duration of the audio file to be processed (set to 300 seconds or 5 minutes).
*   `FILE_RETENTION`:  Time duration for which uploaded files will be retained (set to 30 minutes).

## How to Use

1.  **Upload Audio:** Use the provided web interface to upload an MP3 audio file.
2.  **Set Parameters:** You can optionally set the start time, end time, and frames per second for the video.
3. **Process Audio:** After submitting the audio file, the application will begin processing. This may take some time depending on the file size.
4.  **Download Video:** Once processing is complete, you will be able to download the generated visualization video.

## Visualization Details

The visualization is dynamically generated based on the mood detected from the song lyrics. The script contains three different visualization functions:

### `create_dynamic_visualization1`
*   Divides the screen into four regions, each with its own color.
*   Displays various shapes that move within each region, bouncing off the edges of the screen.
*   Updates background color with a flowing gradient effect.
*   Shapes change size based on a sine wave oscillation.
*   Shape colors also change over time.

### `create_dynamic_visualization2`
*   Displays a frequency spectrum of the audio using `librosa.display.specshow`.
*   Dynamically changes the background color based on the current audio amplitude.
*   Adds moving circles that change size and color based on amplitude and time.

### `create_dynamic_visualization3`
*   Uses a similar circle animation approach to `create_dynamic_visualization2`, with moving circles that change size and color based on the current audio sample.
*   Updates the background color with a flowing gradient that moves from left to right.
*   Features dynamic color and size changes for the circles.

Each visualization function takes parameters such as the audio file path, the analyzed audio data, the detected mood, the output path, and the frames per second.

## Code Snippets

The `app.py` file includes the following key functions:

*   `process_audio(file_path, start_time=0, end_time=None)`: Loads audio file using `librosa` and extracts audio features like tempo, beat times, chroma, and spectral contrast.
*   `get_lyrics(song_name)`: Uses `lyricsgenius` to search for and retrieve the lyrics of a given song.
*   `analyze_mood(lyrics)`: Employs a pre-trained transformer model to classify the mood from the provided lyrics.
*   `create_dynamic_visualization1(file_path, audio_data, mood, output_file, fps)`: Generates the first type of dynamic music visualization video.
*   `create_dynamic_visualization2(file_path, audio_data, mood, output_file, fps)`: Generates the second type of dynamic music visualization video.
*   `create_dynamic_visualization3(file_path, audio_data, mood, output_file, fps)`: Generates the third type of dynamic music visualization video.
*   `upload_file()`: Handles the file upload, processes the audio, and generates the video visualization.

## Notes
*   The application uses a random number generator to choose one of the three visualization styles.
*   The application uses a non-interactive backend for Matplotlib to avoid conflicts with Flask.
*   The application is configured to log debug messages.
*   The video is generated using the `libx264` codec for video and `aac` for audio.
*   The maximum duration of the video is limited to 5 minutes, as set by the `MAX_DURATION` variable.

