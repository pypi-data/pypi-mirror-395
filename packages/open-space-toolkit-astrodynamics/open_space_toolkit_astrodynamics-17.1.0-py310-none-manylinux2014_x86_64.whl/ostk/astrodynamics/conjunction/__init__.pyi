from __future__ import annotations
import ostk.astrodynamics.trajectory
import ostk.physics.coordinate
import ostk.physics.time
import ostk.physics.unit
import typing
from . import close_approach
from . import message
__all__ = ['CloseApproach', 'close_approach', 'message']
class CloseApproach:
    """
    
                Close approach between two objects.
    
                This class represents a close approach event between two objects, providing access to the states of both
                objects at the time of closest approach, the miss distance, and the relative state.
            
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def undefined() -> CloseApproach:
        """
                        Construct an undefined close approach.
        
                        Returns:
                            CloseApproach: An undefined close approach.
        """
    def __eq__(self, arg0: CloseApproach) -> bool:
        """
                        Equal to operator.
        
                        Args:
                            other (CloseApproach): Another close approach.
        
                        Returns:
                            bool: True if close approaches are equal.
        """
    def __init__(self, object_1_state: ostk.astrodynamics.trajectory.State, object_2_state: ostk.astrodynamics.trajectory.State) -> None:
        """
                        Constructor.
        
                        Args:
                            object_1_state (State): The state of Object 1.
                            object_2_state (State): The state of Object 2.
        """
    def __ne__(self, arg0: CloseApproach) -> bool:
        """
                        Not equal to operator.
        
                        Args:
                            other (CloseApproach): Another close approach.
        
                        Returns:
                            bool: True if close approaches are not equal.
        """
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def compute_miss_distance_components_in_frame(self, frame: ostk.physics.coordinate.Frame) -> tuple[ostk.physics.unit.Length, ostk.physics.unit.Length, ostk.physics.unit.Length]:
        """
                        Compute the miss distance components in the desired frame.
        
                        Args:
                            frame (Frame): The frame in which to resolve the miss distance components.
        
                        Returns:
                            tuple[Length, Length, Length]: The miss distance components (x, y, z).
        """
    def compute_miss_distance_components_in_local_orbital_frame(self, local_orbital_frame_factory: ostk.astrodynamics.trajectory.LocalOrbitalFrameFactory) -> tuple[ostk.physics.unit.Length, ostk.physics.unit.Length, ostk.physics.unit.Length]:
        """
                        Compute the miss distance components in a local orbital frame (generated from Object 1 state).
        
                        Args:
                            local_orbital_frame_factory (LocalOrbitalFrameFactory): The local orbital frame factory.
        
                        Returns:
                            tuple[Length, Length, Length]: The miss distance components (radial, in-track, cross-track or similar depending on the factory).
        """
    def get_instant(self) -> ostk.physics.time.Instant:
        """
                        Get the instant of the close approach.
        
                        Returns:
                            Instant: The instant of closest approach.
        """
    def get_miss_distance(self) -> ostk.physics.unit.Length:
        """
                        Get the miss distance.
        
                        Returns:
                            Length: The miss distance between the two objects.
        """
    def get_object_1_state(self) -> ostk.astrodynamics.trajectory.State:
        """
                        Get the state of Object 1.
        
                        Returns:
                            State: The state of Object 1.
        """
    def get_object_2_state(self) -> ostk.astrodynamics.trajectory.State:
        """
                        Get the state of Object 2.
        
                        Returns:
                            State: The state of Object 2.
        """
    def get_relative_state(self) -> ostk.astrodynamics.trajectory.State:
        """
                        Get the relative state (Object 2 relative to Object 1).
        
                        Returns:
                            State: The relative state.
        """
    def is_defined(self) -> bool:
        """
                        Check if the close approach is defined.
        
                        Returns:
                            bool: True if close approach is defined, False otherwise.
        """
