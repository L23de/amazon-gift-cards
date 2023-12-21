from selenium import webdriver
import os

ENV = os.environ

EDGE_USER_DATA_DIR = ENV.get("EDGE_USER_DATA_DIR")
EDGE_BINARY_LOCATION = ENV.get("EDGE_BINARY_LOCATION")

service = webdriver.EdgeService(executable_path="./msedgedriver.exe")
options = webdriver.EdgeOptions()
options.add_argument(f"user-data-dir={EDGE_USER_DATA_DIR}")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.binary_location = EDGE_BINARY_LOCATION

driver = webdriver.Edge(options=options, service=service)
