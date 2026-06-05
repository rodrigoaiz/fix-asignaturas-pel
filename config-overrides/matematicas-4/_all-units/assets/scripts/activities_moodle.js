export const moodleParams = {
  moodleURL: "https://pel.cch.unam.mx/",
  unitActual: "u1",
};
export const unit_themes = [
    {
        unit: "u1",
        themes: [
            { themeName: "Noción de Función, Dominio y Rango", themeURL: "t1", pages: "6" },
            { themeName: "Función Polinomial", themeURL: "t2", pages: "7" },
            { themeName: "División Polinomial", themeURL: "t3", pages: "2" },
            { themeName: "Representación Gráfica de una función Polinomial", themeURL: "t4", pages: "2" }
        ]
    },
    {
        unit: "u2",
        themes: [
            { themeName: "Funciones Racionales", themeURL: "t1", pages: "4" },
            { themeName: "REVISIÓN CONCEPTOS. DOMINIO Y RANGO", themeURL: "t2", pages: "7" },
            { themeName: "ASÍNTOTAS HORIZONTALES", themeURL: "t3", pages: "5" },
            { themeName: "EJEMPLOS DE APLICACIÓN DE LAS FUNCIONES RACIONALES.", themeURL: "t4", pages: "3" },
            { themeName: "MODELOS CON FUNCIONES CON RACIONALES. DOMINIO, RANGO Y CEROS.", themeURL: "t5", pages: "5" },
            { themeName: "EJEMPLO DE GRÁFICA DE UNA FUNCIÓN CON RADICAL. RADICANDO LINEAL (1).", themeURL: "t6", pages: "7" },
            { themeName: "Problemas de aplicación.", themeURL: "t7", pages: "4" },
        ]
    },
    {
        unit: "u3",
        themes: [
            { themeName: "Funciones exponenciales", themeURL: "t1", pages: "10" },
            { themeName: "Funciones logarítmicas", themeURL: "t2", pages: "11" },
        ]
    },
    {
        unit: "u4",
        themes: [
            { themeName: "Situaciones o fenómenos de variación periódica", themeURL: "t1", pages: "4" },
            { themeName: "Medidas angulares en grados y radianes.", themeURL: "t2", pages: "2" },
            { themeName: "Razones trigonométricas seno, coseno y tangente para cualquier ángulo.", themeURL: "t3", pages: "5" },
            { themeName: "Funciones trigonométricas: f(x)=sen x , f(x)=cos x . Gráfica, dominio, rango, ceros, amplitud, periodo.", themeURL: "t4", pages: "3" },
            { themeName: "Gráfica de las funciones: f(x)=D+A sen(Bx+C), f(x)=D+AcosBx+C. Análisis del comportamiento de la gráfica, respecto de los parámetros A, B, C y D.", themeURL: "t5", pages: "5" },
            { themeName: "Problemas de aplicación.", themeURL: "t6", pages: "2" },
        ]
    },
]

export const moodleActivities = [
    /* Unidad 1 */
    { idHTML: "u1a0", url: "course/view.php?id=", id: "38&section=1" },

    // U1 T1
    { idHTML: "u1a1", url: "mod/quiz/view.php?id=", id: "1644" },
    { idHTML: "u1a2", url: "mod/hvp/view.php?id=", id: "1645" },
    { idHTML: "u1a3", url: "mod/assign/view.php?id=", id: "1646" },
    { idHTML: "u1a4", url: "mod/hvp/view.php?id=", id: "1647" },
    // U1 T2
    { idHTML: "u1a5", url: "mod/forum/view.php?id=", id: "1649" },
    { idHTML: "u1a6", url: "mod/hvp/view.php?id=", id: "1650" },
    // U1 T3
    { idHTML: "u1a7", url: "mod/forum/view.php?id=", id: "1652" },
    // U1 T4
    { idHTML: "u1a8", url: "mod/quiz/view.php?id=", id: "1654" },


    /* Unidad 2 */
    { idHTML: "u2a0", url: "course/view.php?id=", id: "38&section=2" },

    // U2 T1
    { idHTML: "u2a1", url: "mod/quiz/view.php?id=", id: "1657" },
    { idHTML: "u2a2", url: "mod/hvp/view.php?id=", id: "1658" },
    // U2 T2
    { idHTML: "u2a3", url: "mod/hvp/view.php?id=", id: "1660" },
    { idHTML: "u2a4", url: "mod/hvp/view.php?id=", id: "1661" },
    { idHTML: "u2a5", url: "mod/hvp/view.php?id=", id: "1662" },
    { idHTML: "u2a6", url: "mod/hvp/view.php?id=", id: "1663" },
    // U2 T3
    { idHTML: "u2a7", url: "mod/hvp/view.php?id=", id: "1665" },
    { idHTML: "u2a8", url: "mod/hvp/view.php?id=", id: "1666" },
    { idHTML: "u2a9", url: "mod/assign/view.php?id=", id: "1667" },
    // U2 T4
    { idHTML: "u2a10", url: "mod/forum/view.php?id=", id: "1669" },
    // { idHTML: "u2a11", url: "mod/hvp/view.php?id=", id: "1769" }, //esta esta duplicada
    // U2 T5
    { idHTML: "u2a11", url: "mod/hvp/view.php?id=", id: "1671" },
    // U2 T6
    { idHTML: "u2a12", url: "mod/hvp/view.php?id=", id: "1673" },
    { idHTML: "u2a13", url: "mod/assign/view.php?id=", id: "1674" },
    // U2 T7
    { idHTML: "u2a14", url: "mod/quiz/view.php?id=", id: "1676" },


    /* Unidad 3 */
    { idHTML: "u3a0", url: "course/view.php?id=", id: "38&section=3" },

    // U3 T1
    { idHTML: "u3a1", url: "mod/quiz/view.php?id=", id: "1679" },
    { idHTML: "u3a2", url: "mod/hvp/view.php?id=", id: "1680" },
    { idHTML: "u3a3", url: "mod/hvp/view.php?id=", id: "1681" },
    { idHTML: "u3a4", url: "mod/hvp/view.php?id=", id: "1682" },
    { idHTML: "u3a5", url: "mod/forum/view.php?id=", id: "1683" },
    { idHTML: "u3a6", url: "mod/hvp/view.php?id=", id: "1684" },
    { idHTML: "u3a7", url: "mod/forum/view.php?id=", id: "1685" },
    { idHTML: "u3a8", url: "mod/hvp/view.php?id=", id: "1686" },
    { idHTML: "u3a9", url: "mod/forum/view.php?id=", id: "1687" },
    { idHTML: "u3a10", url: "mod/hvp/view.php?id=", id: "1688" },
    { idHTML: "u3a11", url: "mod/forum/view.php?id=", id: "1689" },
    { idHTML: "u3a12", url: "mod/hvp/view.php?id=", id: "1690" },
    { idHTML: "u3a13", url: "mod/forum/view.php?id=", id: "1691" },
    { idHTML: "u3a14", url: "mod/hvp/view.php?id=", id: "1692" },
    { idHTML: "u3a15", url: "mod/hvp/view.php?id=", id: "1693" },
    // U3 T2
    { idHTML: "u3a16", url: "mod/hvp/view.php?id=", id: "1695" },
    { idHTML: "u3a17", url: "mod/hvp/view.php?id=", id: "1696" },
    { idHTML: "u3a18", url: "mod/hvp/view.php?id=", id: "1697" },
    { idHTML: "u3a19", url: "mod/hvp/view.php?id=", id: "1698" },
    { idHTML: "u3a20", url: "mod/hvp/view.php?id=", id: "1699" },
    { idHTML: "u3a21", url: "mod/hvp/view.php?id=", id: "1700" },
    { idHTML: "u3a22", url: "mod/assign/view.php?id=", id: "1701" },
    { idHTML: "u3a23", url: "mod/quiz/view.php?id=", id: "1702" },


    /* Unidad 4 */
    { idHTML: "u4a0", url: "course/view.php?id=", id: "38&section=4" },

    // U4 T1
    { idHTML: "u4a1", url: "mod/quiz/view.php?id=", id: "1705" },
    { idHTML: "u4a2", url: "mod/hvp/view.php?id=", id: "1706" },
    { idHTML: "u4a3", url: "mod/assign/view.php?id=", id: "1707" },
    // U4 T2
    { idHTML: "u4a4", url: "mod/forum/view.php?id=", id: "1709" },
    { idHTML: "u4a5", url: "mod/hvp/view.php?id=", id: "1710" },
    // U4 T3
    { idHTML: "u4a6", url: "mod/hvp/view.php?id=", id: "1712" },
    { idHTML: "u4a7", url: "mod/assign/view.php?id=", id: "1713" },
    { idHTML: "u4a8", url: "mod/hvp/view.php?id=", id: "1714" },
    // U4 T4
    { idHTML: "u4a9", url: "mod/assign/view.php?id=", id: "1716" },
    // U4 T5
    { idHTML: "u4a10", url: "mod/h5p/view.php?id=", id: "1718" },
    { idHTML: "u4a11", url: "mod/h5p/view.php?id=", id: "1719" },
    { idHTML: "u4a12", url: "mod/h5p/view.php?id=", id: "1720" },
    { idHTML: "u4a13", url: "mod/h5p/view.php?id=", id: "1721" },
    { idHTML: "u4a14", url: "mod/h5p/view.php?id=", id: "1722" },
    { idHTML: "u4a15", url: "mod/h5p/view.php?id=", id: "1723" },
    { idHTML: "u4a16", url: "mod/forum/view.php?id=", id: "1724" },
    { idHTML: "u4a17", url: "mod/assign/view.php?id=", id: "1725" },
    // U4 T6
    { idHTML: "u4a18", url: "mod/assign/view.php?id=", id: "1727" },
    { idHTML: "u4a19", url: "mod/quiz/view.php?id=", id: "1728" },
];
