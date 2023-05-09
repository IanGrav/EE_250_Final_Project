import paho.mqtt.client as mqtt
from datetime import datetime
import socket
import time
import pandas as pd
import plotly.express as px


# create lists to hold the temperature and humidity measurements over time
temperature_over_time = []
humidity_over_time = []
# also create variables hholding the default target temperature, target humidity,
# and interval of measuurements (to be overwritten later by the user)
target_hum = "50.0"
target_temp = "23.0"
interval = "1.0"

# define default message callback (not used in this project)
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

# define custom callback for csv message containing temperature and 
# humidity published by the rpi
def on_message_from_temperature_humidity(client, userdata, message):
    # receive the message and decode it to a utf-8 string
    temp_hum = message.payload.decode()
    # create a list from the two values before and after the comma
    thList = temp_hum.split(",")
    # convert those values to floats
    temp_float = float(thList[0])
    hum_float = float(thList[1])
    # use global variables to hold the most current temperature and humidity
    # so that they can be accessed in the main while loop
    global temp
    global hum
    temp = temp_float
    hum = hum_float
    # apend the newest measurements to the arrays holding them indexed over time
    temperature_over_time.append(temp_float)
    humidity_over_time.append(hum_float)

# define function to be executed when the client receives connection 
# acknowledgement packet from the server
def on_connect(client, userdata, flags, rc):
    """Once our client has successfully connected, it makes sense to subscribe to
    all the topics of interest. Also, subscribing in on_connect() means that, 
    if we lose the connection and the library reconnects for us, this callback
    will be called again thus renewing the subscriptions"""
    # inform the user that the connection to the server has been made
    print("Connected to server (i.e., broker) with result code " + str(rc) + "\n")
    # subscribe to the temperature and humidity being posted by the rpi
    client.subscribe("temperature_humidity")

# create a client object
client = mqtt.Client()
#attach the on_connect() callback function defined above to the mqtt client
client.on_connect = on_connect
#attach a default callback which we defined above for incoming mqtt messages
client.on_message = on_message
# register a custom callback for the temperature and humidity csv
client.message_callback_add("temperature_humidity", on_message_from_temperature_humidity)
# get the MQTT server host IP adress from the user
# (I used Mosquitto on my computer running Windows as a broker)
host_ip = input("Enter the IP adress of the MQTT broker you will be using: ")
port_num = int(input("Enter the port number you will be connecting to: "))
# connect to the entered host and port number, set keepalive to 60 to keep
# the connection up by sending a message every 60 seconds
client.connect(host=host_ip, port=port_num, keepalive=60)
# start client loop so paho-mqtt will open new thread to handle MQTT messages
client.loop_start()
time.sleep(1)

# list of options for user entry, to be compared against to ensure
# a correct entry was made
options = ["c", "h", "t", "m", "d", "g", "r"]
# list of optiions for time units the user can chhose to make their graph with
# to be compared against to ensure they choose one of these options
time_options = ["s", "m", "h"]

while True:
    try:
        # display to the user their options
        print("Greenhouse Monitor Menu")
        print("Options:")
        print("   c) see most current temperature and humidity conditions")
        print("   h) update the target humidity of the greenhouse")
        print("   t) update the target temperature of the greenhouse")
        print("   m) update the measurement intevals of the sensor (will reset measurement records)")
        print("   d) display a dataframe of the conditions measured so far")
        print("   g) create graph of conditions since start in current directory")
        print("   r) reset current condtion records")
        print("   (Ctrl+C to quit)")
        print("Make an entry for one of the above functions (enter a letter)")

        # take the user's entry for their option of choice
        entry = input("Entry: ").strip().lower()
        # esnure ther entry was a valid one (loop until it's valid)
        while not entry in options:
            print("That is not a valid entry. Please enter again.")
            entry = entry = input("Entry: ").strip().lower()
        print()

        # if the user enters a "c", display them the most recent recorded conditions
        if entry == "c":
            try:
                print("Temperature:", str(temp), "C")
                print("Humidity:", str(hum) + "%")
                if temp >= float(target_temp):
                    print("The temperature is at or above the target temperature of", target_temp, "C.")
                else:
                    print("The temperature is below the target temperature of", target_temp, "C.")
                if hum >= float(target_hum):
                    print("The humidity is at or above the target humidity of", target_hum + "%.")
                else:
                    print("The humidity is below the target humidity of", target_hum + "%.")
                print("The current interval of measurement is", interval, "seconds")
            # if the rpi is still booting up, it will not have published the temperature
            # and humidity yet, so the temp and hum variables will not be defined.
            # inform the user they need to wait and show them all other avaialbe info.
            except NameError:
                print("The temperature and humidity have not been recorded yet. Please wait and try again.")
                print("The current target temperature is", target_temp, "C.")
                print("The current target humidity is", target_hum + "%.")
                print("The current interval of measurement is", interval, "seconds")

        # if the user enters an "h", allow them to update the target humidity
        if entry == "h":
            # take their input and loop until it is a valid double
            print("Enter a target humidity percentage (must be a double):")
            target_hum = input("Entry: ").strip()
            while not (target_hum.replace(".", "", 1).isdigit()):
                print("That is not a valid entry, please enter again.")
                target_hum = input("Entry:")
            # publish their entry so the rpi receives the update
            client.publish("target_humidity", f"{target_hum}")
            # inform the user their update has been made
            print("The target humdity has been updated to", target_hum + "%.")

        # if the user enters a "t", allow them to update the target temperature
        if entry == "t":
            # take their input and loop until it is a valid double
            print("Enter a target temperature in Celcius (must be a double):")
            target_temp = input("Entry: ").strip()
            while not (target_temp.replace(".", "", 1).isdigit()):
                print("That is not a valid entry, please enter again.")
                target_temp = input("Entry: ")
            # publish their entry under the correct topic so the rpi receives the update
            client.publish("target_temperature", f"{target_temp}")
            # inform the user their update has been made
            print("The target temperature has been updated to", target_temp, "C.")

        # if the user enters an "m", allow them to update the measurement interval
        if entry == "m":
            # take their input and loop until it is a valid double
            print("Enter a interval in seconds (must be a double):")
            interval = input("Entry: ").strip()
            while not (interval.replace(".", "", 1).isdigit()):
                print("That is not a valid entry, please enter again.")
                interval = input("Entry:")
            # publish their entry under the correct topic so the rpi receives the update
            client.publish("interval", f"{interval}")
            # inform the user their update has been made
            print("The measurement interval has been updated to", interval, "seconds.")
            # clear all past records because the timings of the measuremets 
            # will now be incorrect
            temperature_over_time.clear()
            humidity_over_time.clear()
            # these should be updated every interval, so this should pose no issue,
            # but handling the case where the lists updated between clears
            if not(len(temperature_over_time) == len(humidity_over_time)):
                temperature_over_time.clear()
                humidity_over_time.clear()
            # inform the user the records have been cleared
            print("The condition records have been reset for accurate graphing purposes")

        # if the user enters an "d", display a dataframe holding the information from
        # the temperature_over_time and humidity_over_time arrays at the current moment
        if entry == "d":
            # take the measurement arrays by value at the moment the user enters "d"
            temp_c_arr = temperature_over_time[:]
            humidity_arr = humidity_over_time[:]
            # create an array that has the time elapsed at each index of the measurement arrays
            # and an array that has the temperature measurements in fahrenheit
            temp_arr_size = len(temp_c_arr)
            time_elapsed_arr = []
            temp_f_arr = []
            interval_float = float(interval)
            for i in range(0, temp_arr_size):
                time_elapsed_arr.append(i * interval_float)
            for x in range(0, temp_arr_size):
                temp_f_arr.append(temp_c_arr[x] * 1.8 + 32)
            # put all the above arrays in a pnadas dataframe
            df_display = pd.DataFrame()
            df_display["Temperature (C)"] = temp_c_arr
            df_display["Temperature (F)"] = temp_f_arr
            df_display["Humidity (%)"] = humidity_arr
            df_display["Time Elapsed (s)"] = time_elapsed_arr
            # set the index to the time elapsed at each measurement
            df_display.set_index("Time Elapsed (s)", inplace=True)
            # display the dataframe to the user
            print(df_display.to_string())
            # free up memory
            temp_c_arr.clear()
            humidity_arr.clear()
            time_elapsed_arr.clear()
            temp_f_arr.clear()
            del df_display

        # if the user enters a "g" create a graph of the conditions over time
        if entry == "g":
            # ask the user if they want their graph to be by seconds, minutes, or hours
            # loop unitl they choose a valid option
            time_unit = input("Choose a time unit for your graph").strip().lower()
            while not (time_unit in time_options):
                time_unit = input("Choose a time unit for your graph").strip().lower()
            # take the measurement arrays by value at the moment the user enters "g"
            temp_c_snapshot = temperature_over_time[:]
            humidity_snapshot = humidity_over_time[:]
            # create array that contains the temperature in fahrenheit
            # and an array that holds the time elapsed at each measurement
            temp_list_size = len(temp_c_snapshot)
            temp_f_snapshot = []
            time_elapsed_snapshot = []
            interval_float = float(interval)
            # convert each measurement to fahrenheit and append it in the parrallel
            # fahrenheit array
            for i in range(0, temp_list_size):
                temp_f_snapshot.append(temp_c_snapshot[i] * 1.8 + 32)
            # create the time array with the decided units
            for x in range(0, temp_list_size):
                if time_unit == "s":
                    time_elapsed_snapshot.append(x * interval_float)
                if time_unit == "m":
                    time_elapsed_snapshot.append(x * interval_float / 60.0)
                if time_unit == "h":
                    time_elapsed_snapshot.append(x * interval_float / 3600.0)
            # create the correct x-axis label based on the decided time units
            if time_unit == "s":
                x_label = "Time Elapsed (seconds)"
            if time_unit == "m":
                x_label = "Time Elapsed (minutes)"
            if time_unit == "h":
                x_label = "Time Elapsed (hours)"
            # create a dataframe with all of the above arrays
            df_graph = pd.DataFrame()
            df_graph["Temperature (C)"] = temp_c_snapshot
            df_graph["Temperature (F)"] = temp_f_snapshot
            df_graph["Humidity (%)"] = humidity_snapshot
            df_graph[x_label] = time_elapsed_snapshot
            # create a bar graph out of the dataframe
            # with temperature in celcius, temperature in Fahrenheit, and humidity percentage
            # graphed on the y axis and time elapsed on the x axis
            fig = px.line(
                df_graph, 
                x= x_label,
                y = ["Temperature (C)", "Temperature (F)", "Humidity (%)"],
                title = "Temperature and Humidity Over Time",
                template = "plotly_white",
            )
            # save the bar graph to the current working directory
            fig.write_image("conditions_graph.png")
            # open a link which will contain an interactive graph for the user
            fig.show()
            # free up space
            temp_c_snapshot.clear()
            temp_f_snapshot.clear()
            humidity_snapshot.clear()
            time_elapsed_snapshot.clear()
            del df_graph
            del fig
            
        # if the user enters an "r", clear the temperature_over_time and humidity_over_time
        # arrays in order to reset the point at which they begin recording to now
        if entry == "r":
            temperature_over_time.clear()
            humidity_over_time.clear()
            # these should be updated every interval, so this should pose no issue,
            # but handling the case where the lists updated between clears
            if not(len(temperature_over_time) == len(humidity_over_time)):
                temperature_over_time.clear()
                humidity_over_time.clear()

        # space out each options menu display
        print()

    # when the user hits Ctrl+C, print goodbye and break the loop, quitting the program
    except KeyboardInterrupt:
        print("\n\nGoodbye!\n")
        break
