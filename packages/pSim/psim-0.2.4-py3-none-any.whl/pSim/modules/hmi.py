from typing import Tuple, Dict, List, Any
import pygame
import numpy as np
import pygame._sdl2.controller as controller
from pygame.locals import (
    K_ESCAPE, K_q, K_e, K_x, K_y,
    KEYDOWN, KEYUP, K_a, K_d, K_r, K_s, K_w, K_b,
)


class HMI:
    """Human-Machine Interface for robot simulation control.
    Supports keyboard and universally mapped joystick inputs.
    """

    def __init__(self, dead_zone: float = 0.1) -> None:
        """Initializes the HMI system and the controller interface.

        Args:
            dead_zone: The dead zone threshold for joystick analog inputs (0.0 to 1.0).
        """
        # Control state variables
        self.active: bool = True
        self.v: float = 0.0  # Linear velocity
        self.w: float = 0.0  # Angular velocity
        self.reset_commanded: bool = False

        # Multi-robot and ball control state
        self.current_team: str = "blue"  # "blue" or "yellow"
        self.current_robot_id: int = 0
        self.ball_control_mode: bool = False
        self.controllable_robots: Dict[str, List[int]] = {"blue": [], "yellow": []}

        # Button states for edge detection
        self.prev_next_robot: bool = False
        self.prev_prev_robot: bool = False
        self.prev_team_blue: bool = False
        self.prev_team_yellow: bool = False
        self.prev_ball_mode: bool = False

        # Initialize pygame and controller system
        pygame.init()
        controller.init()
        controller.set_eventstate(True)

        # Active controllers dictionary
        self.controllers: Dict[int, controller.Controller] = {}
        self.dead_zone: float = dead_zone

        # SDL2 Controller button and axis mapping - Universal across all controllers
        self.button_map = {
            pygame.CONTROLLER_BUTTON_A: "A",
            pygame.CONTROLLER_BUTTON_B: "B",
            pygame.CONTROLLER_BUTTON_X: "X",
            pygame.CONTROLLER_BUTTON_Y: "Y",
            pygame.CONTROLLER_BUTTON_LEFTSHOULDER: "LB",
            pygame.CONTROLLER_BUTTON_RIGHTSHOULDER: "RB",
            pygame.CONTROLLER_BUTTON_BACK: "BACK",
            pygame.CONTROLLER_BUTTON_START: "START",
            pygame.CONTROLLER_BUTTON_GUIDE: "GUIDE",
            pygame.CONTROLLER_BUTTON_LEFTSTICK: "LS",
            pygame.CONTROLLER_BUTTON_RIGHTSTICK: "RS",
            pygame.CONTROLLER_BUTTON_DPAD_UP: "DPAD_UP",
            pygame.CONTROLLER_BUTTON_DPAD_DOWN: "DPAD_DOWN",
            pygame.CONTROLLER_BUTTON_DPAD_LEFT: "DPAD_LEFT",
            pygame.CONTROLLER_BUTTON_DPAD_RIGHT: "DPAD_RIGHT",
        }

        self.axis_map = {
            pygame.CONTROLLER_AXIS_LEFTX: "LEFT_X",
            pygame.CONTROLLER_AXIS_LEFTY: "LEFT_Y",
            pygame.CONTROLLER_AXIS_RIGHTX: "RIGHT_X",
            pygame.CONTROLLER_AXIS_RIGHTY: "RIGHT_Y",
            pygame.CONTROLLER_AXIS_TRIGGERLEFT: "LEFT_TRIGGER",
            pygame.CONTROLLER_AXIS_TRIGGERRIGHT: "RIGHT_TRIGGER",
        }

        self._scan_controllers()
        self._print_instructions()

    def _print_instructions(self):
        """Print control instructions."""
        print("Movement:")
        print("  Robot: W/S forward/back, A/D turn | Controller: Left stick Y, Right stick X")
        print("  Ball: W/S/A/D move | Controller: Left stick only (both axes)")
        print("Robot/Ball Control:")
        print("  E/RB: Next robot, Q/LB: Previous robot")
        print("  Y/Y: Yellow team, X/X: Blue team, B/B: Ball control mode")
        print("Commands:")
        print("  R/BACK: Reset, ESC/START: Exit")
        print("============================\n")

    def update_robot_list(self, agent_team_color: str, agent_movement_types: List[str], adversary_movement_types: List[str]):
        """Update the list of controllable robots.

        Args:
            agent_team_color: Color of agent team ("blue" or "yellow")
            agent_movement_types: List of movement types for agent robots
            adversary_movement_types: List of movement types for adversary robots
        """
        adversary_team_color = "yellow" if agent_team_color == "blue" else "blue"

        self.controllable_robots = {"blue": [], "yellow": []}

        # Add controllable agent robots
        for i, movement_type in enumerate(agent_movement_types):
            if movement_type == "action":
                self.controllable_robots[agent_team_color].append(i)

        # Add controllable adversary robots
        for i, movement_type in enumerate(adversary_movement_types):
            if movement_type == "action":
                self.controllable_robots[adversary_team_color].append(i)

        # Reset to valid robot if current selection is invalid
        if self.current_robot_id not in self.controllable_robots[self.current_team]:
            if self.controllable_robots[self.current_team]:
                self.current_robot_id = self.controllable_robots[self.current_team][0]
            else:
                # Switch to team with controllable robots
                for team, robots in self.controllable_robots.items():
                    if robots:
                        self.current_team = team
                        self.current_robot_id = robots[0]
                        break

        print(f"Controllable robots - Blue: {self.controllable_robots['blue']}, Yellow: {self.controllable_robots['yellow']}")
        print(f"Current: {self.current_team.capitalize()} Robot {self.current_robot_id}")

    def _next_robot(self):
        """Switch to next robot in current team."""
        team_robots = self.controllable_robots[self.current_team]
        if not team_robots:
            return

        current_idx = team_robots.index(self.current_robot_id) if self.current_robot_id in team_robots else 0
        next_idx = (current_idx + 1) % len(team_robots)
        self.current_robot_id = team_robots[next_idx]

        self.ball_control_mode = False
        print(f"{self.current_team.capitalize()} Robot {self.current_robot_id}")

    def _previous_robot(self):
        """Switch to previous robot in current team."""
        team_robots = self.controllable_robots[self.current_team]
        if not team_robots:
            return

        current_idx = team_robots.index(self.current_robot_id) if self.current_robot_id in team_robots else 0
        prev_idx = (current_idx - 1) % len(team_robots)
        self.current_robot_id = team_robots[prev_idx]

        self.ball_control_mode = False
        print(f"← {self.current_team.capitalize()} Robot {self.current_robot_id}")

    def _select_robot_by_number(self, number: int):
        """Select robot by number (1-6) in current team."""
        team_robots = self.controllable_robots[self.current_team]
        index = number - 1

        if 0 <= index < len(team_robots):
            self.current_robot_id = team_robots[index]
            self.ball_control_mode = False
            print(f"#{number} {self.current_team.capitalize()} Robot {self.current_robot_id}")

    def _switch_to_team(self, team: str):
        """Switch to specific team."""
        if team in self.controllable_robots and self.controllable_robots[team]:
            self.current_team = team
            self.current_robot_id = self.controllable_robots[team][0]
            self.ball_control_mode = False
            print(f"Team {team.capitalize()} - Robot {self.current_robot_id}")

    def _toggle_ball_control(self):
        """Toggle ball control mode."""
        self.ball_control_mode = not self.ball_control_mode
        mode_text = "Ball Control" if self.ball_control_mode else f"{self.current_team.capitalize()} Robot {self.current_robot_id}"
        print(f"{mode_text}")

    def _scan_controllers(self) -> None:
        """Scans for and initializes available controllers.

        Detects newly connected controllers and adds them to the active
        controllers dictionary. Removes any that have been disconnected.
        """
        disconnected = [
            idx for idx, ctrl in self.controllers.items()
            if not ctrl.attached()
        ]
        for idx in disconnected:
            self.controllers[idx].quit()
            del self.controllers[idx]

        count = controller.get_count()

        if not count:
            print("No controllers connected, using keyboard input")

        for i in range(count):
            if i not in self.controllers and controller.is_controller(i):
                try:
                    ctrl = controller.Controller(i)
                    if ctrl.attached():
                        self.controllers[i] = ctrl
                        name = controller.name_forindex(i) or f"Controller {i}"
                        print(f"Controller connected: {name}")
                except Exception as e:
                    print(f"Failed to initialize controller {i}: {e}")

    def _apply_deadzone(self, value: float) -> float:
        """Applies dead zone filtering to an analog input value.

        Args:
            value: The raw analog input value (-1.0 to 1.0).

        Returns:
            The filtered value with the dead zone applied.
        """
        if abs(value) < self.dead_zone:
            return 0.0
        sign = 1 if value > 0 else -1
        scaled = (abs(value) - self.dead_zone) / (1.0 - self.dead_zone)
        return sign * scaled

    def _normalize_axis(self, raw_value: int) -> float:
        """Converts a raw axis value to a normalized float.

        Args:
            raw_value: The raw axis value from the controller (-32768 to 32767).

        Returns:
            A normalized value between -1.0 and 1.0.
        """
        return raw_value / 32767.0

    def _normalize_trigger(self, raw_value: int) -> float:
        """Converts a raw trigger value to a normalized float.

        Args:
            raw_value: The raw trigger value from the controller (0 to 32767).

        Returns:
            A normalized value between 0.0 and 1.0.
        """
        return raw_value / 32767.0

    def _handle_controller_button_event(self, event: pygame.event.Event) -> None:
        """Handles controller button press events using the universal mapping.

        Args:
            event: The Pygame controller button event to process.
        """
        if event.type == pygame.CONTROLLERBUTTONDOWN:
            button_name = self.button_map.get(event.button, f"UNKNOWN_{event.button}")

            if button_name == "START":
                self.active = False
            elif button_name == "BACK":
                self.reset_commanded = True
            elif button_name == "RB":
                if not self.prev_next_robot:
                    self._next_robot()
            elif button_name == "LB":
                if not self.prev_prev_robot:
                    self._previous_robot()
            elif button_name == "X":
                if not self.prev_team_blue:
                    self._switch_to_team("blue")
            elif button_name == "Y":
                if not self.prev_team_yellow:
                    self._switch_to_team("yellow")
            elif button_name == "B":
                if not self.prev_ball_mode:
                    self._toggle_ball_control()

    def _handle_controller_axis_event(self, event: pygame.event.Event) -> None:
        """Handles controller axis motion events using the universal mapping.

        Args:
            event: The Pygame controller axis motion event to process.
        """
        if event.type == pygame.CONTROLLERAXISMOTION:
            axis_name = self.axis_map.get(event.axis, f"UNKNOWN_{event.axis}")

            if axis_name in ["LEFT_TRIGGER", "RIGHT_TRIGGER"]:
                normalized_value = self._normalize_trigger(event.value)
            else:
                normalized_value = self._normalize_axis(event.value)

            filtered_value = self._apply_deadzone(normalized_value)

            if axis_name == "LEFT_Y" and not self.ball_control_mode:
                self.v = -filtered_value        # Forward/backward (left stick Y)
            elif axis_name == "RIGHT_X" and not self.ball_control_mode:
                self.w = -filtered_value         # Left/right (left stick X for ball control)
            if axis_name == "LEFT_X" and self.ball_control_mode:
                self.v = filtered_value
            if axis_name == "LEFT_Y" and self.ball_control_mode:
                self.w = -filtered_value

    def _handle_keyboard_events(self, event: pygame.event.Event) -> None:
        """Handles keyboard input events.

        Args:
            event: The Pygame keyboard event to process.
        """
        if event.type == KEYDOWN:
            # Movement controls
            if event.key == K_w: self.v = 1.0   # Forward
            if event.key == K_s: self.v = -1.0  # Backward
            if event.key == K_a: self.w = 1.0   # Turn left
            if event.key == K_d: self.w = -1.0  # Turn right

            # Robot selection
            if event.key == K_q:
                self._previous_robot()
            if event.key == K_e:
                self._next_robot()

            # Team selection
            if event.key == K_x:  # Blue team
                self._switch_to_team("blue")
            if event.key == K_y:  # Yellow team
                self._switch_to_team("yellow")

            # Ball control toggle
            if event.key == K_b:  # Alternative ball control key
                self._toggle_ball_control()

            # Commands
            if event.key == K_r:
                self.reset_commanded = True
            if event.key == K_ESCAPE:
                self.active = False

        elif event.type == KEYUP:
            if event.key in (K_w, K_s):
                self.v = 0.0
            if event.key in (K_a, K_d):
                self.w = 0.0

    def _handle_events(self) -> None:
        """Processes all pygame events for input handling.

        Handles controller connection/disconnection, button presses, axis motion,
        and keyboard input events via the event queue.
        """
        self.reset_commanded = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False
            elif event.type in (pygame.CONTROLLERDEVICEADDED, pygame.CONTROLLERDEVICEREMOVED):
                self._scan_controllers()
            elif event.type == pygame.CONTROLLERBUTTONDOWN:
                self._handle_controller_button_event(event)
            elif event.type == pygame.CONTROLLERAXISMOTION:
                self._handle_controller_axis_event(event)
            elif event.type in (KEYDOWN, KEYUP):
                self._handle_keyboard_events(event)

        # Update button states for edge detection
        if self.controllers:
            ctrl = list(self.controllers.values())[0]
            self.prev_next_robot = ctrl.get_button(pygame.CONTROLLER_BUTTON_RIGHTSHOULDER)
            self.prev_prev_robot = ctrl.get_button(pygame.CONTROLLER_BUTTON_LEFTSHOULDER)
            self.prev_team_blue = ctrl.get_button(pygame.CONTROLLER_BUTTON_X)
            self.prev_team_yellow = ctrl.get_button(pygame.CONTROLLER_BUTTON_Y)
            self.prev_ball_mode = ctrl.get_button(pygame.CONTROLLER_BUTTON_B)

    def __call__(self) -> Dict[str, Any]:
        """Processes input and returns the current control state.

        This method makes the HMI instance callable and should be used in
        the main control loop. It processes all pending events and updates
        control variables.

        Returns:
            Dictionary containing:
            - actions: numpy array [linear_velocity, angular_velocity]
            - reset_commanded: boolean indicating if reset was requested
            - active: boolean indicating if the system should continue running
            - current_team: string ("blue" or "yellow")
            - current_robot_id: int
            - ball_control_mode: boolean
        """
        self._handle_events()
        actions = np.array([self.v, self.w])
        
        return {
            "actions": actions,
            "reset_commanded": self.reset_commanded,
            "active": self.active,
            "current_team": self.current_team,
            "current_robot_id": self.current_robot_id,
            "ball_control_mode": self.ball_control_mode
        }

    def quit(self) -> None:
        """Cleans up and shuts down the HMI system."""
        for ctrl in self.controllers.values():
            ctrl.quit()
        self.controllers.clear()

        controller.quit()
        pygame.quit()