
import datetime
import winsound
import time
import pygame # type: ignore



def alarm(Timing):
    try:
        alarm_time = datetime.datetime.strptime(Timing.strip(), "%I:%M %p")
    except ValueError:
        print("Sorry, I couldn't understand the time format. Please try again.")
        return

    alarm_time = alarm_time.replace(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)

    print(f"Done, alarm is set for {alarm_time.strftime('%I:%M %p')}")

    
    
    # Calculate the duration to play the alarm sound (1 minute in this case)
    duration = datetime.timedelta(minutes=1)

    while True:
        current_time = datetime.datetime.now()
        if current_time >= alarm_time:
            print("Alarm is ringing")
            #winsound.PlaySound('C:\\Users\\jaina\\Desktop\\Project\\JARVIS\\alarm.mp3', winsound.SND_LOOP)
            pygame.init()
            pygame.mixer.music.load('C:\\Users\\jaina\\Desktop\\Project\\JARVIS\\alarm.mp3')
            pygame.mixer.music.play(-1)  # Play indefinitely (-1) or specify number of repeats

            # Keep playing the sound until the duration has passed
            end_time = current_time + duration
            while datetime.datetime.now() < end_time:
                time.sleep(1)  # Adjust the sleep time as needed for smooth playback

            # After the duration, break out of the loop
            break

        # Sleep for a short duration to avoid busy-waiting
        time.sleep(1)
        


"""
        
        
        

    
    
    
    
    
    
    
    
    
    
    
    


    
while True:
        current_time = datetime.datetime.now()
        if current_time >= alarm_time:
            print("Alarm is ringing")
            winsound.PlaySound("C:\\Users\\jaina\\Desktop\\Project\\JARVIS\\alarm.mp3", winsound.SND_FILENAME | winsound.SND_ASYNC)
            break  
        
        
        
 """       
        
        
        
