# Music Visualizer Application

This application is a Flask-based web service that generates dynamic music visualizations from uploaded audio files. It analyzes the audio, extracts key features, detects the mood of the song, and creates a video with a dynamic visual representation.

## Overview

The application takes an uploaded audio file (MP3), processes it to extract tempo, beat times, chroma, and spectral contrast [1]. It then uses the song name to fetch lyrics and analyzes those lyrics to determine the mood of the song [2]. Finally, it generates a video visualization based on the audio features and mood [3]. The generated video is returned to the user for download [4].

## Key Features

*   **Audio Analysis:** Uses `librosa` to analyze audio files, extracting tempo, beat times, chroma, and spectral contrast [1, 2].
*   **Lyrics and Mood Detection:** Uses `lyricsgenius` to fetch song lyrics and a `transformers` pipeline to analyze the mood of the lyrics [2].
*  **Dynamic Visualizations**: Generates dynamic visualizations based on the analyzed audio and mood, using `matplotlib` to create animated visuals [3].
*   **Multiple Visualization Styles:** Offers three different visualization styles that are chosen randomly [4].
*   **File Handling:** Manages file uploads and temporary file storage [5, 6].
*   **User Interface:** Provides a simple web interface for uploading files and downloading the generated videos [7, 8].
*   **Configuration:** Uses a configuration system for setting parameters such as upload folder, output folder, Genius API access token, max duration, and file retention [5].
*   **Error Handling:** Logs errors and handles exceptions during file processing [1, 9].
*   **Temporary File Cleanup**: Cleans up temporary files after processing [9].

## Technologies Used

*   **Flask:** Web framework [10].
*   **Librosa:** Audio analysis library [10].
*   **Transformers:** For mood classification [10].
*   **MoviePy:** Video editing library [10].
*   **LyricsGenius:** Library to fetch lyrics [10].
*  **Matplotlib**: Library for creating visualizations [10].
*  **Numpy**: Library for numerical operations [10].

## File Structure
The application is primarily contained within the `app.py` file [10].
* `app.py`: Contains the main Flask application logic, including audio processing, visualization generation, and route handling.
* `index.html` (not directly included in the provided sources): Serves as the template for the upload page and download page [8, 11].

## Configuration
The application uses the following configuration variables:
*   `UPLOAD_FOLDER`:  Directory where uploaded files are stored [5].
*   `OUTPUT_FOLDER`: Directory where generated videos are stored [5].
*   `GENIUS_ACCESS_TOKEN`:  API token for the LyricsGenius service [5].
*  `MAX_DURATION`: Maximum duration of the audio file to be processed (set to 300 seconds or 5 minutes) [5].
*  `FILE_RETENTION`:  Time duration for which uploaded files will be retained (set to 30 minutes) [5].

## How to Use

1.  **Upload Audio:** Use the provided web interface to upload an MP3 audio file [8].
2.  **Set Parameters:** You can optionally set the start time, end time, and frames per second for the video [8].
3. **Process Audio:** After submitting the audio file, the application will begin processing. This may take some time depending on the file size [8].
4.  **Download Video:** Once processing is complete, you will be able to download the generated visualization video [11].

## Visualization Details

The visualization is dynamically generated based on the mood detected from the song lyrics [2]. The script contains three different visualization functions:

### `create_dynamic_visualization1`
*   Divides the screen into four regions, each with its own color [12].
*   Displays various shapes that move within each region, bouncing off the edges of the screen [12-14].
*   Updates background color with a flowing gradient effect [15].
*   Shapes change size based on a sine wave oscillation [13].
*   Shape colors also change over time [13].

### `create_dynamic_visualization2`
*   Displays a frequency spectrum of the audio using `librosa.display.specshow` [16].
*   Dynamically changes the background color based on the current audio amplitude [16, 17].
*   Adds moving circles that change size and color based on amplitude and time [16-18].

### `create_dynamic_visualization3`
*   Uses a similar circle animation approach to `create_dynamic_visualization2`, with moving circles that change size and color based on the current audio sample [19-21].
*  Updates the background color with a flowing gradient that moves from left to right [20].
*  Features dynamic color and size changes for the circles [20, 21].

Each visualization function takes parameters such as the audio file path, the analyzed audio data, the detected mood, the output path, and the frames per second [3, 22-24].

## Code Snippets

The `app.py` file includes the following key functions:

*   `process_audio(file_path, start_time=0, end_time=None)`: Loads audio file using `librosa` and extracts audio features like tempo, beat times, chroma, and spectral contrast [1].
*   `get_lyrics(song_name)`: Uses `lyricsgenius` to search for and retrieve the lyrics of a given song [2].
*   `analyze_mood(lyrics)`: Employs a pre-trained transformer model to classify the mood from the provided lyrics [2].
*  `create_dynamic_visualization1(file_path, audio_data, mood, output_file, fps)`: Generates the first type of dynamic music visualization video [3].
*  `create_dynamic_visualization2(file_path, audio_data, mood, output_file, fps)`: Generates the second type of dynamic music visualization video [22].
*  `create_dynamic_visualization3(file_path, audio_data, mood, output_file, fps)`: Generates the third type of dynamic music visualization video [23].
*   `upload_file()`: Handles the file upload, processes the audio, and generates the video visualization [6].

## Notes
*   The application uses a random number generator to choose one of the three visualization styles [4].
*   The application uses a non-interactive backend for Matplotlib to avoid conflicts with Flask [10].
*   The application is configured to log debug messages [1].
*   The video is generated using the `libx264` codec for video and `aac` for audio [22-24].
*   The maximum duration of the video is limited to 5 minutes, as set by the `MAX_DURATION` variable [5].

