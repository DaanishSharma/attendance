from flask import Flask, render_template, request, redirect, url_for
from python_arptable import get_arp_table
import csv
import socket
import datetime
import socket
import pyqrcode
from pyqrcode import QRCode
import webbrowser

  

hostname=socket.gethostname()
host_ip=socket.gethostbyname(hostname)
app = Flask(__name__,static_url_path='/static')


presant = []
presant2= []
macs = set()
@app.route('/', methods=['GET', 'POST']) 
def login():
    arp_table = get_arp_table()
    client_mac =  "None"
    ip = request.remote_addr
    for entry in arp_table:
            if entry['IP address'] == ip:
                client_mac =  entry['HW address']
    if client_mac in macs:
        return render_template('./signup.html', msg = "Attendence Marked!")
    elif request.method == 'POST'and 'user' in request.form and 'rollno' in request.form:
        user = request.form['user']
        rollno = request.form['rollno']
        presant2.append([user,rollno,client_mac])
        presant.append([user,rollno,client_mac])
        macs.add(client_mac)
        msg = f'{user} {rollno} is presant'
        return render_template('./signup.html', msg = msg)
    else:
        return render_template('./index.html', msg = "")

@app.route('/end', methods=['GET'])
def end(): 
    if host_ip==request.remote_addr:
        if(len(presant)==0):
            return redirect("./admin")
        x = str(datetime.datetime.now())
        with open(f"attendance_{x}.csv", mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i in presant:
                writer.writerow(i)
        presant.clear()
        macs.clear()    
        return redirect("./admin")
    return "NOT ALLOWED"

@app.route('/admin', methods=['GET'])
def admin(): 
    if host_ip==request.remote_addr:
        return render_template('./admin.html', msg = presant)
    return "NOT ALLOWED"


if __name__ == '__main__':
    hostname=socket.gethostname()
    print(hostname)
    host_ip=socket.gethostbyname(hostname)
    s1=f"http://{host_ip}:5000/admin" 
    s=f"http://{host_ip}:5000/" 
    url = pyqrcode.create(s)  
    url.svg("./static/images/myqr.svg", scale = 8)
    webbrowser.open(s1)   
    app.run(host='0.0.0.0')