document.addEventListener("DOMContentLoaded", function() {

    let search = document.querySelector("#search");
    search.addEventListener("input", async function() {
        let response = await fetch("/search?c=" + search.value);

        if (search.value == "") {
            document.querySelector("#autoresults").innerHTML = "";
        }

        let cities = await response.json();

        console.log(cities)

        let html = "";
        
        for (let i = 0; i < cities.name.length; i++) {
            html += "<li class='list-group-item fontcontrol'>" + cities.name[i] + ", " + cities.state[i] + "</li>";
        }

        document.querySelector("#autoresults").innerHTML = html;
    });

    let weather = document.getElementById("main");
    let main_desc = weather.textContent;

    let bg = document.getElementById("background");

    bg.removeAttribute("class");


    if (main_desc.includes("rain")) {
        bg.classList.add("rainy");
    }
    else if (main_desc.includes("mist")) {
        bg.classList.add("rainy");
    }
    else if (main_desc.includes("cloud")) {
        bg.classList.add("cloudy");
    }
    else if (main_desc.includes("snow")) {
        bg.classList.add("snowy");
    }
    else if (main_desc.includes("storm")) {
        bg.classList.add("stormy");
    }
    else if (main_desc.includes("smoke")) {
        bg.classList.add("smoke");
    }
    else {
        bg.classList.add("clear");
    }
});