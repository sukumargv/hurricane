# Author: Venkata Sukumar Gurugubelli
# Purpose : Adacamic Project
# Description: Extract script from the html page and store information of the data on a disk
# Phase: Raw Data Extraction phase.
# Start Date: September 25th, 2016
# Start Time: 2:27 PM
# Location: New Bedford, MA

# Source URL: http://bcferries.applocation.net/routemaps/route4.html
# Defualt observations:
# 1. The page on the website automatically refreshers for every 30 seconds.
# 2. The size of route0 map is 500px x 500px
# 3. 

# Objective: To extract the script informaiton associated with the document.

# check the loaded packages
# (.packages())

# Required packages for scraping data
# x <- c("XML", "RCurl", "stringr")

# Install above packages
# install.packages(x)

# Load packages
# lapply(x, require, character.only = TRUE)

#setwd("/Users/sukumargv/dropbox/Academia/3rd Semester/Koop/hurricane/hurricane")

route_url <- "http://bcferries.applocation.net/routemaps/route4.html"

# From XML package
# route_page_source <- readLines(route_url, encoding = "UTF-8")

# Parsed Page
# route_parsed <- htmlParse(route_page_source, encoding = "UTF-8")

# Script node which contains information about the location of the marker on the map in reference with pixel grid.
# script_node <- route_parsed ["//script"][[1]]

# Image of the route for each grab. For comparing the data with the data from marine traffic data.
# image_node <- route_parsed ["//img"][[1]]


# links <- getHTMLLinks(route_url)

# making the image name universal platform compatible


image_download_time <- as.POSIXct(Sys.time(), format = "%m-%d-%Y %H:%M:%S")
print("System Time: ")
image_download_time

attr(image_download_time, "tzone") <- "UTC"
print("Converted time in UTC: ")
image_download_time

image_download_time <-  gsub(":", "-", image_download_time)

route_image_url <- gsub("html", "jpg", route_url)

# Download to images folder with EDT Time stamp as the title.
download.file(route_image_url, destfile = paste("images/",image_download_time, ".jpg", sep = ""))
