#!/bin/bash
# try to be in a virtualenv before you start
DATE=`date +%F_%T|sed s/\:/\-/g`
DIRNAME=spinn-dev-git_$DATE
ABSDIRNAME=$PWD/$DIRNAME
echo $ABSDIRNAME

# the gnu arm compiler is necessary for compiling SpiNNaker binaries
sudo apt-get install gcc-arm-none-eabi
# pip is the python package manager, setuptools are used to install stuff
sudo apt-get install python-pip python-setuptools
# this is necessary in order to build sPyNNaker
sudo apt-get install libxml2-dev libxslt1-dev cython zlib1g-dev
# these are basic python requirements
sudo apt-get install python-numpy python-scipy python-matplotlib
# and a capable terminal
sudo apt-get install ipython python-virtualenv

virtualenv $DIRNAME
source $DIRNAME/bin/activate
cd $DIRNAME

# now we should be inside the virtualenv
# let's link the big basic requirements into here:
# scipy
ln -s /usr/lib/python2.7/dist-packages/scipy $VIRTUAL_ENV/lib/python2.7/site-packages/
ln -s /usr/lib/python2.7/dist-packages/scipy-*.egg-info $VIRTUAL_ENV/lib/python2.7/site-packages/
# numpy
ln -s /usr/lib/python2.7/dist-packages/numpy $VIRTUAL_ENV/lib/python2.7/site-packages/
ln -s /usr/lib/python2.7/dist-packages/numpy-*.egg-info $VIRTUAL_ENV/lib/python2.7/site-packages/
# matplotlib and its libraries
ln -sf /usr/lib/pymodules/python2.7/matplotlib $VIRTUAL_ENV/lib/python2.7/site-packages/
ln -sf /usr/lib/pymodules/python2.7/matplotlib-*.egg-info $VIRTUAL_ENV/lib/python2.7/site-packages/
ln -sf /usr/lib/pymodules/python2.7/pylab.py $VIRTUAL_ENV/lib/python2.7/site-packages/
ln -sf /usr/lib/python2.7/dist-packages/dateutil/ $VIRTUAL_ENV/lib/python2.7/site-packages/
ln -sf /usr/lib/python2.7/dist-packages/pyparsing.py $VIRTUAL_ENV/lib/python2.7/site-packages/
ln -sf /usr/lib/python2.7/dist-packages/pyparsing-*.egg-info $VIRTUAL_ENV/lib/python2.7/site-packages/

# these are basic requirements 
pip install six enum34

mkdir dev
cd dev

git clone https://github.com/NeuralEnsemble/PyNN.git
cd PyNN
python setup.py install
cd ..

git clone https://github.com/SpiNNakerManchester/DataSpecification.git
cd DataSpecification
python setup.py develop
cd ..

git clone https://github.com/SpiNNakerManchester/SpiNNMachine.git
cd SpiNNMachine
python setup.py develop
cd ..

git clone https://github.com/SpiNNakerManchester/PACMAN.git
cd PACMAN
python setup.py develop
cd ..

git clone https://github.com/SpiNNakerManchester/spinnaker_tools.git
cd spinnaker_tools
source setup
make -j3
cd ..

git clone https://github.com/SpiNNakerManchester/spinn_common.git
cd spinn_common
make -j3
make install
cd ..

git clone https://github.com/SpiNNakerManchester/SpiNNMan.git
cd SpiNNMan
cd c_models
make -j3
cd ..
python setup.py develop
cd ..

git clone https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git
cd SpiNNFrontEndCommon
cd c_common
make -j3
make install
cd ..
python setup.py develop
cd ..

git clone https://github.com/SpiNNakerManchester/sPyNNaker.git
# this would be Christoph's version
# git clone https://github.com/tophensen/sPyNNaker.git
cd sPyNNaker
cd neural_modelling
source setup
make -j3
cd ..
python setup.py develop
cd ..

# this enables calling "import pyNN.spiNNaker as p"
pip install pyNN-spiNNaker

# now for external device support
git clone https://github.com/SpiNNakerManchester/sPyNNakerExternalDevicesPlugin.git
# git clone https://github.com/tophensen/sPyNNakerExternalDevicesPlugin.git
cd sPyNNakerExternalDevicesPlugin
cd neural_modelling
make -j3
cd ..
python setup.py develop
cd ..

# Get examples
git clone https://github.com/SpiNNakerManchester/PyNNExamples.git

# at this point, let's set up some convenience shortcuts
# in the virtualenv-activate script
ACTSCRIPT=$ABSDIRNAME/bin/activate

echo "" >> $ACTSCRIPT
echo "cd \$VIRTUAL_ENV/dev/spinnaker_tools" >> $ACTSCRIPT
echo "source setup" >> $ACTSCRIPT
echo "cd \$VIRTUAL_ENV/dev/sPyNNaker/neural_modelling" >> $ACTSCRIPT
echo "source setup" >> $ACTSCRIPT
echo "cd \$VIRTUAL_ENV" >> $ACTSCRIPT

# Now let's get the Visualizer running
# Compiling the visualizer would probably need a few additional headers:
sudo apt-get install libglu1-mesa-dev libgl1-mesa-dev freeglut3-dev libsqlite3-dev
git clone https://github.com/SpiNNakerManchester/Visualiser.git
cd Visualiser
cd spynnaker_external_device_lib
make -j3
# cp libspynnaker_external_device_lib.a ../../../lib/
cd examples/receiver_example
make -j3
cd ../sender_example
make -j3
cd ../send_recieve_example/
make -j3
cd ../../..
cd c_based_visualiser_framework
make -j3
cp vis ../../../bin
cd ../..

echo "Your installation is ready."
echo "Enter your new virtualenv like this:"
echo "> source $ACTSCRIPT"
echo "You will find sources in dev/"
echo "Examples in dev/PyNNexamples"
