# Event Scheduling & Resource Allocation System

As per the given requirements, the Event, Resource, Allocation, and Report modules were successfully developed.
The main highlight of this project is the conflict detection logic, which ensures that whenever a resource is already allocated during a specific time, the system automatically throws a conflict error to prevent overlapping bookings.

Video Link:

https://www.linkedin.com/posts/jayaraman-r-50571a376_python-flask-fullstackdevelopment-activity-7398584631177994240-fszS?utm_medium=ios_app&rcm=ACoAAF0Cy1UBni0JhLY9wrfyVUSgIXEbj7XQC4c&utm_source=social_share_send&utm_campaign=copy_link



Screenshots :

Event :

<img width="863" height="458" alt="image" src="https://github.com/user-attachments/assets/2e5b62a5-0818-4e46-8167-abe110b5c190" />


Event (Add,edit,view,delete):

<img width="844" height="407" alt="image" src="https://github.com/user-attachments/assets/62373a40-ffc2-4bc6-80f3-8f3ec11a3fa6" />

Resouce Page:

<img width="975" height="473" alt="image" src="https://github.com/user-attachments/assets/908f88e1-15d4-4210-9dab-89688a3360f2" />

Allocation Page :

<img width="836" height="403" alt="image" src="https://github.com/user-attachments/assets/cf4a6cb8-b847-4176-af84-86dbfefe55f0" />

Allocation Page with Conflict :

<img width="975" height="470" alt="image" src="https://github.com/user-attachments/assets/0fecaf7b-af56-4c3b-8ed8-082a2300ada8" />

Report Page : (with upcoming events):

<img width="879" height="416" alt="image" src="https://github.com/user-attachments/assets/71741fa9-4c96-4a91-afac-727926688872" />

Report Page(with utilization of Resources):

<img width="830" height="402" alt="image" src="https://github.com/user-attachments/assets/757c7fa9-a8a5-43e8-b439-c9c96ca22f0d" />

Project Documentation Summary :

As per the given requirements, the following modules were developed successfully:

•	Event Module – Create, update, and manage events with date and time controls.

•	Resource Module – Add and maintain resources required for event operations.

•	Allocation Module – Assign resources to events with complete validation.

•	Report Module – Generate detailed utilization reports based on date ranges.

The core objective of the project was to ensure that no resource could be double-booked.

To achieve this, a conflict detection mechanism was implemented inside the allocation workflow:

•	Whenever a user tries to allocate a resource that is already booked during the selected event time,
•	The system automatically detects the overlap,

•	And throws a conflict error, preventing invalid or duplicate allocations.

This ensures accurate scheduling, clean resource management, and reliable system behavior across all modules.


