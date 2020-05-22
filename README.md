Tic tac toe
This game is based on gesture recognition. Any interaction with the game occurs using a hand gesture. For instruction how to play the game, please watch the video instructions/video_instruction.mp4

<b>How to run.</b></br>
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
