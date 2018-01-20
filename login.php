<?php
error_reporting(E_ALL ^ E_DEPRECATED);
include("config.php"); 

// connect to the mysql server
$link = mysql_connect($db_host, $db_user, $db_pass)
or die ("Could not connect to mysql because ".mysql_error());

// select the database
mysql_select_db($db_name)
or die ("Could not select database because ".mysql_error());

$match = "select username from $db_table where email = '".$_GET['email']."' and password = '".$_GET['password']."';"; 

$qry = mysql_query($match)
or die ("Could not match data because ".mysql_error());
$num_rows = mysql_num_rows($qry); 

if ($num_rows <= 0) { 
echo "Sorry, there is no email $email with the specified password.<br>";
echo "<a href=login.html>Try again</a>";
exit; 
} else {
$id=mysql_fetch_row($qry);
echo "Welcome $id[0], You are now logged in!<br>"; 
echo "Continue to the <a href=members.php>members</a> section.";
}
?>
