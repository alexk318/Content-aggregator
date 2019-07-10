function sport_func() {
    let sport = document.getElementById("sport");

    let football = document.getElementById("football");
    let basketball = document.getElementById("basketball");
    let hockey = document.getElementById("hockey");

    if ( sport.checked === true ) {
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
    let it = document.getElementById("it");

    let java = document.getElementById("java");
    let php = document.getElementById("php");
    let cplus = document.getElementById("cplus");

    if (it.checked === true) {
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
    let countries = document.getElementById("countries");

    let usa = document.getElementById("usa");
    let russia = document.getElementById("russia");
    let india = document.getElementById("india");

    if (countries.checked === true) {
        usa.checked = 'on';
        russia.checked = 'on';
        india.checked = 'on';
    } else {

        usa.checked = false;
        russia.checked = false;
        india.checked = false;

    }


}