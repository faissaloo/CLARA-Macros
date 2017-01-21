CLARA Macros
===
C Like Anamorphic Rudimentary Accretive Macros, or CLARA Macros 
for short are a text macro system aimed at creating HTML 
webpages. They are meant to be rudimentary for ease of 
implementation and to prevent abuse, as such they are typeless, 
can not be nested and are space insensitive (in definitions, if the parameter is found anywhere it will be replaced with 
the argument, even if it has no spaces, in macros any occurance of the macro is replaced, regardless of the spacing around it).  
The macro expansion cycle is as such, each includes and macros 
are processed until there are no more left:  
includes->definitions->macros  

#Including another file  
The following inserts the contents of another file at the 
position.  
```
$include[beethovens5th.html]
```

#Defining a macro  
```
$define policeBox[textStyle]<b style="textStyle">wibbly wobbly timey wimey</b>|
```
You can also define macros that use macros
```
$define bzz[](__)|
$define screwdriver[]-==$bzz[]|
```
#Using a macro
```
$policeBox[color:blue;]
```
