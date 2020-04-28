# Installing OpenRouteService Backend

This document describes the process of installing, and running, OpenRouteService (ORS) locally.  These instructions were tested on Ubuntu 18.04.

--- 

## 1.  Install Docker

These instructions come from https://docs.docker.com/engine/install/ubuntu/.

```
sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Now, verify that the installation worked:
```
sudo docker run world-hello
```

Next, add the current user to the docker group (so you don't have to use "sudo" every time).  See docs://https.docker.com/engine/install/linux-postinstall/ for more info.

- Create the docker group:
    ```
    sudo groupadd docker
    ```

- Add the user to the docker group:
    ```
    sudo usermod -aG docker $USER
    ```

- Activate the group change:
    ```
    newgrp docker 
    ```

- Verify that it worked:
    ```
    docker run hello-world
    ```

---

## 2.  Install ORS

- Install docker-compose:
    ```
    sudo apt install docker-compose
    ```

- Install `git` and `openjdk11`:
    ```
    sudo apt-get install git
    sudo apt-get install openjdk-11-jdk
    ```

- Clone the ORS repo.  I do this in my `Projects` directory:
    ```
    cd ~/Projects
    git clone https://github.com/GIScience/openrouteservice.git
    ```

- Test out the default installation:
    - Start the service:
        ```
        cd openrouteservice/docker
        docker-compose up -d
        ```
    - Check the service status by visiting http://localhost:8080/ors/health.  You'll first get a message that says "not ready".  When ORS has loaded, the message will say "ready".

    - You can see the running services at http://localhost:8080/ors/status.

    - Using the default dataset, you can issue a query: http://localhost:8080/ors/routes?profile=foot-walking&coordinates=8.676581,49.418204|8.692803,49.409465


## Customizing the Server

These are the steps that I followed, partially as a result of some trial-and-error.  I am quite certain that there are better ways to do this, but these steps appear to work.  More information can be found at https://github.com/GIScience/openrouteservice/tree/master/docker.

1. Download a `.pbf` file of your region of interest from http://download.geofabrik.de.  I 
downloaded http://download.geofabrik.de/north-america/us/new-york-latest.osm.pbf (208 MB).
    - Save the file in the `openrouteservice/docker/data/` directory.

2. Edit `docker-compose.yml` in the `openrouteservice/docker/` directory to make the following changes:
    - Change the port to `8081:8080`.  Cesium uses port 8080, so we need to use a different port; 8081 seems to work well.  Note that Jupyter notebooks default to port 9090.
    - In the "build" section, change the `OSM_FILE:` to your desired `.pbf` file.  I downloaded data from New York state (see instructions above). My resulting line in the `.yml` file became:  
        ```
        OSM_FILE: ./docker/data/new-york-latest.osm.pbf	
        ``` 
        
    - In the "volumes" section, remap the data to the appropriate `.pbf` file.  My resulting line in the `.yml` file became:  
        ```
        - ./data/new-york-latest.osm.pbf:/ors-core/data/osm_file.pbf	
        ```
        
    - I found that I ran out of memory using the default Java "environment" values.  Here's what I ended up using (on a laptop with only 8GB of RAM):
        ```
        - JAVA_OPTS="-Djava.awt.headless=true -server -XX:TargetSurvivorRatio=75 -XX:SurvivorRatio=64 -XX:MaxTenuringThreshold=3 -XX:+UseConcMarkSweepGC -XX:+UseParNewGC -XX:ParallelGCThreads=4 -Xms4g -Xmx4g"
        ```

3. Empty the `openrouteservice/docker/graphs/` directory.  This will force ORS to rebuild with the new data you downloaded.  NOTE: You may need to use `sudo`.
    ```
    cd ~/Projects/openrouteservice/docker
    sudo rm -rf graphs/*
    ```

---

## Running your Customized Server

1. Change directories:
    ```
    cd ~/Projects/openrouteservice/docker
    ```

2. Start the server **for the first time**.  There are a couple of options.  When running the first time with a new `.pbf` file, I'm not entirely sure which option is best.
    1. Use a command line flag to force re-building with new map data:
        ```
        docker-compose up -d --build
    2. Edit the `docker-compose.yml` file to set `BUILD_GRAPHS=True`, and then simply run `docker-compose up -d` from the command line.
    3. Combine steps 1 and 2.

3. Keep an eye on the status here:
    - http://localhost:8081/ors/health
    - http://localhost:8081/ors/status

4. Stop/shutdown the server when you're done:
    ```  
    docker-compose down
    ```

5. Re-start the server (assuming you haven't changed the `.pbf` file:
    ```
    docker-compose up -d
    ```
---

## Test Links:
Here are some queries I tried with New York data:

- Snapping a location to the nearest road:
    - http://localhost:8081/ors/directions?profile=driving-car&geometry_format=geojson&coordinates=-78,42|-78,42&elevation=true

- Driving directions:
    - http://localhost:8081/ors/directions?profile=driving-car&coordinates=-78.001,42|-78,42&elevation=true&geometry_format=geojson&extra_info=waytype|tollways|surface|steepness|waycategory&radiuses=-1|-1&units=m&instructions=true

- Isochrones:
    - http://localhost:8081/ors/isochrones?profile=driving-car&range=20&locations=-78.001,42&location_type=destination&attributes=area|reachfactor&interval=10&smoothing=20&area_units=m&units=m

- Matrix:
    - http://localhost:8081/ors/matrix?profile=driving-car&locations=-78,42|-79,42 

---

## Troubleshooting:
The following links may be helpful:
- https://ask.openrouteservice.org/
- https://ask.openrouteservice.org/t/source-point-s-0-1-2-3-4-n-out-of-bounds/581
- https://gist.github.com/nilsnolde/194631829c9281997c30d011cf2ef6b2
- https://ask.openrouteservice.org/t/getting-started-via-docker-toolbox/1596



