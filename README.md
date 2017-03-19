# ECE1779_Assignment1
ECE1779 Introduction to Cloud Computing Assignment 1
## Team Info
- Dade Sheng (ID:1002229279) dade.sheng@mail.utoronto.ca
- Siyang Zhao (ID:1002187091) kern_zhao@126.com
## Architecture
### Usage
#### Access Point
- User: http://dade.ca/a1
- Admin: http://dade.ca/a1-admin
#### Existing User
- Username: dddaaa
- Password: dddaaa
#### Transformations
When an image is clicked, 4 images would show:
* original image
* 90-degree transformation
* 180-degree transformation
* 270-degree transformation
### S3
- All user images are saved on S3
- Each user has one bucket
- Brower loads images directly from S3 links
### EC2
#### Master instance (one)
- Check CPU utilization of each worker every minute
- Create more instances if average CPU utilization above setting threshold
- Terminate randomly workers if average CPU utilization below setting threshold
#### Database instance (one)
- Store information about user accounts
- Store images owned by a user (and their transformations)
- Store admin settings, such as CPU threshold, ratio to expand the worker pool, etc.
#### Workers instance (multiple)
- All workers are registered to a load balancer
- Receive requests from users and render web contents
- Transform images uploaded by user
- Upload images and their transformations to S3
- Provide image links (valid for 60 seconds) to clients for display
