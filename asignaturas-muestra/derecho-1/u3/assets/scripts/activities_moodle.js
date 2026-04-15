const location = window.location.href.split("/")

export const moodleParams = {
    moodleURL: "https://pel.cch.unam.mx/",
    unitActual: location[location.length-3],
};

export const unit_themes = [
    {
        unit: "u1",
        themes: [
            { themeName: "Dimensiones socio histórica y filosófica del Derecho", themeURL: "t1", pages: "17" }
        ]
    },
    {
        unit: "u2",
        themes: [
            { themeName: "Dimensión normativa del Derecho", themeURL: "t1", pages: "11" },
        ]
    },
    {
        unit: "u3",
        themes: [
            { themeName: "Dimensión jurídica del estado y derechos humanos", themeURL: "t1", pages: "12" },
        ]
    },
]

export const moodleActivities = [
    /* Unidad 1 */
    { idHTML: "u1a0", url: "course/view.php?id=", id: "51&section=1" },

    // U1 T1
    { idHTML: "u1a1", url: "mod/quiz/view.php?id=", id: "2537" },
    { idHTML: "u1a2", url: "mod/hvp/view.php?id=", id: "2538" },
    { idHTML: "u1a3", url: "mod/forum/view.php?id=", id: "2539" },
    { idHTML: "u1a4", url: "mod/forum/view.php?id=", id: "2540" },
    { idHTML: "u1a5", url: "mod/hvp/view.php?id=", id: "2541" },
    { idHTML: "u1a6", url: "mod/assign/view.php?id=", id: "2542" },
    { idHTML: "u1a7", url: "mod/quiz/view.php?id=", id: "2543" },

    /* Unidad 2 */
    { idHTML: "u2a0", url: "course/view.php?id=", id: "51&section=2" },

    // U2 T1
    { idHTML: "u2a1", url: "mod/quiz/view.php?id=", id: "2545" },
    { idHTML: "u2a2", url: "mod/hvp/view.php?id=", id: "2546" },
    { idHTML: "u2a3", url: "mod/hvp/view.php?id=", id: "2547" },
    { idHTML: "u2a4", url: "mod/forum/view.php?id=", id: "2548" },
    { idHTML: "u2a5", url: "mod/assign/view.php?id=", id: "2549" },
    { idHTML: "u2a6", url: "mod/hvp/view.php?id=", id: "2550" },
    { idHTML: "u2a7", url: "mod/hvp/view.php?id=", id: "2551" },
    { idHTML: "u2a8", url: "mod/quiz/view.php?id=", id: "2552" },

    /* Unidad 3 */
    { idHTML: "u3a0", url: "course/view.php?id=", id: "51&section=3" },

    // U1 T1
    { idHTML: "u3a1", url: "mod/quiz/view.php?id=", id: "2554" },
    { idHTML: "u3a2", url: "mod/hvp/view.php?id=", id: "2555" },
    { idHTML: "u3a3", url: "mod/forum/view.php?id=", id: "2556" },
    { idHTML: "u3a4", url: "mod/hvp/view.php?id=", id: "2557" },
    { idHTML: "u3a5", url: "mod/forum/view.php?id=", id: "2558" },
    { idHTML: "u3a6", url: "mod/assign/view.php?id=", id: "2559" },
    { idHTML: "u3a7", url: "mod/quiz/view.php?id=", id: "2560" },

];
