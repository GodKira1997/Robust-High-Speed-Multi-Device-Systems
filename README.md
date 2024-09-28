# Robust-High-Speed-Multi-Device-Systems
a modular system that can be used in lab situations where the reliability of the connection between sensors and the end user is unstable but a stable connection to data is required.

## Introduction
The world of robotics has many challenges plaguing it, sim-to-real, sensor failures, interactions with humans, and many more. For this work, we will be focusing on the ever-present concern of both detecting sensor malfunctions and recovering from them on a closed high-speed system. This problem can exist as the sensor itself is damaged and no longer transmitting data, the sensor is damaged and transmitting bad data, the data being corrupted during transfer, and parts of the internal network going down just to name a few.
In small-scale robotics; where a malfunction might result in a low-speed crash or a bad trial run, problems can be addressed slowly and troubleshooted by a human after the fact. However; in a high-speed system, such as an autonomous drone flying through a crowded street, or a large robot working alongside a human in an assembly line, this is not the case. When malfunctions happen in these systems the potential damage will be significantly more catastrophic and potentially life-threatening to those around the autonomous agent. In these
cases, the system needs to be able to detect failures and recover enough to safely power down and avoid harm to anything or anyone. For the larger robots on the ground this might just be stopping motion, but for a drone in the air just stopping motion will cause it to fall uncontrollably from the sky. So there is a need for a system that can recover enough, perhaps using other sensors to cover for the failing systems until either
the systems come back online or it is safe to power off. As these systems will be working around humans there is a need for these auxiliary systems to not impede the regular function of the autonomous system. It does the a human no good to have the robot stop after it has

## Solution
We propose a fault-tolerant three part system to these problems
* A pub/sub model for sensors transmitting their sensor data
* A central processing system replicated with haproxy
* A heartbeat monitoring system for all the sensors
![Robust High-Speed Multi-Device Systems](https://github.com/user-attachments/assets/eaebf92d-404e-4d8c-9fc4-6d4285563772)

## References
```markdown
1. L Computational Geometry: Algorithms and Applications. Third Edition. By Mark de Berg, Otfried Cheong, Marc van Kreveld, Mark Overmars. – Chapter 13
2. [J. Wang and M. Q. -H. Meng, "Optimal Path Planning Using Generalized Voronoi Graph and Multiple Potential Functions," in IEEE Transactions on Industrial Electronics, vol. 67, no. 12, pp. 10621-10630, Dec. 2020, doi: 10.1109/TIE.2019.2962425.](https://ieeexplore.ieee.org/document/8948325)
````

## Authors
* [Anurag Kalluwar](https://github.com/KD6763)
* [Neel Chaundary](https://github.com/neelchaudhary)
* [Will Gebhardt](https://github.com/willgebhardt)
