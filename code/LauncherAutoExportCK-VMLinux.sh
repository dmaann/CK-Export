#!/bin/bash
/opt/anaconda3/bin/python /run/user/1001/gvfs/smb-share:server=sd00d35,share=dosimetrie/CyberKnife/06_CK-Export/code/run.py >> logs/exporCK.log 2>&1
#/opt/anaconda3/bin/python /run/user/1001/gvfs/smb-share:server=sd00d35,share=dosimetrie/CyberKnife/06_CK-Export/code/run.py >> /run/user/1001/gvfs/smb-share:server=sd00d35,share=dosimetrie/CyberKnife/06_CK-Export/code/logs/exporCK.log 2>&1

#/opt/anaconda3/bin/python /run/user/1001/gvfs/smb-share:server=sd00d35,share=dosimetrie/CyberKnife/06_CK-Export/code/run.py >> /run/user/1001/gvfs/smb-share:server=sd00d35,share=dosimetrie/CyberKnife/06_CK-Export/code/logs/exporCK.log 2>&1

#/home/daniel/anaconda3/bin/python /home/daniel/Documents/CK-Export/code/run.py >> logs/exporCK.log 2>&1
