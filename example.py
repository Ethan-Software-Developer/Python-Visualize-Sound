import pygame
import math
import pyaudio

screen_width = 500
screen_height = 500
pygame.init()
pygame.display.set_caption("Voice Visualizer")
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()



#audio init


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def get_microphone_input_level():
    data = stream.read(CHUNK)
    rms = 0
    for i in range(0,len(data),2):
        sample = int.from_bytes(data[i:i +2],byteorder='little',signed=True)
        rms += sample * sample
    rms = math.sqrt(rms / (CHUNK / 2))
    return rms
                    
def draw_sine_wave(amplitude):
    screen.fill((0,0,0))
    points = []
    if amplitude > 10:
        for x in range(screen_width):
            y = screen_height/2 + int(amplitude * math.sin(x * 0.02))
            points.append((x,y))
    else:
        points.append((0,screen_height/2))
        points.append((screen_width,screen_height/2))
    pygame.draw.lines(screen,(255,255,255),False,points,2)
    pygame.display.flip()

running = True
amplitude = 100
threshold = 50  # Adjust this threshold as needed

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    amplitude_adjustment = get_microphone_input_level() / 150

    if amplitude_adjustment > threshold:
        amplitude_adjustment = max(10, amplitude_adjustment)
    else:
        amplitude_adjustment = 0  # If below threshold, set amplitude adjustment to 0
    
    draw_sine_wave(amplitude_adjustment)
    clock.tick(60)



pygame.quit()
