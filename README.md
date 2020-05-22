## Tic tac toe
This game is based on gesture recognition. Any interaction with the game occurs using a hand gesture. To understand how to play the game, please watch the video instructions/video_instruction.mp4<br/>All my research steps are described below

## How to run.
<ol>
  <li><a href = "https://www.anaconda.com/products/individual">download the Anaconda</a></li>
  <li>run <code>cmd</code> and create new environment <code>conda create --name tic_tac_toe</code></li>
  <li>activate environment <code>conda activate tic_tac_toe</code></li>
  <li>download libraries for interraction with GPU <code>conda install pytorch torchvision cudatoolkit=10.1 -c pytorch</code></li>
  <li>go to downloaded repository and download additional libraries <code>pip install -r requirements.txt</code></li>
  <li><a href ="https://drive.google.com/file/d/1XApBSKKATOBsrSxhckA0_Q5tTkZv4ZBv/view?usp=sharing">download weights for Yolov3 (<code>yolov3_2500.weights</code>)</a> and put it into tools/finger_detection/weights</li>
  <li>check camera connection</li>
  <li>run <code>python main.py</code></li>
</ol>

## Hardware requirements:
<ul>
  <li><a href = "https://en.wikipedia.org/wiki/CUDA">GPU that supports CUDA 10.</a></li>
</ul>

## Research
The task is divided into two stage.
<ul>
  <li>Gesture detection.</li>
  <li>Game engine.</li>
</ul>
Second step is casual so only first stage deserves our attention.
After several days of googling I found two solutions.
<ul>
  <li>Algorithm based on skin selection by hsv range of skin color. After selection we can find contours. Based on the contours, you can say how many fingers a person shows.</li>
  <li>This algorithm differs from the previous one in that the hand selection is not based on color but on the background selection.</li>
</ul>
First algorithm doesn`t work well because if in the background is color that looks like skin it will be also selected. <br/>
Second algorithm doesn`t work well because if the background changes it will destroy the full algorithm.<br/>
This led me to think about using neural networks.<br/>
First my try was to make my own CNN using dataset from <a href ="https://www.kaggle.com/koryakinp/fingers">kaggle</a>.
