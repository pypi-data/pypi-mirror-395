
<!DOCTYPE html>
<html lang="de">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="enocoo | Eigenverbrauch">
    <meta name="author" content="">
    <!--link rel="shortcut icon" href="../images/favicon.ico"-->
	<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
	<link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png">
	<link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png">
	<link rel="manifest" href="../site.webmanifest.json">
	<link rel="mask-icon" href="../safari-pinned-tab.svg" color="#5bbad5">
	<meta name="msapplication-TileColor" content="#2d89ef">
	<meta name="theme-color" content="#ffffff">

    <title>enocoo | Eigenverbrauch</title>

    <!-- enocoo custom styles. Bootstrap core CSS wird in diesem als erstes Nachgeladen -->
    <link rel="stylesheet" href="../css/emsStyle.css">
    <link rel="stylesheet" href="../components/bootstrap/css/bootstrap-theme.min.css"> <!-- Bootstrap theme -->
	<link rel="stylesheet" href="../components/moment-develop/css/bootstrap-datetimepicker.min.css" /> <!-- Bootstrap datetimepicker theme -->
	<!-- 	<link rel="stylesheet" href="../components/font-awesome-4.7.0/css/font-awesome.min.css"> -->
	<link rel="stylesheet" href="../components/fontawesome-free-6.1.2-web/css/all.css">
	<!-- support v4 icon references/syntax -->
	<link rel="stylesheet" href="../components/fontawesome-free-6.1.2-web/css/v4-shims.css">

    <!-- Just for debugging purposes. Don't actually copy this line! -->
    <!--[if lt IE 9]><script src="../../assets/js/ie8-responsive-file-warning.js"></script><![endif]-->

    <!-- HTML5 shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
      <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

	<!-- Sind moment.min.js / bootstrap-datetimepicker.min.js am Skriptende, funktioniert der Kalender-Button nicht... -->
	<script src="../js/jquery-2.1.0.js" type="text/javascript"></script>
    <script src="../components/bootstrap/js/bootstrap.min.js" type="text/javascript"></script>
	<script src="../components/moment-develop/min/moment.min.js" type="text/javascript"></script>
	<script src="../components/moment-develop/lang/de.js" type="text/javascript"></script>
	<script src="../components/bootstrap-datetimepicker-master/build/js/bootstrap-datetimepicker.min.js" type="text/javascript"></script>
	<script src="../components/bootstrap-datetimepicker-master/src/js/locales/bootstrap-datetimepicker.de.js" type="text/javascript"></script>	<!-- Für deutsche Sprache des DateTimePickers -->
	<script src="../js/date.format.js" type="text/javascript"></script>	<!-- Zur formattierten Ausgabe von Datumsobjekten -->

	<script src="../js/RGraph/libraries/RGraph.common.core.js" type="text/javascript"></script>
	<script src="../js/RGraph/libraries/RGraph.common.dynamic.js" type="text/javascript"></script>   <!-- Just needed for dynamic features (eg tooltips) -->
	<script src="../js/RGraph/libraries/RGraph.common.tooltips.js" type="text/javascript"></script>
    <script src="../js/RGraph/libraries/RGraph.line.js" type="text/javascript"></script>
	<script src="../js/RGraph/libraries/RGraph.bar.js" type="text/javascript"></script>	<!-- Für Balkendiagramme, auch gestapelte! -->
    <script src="../js/RGraph/libraries/RGraph.common.key.js" type="text/javascript"></script>
	<!--script src="/js/combined/menuhints.js" ></script--> <!-- zu löschen, nicht mehr nachvollziehbar -->

	<!-- include the menu -->
	<!-- Static navbar = scrollt mit. / Bei Fixed würde der Text drunter wegscrollen! (navbar-default = weiß, navbar-inverse = schwarz) )-->
<!-- ================================================= START topMenu.php ================================================= -->


<div class="navbar navbar-default navbar-static-top" role="navigation">
  <div class="container">
	<!-- To add the responsive features to the navbar, the content that you want to be collapsed needs to be wrapped in a <div> with classes .collapse, .navbar-collapse.
		The collapsing nature is tripped by a button that has a the class of .navbar-toggle and then features two data- elements.
		The first, data-toggle, is used to tell the JavaScript what to do with the button, and the second, data-target, indicates which element to toggle.
		Three with a class of .icon-bar create what I like to call the hamburger button. This will toggle the elements that are in the .nav-collapse <div>.
		For this feature to work, you need to include the Bootstrap Collapse Plugin. -->
	<div class="navbar-header">
		<!-- Knopf mit drei Strichen, der ab einer geringen Breite erscheint und die Menüpunkte darunter versteckt -->
	  <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
		<span class="sr-only">Toggle navigation</span>	<!-- Hide an element to all devices except screen readers with .sr-only -->
		<span class="icon-bar"></span>
		<span class="icon-bar"></span>
		<span class="icon-bar"></span>
	  </button>
	  <a class="navbar-brand" href="mainPage.php" title="Startseite">
		<img src="../images/ENOCOO_LOGO_horizontal_36x178.png" height="36" width="178">
	  </a>
			<p class="navbar-text hide" id="announcementSign"><a href="announcements.php"><img src="../images/AttentionSignSmall.png" title="Aktuelle Informationen liegen vor" height="36" width="36"></a></p>
	  </div>
	<div class="navbar-collapse collapse">
	  <ul class="nav navbar-nav">
		<!--<li><a href="eirqTrafficLight.php">Ampel</a></li>-->

		<!-- Alle Zählerarten, die jeder sehen darf - ->
		<li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown">Zähler-Daten <span class="caret"></span></a>
          <ul class="dropdown-menu" role="menu">
			  <li><a href="photovoltaic.php">Siedlung Strom PV Erzeugung, Einspeisung, Bezug</a></li>
			  <li><a href="eirqQuartierWPumpen.php">Siedlung Wärmepumpen</a></li>
			  <li><a href="#">Ihr Stromverbrauch *</a></li>
			  <li><a href="#">Ihr Kaltwasser *</a></li>
			  <li><a href="#">Ihr Warmwasser *</a></li>
			  <li><a href="downloadConsumption.php">Daten herunterladen</a></li>
          </ul>
        </li>
		-->

		<li><a href="ownConsumption.php"  >Ihr Verbrauch</a></li>		<li><a href="settlement.php" >Siedlung</a></li>
		<li><a href="photovoltaic.php" >PV-Anlage</a></li>
		<li><a href="meterValues.php" >Z&auml;hler</a></li>

		<li><a href="downloadConsumption.php" >Download</a></li>
		<!-- <li><a href="eirqMieterWechsel.php">Test</a></li> -->

		<li class="dropdown">
			<a href="#" class="dropdown-toggle  " data-toggle="dropdown">Hilfe <span class="caret"></span></a>
			<ul class="dropdown-menu" role="menu">
				<li><a href="tips.php">Tipps</a></li>
				<li><a href="fAQSupport.php">FAQ & Kontakt</a></li>
				<li><a href="announcements.php">Aktuelle Informationen</a></li>
			</ul>
		</li>

<!--
		<li>
			<p class="navbar-text" id="announcementSign"><a href="Announcements.php"><img src="../images/AttentionSignSmall.png" title="Aktuelle Informationen liegen vor" height="36" width="36"></a></p>
		</li>
-->

		<!--
		<li class="dropdown">
		  <a href="#" class="dropdown-toggle" data-toggle="dropdown">Administration <span class="caret"></span></a>
		  <ul class="dropdown-menu" role="menu">
			<li><a href="eirqMieterWechsel.php">Mieterwechsel</a></li>
			<li><a href="#">Information an die Verwaltung *</a></li>
			<li class="divider"></li>
			<li><a href="eirqLoadingDemo.php">Demo des 'Lade-Bildes'</a></li>
			<li><a href="eirqSystemAdministration.php">Demo der 'System-Administration'-Mitteilung</a></li>
		  </ul>
		</li>
		-->

		<!--
		<li>
			<p class="navbar-text" id="announcementSign"><a href="Announcements.php"><img src="../images/AttentionSignSmall.png" title="Aktuelle Informationen liegen vor" height="36" width="36"></a></p>
		</li>
		-->
		</ul>


		<ul class="nav navbar-nav navbar-right">
		<span>
		<p class="navbar-text" id="smileys">&nbsp;&nbsp;&nbsp;&nbsp;Strompreis:&nbsp;<img src="../images/SmileysAllGrey.png" title="Ist der Strom gerade günstig oder teuer?" alt="[Ampel inaktiv]" height="36" width="111"></p>
		</span>
		<!-- <p class="navbar-text">&nbsp;&nbsp;&nbsp;&nbsp;Angemeldet als&nbsp;H12W34_01</p> -->	<!-- 4 x &nbsp; damit der Text bei kleinen Bildschirmen auch eingerückt erscheint wie die Menüpunkte -->
		<li class="dropdown">
			<a href="#" class="dropdown-toggle " data-toggle="dropdown">[H12W34_01] <span class="caret"></span></a>
			<ul class="dropdown-menu" role="menu">
				<li><a href="pwChange.php">Kennwort ändern</a></li>				<li><a href="settings.php">Einstellungen</a></li>				<li><a href="logout.php">Abmelden</a></li>
			</ul>
		</li>
	</ul>
	</div><!--/.nav-collapse -->

	<!-- Maintenance mode has been activated. The user will be informed and redirected to the SigninForm -->

  </div>
</div>

<!-- <script src="../js/jquery-2.1.0.js"></script> -->
<script type="text/javascript" src="../js/topMenu.js"></script>

<!-- ================================================= ENDE topMenu.php ================================================= -->




    <!-- ====================================== SPINNER START ====================================== -->
	<!-- <script src="../js/jquery-2.1.0.js"></script> -->
	<link rel="stylesheet" href="../css/spin.css">
	<script type="text/javascript">
		var mySpinner = null;
	</script>

    <script type="module" type="text/javascript">
        import {Spinner} from '../js/spin.js';  // an extra <script src="../js/spin.js"></ script> is not necessary!

        function spinnerInit() {
            var opts = {
                lines: 12, // The number of lines to draw
                length: 40, // The length of each line
                width: 14, // The line thickness
                radius: 42, // The radius of the inner circle
                scale: 1,
                corners: 1, // Corner roundness (0..1)
                rotate: 0, // The rotation offset
                color: '#E9B44C', // #rgb or #rrggbb, evohaus grün: '#62b558', blau: '#02a0b3'
                fadeColor: 'transparent', // CSS color or array of colors
                speed: 0.75, // Rounds per second 0..1
                trail: 60, // Afterglow percentage
                shadow: false, // Whether to render a shadow
                hwaccel: false, // Whether to use hardware acceleration
                className: 'spinner', // The CSS class to assign to the spinner
                zIndex: 2e9, // The z-index (defaults to 2000000000)
                top: '50%', // Top position relative to parent in px. 'auto' ist identisch
                left: '50%', // Left position relative to parent in px. 'auto' ist identisch
                animation: 'spinner-line-shrink', // The CSS animation name for the lines: 'spinner-line-fade-quick', 'spinner-line-fade-default', 'spinner-line-fade-more', 'spinner-line-shrink'
                visibility: true
            };

            // DEBUGGING: alert('Inside SpinnerInit()')
            var target = document.getElementById('spinner'); // id's der RGraph-Grafiken: cvs / cvsEnergyMonthData - kein unterschied zu dashboard...
            target.style.display = "block";
            //mySpinner = new Spinner(opts).spin(target);
			mySpinner = new Spinner(opts);
        }

        spinnerInit();

		// setTimeout(function(){ spinnerHide(); alert("2 seconds have passed.") }, 2000);

		// the only way to access functions in a module from not-module-JS-Code (export/import can only be used in modules!) is to make a function global by attaching it to
		// the global object window. The method xyz then can be accessed with xyz or window.zyx.
		window.startSpinner=function() {
            var target = document.getElementById('spinner'); // id's der RGraph-Grafiken: cvs / cvsEnergyMonthData - kein unterschied zu dashboard...
			mySpinner.spin(target);
        }

        window.hideSpinner=function() {
            mySpinner.stop();
        }

    </script> <!-- ====================================== SPINNER END ====================================== -->

	<script type="text/javascript">

		var kontrolldatum = moment(new Date());  // Ist ein Moment-Objekt!
		var gedrueckterPeriodenKnopf = "";	// Speichert ein Element oder jQuery-Objekt. Text des Knopfs z.B. mit .text() ausgeben.
		var gedrueckterMediumKnopf = "";	// s.o.
		var dataAvailable = true;
		var detailDataAvailable = true;
		var detailDataPossible = true;
		var chosenResidenceId = "123";

		// Registrierung der Eventhandler an den Objekten
		function init () {
			// .onchange aktualisiert nicht, wenn man das Feld verlässt! Die Enter-Taste auch nicht, man muss das Feld mit TAB verlassen!
			//document.getElementById('DateTimePicker').onblur = tagesdatenHolenUndRGraphZeichnen;
			// Das hier bringt den error, setDate wäre keine Methode?!?: document.getElementById('DateTimePicker').setDate("01/10/2011");
			$('#DateTimePicker').data("DateTimePicker").onblur = tagesdatenHolenUndRGraphZeichnen;
			$('#DateTimePicker').data("DateTimePicker").setDate(kontrolldatum.format("DD/MM/YYYY"));
			//tagesdatenHolenUndRGraphZeichnen();	// Sofort den ersten Tag anzeigen! -> Braucht man nicht, passiert durch die Zeile 1 höher schon!!
		}
		window.onload = init;

		// Funktion zum Ermitteln des maximalen Wertes in einem Array (Skalen anpassen...)
		/* Wirft einen Fehler bei solchen Arrays: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], daher doch die Sort-Geschichte genommen!
		Array.prototype.max = function () {
			return this.reduce(function (p, v) {
				return ( p > v ? p : v );
			});
		} */

		/**
		* Datum wechseln. Je nach ausgewählter Granularität wird der Angezeigte Tag um 1 Tag, 1 Woche, 1 Monat oder 1 Jahr gewechselt.
		* In welche Richtung, sagt der übergebene Parameter faktor (1 oder -1). Graphik aktualisieren passiert durch den dadurch ausgelösten onChanged-Event im DateTimePicker
		*/
		function datumWechseln(faktor) {
			switch(gedrueckterPeriodenKnopf.attr('id')) {
				case 'btnLetzte24h':
					/* Hier muss nix berechnet werden, macht die DB */
					kontrolldatum = moment(new Date());
					break;
				case 'btnTag':
					kontrolldatum.add(faktor, 'days');
					break;
				case 'btnLetzte7Tage':
					/* Hier muss nix berechnet werden, macht die DB */
					break;
				case 'btnWoche':
					kontrolldatum.add(faktor, 'weeks');
					break;
				case 'btnMonat':
					kontrolldatum.add(faktor, 'months');
					break;
				case 'btnJahr':
					kontrolldatum.add(faktor, 'years');
					break;
			}
			$('#DateTimePicker').data("DateTimePicker").setDate(kontrolldatum.format("DD/MM/YYYY"));
		}

		/**
		* Funktionen zum Anzeigen/Ausblenden des Spinners
		*/
		function showLoadingGif(bool) {
			if (bool) {
				// $('#loadingGif').html("<img src='../images\\LogoIrqRotating125.gif' /><p>Bitte warten, die Daten werden geladen...</p>");		// Wichtig, Backslash quoten!
				//alert("start");
				startSpinner();
			}
			else {
				// $('#loadingGif').html("");	// Kein HTML-Code -> Bild verschwindet
				//alert("hide");
				hideSpinner();
			}
		}


		/**
		* Neue Tagesdaten aus DB holen und Graphik aktualisieren
		*/
		function tagesdatenHolenUndRGraphZeichnen () {
			showLoadingGif(true);

			/* nocache: Hack für den IE (alle Versionen), da dieser bei gleichem Statement den Cache abfragt, anstatt das PHP-Skript neu aufzurufen
			   Weitere Alternativen siehe hier: http://stackoverflow.com/questions/367786/prevent-caching-of-ajax-call */
			var nocache = new Date().getTime();
			//var datumInDBFormat = new Date(kontrolldatum);
			/* Ganz wichtig: neue moment-Objekte durch Klonen erzeugen, sonst sind beide Variablen nur Zeiger und manipulieren das original kontrolldatum! */
			var datumFromInDBFormat = moment(kontrolldatum);	// Eigenes Moment-Objekt als Kontrolldatum-Klon erzeugen

			// .slice(3) schneidet das "btn" am Anfang der ID weg.
			var url = 'getMeterDataWithParam.php?cache=' + nocache + '&from=' + datumFromInDBFormat.format("YYYY-MM-DD")
				+ '&intVal=' + gedrueckterPeriodenKnopf.attr('id').slice(3) + '&mClass=' + gedrueckterMediumKnopf.attr('id').slice(3) + '&AreaId=' + chosenResidenceId;

			/* Beispiel-Returnparameter:
			[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.02,0.08,0.21,0.17,0.22,0.64,0.94,1.09,0.96,1.03,1.04,0.97,1.05,1.02,0.98,
			1.08,1.05,0.98,1.05,0.91,0.71,0.74,0.93,1.91,1.39,0.98,1.29,1.24,1.08,0.87,0.42,0.74,0.58,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
			-> evtl. mit eval() umwandeln? */

			RGraph.AJAX.getJSON(url, draw);
//            setTimeout(ready, 1000)
			// showLoadingGif(false): das macht hier keinen Sinn mehr, da "draw" asynchron aufgerufen wird und daher showLoadingGif(false) hier sofort wieder aufgerufen wird
		}


        /**
        * Handler für Fensterveränderung registrieren - dieser holt die Tagesdaten nochmal (wäre nicht nötig, Parameter fehlt sonst aber) und zeichnet Grafik neu mit veränderten Dimensionen!
        */
        $(document).ready(ready = function ()
        {
			gedrueckterMediumKnopf = $('#btnStromverbrauch'); // Default = Strom
			mediumKnopfAktivieren(gedrueckterMediumKnopf);
			datenKnopfGedrueckt($("#btnLetzte24h")); // Default = Letzte 24 h. Hier wird auch gleich tagesdatenHolenUndRGraphZeichnen aufgerufen!
			window.onresize = tagesdatenHolenUndRGraphZeichnen;
        })

        /**
        * Je nach Fensterbreite wird einer von x vorgegebenen Breitewerten zurückgeliefert.
		* Orientiert wird sich dabei an den verschiedenen Stufen von Bootstrap
        */
        function canvasDimensionen()
        {
			var gutterGesamt = 45;
			/* Canvas Initialgröße 1200 x 400; je nach reduzierter Größe wird auch die Höhe anteilig angepasst */
			var neueDim = { breite: 1140, hoehe: 400 };	// Maximale Breite 1140, da auch das Bootstrap Menü nicht breiter ist (Gutter von ca. jeweils abgezogen!)
			var fensterBreite = $(window).width();
			if (fensterBreite <  480) { neueDim.breite = 320-gutterGesamt; neueDim.hoehe = 213; return neueDim; };
			if (fensterBreite <  640) { neueDim.breite = 480-gutterGesamt; neueDim.hoehe = 213; return neueDim; };
			if (fensterBreite <  768) { neueDim.breite = 640-gutterGesamt; neueDim.hoehe = 213; return neueDim; };
			if (fensterBreite <  992) { neueDim.breite = 768-gutterGesamt; neueDim.hoehe = 256; return neueDim; };
			if (fensterBreite < 1200) { neueDim.breite = 992-gutterGesamt; neueDim.hoehe = 331 };
			return neueDim;

			/* ToDo: http://stackoverflow.com/questions/6850164/get-the-device-width-in-javascript
				iOS-Geräte liefern ppi zurück (640 Pixel = 320 ppi!!!!, Android & Desktopgeräte Pixel. Daher siehe Link oben mit @media...*/
		}

		function chartTitle() {
			var titelText = gedrueckterMediumKnopf.text();
			switch(gedrueckterMediumKnopf.attr('id')) {
				case 'btnStromverbrauch':
					titelText += ' (kWh), ';
					break;
				case 'btnWarmwasser':
					titelText += ' (Kubikmeter), ';
					break;
				case 'btnKaltwasser':
					titelText += ' (Kubikmeter), ';
					break;
				case 'btnWaerme':
					titelText += ' (kWh), ';
					break;
			}

			switch(gedrueckterPeriodenKnopf.attr('id')) {
				case 'btnLetzte24h':
					titelText += 'letzte 24 Stunden';
					break;
				case 'btnTag':
					titelText += kontrolldatum.format("dd. DD.MM.YYYY") + ' von 0-24 Uhr';
					break;
				case 'btnLetzte7Tage':
					titelText += 'letzte sieben Tage';
					break;
				case 'btnWoche':
					titelText += 'Woche von ' + moment(kontrolldatum).startOf('week').format("dd. DD.MM.") + ' bis ' + moment(kontrolldatum).endOf('week').format("dd. DD.MM.");
					break;
				case 'btnMonat':
					titelText += 'Monat ' + kontrolldatum.format("MMM YYYY");
					break;
				case 'btnJahr':
					titelText += 'Jahr ' + kontrolldatum.format("YYYY");
					break;
			}
			return titelText;
		}

		function yAxisUnit() {
			var unit;
			switch(gedrueckterMediumKnopf.attr('id')) {
				case 'btnStromverbrauch':
					unit = 'kWh';
					break;
				case 'btnWaerme':
					unit = 'kWh';
					break;
				default:
					unit = 'm3';
					break;
			}
			return unit;
		}

		function displayEnergyPrice() {
			return ((gedrueckterMediumKnopf.attr('id')) == 'btnStromverbrauch') && (((gedrueckterPeriodenKnopf.attr('id')) == 'btnTag') || ((gedrueckterPeriodenKnopf.attr('id')) == 'btnLetzte24h'));
		}

		/**
		* Remove duplicates from the labels and if the last label is 0 change it to 24 (o'clock)
		* [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6,...,23,23,23,23,0] is reduced to [0,1,2,3,4,5,6,...,23,24]
		*/
		function reduceLabels(lab) {
			if (lab.length === 0) { return lab; }
			var index;
			var last;
			var labResult = [];
			for (index = 0; index < lab.length; ++index) {
				if (lab[index] != last) {
					if (last == 23 && lab[index] === 0) {
						labResult.push(24);
					} else {
						labResult.push(lab[index]);
					}
					last = lab[index];
				} else {
					labResult.push(null);
				}
			}
			return labResult;
		}

		// Manually round max x-value, because RGraph has a bug in calculationg the ymax when displaying values like 0.003
		function maxValueRoundedUp(myArray) {
			var stufenFaktor = 2;
			var faktor = 0;
			var max = 0;
			max = Math.max.apply(Math, myArray);
			switch (true) {
				case (max >= 0.000 && max < 0.01):
					faktor = 1000;
					break;
				case (max >= 0.01 && max < 0.1):
					faktor = 100;
					break;
				case (max >= 0.1 && max < 1):
					faktor = 10;
					break;
				default:
					faktor = 1;
			}
			if (faktor == 1) {
				return max;
			} else {
				gerundet = Math.floor(max * faktor * 10);
				while ((gerundet / 5) % 5 > 0) {
					gerundet = gerundet + 1;
				}
				return gerundet / 10 / faktor;
			}
			//return (Math.ceil(max * faktor * stufenFaktor) / faktor / stufenFaktor);
		}

        /**
        * This is the AJAX callback function. It adds the number retrieved via AJAX to the data array
		* dataArray sieht z.B. so aus: [[0,0,0,0,0,0,0,0],["Do.","Fr.","Sa.","So.","Mo.","Di.","Mi.","Do."]]
		* ACHTUNG: var n2 = new Array(num[1]); erzeugt ein Array mit vielen "Undefined"-Werten und am Ende irgendwo dem Wert!
        */
        function draw (tempDataArray)
        {
			if (displayEnergyPrice()) {
				var energyPrices = tempDataArray.pop();
				var maxEnergyPrice = maxValueRoundedUp(energyPrices);
			}
//			$('#Infofeld2').html("Medium: " + gedrueckterMediumKnopf.text() + ", Periode: " + gedrueckterPeriodenKnopf.text() + ", BarChart: " + gedrueckterPeriodenKnopf.hasClass('barChart') + ", Kontrolldatum: " + kontrolldatum.format("dd. DD.MM.YYYY"));
			var tempLabels = tempDataArray.pop();	// Letztes Element (= Labels Array) entfernen
			labels = reduceLabels(tempLabels);
//			}

			var dataArray = tempDataArray.pop();	// Die eigentlichen Werte extrahieren aus dem verschachtelten Array
			var anzahlLabels = labels.length;
//			if (anzahlLabels == 0) { anzahlLabels = 1; }	// sonst knallt es beim Zeichnen eines leeren Diagramms, wenn es keine Daten zum Zeichnen gibt
			// Maximalen Wert ermitteln
			var maximum = Math.max.apply(Math, dataArray);
			//2015.06.12 var maximum = 0;
//			if (dataArray.length) {
			//2015.06.12 	var findeMaxarray = dataArray.slice(0, dataArray.length);
			//2015.06.12 	findeMaxarray.sort(function(a, b){return b-a});
			//2015.06.12 	var maximum = findeMaxarray[0];
//			}
				//var maximum = dataArray.max();
			// Maximum nicht explizit anzeigen, sonst auskommentieren: $('#dayMaximum').html(maximum);

			var maxYAxisValue = maxValueRoundedUp(dataArray);
			// Leeres Array: Hinweistext schreiben
			dataAvailable = (dataArray.length > 0);
			if (!dataAvailable) {
				$('#Infofeld').html("<span class='glyphicon glyphicon-info-sign'></span> Für den gewählten Zeitraum liegen keine Daten vor.");
				hide($('#Infofeld'), false);
				hide($('#InfofeldDetail'), true);
			} else {
				$('#Infofeld').html("");
				hide($('#Infofeld'), true);
			}
			detailControlsAusblenden(!(dataAvailable && detailDataPossible)); // || ($(gedrueckterPeriodenKnopf).hasClass('detailsPossible'))

			// Maximalen Wert ermitteln & ein paar Diagrammerte (Gutter...) daran anpassen
			//var maximum = (dataArray.length = 0) ? 0 : dataArray.max;
			//var maximum = dataArray.max();
			var gutterLeft = (Math.round(maximum).toString().length + 2 ) * 7 + 16;
			//alert(gutterLeft);
			var scaleDecimals = (maximum <= 1) ? 3 : 0;	// Zwei Nachkommastellen anzeigen bei Werten < 1

			/* Canvas & Objektbaum im Hintergrund löschen */
			var canvas = document.getElementById("cvs");
			RGraph.Reset(canvas);
			var canvasDetail = document.getElementById("cvsDetail");
			RGraph.Reset(canvasDetail);

			if (dataAvailable) {

				canvas.width  = canvasDimensionen().breite;
				canvas.height = canvasDimensionen().hoehe;
				var text_size = Math.min(10, ($(window).width() / 1000) * 10 );		// einigermaßen sinnvolle mathematische Annäherung
				var linewidth = $(window).width() > 500 ? 2 : 1;
				linewidth = $(window).width() > 750 ? 3 : linewidth;

				// Debugausgabe:
				//$('#Infofeld2').html("Fenster Breite: " + $(window).width() + " Höhe: " + $(window).height() + "<br>Canvas Breite: " + canvas.width + " Höhe: " + canvas.height);

				// Reset the translation fix so that it gets applied again
				canvas.__rgraph_aa_translated__ = false;

				if (gedrueckterPeriodenKnopf.hasClass('lineChart')) {

					var dataArrayAlsText = [];
					for (i in dataArray){
						dataArrayAlsText[i] = dataArray[i].toString();
					}

					// LINIENDIAGRAMM

					var gutterTop = 50;
					var gutterRight = 37;
					var gutterBottom = 35;
					/* var jsonArray = JSON.parse(dataArray); ist nicht nötig, dataArray ist ein geschachteltes JSON-Array, das man RGraph direkt übergeben kann! */
					/* "Key" = Legende */

					// click-function for detail-view #####################################
					function clickForDetails (e, shape) { //debugger;
						if  (!detailDataPossible) {
							// exit, a view was chosen, that does not support a detail-view (only last24h and day do so)
							return -1;
						}
						//var obj   = e.target.__object__
						var klickedIndex   = shape['index_adjusted'];

						//var obj   = e.target.__object__;
						//var klickedShape = obj.getShape(e);
						//if (klickedShape === undefined) { return -1; }
						//var klickedIndex = klickedShape['index_adjusted'];
						// For Debugging
						//var dataset = klickedShape['dataset'];
						//var value   = obj.original_data[dataset][klickedIndex];
						//$('#Infofeld2').html('Value is: ' + value + ', klickedIndex is: ' + klickedIndex);

						var mouseXY = RGraph.getMouseXY(e);
						// var stunde = mouseXY[0] / ((canvas.width - gutterLeft - 10) / dataArray.length);	// Math.round(
						var breite = ((canvas.width - gutterLeft - 10) / labels.length) + 1 + 1;

						var stunde = 0;
						switch(gedrueckterPeriodenKnopf.attr('id')) {
							case 'btnLetzte24h':
								// Hier muss zuerst der richtige Tag und dann die richtige Stunde ermittelt werden
								//stunde = Math.floor((mouseXY[0] - gutterLeft) / breite) - 24 + labels[0];	// Stimmt noch nicht ganz, aber bei 30 Tagen ist es statt 30 ein 30,2 -> gerundet trotzdem o.k.!
								var datumFromInDBFormat = moment(new Date());
								var index24h = labels.indexOf(24);
								if (klickedIndex >= index24h) {
									stunde = Math.round((klickedIndex - index24h) / 4);
								} else {	// Previous day!
									stunde = 24 - Math.round((index24h - klickedIndex) / 4);
									datumFromInDBFormat = datumFromInDBFormat.add(-1, 'days');
								}
								break;
							case 'btnTag':
								//stunde = Math.floor((mouseXY[0] - gutterLeft) / breite);
								var datumFromInDBFormat = moment(kontrolldatum);	// Eigenes Moment-Objekt als Kontrolldatum-Klon erzeugen
								stunde = Math.round(klickedIndex / 4);
								break;
						}
						/* Ganz wichtig: neue moment-Objekte durch Klonen erzeugen, sonst sind beide Variablen nur Zeiger und manipulieren das original kontrolldatum! */
						//datumFromInDBFormat.add(stunde, 'h');	// Eigenes Moment-Objekt als Kontrolldatum-Klon erzeugen
						datumFromInDBFormat = datumFromInDBFormat.set('hour', stunde);
						//var stunde = Math.floor((mouseXY[0] - gutterLeft) / breite) - 24 + labels[0];	// Stimmt noch nicht ganz, aber bei 30 Tagen ist es statt 30 ein 30,2 -> gerundet trotzdem o.k.!
						// var obj   = e.target.__object__;
				//$('#Infofeld2').html("Fenster Breite: " + $(window).width() + " Höhe: " + $(window).height() + "<br>Canvas Breite: " + canvas.width + " Höhe: " + canvas.height + ", Mausposition: x:" + mouseXY[0] + ", y: " + mouseXY[1] + ", GutterLeft +10: " + (gutterLeft + 10) + ", Breite: " + breite + ", Stunde: " + stunde);

						var nocache = new Date().getTime();
						//var datumInDBFormat = new Date(kontrolldatum);

						// .slice(3) schneidet das "btn" am Anfang der ID weg.
						var url = 'getMeterDataWithParam.php?cache=' + nocache + '&from=' + datumFromInDBFormat.format("YYYY-MM-DD HH:mm:ss")
							+ '&intVal=Stunde' + '&mClass=' + gedrueckterMediumKnopf.attr('id').slice(3)  + '&AreaId=' + chosenResidenceId;
				//$('#Infofeld2').html("URL: " + url);

							RGraph.AJAX.getJSON(url, drawDetail);
					}

					var chart = new RGraph.Line({
						id: 'cvs',
						data: dataArray,
						options: {
							shadow: false,
							colors: ['green'],
							'gutter.left': gutterLeft,	// Stellt xxxx,x dar
							'gutter.top': gutterTop,	// 50 wird benötigt, wenn ein Titel angezeigt werden soll, sonst 15.
							'gutter.right': gutterRight,	// Sonst wird die ganze rechte xLabel-Zahl abgeschnitten
							'gutter.bottom': gutterBottom,	// Bei Liniendiagrammen wird meist der Tag & Datum zweizeilig angezeigt
							'background.grid.autofit.numvlines': anzahlLabels - 1,	// Striche an der x-Achse, unter denen die Zahlen stehen. Sollte identisch mit der Anz. numvlines sein. Default: null (linked to number of datapoints) -> 4 x mehr, da 15-Min. Messwerte!
							numxticks: anzahlLabels - 1,
							'scale.decimals': scaleDecimals,	// Wichtig, denn ohne die Nachkommastelle steht bei Max-Werten < 1 auf ganze Int. gerundete y-Labels z.B. 1,1,1,0,0
							'scale.thousand': '.',
							'scale.point': ',',
							'scale.zerostart': true,	// sonst werden 0'en auf der X-Achse nicht angezeigt
							strict: true,
							labels: labels,
							title: chartTitle(),	// Wenn titel, dann gutter.top vergrößern, sonst 15 !!!!!
							tooltips: dataArrayAlsText,
							events: {
								click: clickForDetails,
								mousemove: function (e, shape) {e.target.style.cursor = 'pointer';}
							}
						}
					});

					if (maxYAxisValue < 1) {
						chart.set('ymax', maxYAxisValue);	// Keine feste Angabe der Obergrenze -> diese wird mehr oder weniger sinnig selbst bestimmt (meist 1 oder 5 bei den PV-Zahlen)
					}

					// when displaying energy-prices, add an additional line-chart
					if (displayEnergyPrice()) {
						var keyYPosition = 35;	// Anzahl Pixel nach unten von Ecke links oben.

						// print key in other chart when both charts are displayed
						chart.set('gutter.top', gutterTop + 10)	// 50 wird benötigt, wenn ein Titel angezeigt werden soll, sonst 15.
							.set('key', ['Stromverbrauch', 'Kalkulierter Strompreis'])
							.set('key.color.shape', 'square')
							.set('key.colors', ['green', 'red'])	// grün=PV, blau=interner Verbrauch, rot=externer Zukauf
							.set('key.position', 'gutter')
							.set('key.position.gutter.boxed', true)
							.set('key.position.y', keyYPosition)
							.set('title.y', 25);	// Wenn titel, dann gutter.top vergrößern, sonst 15 !!!!!
						chart.draw();

						var chartEnergyPrices = new RGraph.Line({
							id: 'cvs',
							data: energyPrices,
							options: {
								shadow: false,
								colors: ['red'],
								'gutter.left': gutterLeft,	// Stellt xxxx,x dar
								'gutter.top': gutterTop + 10,	// 50 wird benötigt, wenn ein Titel angezeigt werden soll, sonst 15.
								'gutter.right': gutterRight,	// Sonst wird die ganze rechte xLabel-Zahl abgeschnitten
								'gutter.bottom': gutterBottom,	// Bei Liniendiagrammen wird meist der Tag & Datum zweizeilig angezeigt
								'background.grid.autofit.numvlines': anzahlLabels - 1,	// Striche an der x-Achse, unter denen die Zahlen stehen. Sollte identisch mit der Anz. numvlines sein. Default: null (linked to number of datapoints) -> 4 x mehr, da 15-Min. Messwerte!
								numxticks: anzahlLabels - 1,
								'background.grid': false,
								yaxispos: 'right',
								ymax: maxEnergyPrice,
								'scale.thousand': '.',
								'scale.point': ',',
								'scale.decimals': 2,	// Wichtig, denn ohne die Nachkommastelle steht bei Max-Werten < 1 auf ganze Int. gerundete y-Labels z.B. 1,1,1,0,0
								'scale.zerostart': true	// sonst werden 0'en auf der X-Achse nicht angezeigt
							}
						}).draw();

					} else {
						chart.draw();
					}

					// Workaround for ylabels in scientific notation
					for (var i = 0, arr = ['']; i < chart.scale2.labels.length; i += 1) {
						//arr[i + 1] = String(Number(chart.scale2.labels[i]).toFixed(scaleDecimals));
						arr[i + 1] = chart.scale2.labels[i];
					}
					// Add unit to highest y-axis-value
					arr[arr.length - 1] = yAxisUnit() + '\n' + arr[arr.length - 1]; // index 0 is ylabel at 0
					chart.set('ylabels.specific', RGraph.array_reverse(arr));

					if (displayEnergyPrice()) {
						// Workaround for ylabels in scientific notation
						for (var i = 0, arr = ['']; i < chartEnergyPrices.scale2.labels.length; i += 1) {
							//arr[i + 1] = String(Number(chart.scale2.labels[i]).toFixed(scaleDecimals));
							arr[i + 1] = chartEnergyPrices.scale2.labels[i];
						}
						// Add unit to highest y-axis-value
						arr[arr.length - 1] = '€\n' + arr[arr.length - 1]; // index 0 is ylabel at 0
						chartEnergyPrices.set('ylabels.specific', RGraph.array_reverse(arr));
					}
					RGraph.redraw();
					// showLoadingGif(false);

					//$('#Infofeld2').html("chart-details: " + chart.scale2);

					/* Erkenntnisse:
						- ymax -> Anzahl Y-Achsen-Werte
						- numhlines -> Anzahl horizontale Y-Achsen-Linien (unabhängig von Beschriftung!)
						- numyticks -> Anzahl horizontaler Striche an der y-Achse (unabhängig von Beschriftung!)
					*/
				} else {

					// BALKENDIAGRAMM

					var bar1 = new RGraph.Bar('cvs', dataArray)
						//.set('shadow', false)
						.set('strokestyle', 'rgba(0,0,0,0)')
//						.set('noaxes', true)
//						.set('ylabels', false)
						.set('colors', ['Gradient(#94f776:#50B332)'])	// 'rgba(0,255,0,0.8)'/'green' ... 0.6 => Transparenz zw. 0 = 100% transparent bis 1 = nicht transparent
						.set('numxticks', anzahlLabels)	// Striche an der x-Achse, unter denen die Zahlen stehen. Sollte identisch mit der Anz. numvlines sein. Default: null (linked to number of 						//.set('hmargin', 25)
//						.set('background.grid', false)
						.set('gutter.left', gutterLeft)	// Stellt xxxx,x dar
						.set('gutter.top', 50)	// 50 wird benötigt, wenn ein Titel angezeigt werden soll, sonst 15.
						.set('gutter.right', 10)	// Sonst wird die ganze rechte xLabel-Zahl abgeschnitten
						.set('background.grid.autofit.numvlines', anzahlLabels)	// Anzahl vertikale Linien (ergibt 25 mit der y-Achse bei 0). Default: 20
						//.set('gutter.bottom', mitte)	// das obere Diagramm setzt auf der Diagrammitte auf!
//						.set('grouping', 'stacked')
						//.set('ymax', 20)
/*						.set('key', ['Bezug', 'PV Produktion', 'Einspeisung'])
						.set('key.color.shape', 'square')
						.set('key.colors', ['rgba(255,0,0,0.6)', 'rgba(255,255,0,0.6)', 'rgba(0,255,0,0.6)'])	// grün=PV, blau=interner Verbrauch, rot=externer Zukauf
						.set('key.position', 'gutter')
						.set('key.position.gutter.boxed', true)
						.set('key.position.y', 5) */
						.set('scale.thousand', '.')
						.set('scale.point', ',')
						.set('scale.zerostart', true)	// sonst werden 0'en auf der X-Achse nicht angezeigt
						.set('scale.decimals', scaleDecimals)	// Wichtig, denn ohne die Nachkommastelle steht bei Max-Werten < 1 auf ganze Int. gerundete y-Labels z.B. 1,1,1,0,0
						.set('labels', labels)	// ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]
						.set('labels.above', true)	// Zahlenwerte über dem Balken anzeigen
						.set('labels.above.decimals', 2) // WARNING: set to 1 some Values are displayed as 0,0 instad of 0,05 or 0,03!
						.set('labels.above.size', text_size)	// fest vorgeben, da sonst abhängig von text.size (davon -2, x-Achsen-Label), die aber zwischen 8 & 10 wechseln!
						.set('title', chartTitle());	// Wenn titel, dann gutter.top vergrößern, sonst 15 !!!!!
						//.set('tooltips', dataArrayAlsText) // Funktioniert nicht...

						if (maxYAxisValue < 1) {
							bar1.set('ymax', maxYAxisValue);	// Keine feste Angabe der Obergrenze -> diese wird mehr oder weniger sinnig selbst bestimmt (meist 1 oder 5 bei den PV-Zahlen)
						}

						bar1.draw();

					// Workaround for ylabels in scientific notation
					for (var i = 0, arr = ['']; i < bar1.scale2.labels.length; i += 1) {
						arr[i + 1] = bar1.scale2.labels[i];
					}
					arr[arr.length - 1] = yAxisUnit() + '\n' + arr[arr.length - 1]; // index 0 is ylabel at 0
					bar1.set('ylabels.specific', RGraph.array_reverse(arr));
					RGraph.redraw();
				}

			} else {
				detailControlsAusblenden(true);
				canvas.onclick = function (e, shape) {} // no click possible: do not draw the detail-chart when there is no data in the upper chart
			}

			showLoadingGif(false);
		}

        function drawDetail (tempDataArrayDetail)
        {
//			$('#Infofeld2').html("Medium: " + gedrueckterMediumKnopf.text() + ", Periode: " + gedrueckterPeriodenKnopf.text() + ", BarChart: " + gedrueckterPeriodenKnopf.hasClass('barChart'));
			var tempLabelsDetail = tempDataArrayDetail.pop();	// Letztes Element (= labels Array) entfernen
			labelsDetail = reduceLabels(tempLabelsDetail);
//			}

			var dataArrayDetail = tempDataArrayDetail.pop();	// Die eigentlichen Werte extrahieren aus dem verschachtelten Array
			var anzahlLabelsDetail = labelsDetail.length;
//			if (anzahlLabelsDetail == 0) { anzahlLabelsDetail = 1; }	// sonst knallt es beim Zeichnen eines leeren Diagramms, wenn es keine Daten zum Zeichnen gibt
			// Maximalen Wert ermitteln
			var maximumDetail = Math.max.apply(Math, dataArrayDetail);
			//2015.06.12 var maximumDetail = 0;
//			if (dataArrayDetail.length) {
				//2015.06.12 var findeMaxarray = dataArrayDetail.slice(0, dataArrayDetail.length);
				//2015.06.12 findeMaxarray.sort(function(a, b){return b-a});
				//2015.06.12 var maximumDetail = findeMaxarray[0];
//			}
				//var maximumDetail = dataArrayDetail.max();
			// Maximum nicht explizit anzeigen, sonst auskommentieren: $('#dayMaximum').html(maximumDetail);

			var detailMaxYAxisValue = maxValueRoundedUp(dataArrayDetail);
			// Leeres Array: Hinweistext schreiben
			detailDataAvailable = (dataArrayDetail.length > 0);
			if (!dataArrayDetail.length) {
				$('#InfofeldDetail').html("<span class='glyphicon glyphicon-info-sign'></span> Für den gewählten Zeitraum liegen keine Daten vor.");
				hide($('#InfofeldDetail'), false);
			} else {
				$('#InfofeldDetail').html("");
				hide($('#InfofeldDetail'), true);
			}

			// Maximalen Wert ermitteln & ein paar Diagrammerte (Gutter...) daran anpassen
			//var maximumDetail = (dataArrayDetail.length = 0) ? 0 : dataArrayDetail.max;
			//var maximumDetail = dataArrayDetail.max();
			var gutterLeft = (Math.round(maximumDetail).toString().length + 2 ) * 7 + 16;
			//alert(gutterLeft);
			var scaleDecimals = (maximumDetail <= 1) ? 3 : 0;	// Zwei Nachkommastellen anzeigen bei Werten < 1

			/* Canvas & Objektbaum im Hintergrund löschen */
			var canvasDetail = document.getElementById("cvsDetail");
			RGraph.Reset(canvasDetail);

			if (detailDataAvailable) {

				canvasDetail.width  = canvasDimensionen().breite;
				canvasDetail.height = canvasDimensionen().hoehe;
				var text_size = Math.min(12, ($(window).width() / 1000) * 10 );		// einigermaßen sinnvolle mathematische Annäherung
				var linewidth = $(window).width() > 500 ? 2 : 1;
				linewidth = $(window).width() > 750 ? 3 : linewidth;

				// Debugausgabe:
				//$('#Infofeld2').html("Fenster Breite: " + $(window).width() + " Höhe: " + $(window).height() + "<br>CanvasDetail Breite: " + canvasDetail.width + " Höhe: " + canvasDetail.height);

				// Reset the translation fix so that it gets applied again
				canvasDetail.__rgraph_aa_translated__ = false;

				var dataArrayDetailAlsText = [];
				for (i in dataArrayDetail){
					dataArrayDetailAlsText[i] = dataArrayDetail[i].toString();
				}

				// DETAIL - LINIENDIAGRAMM

				/* var jsonArray = JSON.parse(dataArrayDetail); ist nicht nötig, dataArrayDetail ist ein geschachteltes JSON-Array, das man RGraph direkt übergeben kann! */
				/* "Key" = Legende */
				chartDetail = new RGraph.Line('cvsDetail', dataArrayDetail)
					.set('shadow', false)	// von true geändert am 07.05.2015
				//            .set('background.grid.autofit', true)
					//.set('spline', true)	// Interpoliert, nicht zackig
					//.set('background.grid.autofit.numhlines', 5)	// Anzahl horizontale Linien (ergibt 6 mit der x-Achse bei 0). Hat nichts mit der Y-Achsenbeschriftung zu tun! Default: 5
					.set('colors', ['green'])	// grün = PV Ertrag. Parameter muss ein Array sein, auch wenn nur mit einer Farbe
					//.set('colors', ['green', 'red', 'blue'])	// grün=PV, blau=interner Verbrauch, rot=externer Zukauf
					//.set('key', ['PV production', 'External purchase', 'Internal consumption'])
		//			.set('key.color.shape', 'square')
					//.set('key.colors', ['green', 'blue', 'red'])	// grün=PV, blau=interner Verbrauch, rot=externer Zukauf
					.set('key.colors', ['green'])	// grün=PV, blau=interner Verbrauch, rot=externer Zukauf
					.set('key.position', 'gutter')
					.set('key.position.gutter.boxed', false)
					.set('key.position.y', 0)
					//.set('filled', true)
					//.set('fillstyle', ['rgba(255,0,0,0.3)', 'rgba(0,255,0,0.3)','rgba(0,0,255,0.3)'])
					.set('gutter.left', gutterLeft)	// Stellt xxxx,x dar
					.set('gutter.top', 50)	// 50 wird benötigt, wenn ein Titel angezeigt werden soll, sonst 15.
					.set('gutter.right', 20)	// Sonst wird die ganze rechte xLabel-Zahl abgeschnitten
					.set('gutter.bottom', 35)	// Bei Liniendiagrammen wird meist der Tag & Datum zweizeilig angezeigt
					.set('background.grid.autofit.numvlines', anzahlLabelsDetail - 1)	// Anzahl vertikale Linien (ergibt 25 mit der y-Achse bei 0). Default: 20
					.set('numxticks', anzahlLabelsDetail - 1)	// Striche an der x-Achse, unter denen die Zahlen stehen. Sollte identisch mit der Anz. numvlines sein. Default: null (linked to number of datapoints) -> 4 x mehr, da 15-Min. Messwerte!
					//.set('hmargin', 10)	// Das lässt zwischen dem ersten und letzten Punkt je ein Rand von 10 Punkten zur Y-Achse & dem rechten Rand
					//.set('tickmarks', true)
					//.set('tickmarks', 'circle')	// endcircle macht nur am Anfang & Ende einen Kreis! round/square... überall!
					//.set('ymax', 5)	// Keine feste Angabe der Obergrenze -> diese wird mehr oder weniger sinnig selbst bestimmt (meist 1 oder 5 bei den PV-Zahlen)
					//.set('ylabels.specific', [5,4,3,2,1])
					.set('scale.decimals', scaleDecimals)	// Wichtig, denn ohne die Nachkommastelle steht bei Max-Werten < 1 auf ganze Int. gerundete y-Labels z.B. 1,1,1,0,0
					//.set('numyticks', 3)	// Anzahl horizontaler Striche an der y-Achse
					// Hinweis: 'labels' als Zahlen und nicht als Strings: Die führende 0 als erster Eintrag wird nicht gedruckt, auch wenn die 1 erst beim nächsten Strich anfängt...
					.set('scale.thousand', '.')
					.set('scale.point', ',')
					.set('scale.zerostart', true)	// sonst werden 0'en auf der X-Achse nicht angezeigt
					.set('strict', true)
					.set('labels', labelsDetail)	// ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]
					//.set('title', gedrueckterMediumKnopf.text() + ', ' + gedrueckterPeriodenKnopf.text())	// Wenn titel, dann gutter.top vergrößern, sonst 15 !!!!!
					.set('title', 'Detailansicht')	// Wenn titel, dann gutter.top vergrößern, sonst 15 !!!!!
					.set('tooltips', dataArrayDetailAlsText);

					if (detailMaxYAxisValue < 1) {
						chartDetail.set('ymax', detailMaxYAxisValue);
					}
					chartDetail.draw();
					//showLoadingGif(false);

					// Workaround for ylabels in scientific notation
					for (var i = 0, arr = ['']; i < chartDetail.scale2.labels.length; i += 1) {
						//arr[i + 1] = String(Number(chartDetail.scale2.labels[i]).toFixed(scaleDecimals));
						arr[i + 1] = chartDetail.scale2.labels[i];
					}
					arr[arr.length - 1] = yAxisUnit() + '\n' + arr[arr.length - 1]; // index 0 is ylabel at 0
					chartDetail.set('ylabels.specific', RGraph.array_reverse(arr));
					RGraph.redraw();
			}
		}


		/**
		* Funktion wird vom onChanged-Event des DateTimePickers aufgerufen, setzt das Kontrolldatum im Hintergrund auf dessen neues Datum und aktualisiert die Grafik
        */
		function datumsAenderung(dpObjekt) {
			//$('#Infofeld2').html('Change aufgerufen: ' + $("#DateTimePicker").data("DateTimePicker").getDate() + ' - Alt: ' + e.oldDate.format("DD.MM.YYYY")  + ' - Neu: ' + e.date.format("DD.MM.YYYY"));
			kontrolldatum = dpObjekt.date;	// das neue Datum des DateTimePickers
			tagesdatenHolenUndRGraphZeichnen();
		}

		function datumControlsAusblenden(jaNein) {
			hide($('#PreviousBtn'), jaNein);
			hide($('#NextBtn'), jaNein);
			hide($('#DateTimePicker'), jaNein);
		}

		function detailControlsAusblenden(jaNein) {
			hide($('#detailView'), jaNein);
			}

		function mediumKnopfGedrueckt(knopf) {
			gedrueckterMediumKnopf = $(knopf);
			mediumKnopfAktivieren(gedrueckterMediumKnopf);
			tagesdatenHolenUndRGraphZeichnen();
		}

		// Gedrückter "Daten"-Knopf - ggf. Datum-Control ausblenden, ansonsten Knopf aktivieren, Graphik neu zeichnen
		function datenKnopfGedrueckt(knopf) {
			detailDataPossible = $(knopf).hasClass('detailsPossible');
			detailControlsAusblenden(!detailDataPossible);

			datumControlsAusblenden(!($(knopf).hasClass('dayChooser')));
			gedrueckterPeriodenKnopf = $(knopf);
			periodenKnopfAktivieren(gedrueckterPeriodenKnopf);
			tagesdatenHolenUndRGraphZeichnen();
		}

		/* Alle Medium-Knöpfe außer dem übergebenen inaktivieren */
		function mediumKnopfAktivieren(knopf) {
			$('.mediumKnopf').each(function( index ) {
				if ($( this ).attr('id') == knopf.attr('id')) {
					$( this ).addClass('active');
				} else {
					$( this ).removeClass('active');
				}
			});
			// Debugausgabe Name des Knopfes: $('#Infofeld2').html("Aktiver Medium-Knopf: " + knopf.text());
		}

		/* Alle Perioden-Knöpfe außer dem übergebenen inaktivieren */
		function periodenKnopfAktivieren(knopf) {
			$('.periodenKnopf').each(function( index ) {
				if ($( this ).attr('id') == knopf.attr('id')) {
					$( this ).addClass('active');
				} else {
					$( this ).removeClass('active');
				}
			});
			// Debugausgabe Name des Knopfes: $('#Infofeld2').html("Aktiver Perioden-Knopf: " + knopf.text());
		}

		/* function hide(target, jaNein) {
			if (jaNein) {
				target.addClass("hide"); }
			else {
				target.removeClass("hide"); }
		} */

		function dropDownAction(menuEntry) {
			// menueEintrag z.B.: "#dropDownCompByResidences"
			chosenResidenceId = menuEntry.id;
			//console.log("Aktiver Vergleichsgrundlage-Menüeintrag: " + gewaehlteVergleichsgrundlage);
			//// $('#VergleichsText').val($(menueEintrag).text());
			$('#residence').html($(menuEntry).text() + ' <span class="caret"></span>');
			$('#data-valFromTo').html($(menuEntry).attr('data-valFrom') + ' - ' + $(menuEntry).attr('data-valTo'));
			tagesdatenHolenUndRGraphZeichnen();
			// document.location.href = "/php/ownConsumption.php?mode=ok&Preis=5";

		}

		</script>

	</head>

  <body role="document">

    <div class="container theme-showcase" role="main">


	<h1><span class="fa fa-area-chart"></span> Ihre Verbrauchszahlen</h1>
	<p>Hier finden Sie Ihre Verbrauchszahlen zu Strom, Warm- bzw. Kaltwasser und Heizung. Die Verbräuche liegen im 15 Minuten-Raster vor.</p>	<!--  Maximum:&nbsp;<span id="dayMaximum"></span> kWh. -->
	<p>Wählen Sie mittels der Knöpfe die Verbrauchsart und ein Zeitintervall. Bei den Intervallen Tag, Woche, Monat und Jahr kann geblättert werden.</p>
	<p>Der besseren Darstellung auf Tablets oder Smartphones halber werden Diagramme mit wenigen Werten als Balkendiagramm, solche mit mehr als zwölf Werten als Liniendiagramm dargestellt.<br />
	Bewegen Sie in den Liniendiagrammen den Mauszeiger auf die Linienpunkte, um deren Werte anzeigen zu lassen.</p>
	<p><b>Hinweise zu einzelnen Zählerarten:</b>
	<ol>
		<li><b>Strom:</b> Zusätzlich wird in der Tagesansicht und den letzten 24 Stunden auch der Strompreis angezeigt, so dass Sie sehen können, ob Ihre Verbräuche in Zeiten günstigen Stroms stattfanden.</li>
		<li><b>Wärme:</b> Diese Zähler senden ein Signal, wenn die erzeugte Wärmemenge eine Kilowattstunde (kWh) erreicht hat. Die Tages-/24h-Ansicht ist daher anders als bei den anderen Zählern: es werden diese einzelnen Impulse zu einer Kurve mit Treppenform aufaddiert. Zu den Zeitpunkten ansteigender Kurven wurde Energie zur Wärmeerzeugung aufgewendet. Je mehr Treppenstufen auf einander folgen, desto höher war hier die Wärmeerzeugung.</li>
		<li><b>Wasser:</b> Im Messintervall von 15 Minuten fallen meist nur ein- bis zweistellige Wasserverbräuche in Litern an, daher gibt es hier nur sehr wenige und niedrige Spitzen in den Liniendiagrammen.</li>
	</ol>
	</p>
	<!-- Session-details (debug-information):  -->
	<div id="spinner"></div>

		<div class="row">
			<div class="col-lg-12">
				<form class="form-inline">
					<!-- Bei nur einer Wohneinheit nur Text anzeigen, sonst Auswahlbox -->
					<label for="residence">Wohneinheit:</label> <div class="form-group"><div class="input-group"><button type="button" class="btn btn-warning dropdown-toggle" id="residence" data-toggle="dropdown">H12W34 <span class="caret"></span></button><ul class="dropdown-menu" role="menu"><li><a href="#" class="pdm" id="123" data-valFrom="01.01.2021" data-valTo="01.01.2021">H12W34 </a></li><li><a href="#" class="pdm" id="124" data-valFrom="01.01.2021" data-valTo="01.01.2021">SP567 TNr:890 </a></li></ul></div></div> (Zugreifbarer Zeitraum: <span id="data-valFromTo">01.01.2021 - 02.02.2022</span>)				</form>
			</div><!-- /.col-lg-6 -->
		</div><!-- /row -->



		<div class="row top-buffer">
			<div class="col-lg-12">
				<div class="col-md-5">
					<form class="form-horizontal" role="form" accept-charset="UTF-8">		<!--  method="post" action="/php/ownConsumption.php" -->
					   <div class="form-group">
							<button type="button" class="btn btn-warning mediumKnopf" id="btnStromverbrauch"><span class="glyphicon glyphicon-flash"></span> Strom</button>
							<button type="button" class="btn btn-warning mediumKnopf" id="btnWarmwasser"><span class="glyphicon glyphicon-fire"></span> Warmwasser</button>
							<button type="button" class="btn btn-warning mediumKnopf" id="btnKaltwasser"><span class="glyphicon glyphicon-tint"></span> Kaltwasser</button>
							<button type="button" class="btn btn-warning mediumKnopf" id="btnWaerme"><span class="fa fa-fire"></span> Wärme</button>
					   </div>
					</form>
				</div><!-- /.col-md-5 -->

				<div class="col-md-7 text-right">
					<form class="form-horizontal" role="form" accept-charset="UTF-8">		<!--  method="post" action="/php/ownConsumption.php" -->
					   <div class="form-group">
							<button type="button" class="btn btn-warning periodenKnopf lineChart detailsPossible" id="btnLetzte24h">Letzte 24 h</button>		<!-- Wenn als  btn-default deklariert, dann ist die weiße Schrift fett - sieht nicht gut aus... -->
							<button type="button" class="btn btn-warning periodenKnopf lineChart dayChooser detailsPossible" id="btnTag">Tag</button>
							<button type="button" class="btn btn-warning periodenKnopf barChart" id="btnLetzte7Tage">Letzte 7 Tage</button>
							<button type="button" class="btn btn-warning periodenKnopf barChart dayChooser" id="btnWoche">Woche</button>
							<button type="button" class="btn btn-warning periodenKnopf lineChart dayChooser" id="btnMonat">Monat</button>
							<button type="button" class="btn btn-warning periodenKnopf barChart dayChooser" id="btnJahr">Jahr</button>
							<!-- <button type="button" class="btn btn-warning periodenKnopf lineChart" id="btnNaechste24h">Nächste 24 h</button> -->
							<!-- <button type="button" class="btn btn-warning periodenKnopf lineChart" id="btnMorgen">Morgen</button> -->
							<!-- <button type="button" class="btn btn-warning periodenKnopf lineChart" id="btnNaechste72h">Nächste 72 h</button> -->
					   </div>
					</form>
				</div><!-- /.col-md-7 -->
			</div><!-- /.col-lg-12 -->
		</div><!-- /row -->

		<div class="row">
			<!--<div class="col-lg-offset-4 col-lg-3">-->
			<div class="col-lg-offset-4 col-lg-3 col-md-offset-3 col-md-6 col-sm-offset-2 col-sm-8 col-xs-12 text-center">
				<form class="form-dayChooser" role="form" accept-charset="UTF-8"> <!--  method="post" action="/php/ownConsumption.php?page=log" -->
					<div class="input-group">
						<span class="input-group-btn">
							<button type="button" id="PreviousBtn" class="btn btn-sm" title="Zurück blättern">
							  <span class="glyphicon glyphicon-backward"></span>
							</button>
						</span>
						<!-- <input type="day" class="form-control" placeholder="01.01.2021" name="day" required autofocus> -->
						<div class="input-group date" id="DateTimePicker" data-date-format="dd. DD.MM.YYYY">
							<input type="text" class="form-control" title="Datum eintragen" autofocus>
							<span class="input-group-addon" title="Kalender öffnen. Klick auf den Monatsnamen &#10;zum schnellen Jahres-Monatswechsel"><span class="glyphicon glyphicon-calendar"></span>
							</span>
						</div>
						<span class="input-group-btn">
							<button type="button" id="NextBtn" class="btn btn-sm" title="Vorwärts blättern">
							  <span class="glyphicon glyphicon-forward"></span>
							</button>
						</span>
					</div><!-- /input-group -->
					<script type="text/javascript">
						$(function () {
							// Define click-Function for all dropdown-elements with class 'pdm'
							$('.pdm').click(function() {dropDownAction(this)});	// this = "#dropDownCompByResidences"
							// jQuery-Sytax, um ein Objekt über dessen ID anzusprechen: $('#ID').
							// Funktionsnamen hier immer ohne () angeben, da das sonst ein sofortiger Aufruf der Funktion darstellt!
							//Das hier erzeugt einen neuen DateTimePicker im DIV mit der gleichnamigen ID und setzt bei diesem best. Initialwerte
							$('#DateTimePicker').datetimepicker({
								language: 'de',
								todayHighlight: true,
								pickTime: false	// Blendet die kleine Uhr unten aus, mit der man zwischen Datum & Uhrzeit-Selektor umschalten kann
								//startDate: new Date(),
								//change: datumsAenderung
							});
							$("#DateTimePicker").on("dp.change",function (dpObjekt) { datumsAenderung(dpObjekt); });
							$("#DateTimePicker").on("dp.error",function (dpObjekt) {	// Funktion wird vom DateTimePicker aufgerufen, wenn dieser mit der Eingabe nichts anfangen kann!
								$('#Infofeld').html("<span class='glyphicon glyphicon-info-sign'></span> Das eingegebene Datum ist kein gültiges Datum!");
								hide($('#Infofeld'), false);
							});
							$("#PreviousBtn").click(function(){ datumWechseln(-1) });
							$("#NextBtn").click(function(){ datumWechseln( 1) });

							// Allen Periodenknöpfen & Medienknöpfen Callbackfunktion zuweisen
							$('.periodenKnopf').each(function( index ) {
								$( this ).click(function(){ datenKnopfGedrueckt(this) });
							});
							$('.mediumKnopf').each(function( index ) {
								$( this ).click(function(){ mediumKnopfGedrueckt(this) });
							});

						});
					</script>
					<div id="Infofeld2"></div>	<!-- NUR ZU DEBUGGINGZWECKEN! Hier kann mann Kommentare reinschreiben, wie z.B. kein gültiges Datum o.ä-->
				</form>
			</div><!-- /.col-lg-3 -->
			<div class="col-lg-5">
			</div>
		</div><!-- /row -->

		<!-- Infofeld -->
		<div class="col-lg-6 col-lg-offset-3">
			<div class="alert alert-danger text-center top-buffer hide" role="alert" id="Infofeld"></div>
		</div><!-- /.col-lg-12 -->

		<!-- Zeile mit RGraph Diagramm -->
		<div class="row ">
			<div class="col-lg-12">
				<div class="text-center" id="loadingGif"></div>
				<canvas id="cvs" width="1140" height="400">[Keine Canvas Unterstützung: das Diagramm kann in Ihrem Browser nicht angezeigt werden!]</canvas>
			</div><!-- /.col-lg-12 -->
		</div><!-- /row -->

		<div id="HinweisStrom"> <!--  class="hide" -->
			<h4>Hinweise:</h4>
			<p>Der Strompreis ist innerhalb des Monats ein kalkulierter Strompreis, d.h. nicht der reale Strompreis. Werden im Folgemonat der Bezugspreis und eventuelle andere Komponenten der Stromrechnung im System eingepflegt, werden die kalkulierten Strompreise durch die tatsächlichen Werte ersetzt.</p>
		</div>

		<span id="detailView">
			<h3>Detailansicht:</h3>
			<p>Klicken Sie im oberen Diagramm auf einen Zeitpunkt, um sich in der Detailansicht die detaillierten Messwerte im Bereich zweier Stunden anzeigen zu lassen.</p>
		</span>

		<!-- Infofeld -->
		<div class="col-lg-6 col-lg-offset-3">
			<div class="alert alert-danger text-center top-buffer hide" role="alert" id="InfofeldDetail"></div>
		</div><!-- /.col-lg-12 -->

		<div class="row ">
			<div class="col-lg-12">
				<div class="text-center" id="loadingGif"></div>
				<canvas id="cvsDetail" width="1140" height="400">[Keine Canvas Unterstützung: das Diagramm kann in Ihrem Browser nicht angezeigt werden!]</canvas>
			</div><!-- /.col-lg-12 -->
		</div><!-- /row -->

	</div> <!-- /container -->

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
  </body>
</html>
