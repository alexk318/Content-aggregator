function sport_func() {
    var sport = document.getElementById("sport");

    var football = document.getElementById("football");
    var basketball = document.getElementById("basketball");
    var hockey = document.getElementById("hockey");

    if ( sport.checked == true ) {
        football.checked = 'on';
        basketball.checked = 'on';
        hockey.checked = 'on';
    } else {

        football.checked = false;
        basketball.checked = false;
        hockey.checked = false;

    }


}


function it_func() {
    var it = document.getElementById("it");

    var java = document.getElementById("java");
    var php = document.getElementById("php");
    var cplus = document.getElementById("cplus");

    if (it.checked == true) {
        java.checked = 'on';
        php.checked = 'on';
        cplus.checked = 'on';
    } else {

        java.checked = false;
        php.checked = false;
        cplus.checked = false;

    }


}


function countries_func() {
    var countries = document.getElementById("countries");

    var usa = document.getElementById("usa");
    var russia = document.getElementById("russia");
    var india = document.getElementById("india");

    if (countries.checked == true) {
        usa.checked = 'on';
        russia.checked = 'on';
        india.checked = 'on';
    } else {

        usa.checked = false;
        russia.checked = false;
        india.checked = false;

    }


}
