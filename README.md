# **Open Source Term Project Team 32**

# **Handy Controller**
--------------------------------------------------
#### ***Control your computer with simple hand gestures***
> Sometimes We just want to stay away from our computer then watch the media in a comfortable position.  
> Our project provides that performing useful functions through hand gestures without direct keyboard mouse manipulation.

--------------------------------------------------
#### ***Installation***

##### Before Installation  
> Our project need **webcam** for hand detection. 
And Our program written in Python, So you have to install python. We used Python versions **3.8 or higher**. But We think 3.xx version would be fine.
If you have problem with python version, Please open issue. 
1. First. You have to download our project. You can download easily with git clone.
   ```sh
   $ git clone https://github.com/chanhoim/Handy-Controller.git
   ```
2. Then, You have to install some python libraries for our project. 
   ```sh
   $ pip install -r requirements.txt 
    ```
3. Now, You can run our program.
   ```sh
   $ python main.py
   ```




#### ***How to use***

>The most basic of our program is to specify the mode with your left hand and take action with your right hand. 


##### Left Hand (Mode Selection)
As mentioned above, the mode is selected through the left hand. 
![Exmaple](https://user-images.githubusercontent.com/101717041/207253397-e8b652c8-3e37-4fda-99bf-f8d8baa5ed73.gif)
The reason why the mode cannot be specified at the beginning of the video is that it is an idle state. The idle mode is specified by the user to prevent unnecessary mode recognition and action, and can be canceled by taking the idle motion again.  

##### Right Hand (Action)
Now let's look at an example of a right-handed action. In mouse-mode-1 action, 
-you can move mouse with your thumb, index finger, and middle finger out.
-you can left click with folding your index finger.
-you can right click with folding your middle finger.
-you can go back or go forward with pressing your thumb at a specific position on your index finger.

![mouse-mode-1_example](https://user-images.githubusercontent.com/101717041/207259502-1bb6c5aa-9e8c-4094-b2d7-ea5b80882ba2.gif)

To take an action as described above, We use the distance of specific points on the right hand.
You can get a hint about which particular point induces which behavior through code or webcam.
Please refer to the landmark index information below and what actions you can perform.
 

![Hand_Landmarks](https://github.com/chanhoim/Handy-Controller/blob/dev_KKDDJJ/hand_landmarks.png?raw=true)



1. **Thumb**  
-> **Brightness Control Mode**  : Set brightness 0, Set brightness 100, Increase in brightness, Decerese in brightness
2. **Fist Gesture**  
-> **Idle State Mode** : Do nothing with mode selection or action  
3. **Middle Finger**  : 
-> **Quit**  : exit program 
4. **Index Finger**  
-> **Volume Control Mode**  : Increase volume, Decrease in volume, Toggle mute
5. **Index Finger + Middle Finger**  
If you put your index and middle finger together
->**Mouse Control Mode-1**: moving mouse point, left click, right click, go back, go forward
If you keep your index and middle fingers away
->**Mouse Control Mode-2**: moving mouse point, mouse drag, page up, page down
6. **Index Finger + Middle Finger + Ring Finger**  
-> **Media Control Mode**: play previous , play next, play/puase
7. **Index Finger + Middle Finger + Ring Finger + Little Finger**  
-> **Page Control Mode**  : page up, page down, home, end
8. **All Fingers**  
-> **Desktop Control Mode**  : (In multi desktop environment) previous desktop, next desktop, show desktop, show applications

**You can add action triggers and actions as you like.**

--------------------------------------------------

#### ***Member Information***

> 202234863 Kim Dong Ju  
> 201638413 Nam Jong Su  
> 201835510 Lim Chan Ho  

#### ***References***  
--------------------------------------------------
-  **[PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/)**
- **[MediaPipe](https://google.github.io/mediapipe/)**
- **[MedaiPipe Solutions](https://mediapipe.dev/)**
- **[AI Virtual Mouse | OpenCV Python | Computer Vision](https://youtu.be/8gPONnGIPgw)**
- **[Multiple Hand Gesture Control with OpenCV Python | CVZone](https://youtu.be/3xfOa4yeOb0)**
- **[pynput](https://pypi.org/project/pynput/)**
