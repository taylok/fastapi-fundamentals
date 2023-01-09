To run the cors demo open the terminal and run 
```
python -m http.server 8080
```
then ```http://localhost:8080``` and open the cors_demo page

Open network monitoring developer tool and see what happens when the button is clicked
```
Not allowed by Access-Control-Allow-Origin
```
The browser allows javascript to call services only when they have the same origin as the web page that is calling them.

This web page is on port 8080, but the service runs on port 8000.  The same would be true if we were on a different 
domain, or the protocol was different. 

