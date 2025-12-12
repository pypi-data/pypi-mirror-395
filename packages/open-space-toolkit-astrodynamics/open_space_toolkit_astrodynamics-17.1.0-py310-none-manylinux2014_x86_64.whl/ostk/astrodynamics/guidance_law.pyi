from __future__ import annotations
import numpy
import ostk.astrodynamics
import ostk.astrodynamics.flight
import ostk.astrodynamics.trajectory
import ostk.astrodynamics.trajectory.orbit.model.kepler
import ostk.core.type
import ostk.physics.coordinate
import ostk.physics.time
import ostk.physics.unit
import typing
__all__ = ['ConstantThrust', 'HeterogeneousGuidanceLaw', 'QLaw']
class ConstantThrust(ostk.astrodynamics.GuidanceLaw):
    """
    
                    Constant Thrust, Constant Direction guidance law.
    
                
    """
    @staticmethod
    def from_maneuver(maneuver: ostk.astrodynamics.flight.Maneuver, local_orbital_frame_factory: ostk.astrodynamics.trajectory.LocalOrbitalFrameFactory, maximum_allowed_angular_offset: ostk.physics.unit.Angle = ...) -> ConstantThrust:
        """
                            Create a constant thrust guidance law from a maneuver.
        
                            The local orbital frame maneuver's mean thrust direction is calculated and used to create a 
                            constant thrust guidance law in said direction.
                            
                            If defined, a runtime error will be thrown if the maximum allowed angular offset between the original thrust acceleration 
                            direction and the mean thrust direction is violated.
        
                            Args:
                                maneuver (Maneuver): The maneuver.
                                local_orbital_frame_factory (LocalOrbitalFrameFactory): The local orbital frame factory.
                                maximum_allowed_angular_offset (Angle, optional): The maximum allowed angular offset to consider (if any). Defaults to Undefined.
        
                            Returns:
                                ConstantThrust: The constant thrust guidance law.
        """
    @staticmethod
    def intrack(velocity_direction: bool = True) -> ConstantThrust:
        """
                            Create a constant thrust guidance law in the in-track direction.
        
                            Args:
                                velocity_direction (bool, optional): If True, the thrust is applied in the velocity direction. Otherwise, it is applied in the opposite direction. Defaults to True.
        
                            Returns:
                                ConstantThrust: The constant thrust guidance law in the in-track direction.
        """
    def __init__(self, thrust_direction: ostk.astrodynamics.trajectory.LocalOrbitalFrameDirection) -> None:
        """
                            Constructor.
        
                            Args:
                                thrust_direction (LocalOrbitalFrameDirection): The thrust direction.
        """
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def calculate_thrust_acceleration_at(self, instant: ostk.physics.time.Instant, position_coordinates: numpy.ndarray[numpy.float64[3, 1]], velocity_coordinates: numpy.ndarray[numpy.float64[3, 1]], thrust_acceleration: ostk.core.type.Real, output_frame: ostk.physics.coordinate.Frame) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
                            Compute the acceleration due to constant thrust.
        
                            Args:
                                instant (Instant): The instant of the state vector.
                                position_coordinates (numpy.ndarray): The position coordinates.
                                velocity_coordinates (numpy.ndarray): The velocity coordinates.
                                thrust_acceleration (float): The thrust acceleration magnitude.
                                output_frame (Frame): The frame the acceleration will be expressed in.
        
                            Returns:
                                numpy.ndarray: The contribution of the constant thrust to the state vector.
        """
    def get_local_thrust_direction(self) -> ostk.astrodynamics.trajectory.LocalOrbitalFrameDirection:
        """
                            Get the local thrust direction.
        
                            Returns:
                                LocalOrbitalFrameDirection: The local thrust direction.
        """
class HeterogeneousGuidanceLaw(ostk.astrodynamics.GuidanceLaw):
    """
    
                A guidance law that sequences multiple guidance laws over specific time intervals.
                
                At each point in time, the applicable guidance law is selected and used to calculate
                the thrust acceleration. Guidance laws don't need to be contiguous, and can be added
                in any order. If the instant does not fall within any of the intervals, the thrust
                acceleration is zero. The guidance law intervals must not intersect each other.
            
    """
    def __init__(self, guidance_laws_with_intervals: list[tuple[ostk.astrodynamics.GuidanceLaw, ostk.physics.time.Interval]] = []) -> None:
        """
                        Constructor.
        
                        Args:
                            guidance_laws_with_intervals (list[tuple[GuidanceLaw, Interval]], optional): Array of tuples containing the guidance laws and their corresponding intervals. Defaults to empty array.
        
                        Raises:
                            RuntimeError: If any interval is undefined, if the guidance law is null or if the interval intersects with an existing interval.
        """
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def add_guidance_law(self, guidance_law: ostk.astrodynamics.GuidanceLaw, interval: ostk.physics.time.Interval) -> None:
        """
                        Add a guidance law with its corresponding interval.
        
                        Args:
                            guidance_law (GuidanceLaw): The guidance law to add.
                            interval (Interval): The interval during which the guidance law is active.
        
                        Raises:
                            RuntimeError: If the interval is undefined, if the guidance law is null or if the interval intersects with an existing interval.
        """
    def calculate_thrust_acceleration_at(self, instant: ostk.physics.time.Instant, position_coordinates: numpy.ndarray[numpy.float64[3, 1]], velocity_coordinates: numpy.ndarray[numpy.float64[3, 1]], thrust_acceleration: ostk.core.type.Real, output_frame: ostk.physics.coordinate.Frame) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
                        Calculate thrust acceleration at a given instant and state.
        
                        Args:
                            instant (Instant): The instant.
                            position_coordinates (numpy.ndarray): The position coordinates.
                            velocity_coordinates (numpy.ndarray): The velocity coordinates.
                            thrust_acceleration (float): The thrust acceleration magnitude.
                            output_frame (Frame): The frame in which the acceleration is expressed.
        
                        Returns:
                            numpy.ndarray: The acceleration vector at the provided coordinates.
        """
    def get_guidance_laws_with_intervals(self) -> list[tuple[ostk.astrodynamics.GuidanceLaw, ostk.physics.time.Interval]]:
        """
                        Get the guidance laws with their corresponding intervals.
        
                        Returns:
                            list[tuple[GuidanceLaw, Interval]]: Array of tuples containing the guidance laws and their corresponding intervals.
        """
class QLaw(ostk.astrodynamics.GuidanceLaw):
    """
    
                This class implements the Q-law guidance law.
    
                - Ref: https://dataverse.jpl.nasa.gov/api/access/datafile/10307?gbrecs=true
                - Ref: https://www.researchgate.net/publication/370849580_Analytic_Calculation_and_Application_of_the_Q-Law_Guidance_Algorithm_Partial_Derivatives
                - Ref for derivations: https://dataverse.jpl.nasa.gov/api/access/datafile/13727?gbrecs=true
    
                The Q-law is a Lyapunov feedback control law developed by Petropoulos,
                based on analytic expressions for maximum rates of change of the orbit elements and
                the desired changes in the elements. Q, the proximity quotient, serves as a candidate Lyapunov
                function. As the spacecraft approaches the target orbit, Q decreases monotonically (becoming zero at the target orbit).
    
            
    """
    class COEDomain:
        """
        
                    Classical Orbital Elements domain.
                
        
        Members:
        
          Osculating : Osculating
        
          BrouwerLyddaneMeanLong : Brouwer Lyddane Mean Long
        
          BrouwerLyddaneMeanShort : Brouwer Lyddane Mean Short
        """
        BrouwerLyddaneMeanLong: typing.ClassVar[QLaw.COEDomain]  # value = <COEDomain.BrouwerLyddaneMeanLong: 1>
        BrouwerLyddaneMeanShort: typing.ClassVar[QLaw.COEDomain]  # value = <COEDomain.BrouwerLyddaneMeanShort: 2>
        Osculating: typing.ClassVar[QLaw.COEDomain]  # value = <COEDomain.Osculating: 0>
        __members__: typing.ClassVar[dict[str, QLaw.COEDomain]]  # value = {'Osculating': <COEDomain.Osculating: 0>, 'BrouwerLyddaneMeanLong': <COEDomain.BrouwerLyddaneMeanLong: 1>, 'BrouwerLyddaneMeanShort': <COEDomain.BrouwerLyddaneMeanShort: 2>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class GradientStrategy:
        """
        
                    Gradient strategy.
                
        
        Members:
        
          Analytical : Analytical
        
          FiniteDifference : Finite Differenced
        """
        Analytical: typing.ClassVar[QLaw.GradientStrategy]  # value = <GradientStrategy.Analytical: 0>
        FiniteDifference: typing.ClassVar[QLaw.GradientStrategy]  # value = <GradientStrategy.FiniteDifference: 1>
        __members__: typing.ClassVar[dict[str, QLaw.GradientStrategy]]  # value = {'Analytical': <GradientStrategy.Analytical: 0>, 'FiniteDifference': <GradientStrategy.FiniteDifference: 1>}
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    class Parameters:
        """
        
                    Q-law parameters.
        
                
        """
        def __init__(self, element_weights: dict[ostk.astrodynamics.trajectory.orbit.model.kepler.COE.Element, tuple[float, float]], m: int = 3, n: int = 4, r: int = 2, b: float = 0.01, k: int = 100, periapsis_weight: float = 0.0, minimum_periapsis_radius: ostk.physics.unit.Length = ..., absolute_effectivity_threshold: ostk.core.type.Real = ..., relative_effectivity_threshold: ostk.core.type.Real = ...) -> None:
            """
                            Constructor.
            
                            Args:
                                element_weights (dict): Key-value pair of COE elements and the (weights, tolerances) for the targeter.
                                m (int): Scaling parameter for Semi-Major Axis delta. Default to 3.
                                n (int): Scaling parameter for Semi-Major Axis delta. Default to 4.
                                r (int): Scaling parameter for Semi-Major Axis delta. Default to 2.
                                b (float): Scaling parameter for Argument of Periapsis maximal change. Default to 0.01.
                                k (int): Penalty parameter for periapsis. Default to 100.
                                periapsis_weight (float): Periapsis weight. Default to 0.0.
                                minimum_periapsis_radius (Length): Minimum periapsis radius. Default to 6578.0 km.
                                absolute_effectivity_threshold (Real): Absolute effectivity threshold. Default to undefined (not used).
                                relative_effectivity_threshold (Real): Relative effectivity threshold. Default to undefined (not used).
            """
        def get_control_weights(self) -> numpy.ndarray[numpy.float64[5, 1]]:
            """
                            Get the control weights.
            
                            Returns:
                                np.array: The control weights.
            """
        def get_minimum_periapsis_radius(self) -> ostk.physics.unit.Length:
            """
                            Get the minimum periapsis radius.
            
                            Returns:
                                Length: The minimum periapsis radius.
            """
        @property
        def absolute_effectivity_threshold(self) -> ostk.core.type.Real:
            """
                            Absolute effectivity threshold.
            
                            Type:
                                Real
            """
        @property
        def b(self) -> float:
            """
                            Scaling parameter for Argument of Periapsis.
            
                            Type:
                                float
            """
        @property
        def k(self) -> float:
            """
                            Penalty parameter for periapsis.
            
                            Type:
                                int
            """
        @property
        def m(self) -> float:
            """
                            Scaling parameter for Semi-Major Axis delta.
            
                            Type:
                                int
            """
        @property
        def n(self) -> float:
            """
                            Scaling parameter for Semi-Major Axis delta.
            
                            Type:
                                int
            """
        @property
        def periapsis_weight(self) -> float:
            """
                            Periapsis weight.
            
                            Type:
                                float
            """
        @property
        def r(self) -> float:
            """
                            Scaling parameter for Semi-Major Axis delta.
            
                            Type:
                                int
            """
        @property
        def relative_effectivity_threshold(self) -> ostk.core.type.Real:
            """
                            Relative effectivity threshold.
            
                            Type:
                                Real
            """
    def __init__(self, target_coe: ostk.astrodynamics.trajectory.orbit.model.kepler.COE, gravitational_parameter: ostk.physics.unit.Derived, parameters: QLaw.Parameters, coe_domain: QLaw.COEDomain, gradient_strategy: QLaw.GradientStrategy = ...) -> None:
        """
                        Constructor.
        
                        Args:
                            coe (COE): The target orbit described by Classical Orbital Elements.
                            gravitational_parameter (float): The gravitational parameter of the central body.
                            parameters (QLaw.Parameters): A set of parameters for the QLaw.
                            coe_domain (QLaw.COEDomain): The domain of the Classical Orbital Elements.
                            gradient_strategy (QLaw.GradientStrategy): The strategy used to compute the gradient dQ_dOE. Defaults to FiniteDifference.
        """
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def calculate_thrust_acceleration_at(self, instant: ostk.physics.time.Instant, position_coordinates: numpy.ndarray[numpy.float64[3, 1]], velocity_coordinates: numpy.ndarray[numpy.float64[3, 1]], thrust_acceleration: ostk.core.type.Real, output_frame: ostk.physics.coordinate.Frame) -> numpy.ndarray[numpy.float64[3, 1]]:
        """
                        Calculate the thrust acceleration at the provided coordinates and instant.
        
                        Args:
                            instant (Instant): Instant of computation.
                            position_coordinates (np.array): Position coordinates.
                            velocity_coordinates (np.array): Velocity coordinates.
                            thrust_acceleration (float): Thrust acceleration magnitude.
                            output_frame (Frame): The frame the acceleration is expressed in.
        
                        Returns:
                            np.array: The acceleration.
        """
    def get_coe_domain(self) -> QLaw.COEDomain:
        """
                        Get the COE domain.
        
                        Returns:
                            QLaw.COEDomain: The COE domain.
        """
    def get_gradient_strategy(self) -> QLaw.GradientStrategy:
        """
                        Get the gradient strategy.
        
                        Returns:
                            QLaw.GradientStrategy: The gradient strategy.
        """
    def get_parameters(self) -> QLaw.Parameters:
        """
                        Get the parameters.
        
                        Returns:
                            QLaw.Parameters: The parameters.
        """
    def get_target_coe(self) -> ostk.astrodynamics.trajectory.orbit.model.kepler.COE:
        """
                        Get the target COE.
        
                        Returns:
                            COE: The target COE.
        """
