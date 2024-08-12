import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.by import By

def try_pins(start, end):
    # Create a new instance of the Firefox driver
    driver = webdriver.Firefox()
    driver.get("https://www.guessthepin.com")

    # Consent handling (click 'Don't Consent')
    dontconsent = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[2]/div[2]/button[2]")
    dontconsent.click()

    # Loop through the PINs in the given range
    for pin in range(start, end):
        textbox = driver.find_element(By.XPATH, "/html/body/div[1]/form/input[1]")
        textbox.send_keys(f"{pin:04d}")

        guessbutton = driver.find_element(By.XPATH, "/html/body/div[1]/form/input[2]")
        guessbutton.click()


def main():
    # Define the number of processes you want to use
    num_processes = 4

    # Total PINs to check
    total_pins = 10000

    # Calculate the range of PINs each process will check
    pins_per_process = total_pins // num_processes

    # Create a list to hold the processes
    processes = []

    for i in range(num_processes):
        start = i * pins_per_process
        end = start + pins_per_process
        if i == num_processes - 1:
            end = total_pins

        # Create a process and assign it a range of PINs to test
        process = multiprocessing.Process(target=try_pins, args=(start, end))
        processes.append(process)

        # Start the process
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()


if __name__ == "__main__":
    main()
