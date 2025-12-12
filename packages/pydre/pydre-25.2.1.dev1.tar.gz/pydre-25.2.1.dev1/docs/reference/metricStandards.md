## SAE Standards

### SAE J2944
___
The Society of Automotive Engineers `(SAE)` released a document entitled `Surface Vehicle Recommended Practice`. This document establishes a common standard for the "Operational Definitions of Driving Performance Measures and Statistics". The aforementioned document is tagged by SAE as `J2944`. From here forth, this tag will serve as the document's name: `SAE J2944`.

### Application to Pydre
___
With the standards that `SAE J2944` sets forth, the applicable metrics from Pydre should conform to each of their respective, predetermined requirements. Below, there is a list of all mentioned metrics and each of their requirements. With that, there are some metrics in Pydre that collect specialized data or perform simple statistics calculations. These metrics are not specified in `SAE J2944`. For these situations, the metrics are omitted from the list below with the understanding that fundamental research standards are employed at all times during studies.

### Pydre Metrics Conform to SAE J2944 Standards
___

This section will enumerate every applicable metric found within Pydre, show their requirements per SAE J2944, and expound on said requirements with any relevant notes.

1. Steering Entropy
    - Requirements from `SAE J2944 - 9.2.1`:
        - "*The first instance the term steering entropy is used in a document, the calculation method (1999 or 2005) shall be reported.  If other computation methods are used, a link to the source code should be provided.*"
    - The steering entropy function in Pydre uses Boer's 1999 method for calculating steering entropy.

2. Tailgating Time
    - Requirements from `SAE J2944 - 8.1.4`:
        - "*... the two vehicles in the measurement, the common external feature (option A, B, or C), and the value above which time headway is ignored, if any, shall be reported.  The method for sensing the time separation shall also be reported.*"
    - Like many other metrics omitted from this list, how SimCreator collects data is something that the experimenter has limited control over. Despite no guidelines for tailgating, `SAE J2944` does mention `time headway` calculations between a subject and a lead car. The requirements, however, only address the need for measurements to be based on a consistent external feature present on both vehicles, the threshold for following, and the method for time sensing. With that, these measurements are collected by SimCreator and are not included within the `Pydre` program. 

3. Lane Position
    - `SDLP` (Standard Deviation of Lane Position)
        - Requirements from `SAE J2944 - 10.1.3`:
            - "*... the denominator term (N or N-1), the option used to compute the mean (option A, B, or C), the reference point on the vehicle used to determine lateral lane position (1 - lateral midpoint of front bumper, 2 - center of the vehicle front axle, 3 - center of gravity, 4 - spatial center), the time or distance in front of the vehicle bumper (if vehicle position is predicted), and the test condition(s) and/or independent variables over which the mean was determined (e.g., conditions, subjects, etc.) shall be reported.*"
        - Pydre uses `polars` and `numpy` for any statistics calculations. In SimCreator 3.x, distance measures are generally calculated from the center of gravity of the vehicle. 
    - `Mean Lane Position`
        - Requirements from `SAE J2944 - 10.1.2`:
            -  "*... the method used to calculate lane position (option A, B, or C) and the reference point on the vehicle (1 - lateral midpoint of front bumper, 2 - center of the vehicle front axle, 3 - center of gravity, or 4 - spatial center) shall be reported.*"
        - The point by which SimCreator calculates following distances is consistent and not within the scope of metrics.py. This is the case for many speed and time-based metrics. In SimCreator 3.x, distance measures are generally calculated from the center of gravity of the vehicle.  

4. Brake Jerk
    - Calculation guidance from `SAE J2944 - 7.2.13`:
        - "Jerk is the time derivative of acceleration and is positive if the vehicle is accelerating, negative if decelerating. ... For driving simulators, vehicle speed is a default measure, and longitudinal acceleration may be available directly or be determined by differentiation of the speed signal."
    - Within metrics.py, the function `brakeJerk()` is supplied longitudinal acceleration and time. With those two data frames, the function calculates the time derivative of long. acceleration using numpy's gradient() function.

5. Reaction Time
    - Definition from `SAE J2944 - 6.5.2`:
        - "Time interval, usually measured in seconds or milliseconds, from onset of an initiating event to the first observable response to that event, such as a movement of the driver’s hand (on the steering wheel) or foot (on a pedal or from the floor), or, the beginning or end of an utterance by the driver (for voice-activated controls)."
    - All metric functions that consider reaction time within metrics.py (such as `tbiReaction()` and `ecocar()`) have initiating events tracked in the form of Activation values that read as 1- if the reaction time is being considered- or 0- if it is not. This qualifies as an initiating event, as decribed in SAE's definition of reaction time. While the first observable response varies for each of these functions, SAE does not specify any parameters for this category.