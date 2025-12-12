import pygame
import numpy as np

class PygameRenderer:
    """
    Renderer that ALWAYS displays a fixed-size window (e.g., 512x512)
    and scales any incoming frame to that size.
    """

    def __init__(self, window_name="SAI Renderer", fixed_size=(600, 600)):
        """
        Args:
            window_name (str): Title of the window.
            fixed_size (tuple): (width, height) of the display window.
        """
        self.window_name = window_name
        self.fixed_width, self.fixed_height = fixed_size

        pygame.init()
        pygame.display.set_caption(self.window_name)

        # Create fixed-size window ONCE
        self.window = pygame.display.set_mode(
            (self.fixed_width, self.fixed_height),
            pygame.RESIZABLE
        )

    def render(self, frame: np.ndarray, mode="human"):
        if frame is None:
            return None

        frame = np.transpose(frame, (1, 2, 0))
        # Convert to uint8 if float
        if frame.dtype != np.uint8:
            frame = np.clip(frame * 255, 0, 255).astype(np.uint8)

        if mode == "rgb_array":
            return frame

        # Normal pygame expects surface in (W, H, C) but surfarray uses (C, W, H)
        surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))

        # Scale the surface to the fixed window size
        surface = pygame.transform.scale(surface, (self.fixed_width, self.fixed_height))

        # Process events (must have for macOS to avoid freeze)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()

        # Draw and update window
        self.window.blit(surface, (0, 0))
        pygame.display.flip()

    def close(self):
        pygame.quit()
