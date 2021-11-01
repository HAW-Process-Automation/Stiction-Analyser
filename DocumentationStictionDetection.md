[![N|Solid](https://www.seeq.com/sites/default/files/seeq-logo-navbar-small.png)](https://www.seeq.com)

# User Guide

[![N|Scheme](StictionDetectionExample.png)](https://www.seeq.com)

----

## Overview

The following section will be used to explain the workflow and the algorithm behind the seeq-stictiondetection add-on. At a starting point important technical terms and the physical background will be explained. This section is followed by the workflow of the developed approach and the limitation.

## What is Valve Stiction and why should it be detected?

Every plant in the process industry requires the ability to control their parameters during production to ensure a safe manufacturing process. In order to control the process, several so-called actuators are being used. Above all of the actuators are the valves. For instance, valves are used to increase or decrease the amount of fluid to cool a reactor or even the particle flow inside a pipe. In fact, a valve can be used to directly interevent in the process. Additionally, with the nearly infinite possible use cases in the process industry valves are one of the most common control apparatus. Therefore, it is of outmost importance to rely on the impeccable operation of the valves. Otherwise, the process is not in complete control of the operators and process engineers which could lead in less product amount ore a decrease in the product quality. In the worst-case scenario, a safety gap could occur followed by an explosion or a hazard substance could escape into the environment. All in all, it is of great interest to maintain the control equipment on a frequent basis and detect equipment failure as quickly as possible.  
As outlined above valves are the most common control actuators. To ensure an unobstructed manufacturing process it is of importance to monitor the performance of the valves. One possible way is to investigate the data received from the process monitoring system and try to find characteristic patterns inside the data. At this point it is required to understand the basics of automation and control loops to further perceive the basic workflow of the algorithm. 

## Control Theory

In this section will be explaining the absolute basics of control by understanding a simple feedback control loop. For instance, a control loop could be one temperature sensor and one valve as the actuator. The logic behind the system could be a simple threshold which would open the valve 100 % once the signal received from the sensor is above the predefined value. This simple control loop is illustrated in the following figure. 

[![N|Solid](https://github.com/Timothy716/seeq-stictiondetection/DocumentationImages/Feedback_loop.png)]
#### Figure 1: Feedback loop

The first indication of a problem with the valve is an oscillation in the process variable (PV) and the Controller output. Therefore, it is best practice to search for oscillation behaviour in the OP and PV signal. The cause of the oscillation is a higher friction inside the valve stamp initiated by the accumulation of particles. Once the valve receives the command to open or close it will be impeding by the debris. A higher force compared to the clean valve is needed to open the valve. This leads in a time delay in the response of the valve. The Error however will further increase as well as the force to move the valve stamp until the valve start to move. It is common to observe a slip jump behaviour. Once it is required to move the valve in a different direction the same physical behaviour will appear. The explained behaviour is common labelled as valve stiction. The explained process can be determined by plotting the data in a PV OP plot. As some of the feedback loops are in cascade mode it is best practice to use the Error signal instead of the PV signal. In case the signals are oscillating the plot will show an ellipse. The combination of oscillation and stiction will end up in a sharp cornered ellipse. In conclusion, if one is looking for valve stiction, sharp cornered ellipses are the kind of images to investigate for.  

# Stiction Detection Algorithm

As explained in the above section the detection algorithm should first detect oscillations and in case the oscillations are sharp cornered in the Error OP plot the valve suffers with a high probability from stiction. The algorithm for the oscillation detection examined and counts the zero crossings. Additionally, the approach evaluates if the amplitude of one cycle (data between two zero crossings) is above a user defined percentage this cycle will be counted. If the number of counted cycles exceeds the predefined number within the supervision time this time period contains an oscillating signal. The algorithm was taken to determine the start and end point of the oscillation and then to slice the raw signal. The sliced signal will then further be sliced containing one full oscillation cycle. This data will be plotted in a scatterplot and an image will be created out of that. The following figure can be taken as an example on how the images could look like. 

[![N|Solid](https://github.com/Timothy716/seeq-stictiondetection/DocumentationImages/Sharp_cornered_ellipse.png)]
#### Figure 2: Sharp cornered ellipse and smooth cornered ellipse

To ensure that the investigated images contain an elliptical shape a shape detection will be applied. For that the OpenCV library will be utilized by finding first the contours and then compare the ellipse with three different ellipses. In case the similarity with one of the compared ellipses is higher than 50 % the analysis will be continued. In the next step the two end edges of the ellipse will be cropped and stored as separated images. This step is followed by closing and detecting the contour of the shapes. The images could now look like the ones illustrated in the following figure. 

[![N|Solid](https://github.com/Timothy716/seeq-stictiondetection/DocumentationImages/Sharp_cornered_ellipse_detail.png)]
#### Figure 3: Sharp cornered ellipse compared to smooth cornered ellipse detail

Then the Ramer–Douglas–Peucker Algorithm is applied which will be used to find the minimum number of points which could connected with straight lines to represent the original shape. If the shape could be presented by three point it shows a triangle which means that it is a sharp cornered ellipse and therefore and clear evidence of stiction in the valve. The result of the analysis is then a signal which contains the amount of stiction in percent. In addition, the user could send the oscillating signal back to the Workbench. The oscillating signal equals one if an oscillation is present and zero if no oscillation is detected. The user could now apply a “Value Search” to find the time intervals where signal is oscillating or is above a certain amount of stiction. The magnitude of the stiction will be calculated by fitting and ellipse in the sharp cornered ellipse. Then the width of the fitted ellipse will be calculated which represents the amount of stiction in the control valve. 


# How to Use

The workflow than be divided into x main parts. In the following section those part will be explained. The workflow in short is given below. A more detailed explanation can be found in the outlined section of each step. 

[![N|Solid](https://github.com/Timothy716/seeq-stictiondetection/DocumentationImages/Stiction_Detection_UI.png)]
#### Figure 4: Stiction Detection UI

### Workflow

## 1)	Select the Error and the OP signal
## 2)	Review if the selected time range is sufficient (the default is the display range)
## 3)	Select a condition if needed (Selection of the wrong Condition could be changed by clicking on the “CANCEL” button)
## 4)	Click on the “ANALYSE” button (wait until the loader in the button disappears)
## 5)	In case something interesting was found it will be displayed in the “Results” section
## 6)	Give the signals names and check the box if it should be sent to the workbench
## 7)	Click on “SEND SIGNAL TO WORKBOOK” button 
## 8)	Use “Deploy Stiction Analysis” to schedule the stiction analysis (coming soon)

# Example Use Cases 

## First Use Case: Oscillation Detection 

The first step by detecting stiction in control valves is to identify oscillation behaviour in the OP signal. The following figure shows a signal (green) with three separated areas of oscillations. The other signal (purple) is the result from the oscillation detection. From this short example can be derived that the algorithm is able to detect oscillations and locate the start and end points. 

[![N|Solid](https://github.com/Timothy716/seeq-stictiondetection/DocumentationImages/Stiction_Detection_UI.png)]
#### Figure 5: Oscillating signal and results from the Oscillation Finder

Choosing a more detailed view the green signal is clear suffering from oscillation behaviour. 

[![N|Solid](https://github.com/Timothy716/seeq-stictiondetection/DocumentationImages/Stiction_Detection_UI_detail.png)]
#### Figure 6: Detail view of the oscillation signal


## Second Use case: Stiction Contained Signal (Level)

The first example containing information of stiction is taken from the SACAC Database and contains information about a level loop. A detailed look at the signal shows clear sign of stiction. Those signs are illustrated in the following figure. A first indicator is that the signal is oscillating. The second indicator is the flat corners of the oscillation. Those flat corners lead in the Error OP plot to sharp cornered ellipses. 

Use_case_stiction_level.png
#### Figure 7: Detailed time trend of the level signal
The results of the can be seen in the following figure. In this figure is the Error signal (orange), the OP signal (purple), the stiction signal (blue) and the results of the oscillation finder (green). From the analysis can be seen that there the algorithm detected it as a stiction case with a magnitude of 2 %. 

Use_case_stiction_level_results.png
#### Figure 8: Results of the stiction analysis 

## Third Use Case Stiction Contained Signal (Flow)

The third use case is a flow loop suffering from stiction. A slice of the signal can be investigated in the following figure. The flat cornered peaks of the oscillation are clear signs of a loop suffering from stiction. 

Use_case_stiction_flow.png
#### Figure 8: Detailed time trend of the flow signal

The results generated by the Stiction Detection add-on can be reviewed in the following figure. The add-on can detect the oscillation and the signs of stiction in the signals. The calculated magnitude of stiction is 5 %.

Use_case_stiction_flow._results.png
#### Figure 9: Results flow loop