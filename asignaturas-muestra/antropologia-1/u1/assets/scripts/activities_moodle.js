const location = window.location.href.split("/")

export const moodleParams = {
    moodleURL: "https://pel.cch.unam.mx/",
    unitActual: location[location.length-3],
};

export const unit_themes = [
    {
        unit: "u1",
        themes: [
            { themeName: "La Antropología y la cultura", themeURL: "t1", pages: "7" },
        ]
    },
    {
        unit: "u2",
        themes: [
            { themeName: "Las disciplinas antropológicas: una visión integradora", themeURL: "t1", pages: "5" },
        ]
    },
    {
        unit: "u3",
        themes: [
            { themeName: "La antropología en el proceso de globalización", themeURL: "t1", pages: "7" },
        ]
    },
]

export const moodleActivities = [
    /* Unidad 1 */
    { idHTML: "u1a0", url: "course/view.php?id=", id: "52&section=1" },
    // U1 T1
    { idHTML: "u1a1", url: "mod/quiz/view.php?id=", id: "2564" },
    { idHTML: "u1a2", url: "mod/forum/view.php?id=", id: "2565" },
    { idHTML: "u1a3", url: "mod/hvp/view.php?id=", id: "2566" },
    { idHTML: "u1a4", url: "mod/hvp/view.php?id=", id: "2567" },
    { idHTML: "u1a5", url: "mod/hvp/view.php?id=", id: "2568" },
    { idHTML: "u1a6", url: "mod/forum/view.php?id=", id: "2569" },
    { idHTML: "u1a7", url: "mod/hvp/view.php?id=", id: "2570" },
    { idHTML: "u1a8", url: "mod/hvp/view.php?id=", id: "2571" },
    { idHTML: "u1a9", url: "mod/assign/view.php?id=", id: "2572" },
    { idHTML: "u1a10", url: "mod/quiz/view.php?id=", id: "2573" },

    /* Unidad 2 */
    { idHTML: "u2a0", url: "course/view.php?id=", id: "52&section=2" },
    // U2 T1
    { idHTML: "u2a1", url: "mod/quiz/view.php?id=", id: "2576" },
    { idHTML: "u2a2", url: "mod/hvp/view.php?id=", id: "2577" },
    { idHTML: "u2a3", url: "mod/forum/view.php?id=", id: "2578" },
    { idHTML: "u2a4", url: "mod/hvp/view.php?id=", id: "2579" },
    { idHTML: "u2a5", url: "mod/hvp/view.php?id=", id: "2580" },
    { idHTML: "u2a6", url: "mod/assign/view.php?id=", id: "2581" },
    { idHTML: "u2a7", url: "mod/hvp/view.php?id=", id: "2582" },
    { idHTML: "u2a8", url: "mod/quiz/view.php?id=", id: "2583" },

    /* Unidad 3 */
    { idHTML: "u3a0", url: "course/view.php?id=", id: "52&section=3" },
    // U3 T1
    { idHTML: "u3a1", url: "mod/quiz/view.php?id=", id: "2586" },
    { idHTML: "u3a2", url: "mod/forum/view.php?id=", id: "2587" },
    { idHTML: "u3a3", url: "mod/hvp/view.php?id=", id: "2588" },
    { idHTML: "u3a4", url: "mod/hvp/view.php?id=", id: "2589" },
    { idHTML: "u3a5", url: "mod/hvp/view.php?id=", id: "2590" },
    { idHTML: "u3a6", url: "mod/hvp/view.php?id=", id: "2591" },
    { idHTML: "u3a7", url: "mod/hvp/view.php?id=", id: "2592" },
    { idHTML: "u3a8", url: "mod/hvp/view.php?id=", id: "2593" },
    { idHTML: "u3a9", url: "mod/assign/view.php?id=", id: "2594" },
    { idHTML: "u3a10", url: "mod/forum/view.php?id=", id: "2595" },
    { idHTML: "u3a11", url: "mod/quiz/view.php?id=", id: "2596" },
];
