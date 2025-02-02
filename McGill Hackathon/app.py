#app.py
import os
import random

from flask import Flask, render_template, request, send_file, redirect, url_for
import librosa
import numpy as np
from transformers import pipeline
from moviepy.editor import AudioFileClip, VideoClip
import lyricsgenius
import uuid
import matplotlib
import logging
from datetime import datetime, timedelta

# Set Matplotlib to use a non-interactive backend
matplotlib.use('Agg')  # Prevents Flask and Matplotlib from conflicting
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['GENIUS_ACCESS_TOKEN'] = os.environ.get('GENIUS_ACCESS_TOKEN',
                                                   'v6Hzb7oUDavfXharNiy9IZvA3w92OsjsmPkHaI-h1hzr14hYka_fxtGC0rPPkjzP')

app.config['MAX_DURATION'] = 300  # 5 minutes maximum
app.config['FILE_RETENTION'] = timedelta(minutes=30)  # Keep files for 30 minutes

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def process_audio(file_path, start_time=0, end_time=None):
    y, sr = librosa.load(file_path, offset=start_time, duration=end_time - start_time if end_time else None)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)

    return {
        "tempo": tempo,
        "beat_times": librosa.frames_to_time(beat_frames, sr=sr),
        "chroma": chroma,
        "spectral_contrast": spectral_contrast,
        "raw_audio": y,
        "sr": sr
    }


def get_lyrics(song_name):
    genius = lyricsgenius.Genius(app.config['GENIUS_ACCESS_TOKEN'])
    song = genius.search_song(song_name)
    return song.lyrics if song else None


def analyze_mood(lyrics):
    classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
    result = classifier(lyrics[:1000], truncation=True)[0]  # Truncate to avoid long texts
    return result['label']


# Set up color palette based on mood, mapping to specific color pairs for each mood
# Update color in regions based on mood and time
def create_dynamic_visualization1(file_path, audio_data, mood, output_file, fps):
    try:
        y, sr = audio_data["raw_audio"], audio_data["sr"]
        beat_times = audio_data["beat_times"]

        # Create a figure for animation
        fig, ax = plt.subplots(figsize=(16, 9))
        ax.axis("off")  # Remove axis

        # Mood-based color palette for four regions
        mood_colors = {
            "joy": [("#FFD700", "#FF4500"), ("#32CD32", "#98FB98"), ("#00BFFF", "#4682B4"), ("#FF6347", "#FF1493")],
            "sadness": [("#4169E1", "#87CEEB"), ("#2F4F4F", "#708090"), ("#778899", "#B0C4DE"), ("#A9A9A9", "#D3D3D3")],
            "anger": [("#8B0000", "#FF0000"), ("#B22222", "#DC143C"), ("#FF6347", "#FF4500"), ("#FF1493", "#C71585")],
            "neutral": [("#808080", "#FFFFFF"), ("#A9A9A9", "#D3D3D3"), ("#BEBEBE", "#DCDCDC"), ("#C0C0C0", "#DCDCDC")],
            "fear": [("#4B0082", "#8A2BE2"), ("#800080", "#4B0082"), ("#8B008B", "#9932CC"), ("#9400D3", "#8B0000")],
            "disgust": [("#006400", "#32CD32"), ("#556B2F", "#6B8E23"), ("#228B22", "#ADFF2F"), ("#9ACD32", "#808000")],
            "surprise": [("#FFA500", "#FFFF00"), ("#FF4500", "#FF6347"), ("#FFD700", "#FF1493"), ("#FF00FF", "#8A2BE2")]
        }

        colors = mood_colors.get(mood.lower(), [("#FFFFFF", "#000000")] * 4)

        # Define four regions in the screen
        regions = [((0, 0), (0.5, 0.5)), ((0.5, 0), (1, 0.5)), ((0, 0.5), (0.5, 1)), ((0.5, 0.5), (1, 1))]

        # Number of elements per region
        num_elements = 10

        # Random positions and velocities for various shapes in each region
        shapes = []
        for i in range(4):  # Four regions
            region_shapes = []
            for j in range(num_elements):
                shape_type = np.random.choice(["circle", "bar", "line", "triangle"])
                velocity = (np.random.rand(2) - 0.5) * 0.1  # Randomized initial velocity
                region_shapes.append({"type": shape_type, "velocity": velocity, "position": np.random.rand(2)})
            shapes.append(region_shapes)

        def make_frame(t):
            ax.clear()

            # Update background color with a flowing gradient effect
            gradient_direction = np.sin(t * 0.3)  # Flowing effect
            bg_colors = [np.array([0.5 + 0.5 * np.sin(gradient_direction + i), 0.5 + 0.5 * np.cos(gradient_direction + i),
                                   0.5 + 0.5 * np.sin(gradient_direction + i)]) for i in range(4)]

            # Assign each region a dynamic color based on time
            for i, (color1, color2) in enumerate(colors):
                ax.set_facecolor(tuple(bg_colors[i]))  # Apply color to each quadrant
                region = regions[i]
                ax.fill_betweenx([region[0][1], region[1][1]], region[0][0], region[1][0], color=bg_colors[i])

            # Add elements to each region
            for i, region_shapes in enumerate(shapes):
                for shape in region_shapes:
                    # Update shape properties based on beat
                    size_factor = 1 + 0.5 * np.sin(t * 0.1)  # Sine wave oscillation effect
                    color = np.array([1 - np.abs(np.sin(t * 0.5)), 0.5, np.abs(np.cos(t * 0.5))])

                    # Update position and movement (random directions)
                    shape["position"] += shape["velocity"]

                    # Bounce off the edges of the screen
                    if shape["position"][0] < 0 or shape["position"][0] > 1:
                        shape["velocity"][0] *= -1  # Reverse X velocity
                    if shape["position"][1] < 0 or shape["position"][1] > 1:
                        shape["velocity"][1] *= -1  # Reverse Y velocity

                    if shape["type"] == "circle":
                        ax.scatter(shape["position"][0], shape["position"][1], s=size_factor * 1000, color=color, alpha=0.7)
                    elif shape["type"] == "bar":
                        ax.add_patch(plt.Rectangle((shape["position"][0], 0), 0.05, size_factor, color=color, alpha=0.7))
                    elif shape["type"] == "line":
                        ax.plot([shape["position"][0], shape["position"][0] + 0.1], [shape["position"][1], shape["position"][1] + size_factor],
                                color=color, linewidth=2)
                    elif shape["type"] == "triangle":
                        ax.fill([shape["position"][0], shape["position"][0] + 0.05, shape["position"][0] - 0.05],
                                [shape["position"][1], shape["position"][1] + size_factor, shape["position"][1] + size_factor], color=color, alpha=0.7)

            # Ensure no axis is visible
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            fig.canvas.draw()
            image = np.array(fig.canvas.buffer_rgba())
            return image[:, :, :3]  # Only return RGB channels

        # Render video
        duration = librosa.get_duration(y=y, sr=sr)
        animation = VideoClip(make_frame, duration=duration)
        audio_clip = AudioFileClip(file_path).subclip(0, duration)
        animation = animation.set_audio(audio_clip)
        animation.write_videofile(output_file, fps=fps, codec="libx264", audio_codec="aac")
        plt.close()

    except Exception as e:
        logger.error(f"Error in create_dynamic_visualization: {str(e)}")

# Define screen regions for animation, each with random shape generation (circle, bar, line, triangle)
# Create random positions and velocities for shapes to simulate dynamic movement
# Update shape properties (size, color, position) based on beat times and oscillating effects
# Implement boundary checks to ensure shapes remain within screen bounds (bounce off edges)
# Display different shape types (circle, bar, line, triangle) at random positions
def create_dynamic_visualization2(file_path, audio_data, mood, output_file, fps):
    try:
        y, sr = audio_data["raw_audio"], audio_data["sr"]
        beat_times = audio_data["beat_times"]

        # Create a figure for animation
        fig, ax = plt.subplots(figsize=(16, 9))
        ax.axis("off")

        # Mood-based color palette
        mood_colors = {
            "joy": ("#FFD700", "#FF4500"),
            "sadness": ("#4169E1", "#87CEEB"),
            "anger": ("#8B0000", "#FF0000"),
            "neutral": ("#808080", "#FFFFFF"),
            "fear": ("#4B0082", "#8A2BE2"),
            "disgust": ("#006400", "#32CD32"),
            "surprise": ("#FFA500", "#FFFF00")
        }
        colors = mood_colors.get(mood.lower(), ("#FFFFFF", "#000000"))

        # Generate random positions for circles
        num_circles = 15
        positions = np.random.rand(num_circles, 2)
        circle_velocities = (np.random.rand(num_circles, 2) - 0.5) * 0.1
        circle_radii = np.random.rand(num_circles) * 0.1 + 0.05

        def make_frame(t):
            ax.clear()
            t_index = int(t * sr)
            current_amplitude = np.abs(y[t_index])

            # Plot frequency spectrum
            D = librosa.amplitude_to_db(np.abs(librosa.stft(y[:t_index])), ref=np.max)
            librosa.display.specshow(D, sr=sr, x_axis="time", y_axis="log", ax=ax, cmap="inferno")

            # Update background based on current amplitude (reactive)
            background_color_factor = np.clip(current_amplitude * 10, 0, 1)  # Scale based on amplitude
            bg_color = np.array([background_color_factor, 0, 1 - background_color_factor])  # Smooth gradient
            ax.set_facecolor(tuple(bg_color))  # Apply dynamic background color

            # Add random moving circles
            for i in range(num_circles):
                size_factor = 1 + 0.5 * np.sin(t * (i + 1) * 0.2) * current_amplitude
                color = np.array([1 - current_amplitude, 0.5, current_amplitude])
                positions[i] += circle_velocities[i]
                circle_velocities[i] += (np.random.rand(2) - 0.5) * 0.001
                circle_velocities[i] = np.clip(circle_velocities[i], -0.02, 0.02)
                for j in range(2):
                    if positions[i, j] < 0 or positions[i, j] > 1:
                        circle_velocities[i, j] *= -1
                    positions[i, j] = np.clip(positions[i, j], 0, 1)
                ax.scatter(positions[i, 0], positions[i, 1], s=(size_factor * 1000), color=color, alpha=0.7)

            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            fig.canvas.draw()
            image = np.array(fig.canvas.buffer_rgba())
            return image[:, :, :3]

        # Render video
        duration = librosa.get_duration(y=y, sr=sr)
        animation = VideoClip(make_frame, duration=duration)
        audio_clip = AudioFileClip(file_path).subclip(0, duration)
        animation = animation.set_audio(audio_clip)
        animation.write_videofile(output_file, fps=fps, codec="libx264", audio_codec="aac")
        plt.close()

    except Exception as e:
        logger.error(f"Error in create_dynamic_visualization: {str(e)}")
        raise

# Plot dynamic frequency spectrum and update background color based on audio amplitude
# Animate moving circles with size and position changes based on beat and amplitude
# Generate video and audio synchronization, writing the output to the specified file
def create_dynamic_visualization3(file_path, audio_data, mood, output_file, fps):
    try:
        y, sr = audio_data["raw_audio"], audio_data["sr"]
        beat_times = audio_data["beat_times"]

        # Create a figure for animation
        fig, ax = plt.subplots(figsize=(16, 9))
        ax.axis("off")  # Remove axis

        # Mood-based color palette (keep mood-dependent colors for variation)
        mood_colors = {
            "joy": ("#FFD700", "#FF4500"),
            "sadness": ("#4169E1", "#87CEEB"),
            "anger": ("#8B0000", "#FF0000"),
            "neutral": ("#808080", "#FFFFFF"),
            "fear": ("#4B0082", "#8A2BE2"),
            "disgust": ("#006400", "#32CD32"),
            "surprise": ("#FFA500", "#FFFF00")
        }
        colors = mood_colors.get(mood.lower(), ("#FFFFFF", "#000000"))

        # Generate random positions for circles (same as before)
        num_circles = 15
        positions = np.random.rand(num_circles, 2)
        circle_velocities = (np.random.rand(num_circles, 2) - 0.5) * 0.1
        circle_radii = np.random.rand(num_circles) * 0.1 + 0.05

        def make_frame(t):
            ax.clear()

            # Set the amplitude (brightness) based on the current audio sample
            t_index = int(t * sr)
            current_amplitude = np.abs(y[t_index])

            # Update background color with flowing gradient effect
            # Create a moving gradient
            gradient_direction = np.sin(t * 0.5)  # Creates left-to-right flowing effect
            bg_color = np.array([0.5 + 0.5 * np.sin(gradient_direction + 0), 0.5 + 0.5 * np.cos(gradient_direction + 1),
                                 0.5 + 0.5 * np.sin(gradient_direction + 2)])  # Dynamic flowing gradient
            ax.set_facecolor(tuple(bg_color))  # Apply dynamic background color

            # Add dynamic moving circles with amplitude-driven size/color
            for i in range(num_circles):
                size_factor = 1 + 0.5 * np.sin(t * (i + 1) * 0.2) * current_amplitude
                color = np.array([1 - current_amplitude, 0.5, current_amplitude])
                positions[i] += circle_velocities[i]
                circle_velocities[i] += (np.random.rand(2) - 0.5) * 0.001
                circle_velocities[i] = np.clip(circle_velocities[i], -0.02, 0.02)

                for j in range(2):
                    if positions[i, j] < 0 or positions[i, j] > 1:
                        circle_velocities[i, j] *= -1
                    positions[i, j] = np.clip(positions[i, j], 0, 1)

                ax.scatter(positions[i, 0], positions[i, 1], s=(size_factor * 1000), color=color, alpha=0.7)

            ax.set_xticks([])  # Remove x-axis ticks
            ax.set_yticks([])  # Remove y-axis ticks
            ax.set_xlim(0, 1)  # Set consistent scale
            ax.set_ylim(0, 1)  # Set consistent scale
            fig.canvas.draw()
            image = np.array(fig.canvas.buffer_rgba())
            return image[:, :, :3]  # Only return RGB channels

        # Render video
        duration = librosa.get_duration(y=y, sr=sr)
        animation = VideoClip(make_frame, duration=duration)
        audio_clip = AudioFileClip(file_path).subclip(0, duration)
        animation = animation.set_audio(audio_clip)
        animation.write_videofile(output_file, fps=fps, codec="libx264", audio_codec="aac")
        plt.close()

    except Exception as e:
        logger.error(f"Error in create_dynamic_visualization: {str(e)}")
        raise

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    start_time = request.form.get('start_time', type=float, default=0)
    end_time = request.form.get('end_time', type=float)
    fps = request.form.get('fps', type=int)  # Get fps and convert to integer

    # Generate unique filenames
    unique_id = str(uuid.uuid4())
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{unique_id}_output.mp4")

    # Save the uploaded file
    file.save(upload_path)

    try:
        # Process audio with start_time and end_time
        audio_data = process_audio(upload_path, start_time, end_time)
        song_name = os.path.splitext(file.filename)[0]

        # Get lyrics and mood
        lyrics = get_lyrics(song_name)
        mood = analyze_mood(lyrics) if lyrics else "neutral"

        # Create visualization
        rando = random.randint(1, 3)
        if rando == 1:
            create_dynamic_visualization1(upload_path, audio_data, mood, output_path, fps)
        elif rando == 2:
            create_dynamic_visualization2(upload_path, audio_data, mood, output_path, fps)
        else:
            create_dynamic_visualization3(upload_path, audio_data, mood, output_path, fps)

        # Generate the video URL for the result page
        video_url = url_for('serve_video', filename=f"{unique_id}_output.mp4")

        # Render the result template with the video URL, song name, and mood
        return render_template('result.html',
                               video_url=video_url,
                               song_name=song_name,
                               mood=mood)

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return f"Error processing file: {str(e)}", 500

    finally:
        # Cleanup temporary files
        if os.path.exists(upload_path):
            os.remove(upload_path)

@app.route('/video/<filename>')
def serve_video(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))


if __name__ == '__main__':
    app.run(debug=True)