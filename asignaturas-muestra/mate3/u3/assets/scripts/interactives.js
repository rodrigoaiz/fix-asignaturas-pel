const accordion = () => {
    document.addEventListener('click', event => {

        if (!event.target.classList.contains('accordion-toggle')) return;

        let content = document.querySelector(event.target.hash);
        if (!content) return;

        event.preventDefault();

        if (content.classList.contains('active')) {
            content.classList.remove('active');
            return;
        }

        let accordions = document.querySelectorAll('.accordion-content.active');
        accordions.forEach((accordion, i) => {
            accordion.classList.remove('active');
        })

        content.classList.toggle('active');
    })
}


const zoom = () => {
    let images = document.querySelector('#zoom-image');
    let imgSrc = images.style.backgroundImage;
    imgSrc = imgSrc.replace('url(', '').replace(')', '').replace(/\"/gi, "");

    let img = new Image();

    img.src = imgSrc;

    img.onload = () => {
        let imgWidth = img.naturalWidth;
        let imgHeight = img.naturalHeight;
        let ratio = imgHeight / imgWidth;

        images.onmousemove = (e) => {
            let boxWidth = images.clientWidth;
            let x = e.pageX - images.offsetLeft;
            let y = e.pageY - images.offsetTop;

            let xPercent = x / (boxWidth / 100) + '%';
            let yPercent = y / (boxWidth * ratio / 100) + '%';

            Object.assign(images.style, {
                backgroundPosition: `${ xPercent } ${ yPercent }`,
                backgroundSize: imgWidth + 'px',
            })
        }

        images.onmouseleave = (e) => {
            Object.assign(images.style, {
                backgroundPosition: 'center',
                backgroundSize: 'cover',
            })
        }
    }
}

const darkMode = () => {
    const darkMode = document.querySelector('#dark-mode');
    const lightMode = document.querySelector('#light-mode');
    const html = document.querySelector('html');

    darkMode.addEventListener('click', () => {
        html.classList.add('dark');
    });

    lightMode.addEventListener('click', () => {
        html.classList.remove('dark');
    });
}

if(document.getElementsByClassName('popoverTW')) {
    if(document.getElementsByClassName('popoverTW')) {
        let exampleEl = new Array()
        const popoverArray = document.getElementsByClassName('popoverTW');
        for(let i=0; i < popoverArray.length; i++) {
            exampleEl[i] = document.getElementById(popoverArray[i].getAttribute("id"));
            new te.Popover(exampleEl[i], {
                placement: popoverArray[i].getAttribute("data-te-placement"),
                html: true
            });
        } 
    }  
}

darkMode();
accordion();
zoom();
