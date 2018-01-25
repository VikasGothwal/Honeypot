Cross-site scripting (XSS) is a client-side injection attack in which an attacker can execute malicious scripts into a legitimate website.

In order to run malicious javascript code in a victim's browser, an attacker must first find a way to inject a payload into a web page that the victim visits.

Suppose there is a input field which is vulnerable to XSS attack then an attacker can inject his code into it. For example : 
```
<script>alert("You've been hacked")</script>
```
This will result in displaying an alert box that says "You've been hacked".

Now if an attacker somehow use this in URL and hide the URL using any URL shortner and then inject any script and give that link to the victim. Then victim browser will automatically run that malicious script.

There are three types of XSS :

#### Reflected XSS
The **non-persistent** (or reflected) XSS is the most basic XSS.
The attacker's payload/script has to be part of the request which is sent to the web server and reflected back in such a way that the HTTP response includes the payload from the HTTP request.

#### Stored XSS
The **persistent** (or stored) XSS involves an attacker injecting a script that is permanently stored on the target application. For example - a malicious script stored by an attacker in a comment field on a blog or in a forum post.
When a victim navigates to the affected web page in a browser, the XSS payload will be served as part of the web page.

#### DOM-based XSS
DOM-based XSS is an advanced type of XSS which is made possible when the web application's client side scripts write user provided data to the Document Object Model(DOM).

