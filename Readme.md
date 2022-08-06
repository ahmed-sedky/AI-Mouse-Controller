# AI Mouse COntroller
Author: Ahmed Hossam Sedky
----
## Libraries versions
* numpy version **1.21.3**
* cv2 version **4.5.4-dev**
* autopy version **4.0.0**
* mediapipe version **0.8.10.1**
-----
## Code architecture
* Hand Detection 
    * use mediapipe and cv2  to detect and track hand landmarks in the input image 

* move mouse using one finger up and click by raising index and middle finger together
    * Use autopy to click mouse 

