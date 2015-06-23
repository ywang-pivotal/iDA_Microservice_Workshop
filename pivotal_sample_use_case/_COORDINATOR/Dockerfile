#Set the base image to webapp
FROM webapp

#File Author
MAINTAINER Jack Ong <jackong2013@gmail.com>

#Copy the application files
Add . /webapp/coordinator

#Change the working directory
WORKDIR /webapp/coordinator

#Expose the port for this application
EXPOSE 2000

#Run the application
CMD ["python", "web_coordinator.py"]