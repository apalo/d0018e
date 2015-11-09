#!/usr/bin/env bash

mkdir /home/vagrant/src

echo -e "deb http://archive.ubuntu.com/ubuntu precise main universe" | sudo tee /etc/apt/sources.list
echo -e "deb http://us.archive.ubuntu.com/ubuntu/ precise-updates main restricted" | sudo tee -a /etc/apt/sources.list.d/precise-updates.list

sudo apt-get update
sudo apt-get install -qy vim curl git-core

# build tools
sudo apt-get install -qy libtool autoconf automake uuid-dev build-essential g++ make tcl8.5

# bz2: required by the python version since it isn't bundled with the source-provided 2.7.8
sudo apt-get install -qy libbz2-dev


# required by bcrypt that require cffi
sudo apt-get install -qy libffi-dev

# libxml2 and libxslt
sudo apt-get install -qy libxml2 libxml2-dev libxslt-dev

# install python-software-properties (tools)
sudo apt-get install -qy python-software-properties

# install Python 2.7.8
cd /home/vagrant/src
wget http://www.python.org/ftp/python/2.7.10/Python-2.7.10.tar.xz
xz -d Python-2.7.10.tar.xz
tar -xvf Python-2.7.10.tar 
cd /home/vagrant/src/Python-2.7.10/
./configure
make
sudo make altinstall
sudo update-alternatives --install /usr/local/bin/python python /usr/local/bin/python2.7 10

# install pip
cd /home/vagrant/src
curl -O https://bootstrap.pypa.io/get-pip.py
python get-pip.py --user

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_profile

# TODO: install and configure MySQL
debconf-set-selections <<< 'mysql-server mysql-server/root_password password d00018epwd'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password d0018epwd'
apt-get update
apt-get install -y mysql-server