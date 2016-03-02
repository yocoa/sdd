sdd
===

Suspicious Domain Detection

Dependencies
---

```
apt-get install python-dev python-virtualenv openjdk-7-jre
apt-get install libblas-dev liblapack-dev libatlas-base-dev gfortran #scipy
apt-get install libjpeg8-dev libfreetype6-dev #pillow
apt-get install weka libsvm-java #weka
```

Installation
---

```
cd sdd
virtualenv env
source env/bin/activate
pip install -r requirements
```
