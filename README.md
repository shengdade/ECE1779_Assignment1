# ECE1779-Project1
ECE1779: Introduction to Cloud Computing
## Team Info
Name | ID | Email
------------ | ------------- | -------------
Dade Sheng | 1002229279 | dade.sheng@mail.utoronto.ca
Siyang Zhao | 1002187091 | kern_zhao@126.com
## Instructions
#### Web Interfaces
- User: http://dade.ca/a1
- Admin: http://dade.ca/a1-admin
#### Existing User
- Username: _dddaaa_
- Password: _dddaaa_
#### Console Access
- URL: https://554376045366.signin.aws.amazon.com/console
- Username: _ece1779ta_
- Password: _ece1779ta_
#### Instances Access
- Acquire Key Pair
```
  wget http://www.ecf.utoronto.ca/\~shengdad/file/keypair.tar
  tar xvf keypair.tar
```
- Log into __Master__ instance _(description below)_
```
  ssh -i ece1779.pem ubuntu@54.175.182.31
```
- Log into __Database__ instance _(description below)_
```
  ssh -i ece1779.pem ubuntu@54.159.199.112
```
- Log into __Primary Worker__ instance _(description below)_
```
  ssh -i ece1779.pem ubuntu@54.205.86.184
```
## Architecture
### Transformations
* 90-degree transformation
* 180-degree transformation
* 270-degree transformation
### S3
- All user images are saved on S3
- Each user has one bucket
- Browser loads images directly from S3 links
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
- There is at least one worker always running, which is called 'primary worker'
## Workflow
### Users Perspective
#### Frond End
1. Go to http://dade.ca/a1
2. Create a new user if needed
3. Log in as an existing user (e.g. dddaaa:dddaaa)
4. Upload a new image by clicking 'Upload Image'
5. Browse all images uploaded
6. Click an image to view its transformations
7. Log out by clicking the icon on top right corner
#### Back End
1. Render Log-in and Register pages
2. If register: store user account to database after input validation
3. If log-in: validate username and password, redirect to main page if success
4. Fetch temporary image URLs from S3 and present an album page to browser
5. If user uploaded an image: upload original image to S3, fire a celery background task which do transformations, upload transformations to S3, and write S3 keys to database
6. Maintain a log-in session which expire in 5 minutes
7. Automatically log out the user if it's idle for 5 minutes
### Admin Perspective
#### Frond End
1. Go to http://dade.ca/a1-admin
2. Choose from 'Manually setting worker pool' or 'Auto-scaling the worker pool'
3. If manually, select the number of worker to create/destroy, and click 'Create'/'Destroy' button
4. If auto-scaling, adjust parameters (threshold or ratio), which will be saved to database once changed
5. View CPU utilization graph and detailed statistics, such as instance state, etc.
6. Click the button 'Delete all user images' if necessary
#### Back End
1. Fetch admin settings (thresholds and ratios) from database and render them on admin page
2. Update settings to database if changed
3. Handle requests for creating new workers and register new instances to load balancer
4. Handle requests for destroying existing workers, which are then automatically removed from load balancer
5. Make sure there is at least one worker running, which is called 'primary-worker'
6. Execute a periodic task, check workers' status for every minute:
   * Calculate average CPU utilization of workers
   * Fetch admin settings (thresholds and ratios) from database
   * If auto-scaling is on and all workers running (in case there are pending or shutting-down instances):
      * if average CPU utilization is above growing threshold, create more instances based on expand ratio
      * if average CPU utilization is below shrinking threshold, destroy instances based on shrink ratio
## Additional Feature
### Asynchronous Process
- Run background tasks using [Celery distributed task queue](http://www.celeryproject.org)
- Execute tasks which are not necessary in main thread, such as image transformations, CPU status checking
### Responsive Web
- Employ [Bootstrap framework](http://getbootstrap.com) for developing responsive pages
- Make web pages look good on all devices, for example, on phones
![Alt text](/document/responsive.jpg?raw=true "Optional Title")
