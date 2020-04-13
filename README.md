wthr
--------

A simple package to get the current weather conitions, forecast, and alerts from Environemnt Canada, in English or French

## Installation

Run
```git clone https://github.com/matthewauld/wthr
cd wthr
sudo python3 setup.py install
```
Verified to work on Ubuntu


## Usage
Run ```wthr --config``` to set your preferences. You can get the region_id from the weather page URL. For example, https://weather.gc.ca/city/pages/on-118_metric_e.html is the forecast page for Ottawa, and the region_id is 118. Will create /home/$USER/.local/share/wthr directory if it does not already exist.


```-c, -f, -a``` get the current weather, forecast, and alerts respectively. Omitting them all will print out all three.

```
Get weather information from Environment Canada

optional arguments:
  -h, --help            show this help message and exit
  -p {on,ab,mb,sk,bc,qc,nb,ns,pe,nl,nt,yt,nu}, --province {on,ab,mb,sk,bc,qc,nb,ns,pe,nl,nt,yt,nu}
                        selected province
  -fr, --francais       print in french
  -r REGION_ID, --region_id REGION_ID
                        selected region
  -c, --current         print current conditions
  -f, --forecast        print forecast
  -a, --alerts          print alerts
  -d {m,t,w,th,f,s,su}, --day {m,t,w,th,f,s,su}
  --config              configure default values
```

## Known Bugs
- day of the week selector does not work in french.
- config does not verify your id is correct

## Future work
- remove the need to get the ID manually
