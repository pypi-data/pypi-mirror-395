import numpy as np
import pygame


class RenderVSSS:
    def __init__(
        self, ball_radius=0.02125, robot_size=0.08, scale=400, window_size=(680, 520)
    ):
        self.ball_radius = ball_radius * scale
        self.robot_size = robot_size * scale
        self.scale = scale
        self.window_size = window_size

        self.COLORS = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "gray": (50, 50, 50),
            "green": (0, 255, 0),
            "red": (255, 0, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0),
            "orange": (255, 128, 0),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255),
        }

    def _create_cross(self, screen, point, size):
        pygame.draw.line(
            screen,
            self.COLORS["white"],
            (point[0] * self.scale - size / 2 * self.scale, point[1] * self.scale),
            (point[0] * self.scale + size / 2 * self.scale, point[1] * self.scale),
            2,
        )
        pygame.draw.line(
            screen,
            self.COLORS["white"],
            (point[0] * self.scale, point[1] * self.scale - size / 2 * self.scale),
            (point[0] * self.scale, point[1] * self.scale + size / 2 * self.scale),
            2,
        )

    def field(self, screen):
        line_width = 2
        screen.fill(self.COLORS["gray"])
        pygame.draw.circle(
            screen,
            self.COLORS["white"],
            (17e-2 * self.scale, 1.30 / 2 * self.scale),
            13e-2 * self.scale,
            width=line_width,
        )
        pygame.draw.circle(
            screen,
            self.COLORS["white"],
            (1.53 * self.scale, 1.30 / 2 * self.scale),
            13e-2 * self.scale,
            width=line_width,
        )
        screen.fill(
            self.COLORS["gray"], rect=(0, 0, 25e-2 * self.scale, 1.30 * self.scale)
        )
        screen.fill(
            self.COLORS["gray"],
            rect=(1.45 * self.scale, 0, 25e-2 * self.scale, 1.30 * self.scale),
        )
        pygame.draw.rect(
            screen,
            self.COLORS["white"],
            rect=(10e-2 * self.scale, 0, self.scale * 1.50, self.scale * 1.30),
            width=line_width,
        )
        pygame.draw.rect(
            screen,
            self.COLORS["white"],
            rect=(0, 45e-2 * self.scale, 10e-2 * self.scale, 40e-2 * self.scale),
            width=line_width,
        )
        pygame.draw.rect(
            screen,
            self.COLORS["white"],
            rect=(
                1.60 * self.scale,
                45e-2 * self.scale,
                10e-2 * self.scale,
                40e-2 * self.scale,
            ),
            width=line_width,
        )
        pygame.draw.rect(
            screen,
            self.COLORS["white"],
            rect=(
                10e-2 * self.scale,
                30e-2 * self.scale,
                15e-2 * self.scale,
                70e-2 * self.scale,
            ),
            width=line_width,
        )
        pygame.draw.rect(
            screen,
            self.COLORS["white"],
            rect=(
                1.45 * self.scale,
                30e-2 * self.scale,
                15e-2 * self.scale,
                70e-2 * self.scale,
            ),
            width=line_width,
        )
        pygame.draw.circle(
            screen,
            self.COLORS["white"],
            (1.70 / 2 * self.scale, 1.30 / 2 * self.scale),
            20e-2 * self.scale,
            width=line_width,
        )
        pygame.draw.line(
            screen,
            self.COLORS["white"],
            (1.70 / 2 * self.scale, 0),
            (1.70 / 2 * self.scale, 1.30 * self.scale),
            width=line_width,
        )
        points = [
            (47.5e-2, 25e-2),
            (1.70 - 47.5e-2, 25e-2),
            (47.5e-2, 1.30 - 25e-2),
            (1.70 - 47.5e-2, 1.30 - 25e-2),
            (47.5e-2, 1.30 / 2),
            (1.70 - 47.5e-2, 1.30 / 2),
        ]
        for point in points:
            self._create_cross(screen, point, 5e-2)
        pygame.draw.polygon(
            screen,
            self.COLORS["white"],
            (
                (10e-2 * self.scale, 0),
                (17e-2 * self.scale, 0),
                (10e-2 * self.scale, 7e-2 * self.scale),
            ),
        )
        pygame.draw.polygon(
            screen,
            self.COLORS["white"],
            (
                (10e-2 * self.scale, self.scale * 1.30),
                (17e-2 * self.scale, self.scale * 1.30),
                (10e-2 * self.scale, (1.30 - 7e-2) * self.scale),
            ),
        )
        pygame.draw.polygon(
            screen,
            self.COLORS["white"],
            (
                (1.53 * self.scale, 0),
                (1.60 * self.scale, 0),
                (1.60 * self.scale, 7e-2 * self.scale),
            ),
        )
        pygame.draw.polygon(
            screen,
            self.COLORS["white"],
            (
                (1.53 * self.scale, self.scale * 1.30),
                (1.60 * self.scale, self.scale * 1.30),
                (1.60 * self.scale, (1.30 - 7e-2) * self.scale),
            ),
        )
        pygame.draw.rect(
            screen,
            self.COLORS["black"],
            rect=(0, 0, 10e-2 * self.scale, 45e-2 * self.scale),
        )
        pygame.draw.rect(
            screen,
            self.COLORS["black"],
            rect=(0, 85e-2 * self.scale, 10e-2 * self.scale, 45e-2 * self.scale),
        )
        pygame.draw.rect(
            screen,
            self.COLORS["black"],
            rect=(1.60 * self.scale, 0, 10e-2 * self.scale, 45e-2 * self.scale),
        )
        pygame.draw.rect(
            screen,
            self.COLORS["black"],
            rect=(
                1.60 * self.scale,
                85e-2 * self.scale,
                10e-2 * self.scale,
                45e-2 * self.scale,
            ),
        )

    def robot(self, screen, x, y, direction, team_color, idx):
        default_color = "green" if team_color == "blue" else "cyan"

        color_by_idx = {
            0: "cyan" if team_color == "blue" else "green",
            1: "magenta",
            2: "red",
        }

        x = self.window_size[0] / 2 + x * self.scale
        y = self.window_size[1] / 2 - y * self.scale  # - because the y axis is inverted

        # A rotated surface to draw the robot
        rotated_surface = pygame.Surface(
            (self.robot_size * 2, self.robot_size * 2), pygame.SRCALPHA
        )
        pygame.draw.rect(
            rotated_surface,
            self.COLORS["black"],
            rect=(
                self.robot_size // 2,
                self.robot_size // 2,
                self.robot_size,
                self.robot_size,
            ),
        )

        # Team color
        rect = (
            self.robot_size // 2 + 7.5e-3 * self.scale,  # Top left x
            self.robot_size // 2 + 7.5e-3 * self.scale,  # Top left y
            30e-3 * self.scale,  # Width
            65e-3 * self.scale,  # Height
        )
        pygame.draw.rect(rotated_surface, self.COLORS[team_color], rect=rect)

        # Defaul color
        rect = (
            self.robot_size // 2 + 42.5e-3 * self.scale,  # Top left x
            self.robot_size // 2 + 7.5e-3 * self.scale,  # Top left y
            30e-3 * self.scale,  # Width
            30e-3 * self.scale,  # Height
        )
        pygame.draw.rect(rotated_surface, self.COLORS[default_color], rect=rect)

        # Tag color
        rect = (
            self.robot_size // 2 + 42.5e-3 * self.scale,  # Top left x
            self.robot_size // 2 + 42.5e-3 * self.scale,  # Top left y
            30e-3 * self.scale,  # Width
            30e-3 * self.scale,  # Height
        )
        pygame.draw.rect(rotated_surface, self.COLORS[color_by_idx[idx]], rect=rect)

        # Draw the robot
        # about the center
        rotated_surface = pygame.transform.rotate(
            rotated_surface, np.rad2deg(direction)
        )
        new_rect = rotated_surface.get_rect(center=(x, y))
        screen.blit(rotated_surface, new_rect.topleft)

    def ball(self, screen, x, y):
        x = self.window_size[0] / 2 + x * self.scale
        y = self.window_size[1] / 2 - y * self.scale
        pygame.draw.circle(screen, self.COLORS["orange"], (x, y), self.ball_radius)
        pygame.draw.circle(screen, self.COLORS["black"], (x, y), self.ball_radius, 1)
