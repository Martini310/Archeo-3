# Archeo3
The third version of my Archeo App. This time in Django!

## 📋 Content of project
* [General info](#general-info)
* [Tech stack](#tech-stack)
* [Installation](#installation)
* [Application view](#application-view)
* [Functionalities](#functionalities)
* [Inspiration & Sources](#inspiration--sources)
* [Contact](#contact)

# 🔍 General info

Archeo app is a comprehensive solution for managing, control and monitoring different registers, list etc.
Beyond borrowing files from office archive, app will let for creating handover lists, transfer files between users and will support notifications.
# 🛠️ Tech stack

<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green">
<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
<img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white">
<img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white">
<br/>
<br/>

# 🏗️ Installation

### Docker
To run container with some sample data just type this command:
```
docker run -p 8000:8000 martin310/archeo3v1.0.0
```

# 💻 Application view

<img src="https://github.com/Martini310/Archeo-3/assets/108935246/721bcc82-615e-43e2-bf4b-585772aadc22" width="40%" height="40%">

<img src="https://github.com/Martini310/Archeo-3/assets/108935246/baef18e4-f351-4150-8e59-fc14c5ced668" width="40%" height="40%">



# 🔧  Functionalities

## 🚗 Vehicle
In this module You can manage and control the vehicle files that are taken or return from office archive.
1. Firtst create new order. Add all registration numbers you need and eventually comments to them and send it. In standard there are 10 rows, you can add them if need bigger order.
2. System admin can now print this order and pass it to someone to find the files in achive.
3. Whether they find it or not admin can accept order and give files or reject it. He can do it with particular files instead of all order too.
4. After return admin update record by provide registration number and returner.
5. Every user can check status of all files in any moment. It is possible to filter results by registration number, status or responsible person
6. Additionally user can check his orders and files and if needed transfer them to another user (Another user have to accept new file, if reject - file will go back)
7. Admin can add files directly without creating new order (in case of urgent need), or edit any case (eg. mistakes)
8. Orders to do can be filtered by status. They also have a files to do/all summary. In case when file will be taken and never return, admin can mark it while accepting the order

## Driver
This module is very similar to the Vehicle with some minor differences which I will describe here
1. Searching is based on name, surname and PESEL number.
2. Return is based on the PESEL number, and if the driver does not have a PESEL number, then according to the name, surname and date of birth.

## 📒 Transfer List
In this module users can create lists of drivers transfered to the archive.
This is pretty simple
1. User create a list of drivers with all needed informations.
2. After acceptance user can print it.
3. All user can view all lists, filter them and print in any moment. Only admins can edit them.
4. Validation - if driver is ordered or taken in Driver module then it can not be transfered in this list.

# ❓ Inspiration & Sources
Like in previous version of this app, inspiration is the excessive bureaucracy and my faith that this all can be much simpler and faster.

# 📱 Contact
If you have any questions or ideas for development feel free to contact me via email:</br>
📨 [martin.brzezinski@wp.eu](mailto:maritn.brzezinski@wp.eu)

