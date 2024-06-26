# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the modified squeeze_pro.py to the appropriate location
COPY modified_squeeze_pro.py /usr/local/lib/python3.12/site-packages/pandas_ta/momentum/squeeze_pro.py

# Make port 80 available to the world outside this container (if needed)
EXPOSE 80

# Run bot.py when the container launches
CMD ["python", "bot.py"]
