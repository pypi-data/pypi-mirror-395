let html = document.documentElement

if (window.frameElement) {
    html.setAttribute('page_type', 'iframe')
    document.querySelector('head').insertAdjacentHTML('afterbegin', `<link rel="stylesheet" href="/cdn/markdown_css/light.css">`)
}
else {
    html.setAttribute('page_type', 'standalone')
    document.querySelector('head').insertAdjacentHTML('afterbegin', `<link rel="stylesheet" href="/cdn/markdown_css/dark.css">`)
}

html.addEventListener('click', async (event) => {
    event.preventDefault()
    let target = event.target
    let uri = target.href || target.src || target.getAttribute('href') || target.getAttribute('src')
    if (uri) {
        window.open(uri, '_blank')
    }
    else if (window.frameElement) {
        window.open(document.URL, '_blank')
    }
})

art = {}

art.render_s = () => {
    if (window.frameElement) {
    }
    else {
        document.querySelector('.markdown-body').insertAdjacentHTML('afterbegin', `<ct1>${document.title}</ct1>`)
    }
}

art.render = () => {
    if (window.frameElement) {
    }
    else {
        document.body.insertAdjacentHTML('beforeend', `<home_link><button href='/'>灵火与机器 👈</button></home_link>`)
    }
}