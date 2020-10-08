# Recommender
![image info](./homepage.png)

## Environment setup
1. Build docker image:  
`make build`
This command will build a docker image named 'recommender' which all the specified dependencies.

### Usage
For convenience we use Makefile with common commands but you can start and interact with docker containers manually if you wish.  

1. Execute the following command to start the container.  
`make dev`  
It will start a docker container with default parameters. Your current working directory will be mounted to a '/project' directory inside the container. Additionally you can specify another mounting path to a volume containing required datasets etc.

2. You can specify the following parameters:  
`PORT` - default is 8888  
`GPU` - index of the GPU you want to make available to docker container, the default is 0. Doesn't apply to the `dev_cpu` command.  
`NAME` - name of the container, the default is <YOUR_USERNAME>_<IMAGE_NAME>.  
`DATA_PATH` - absolute path to the directory where the data is stored on the host machine, the default is unset.

For example you can run:  
`make dev PORT=9000 NAME=recommender DATA_PATH=/home`

### Jupyter lab
From within container run:  
`make lab`
Jupyter lab can be useful when developing on remote machines.
