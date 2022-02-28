#ARG IMAGE=containers.intersystems.com/intersystems/iris-ml:2021.2.0.651.0
ARG IMAGE=containers.intersystems.com/intersystems/irishealth-ml-community:2021.2.0.651.0
#ARG IMAGE=containers.intersystems.com/intersystems/iris-community:2022.1.0.114.0
FROM $IMAGE

USER ${ISC_PACKAGE_MGRUSER}
COPY  iris.script /tmp/iris.script
COPY src /tmp/src
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# run iris and initial 
RUN iris start IRIS \
    && iris session IRIS < /tmp/iris.script \
    && iris stop IRIS quietly