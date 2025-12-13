



<!DOCTYPE html>
<html lang="de">
  <head>
	    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="enocoo | Anmeldung">
    <meta name="author" content="">
	    <!--link rel="shortcut icon" href="../images/favicon.ico"-->
	<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
	<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
	<link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
	<link rel="manifest" href="site.webmanifest.json">
	<link rel="mask-icon" href="safari-pinned-tab.svg" color="#5bbad5">
	<meta name="msapplication-TileColor" content="#2d89ef">
	<meta name="theme-color" content="#ffffff">

    <title>enocoo | Anmeldung</title>

    <!-- enocoo custom styles. Bootstrap core CSS wird in diesem als erstes Nachgeladen -->
    <link href="css/signInStyle.css" rel="stylesheet">

    <!-- Just for debugging purposes. Don't actually copy this line! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

	<script src="js/jquery-2.1.0.js" type="text/javascript"></script>

  </head>

  <body>
	    <div class="container">

      <form class="form-signin" role="form" method="post" action="/signinForm.php?mode=ok" accept-charset="UTF-8">
		<a id="logo"><img align="center" src="images/ENOCOO_LOGO_300x111.png" alt="enocoo Logo" /></a>
		
		<!-- Bei nur einem Projekt nichts anzeigen, sonst Auswahlbox -->
        
		<!-- Bei nur einer Sprache nichts anzeigen, sonst Auswahlbox -->
		
		 <!-- bei nur 1 Projekt/Sprache keine Auswahlbox anzeigen und die einzige ID in jeweiliges Übergabefeld schreiben. value statt placeholder! -->
		<input type="text" class="form-control" id="idProject" name="idProject" style="display:none;"  value="1">
		<input type="text" class="form-control" id="idLanguage" name="idLanguage" style="display:none;"  value="1">
        <h2 class="form-signin-heading">Ihre Anmeldung:</h2>
        <input type="user" class="form-control" placeholder="Benutzername" name="user" required autofocus >
        <input type="password" class="form-control" placeholder="Passwort" name="passwort" required >
			<!-- <label class="checkbox">
          <input type="checkbox" value="remember-me"> Remember me
        </label> -->
        <button class="btn btn-lg btn-primary btn-block" type="submit" >Anmelden</button>

		<!-- PW-Änderung im Maintenancemode nicht möglich -->
		</br><a href="php/pwLost.php">Passwort vergessen?</a>
		<div align='center'><p></p></div> <div align='center'><p><strong>Ihre Anmeldedaten waren nicht korrekt. Bitte melden Sie sich erneut an.</strong></p></div>
		</form>

    </div> <!-- /container -->
	
	<script type="text/javascript">
		var chosenProject = "1";
		var chosenLanguage = "1";

		function dropDownActionProj(menuEntry) {
			chosenProject = menuEntry.id;
			// document.getElementById("resultColorValue").innerHTML = document.getElementById("Color").value;
			$('#idProject').val(menuEntry.id);
			$('#project').html($(menuEntry).text() + ' <span class="caret"></span>');
		}

		function dropDownActionLang(menuEntry) {
			chosenLanguage = menuEntry.id;
			$('#idLanguage').val(menuEntry.id);
			$('#language').html($(menuEntry).text() + ' <span class="caret"></span>');
		}

		// assign all dropdown-entries a callback-function. Without event_ref.preventDefault(); the page scrolls to the top after the change! (a often suggested "return false;" instead of it does not work.
		$('.pdmProj').each(function( index ) {
			$( this ).click(function(event_ref){ dropDownActionProj(this); event_ref.preventDefault();  });
		});
		$('.pdmLang').each(function( index ) {
			$( this ).click(function(event_ref){ dropDownActionLang(this); event_ref.preventDefault();  });
		});
	</script>


	<!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
	<script src="js/jquery-2.1.0.js" type="text/javascript"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="components/bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
	</body>
</html>
