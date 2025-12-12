from __future__ import annotations
import ostk.astrodynamics
import ostk.astrodynamics.conjunction
import ostk.physics.time
__all__ = ['Generator']
class Generator:
    """
    
                Compute close approaches to a reference trajectory.
    
                This class computes close approach events between a reference trajectory and other object trajectories
                over a specified time interval. It uses a temporal condition solver to identify time periods when objects
                are approaching and then determines the exact time of closest approach.
            
    """
    @staticmethod
    def undefined() -> Generator:
        """
                        Construct an undefined generator.
        
                        Returns:
                            Generator: An undefined generator.
        """
    def __init__(self, reference_trajectory: ostk.astrodynamics.Trajectory, step: ostk.physics.time.Duration = ..., tolerance: ostk.physics.time.Duration = ...) -> None:
        """
                        Constructor.
        
                        Args:
                            reference_trajectory (Trajectory): The reference trajectory for which to compute close approaches (Object 1).
                            step (Duration): The step to use during the close approach search. Set it to a duration smaller than the minimum possible
                                interval where both objects can be moving apart - which is about a quarter of an orbital period. Defaults to Duration.minutes(20.0).
                            tolerance (Duration): The tolerance to use during the close approach search. Defaults to Duration.milliseconds(1.0).
        """
    def compute_close_approaches(self, trajectory: ostk.astrodynamics.Trajectory, search_interval: ostk.physics.time.Interval) -> list[ostk.astrodynamics.conjunction.CloseApproach]:
        """
                        Compute close approaches between the reference trajectory and another object over a search interval.
        
                        Args:
                            trajectory (Trajectory): The trajectory of the other object (Object 2).
                            search_interval (Interval): The interval over which close approaches are searched.
        
                        Returns:
                            list[CloseApproach]: Array of close approaches over the search interval (with Object 1 being the reference trajectory).
        """
    def get_reference_trajectory(self) -> ostk.astrodynamics.Trajectory:
        """
                        Get the reference trajectory.
        
                        Returns:
                            Trajectory: The reference trajectory.
        """
    def get_step(self) -> ostk.physics.time.Duration:
        """
                        Get the step.
        
                        Returns:
                            Duration: The step.
        """
    def get_tolerance(self) -> ostk.physics.time.Duration:
        """
                        Get the tolerance.
        
                        Returns:
                            Duration: The tolerance.
        """
    def is_defined(self) -> bool:
        """
                        Check if the generator is defined.
        
                        Returns:
                            bool: True if generator is defined, False otherwise.
        """
    def set_step(self, step: ostk.physics.time.Duration) -> None:
        """
                        Set the step.
        
                        Args:
                            step (Duration): The step.
        """
    def set_tolerance(self, tolerance: ostk.physics.time.Duration) -> None:
        """
                        Set the tolerance.
        
                        Args:
                            tolerance (Duration): The tolerance.
        """
