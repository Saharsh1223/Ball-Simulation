import pygame
import sys
import random
import math
import os
import record_audio
import export_vid
import vidmaker

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 495, 880
FPS = 60
GRAVITY = 0.5
BALL_RADIUS = 10
CIRCLE_RADIUS = 170
DISPLACEMENT = 2  # Adjust as needed
SIZE_INCREASE = 1  # Adjust as needed
REFLECTION_FORCE = 12  # Adjust as needed
COLOR_CHANGE_SPEED = 8  # Adjust as needed

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initial color of the ball (green)
initial_color = (0, 255, 0)

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Ball with Curved Circle and Size Increase")

video = vidmaker.Video("output.mp4", late_export=True)

# Load custom font
font_path = "roboto-mono.ttf"  # Replace with the actual file path
font = pygame.font.Font(font_path, 24)  # Adjust the font size as needed

collisions = 0

# Ball properties
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = random.uniform(-5, 5)  # Initial force along the x-axis
ball_speed_y = random.uniform(-5, 5)  # Initial force along the y-axis
ball_radius = BALL_RADIUS

# Game loop
clock = pygame.time.Clock()
physics_update_rate = 1  # Update physics every frame

# Variable to track the end of the simulation
simulation_end_time = None
closing_delay = 5000  # 5 seconds in milliseconds

# List to store ball trail components
ball_trail = []

# Initialize the mixer
pygame.mixer.init()

# Load the collision sound
collision_sound = pygame.mixer.Sound("collision_sound.mp3")

def reflect_vector(incident, normal):
    dot = incident[0] * normal[0] + incident[1] * normal[1]
    reflected = [incident[0] - 2 * dot * normal[0], incident[1] - 2 * dot * normal[1]]
    return reflected

def interpolate_color(start_color, end_color, t):
    start_hsv = pygame.Color(start_color).hsva
    end_hsv = pygame.Color(end_color).hsva
    
    # Ensure the hue values stay within the valid range (0-360)
    current_hsv = (
        (start_hsv[0] + t * (end_hsv[0] - start_hsv[0])) % 360,
        start_hsv[1] + t * (end_hsv[1] - start_hsv[1]),
        start_hsv[2] + t * (end_hsv[2] - start_hsv[2]),
    )
    
    # Convert HSV to RGB manually
    current_rgb = pygame.Color(0, 0, 0)
    current_rgb.hsva = current_hsv
    return current_rgb

record_audio.start_recording()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            record_audio.stop_recording()
            video.export(verbose=True)
            
            video_file = "output.mp4"
            audio_file = "output.wav"
            output_file = "output_upgraded_resolution_with_text.mp4"

            text_value = "Test text here"
            text_position = (0, 0.05)

            export_vid.join_video_and_audio(video_file, audio_file, output_file, text=text_value, text_position=text_position)
            
            pygame.quit()
            sys.exit()

    # Physics updates
    for _ in range(physics_update_rate):
        # Check if the ball size is less than the circle size
        if ball_radius < CIRCLE_RADIUS:
            # Check collision with the circle
            distance = math.sqrt((ball_x - WIDTH // 2) ** 2 + (ball_y - HEIGHT // 2) ** 2)
            if distance >= CIRCLE_RADIUS - ball_radius:
                # Reflect the ball off the curved surface with a fixed force
                normal = [WIDTH // 2 - ball_x, HEIGHT // 2 - ball_y]
                normal_length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
                normal = [normal[0] / normal_length, normal[1] / normal_length]

                incident = [ball_speed_x, ball_speed_y]
                reflected = reflect_vector(incident, normal)

                # Normalize the reflected vector and apply the fixed reflection force
                reflected_length = math.sqrt(reflected[0] ** 2 + reflected[1] ** 2)
                reflected = [REFLECTION_FORCE * reflected[0] / reflected_length, REFLECTION_FORCE * reflected[1] / reflected_length]

                ball_speed_x, ball_speed_y = reflected

                # Displace the ball slightly from the border to avoid getting stuck
                displacement = [DISPLACEMENT * normal[0], DISPLACEMENT * normal[1]]
                ball_x += displacement[0]
                ball_y += displacement[1]

                # Increase ball size
                ball_radius += SIZE_INCREASE

                # Increment collision count
                collisions += 1

                # Play the collision sound
                collision_sound.play()

        # Apply gravity to the ball when not reflecting
        if distance < CIRCLE_RADIUS - ball_radius:
            ball_speed_y += GRAVITY

        # Update ball position
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Check collision with the bottom of the window
        if ball_y + ball_radius >= HEIGHT:
            ball_speed_y = -ball_speed_y

        # Check if the ball size exceeds the circle size
        if ball_radius >= CIRCLE_RADIUS:
            if simulation_end_time is None:
                simulation_end_time = pygame.time.get_ticks()  # Record the time when the simulation ends

            # Stop the ball's movement
            ball_speed_x = 0
            ball_speed_y = 0
            ball_x = WIDTH // 2  # Position the ball at the center of the circle
            ball_y = HEIGHT // 2

            # Calculate elapsed time since the simulation ended
            elapsed_time = pygame.time.get_ticks() - simulation_end_time

            # If 2 seconds have passed, close the window
            if elapsed_time >= closing_delay:
                record_audio.stop_recording()
                video.export(verbose=True)
                
                video_file = "output.mp4"
                audio_file = "output.wav"
                output_file = "output_upgraded_resolution_with_text.mp4"

                text_value = "Your Custom Text Here"
                text_position = (0, 0.05)

                export_vid.join_video_and_audio(video_file, audio_file, output_file, text=text_value, text_position=text_position)
                
                pygame.quit()
                sys.exit()

    # Rendering
    # Calculate the gradient color based on the ball's position
    t = min(1.0, (ball_radius - BALL_RADIUS) / (CIRCLE_RADIUS - BALL_RADIUS))
    current_color = interpolate_color(initial_color, (255, 255, 0), t * COLOR_CHANGE_SPEED)  # Green to yellow gradient

    # Draw background
    screen.fill(BLACK)

    # Draw circle
    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), CIRCLE_RADIUS, 2)

    # Draw trailing circles
    for trail_component in ball_trail:
        trail_color, trail_position, trail_radius, trail_ball_color = trail_component
        pygame.draw.circle(screen, trail_ball_color, trail_position, trail_radius)
        pygame.draw.circle(screen, WHITE, trail_position, trail_radius, 1)

    # Draw ball outline
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), int(ball_radius) + 1.5)

    # Draw ball with rainbow-like color change
    pygame.draw.circle(screen, current_color, (int(ball_x), int(ball_y)), int(ball_radius))

    # Display collision count just below the circle with padding
    padding = 20  # Adjust the padding value as needed
    text = font.render(f'Collisions: {collisions}', True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + CIRCLE_RADIUS + padding))
    screen.blit(text, text_rect)

    # Save the rendering components of the ball to the trail list
    ball_trail.append(((255, 255, 255), (int(ball_x), int(ball_y)), int(ball_radius), current_color))

    # Remove oldest trail components to keep the length of the trail
    if len(ball_trail) > 30:
        ball_trail.pop(0)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    video.update(pygame.surfarray.pixels3d(screen).swapaxes(0, 1), inverted=False)