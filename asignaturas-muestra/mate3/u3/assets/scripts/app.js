import {
  moodleActivities,
  moodleParams,
  unit_themes,
} from "./activities_moodle.js";

let fontSize = 1.125;

const getActivities = () => {
  moodleActivities.forEach((activity) => {
    const { idHTML, url, id } = activity;
    const { moodleURL } = moodleParams;

    if (document.getElementById(idHTML)) {
      const activityHtml = document.getElementById(idHTML);

      if (activityHtml.getAttribute("src")) {
        activityHtml?.setAttribute("src", `${moodleURL}${url}${id}`);
      } else if (activityHtml.getAttribute("href")) {
        activityHtml?.setAttribute("href", `${moodleURL}${url}${id}`);
      }
    }
  });
};

const setSideThemes = () => {
  const location = window.location.href.split("/")
  const themeURL = location[location.length-2];

  let sideBarContent = "";
  const sideContainer = document.querySelector(".summary__content__items");
  unit_themes.forEach((theme) => {
    if (theme.unit === moodleParams.unitActual) {
      theme.themes.forEach((t) => {
        sideBarContent += `
						<div class="summary__content__items--item">
							<a
							href='../../${moodleParams.unitActual}/${t.themeURL}/1.html'
							class="summary__content__items__item--link ${
                t.themeURL == location[location.length-2] ? "active" : ""
              }"
							data-theme="${t.themeURL}"
							>
							<div class="summary__content__items__item__link--title">
								${t.themeName}
							</div>
							<div class="summary__content__items__item__link--icon">
								<i class="ri-arrow-right-s-line"></i>
							</div>
							</a>
						</div>
					`;
        localStorage.setItem("theme-active", themeURL);
      });

      sideContainer.innerHTML = sideBarContent;
    }
  });
};

const setActiveTheme = () => {
  const sideThemes = document.querySelectorAll(
    ".summary__content__items__item--link"
  );
  const themeActive = localStorage.getItem("theme-active") || "";
  sideThemes.forEach((theme) => {
    theme.addEventListener("click", () => {
      localStorage.setItem("theme-active", theme.getAttribute("data-theme"));
    });
  });

  sideThemes.forEach((theme) => {
    if (theme.getAttribute("data-theme") === themeActive) {
      theme.classList.add("active");
    }
  });
};

const buildPaginate = () => {
  const paginador = document.querySelector(".summary__content__pages");
  const url = window.location.pathname;
  const tema = url.split("/");
  const unitThemes = unit_themes.filter(
    (theme) => theme.unit === moodleParams.unitActual
  );
  const { themes } = unitThemes[0];
  let itemsPaginador = "";
  let paginasNumber = 0;

  themes.forEach((t) => {
    if (t.themeURL == tema[tema.length - 2]) {
      paginasNumber = t.pages;
    }
  });

  for (let i = 1; i <= paginasNumber; i++) {
    itemsPaginador += `
				<div class="summary__content__pages__links__item${i == parseInt(tema[tema.length-1]) ? "--visited" : ""}">
					<a class="summary__content__pages__links--item" href="${i}.html">
						${i}
					</a>
				</div>
			`;
  }

  paginador.innerHTML = `
			<div class="summary__content__pages__links">
				${itemsPaginador}
			</div>
		`;
};

const zoomIn = () => {
  const body = document.querySelector("body");
  fontSize += 0.1;
  body.style.fontSize = `${fontSize}rem`;
};

const zoomOut = () => {
  const body = document.querySelector("body");
  fontSize -= 0.1;
  body.style.fontSize = `${fontSize}rem`;
};

const accesibilityUser = () => {
  const btnZoomIn = document.querySelector("#zoomIn");
  const btnZoomOut = document.querySelector("#zoomOut");
  const btnPrint = document.querySelector("#print");

  btnZoomIn.addEventListener("click", zoomIn);
  btnZoomOut.addEventListener("click", zoomOut);
  btnPrint.addEventListener("click", () => {
    window.print();
  });
};

const setPaginate = () => {
  const pLeft = document.getElementById("pLeft");
  const pRight = document.getElementById("pRight");
  const location = window.location.href.split("/");
  const newLocation = location.splice(0, location.length - 3);
  let baseURL = "";
  newLocation.forEach((nL) => {
    baseURL += nL + "/";
  });
  const dataLeft = pLeft.getAttribute("data-link").split("/");
  const dataRight = pRight.getAttribute("data-link").split("/");

  if (dataLeft[0] != "http:" && dataLeft[0] != "https:")
    pLeft.setAttribute("href", `${baseURL}${pLeft.getAttribute("data-link")}`);
  else pLeft.setAttribute("href", `${pLeft.getAttribute("data-link")}`);

  if (dataRight[0] != "http:" && dataRight[0] != "https:")
    pRight.setAttribute(
      "href",
      `${baseURL}${pRight.getAttribute("data-link")}`
    );
  else pRight.setAttribute("href", `${pRight.getAttribute("data-link")}`);
};

const main = () => {
  getActivities();
  setSideThemes();
  setActiveTheme();
  buildPaginate();
  setPaginate();
  accesibilityUser();
};

main();
