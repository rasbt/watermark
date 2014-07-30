watermark
=========

An IPython magic extension for printing date and time stamps, version numbers, and hardware information

<br>
#### Contents

- [Examples](#examples)
- [Installing watermark](#installing-watermark)
- [Usage](#usage)


<br>
<br>

## Examples
[[back to contents](#contents)]

![](./images/ex1.png)

![](./images/ex2.png)

![](./images/ex3.png)

For more examples can be found in this [IPython notebook](http://nbviewer.ipython.org/github/rasbt/watermark/blob/master/docs/watermark.ipynb).

<br>
<br>

## Installing watermark
[[back to contents](#contents)]

Simply execute the the following code snippet in an IPython shell or IPython notebook cell.

	%install_ext https://raw.githubusercontent.com/rasbt/watermark/master/watermark.py

<br>
<br>	
	
## Usage
[[back to contents](#contents)]

After successful installation, the `watermark` magic extension can be loaded via:

	%load_ext watermark

<br>
<br>	
	
To get an overview of all available commands, type:

	%watermark?
	
<br>



	%watermark [-a AUTHOR] [-d] [-n] [-t] [-z] [-u] [-c CUSTOM_TIME] [-v]
	                 [-p PACKAGES] [-h] [-m] [-g]


	IPython magic function to print date/time stamps 
	and various system information.

	watermark version 1.1.0

	optional arguments:
	  -a AUTHOR, --author AUTHOR
	                        prints author name
	  -d, --date            prints current date
	  -n, --datename        prints date with abbrv. day and month names
	  -t, --time            prints current time
	  -z, --timezone        appends the local time zone
	  -u, --updated         appends a string "Last updated: "
	  -c CUSTOM_TIME, --custom_time CUSTOM_TIME
	                        prints a valid strftime() string
	  -v, --python          prints Python and IPython version
	  -p PACKAGES, --packages PACKAGES
	                        prints versions of specified Python modules and
	                        packages
	  -h, --hostname        prints the host name
	  -m, --machine         prints system and machine info
	  -g, --githash         prints current Git commit hash
	  
	 