# CIR-AutoDJ

# local Prototyp
Requirements:
-Virtualbox
-debian-VM
http://debian.uvigo.es/debian-cd/9.2.1/multi-arch/iso-cd/

-install openCV: find the installation script here:
http://milq.github.io/install-opencv-ubuntu-debian/
https://github.com/milq/milq/blob/master/scripts/bash/install-opencv.sh

% TODO check if needed
(apt-get install build-essential module-assistant
m-a prepare)
https://virtualboxes.org/doc/installing-guest-additions-on-debian/

% guest additions einlegen
sh /media/cdrom/VBoxLinuxAdditions.run
% reboot
% optional: guvcview installieren um kamera zu testen

Used repositories:
https://github.com/LukashenkoEvgeniy/People-Counter


# mac Dev-Env

https://www.learnopencv.com/install-opencv3-on-macos/


mkvirtualenv cvp3 -p python3
workon cvp3
pip install numpy ipython
(pip install numpy scipy matplotlib scikit-image scikit-learn ipython)
deactivate


brew search opencv
brew install opencv



python3 --version
which python3

(python2 --version
which python2

echo /usr/local/opt/opencv/lib/python2.7/site-packages >> /usr/local/lib/python2.7/site-packages/opencv3.pth)

echo /usr/local/opt/opencv/lib/python3.6/site-packages >> /usr/local/lib/python3.6/site-packages/opencv3.pth

find /usr/local/opt/opencv@3/lib/ -name cv2*.so
/usr/local/opt/opencv@3/lib//python3.6/site-packages/cv2.cpython-36m-darwin.so

ls ~/.virtualenvs/cvp3/lib/python3.6/site-packages/
cd ~/.virtualenvs/cvp3/lib/python3.6/site-packages/
ln -s /usr/local/opt/opencv@3/lib/python3.6/site-packages/cv2.cpython-36m-darwin.so cv2.so

workon cvp3

ipython

import cv2
print(cv2.__version__)

(print cv2.__version__)

(brew install opencv -- with-contrib)

(brew install homebrew/science/opencv3
brew install homebrew/science/opencv3 -- with-contrib)



workon cv
...
deactivate

https://www.pyimagesearch.com/2016/12/05/macos-install-opencv-3-and-python-3-5/

ls /usr/local/Cellar/python3/3.*/Frameworks/Python.framework/Versions/3
ls /usr/local/Cellar/python3/3.*/Frameworks/Python.framework/Versions/3.5/lib/python3.5/config-3.5m/libpython3.5.dylib
ls /usr/local/Cellar/python3/3.5.2_3/Frameworks/Python.framework/Versions/3.5/lib/python3.5/config-3.5m/libpython3.5.dylib
ls -d /usr/local/Cellar/python3/3.*/Frameworks/Python.framework/Versions/3.5/include/python3.5m/
ls -d /usr/local/Cellar/python3/3.5.2_3/Frameworks/Python.framework/Versions/3.5/include/python3.5m/

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D PYTHON3_LIBRARY=/usr/local/Cellar/python3/3.5.2_3/Frameworks/Python.framework/Versions/3.5/lib/python3.5/config-3.5m/libpython3.5.dylib \
    -D PYTHON3_INCLUDE_DIR=/usr/local/Cellar/python3/3.5.2_3/Frameworks/Python.framework/Versions/3.5/include/python3.5m/ \
    -D PYTHON3_EXECUTABLE=$VIRTUAL_ENV/bin/python \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_python3=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=ON ..

without replacement:
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D PYTHON3_LIBRARY=YYY \
    -D PYTHON3_INCLUDE_DIR=ZZZ \
    -D PYTHON3_EXECUTABLE=$VIRTUAL_ENV/bin/python \
    -D BUILD_opencv_python2=OFF \
    -D BUILD_opencv_python3=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=ON ..

Source:
https://grantwinney.com/how-to-create-a-raspberry-pi-virtual-machine-vm-in-virtualbox/

q-learning:
source: https://github.com/rlcode/reinforcement-learning/

---
mac:

python3 --version
python3 -m pip install -r requirements.txt
sudo python3 -m pip uninstall numpy
python3 -m pip install numpy==1.12.
python3 -m pip install numpy

python3 -m pip list

---

python3 q_learning_agent.py


