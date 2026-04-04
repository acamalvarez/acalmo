/*==================== MENU SHOW Y HIDDEN ====================*/
const navMenu = document.getElementById('nav-menu');
const navToggle = document.getElementById('nav-toggle');
const navClose = document.getElementById('nav-close');

/* Menu show */
if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.add('show-menu');
        navToggle.setAttribute('aria-expanded', 'true');
    });
}

/* Menu hidden */
if (navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu');
        navToggle.setAttribute('aria-expanded', 'false');
    });
}

/*==================== REMOVE MENU MOBILE ====================*/
const navLink = document.querySelectorAll('.nav__link');

function linkAction() {
    navMenu.classList.remove('show-menu');
    navToggle.setAttribute('aria-expanded', 'false');
}
navLink.forEach(n => n.addEventListener('click', linkAction));

/*==================== ACCORDION SKILLS ====================*/
const skillsContent = document.querySelectorAll('.skills__content');
const skillsHeader = document.querySelectorAll('.skills__header');

function toggleSkills() {
    const parent = this.parentNode;
    const wasOpen = parent.classList.contains('skills__open');

    for (const content of skillsContent) {
        content.classList.remove('skills__open');
        content.classList.add('skills__close');
    }

    if (!wasOpen) {
        parent.classList.remove('skills__close');
        parent.classList.add('skills__open');
    }
}

skillsHeader.forEach((el) => {
    el.addEventListener('click', toggleSkills);
});

/*==================== QUALIFICATION TABS ====================*/
const tabs = document.querySelectorAll('[data-target]');
const tabContents = document.querySelectorAll('[data-content]');

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const target = document.querySelector(tab.dataset.target);

        tabContents.forEach(tabContent => {
            tabContent.classList.remove('qualification__active');
        });
        target.classList.add('qualification__active');

        tabs.forEach(t => {
            t.classList.remove('qualification__active');
        });
        tab.classList.add('qualification__active');
    });
});

/*==================== PORTFOLIO SWIPER  ====================*/
const swiperPortfolio = new Swiper('.portfolio__container', {
    cssMode: true,
    loop: true,

    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
});

/*==================== SCROLL SECTIONS ACTIVE LINK ====================*/
const sections = document.querySelectorAll('section[id]');

function scrollActive() {
    const scrollY = window.scrollY;

    sections.forEach(current => {
        const sectionHeight = current.offsetHeight;
        const sectionTop = current.offsetTop - 50;
        const sectionId = current.getAttribute('id');
        const link = document.querySelector(`.nav__menu a[href*="${sectionId}"]`);

        if (!link) return;

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            link.classList.add('active-link');
        } else {
            link.classList.remove('active-link');
        }
    });
}

/*==================== CHANGE BACKGROUND HEADER ====================*/
function scrollHeader() {
    const nav = document.getElementById('header');
    if (window.scrollY >= 80) {
        nav.classList.add('scroll-header');
    } else {
        nav.classList.remove('scroll-header');
    }
}

/*==================== SHOW SCROLL UP ====================*/
function scrollUp() {
    const scrollUpEl = document.getElementById('scroll-up');
    if (window.scrollY >= 560) {
        scrollUpEl.classList.add('show-scroll');
    } else {
        scrollUpEl.classList.remove('show-scroll');
    }
}

/*==================== THROTTLED SCROLL HANDLER ====================*/
let ticking = false;

function onScroll() {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            scrollActive();
            scrollHeader();
            scrollUp();
            ticking = false;
        });
        ticking = true;
    }
}

window.addEventListener('scroll', onScroll, { passive: true });

/*==================== DARK LIGHT THEME ====================*/
const themeButton = document.getElementById('theme-button');
const darkTheme = 'dark-theme';
const iconTheme = 'uil-sun';

// Check for previously saved theme or system preference
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const selectedTheme = localStorage.getItem('selected-theme');
const selectedIcon = localStorage.getItem('selected-icon');

const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light';
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'uil-moon' : 'uil-sun';

if (selectedTheme) {
    // User explicitly chose a theme — respect it
    document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme);
    themeButton.classList[selectedIcon === 'uil-moon' ? 'add' : 'remove'](iconTheme);
} else if (prefersDark) {
    // No explicit choice — follow OS preference
    document.body.classList.add(darkTheme);
    themeButton.classList.add(iconTheme);
}

// Listen for OS theme changes in real time
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('selected-theme')) {
        document.body.classList[e.matches ? 'add' : 'remove'](darkTheme);
        themeButton.classList[e.matches ? 'add' : 'remove'](iconTheme);
    }
});

// Toggle theme manually
themeButton.addEventListener('click', () => {
    document.body.classList.toggle(darkTheme);
    themeButton.classList.toggle(iconTheme);
    localStorage.setItem('selected-theme', getCurrentTheme());
    localStorage.setItem('selected-icon', getCurrentIcon());
});

/*==================== REMOVE MESSAGE ====================*/
const messages = document.querySelectorAll('.message');

if (messages.length > 0) {
    setTimeout(() => {
        messages.forEach(message => {
            message.remove();
        });
    }, 3000);
}
