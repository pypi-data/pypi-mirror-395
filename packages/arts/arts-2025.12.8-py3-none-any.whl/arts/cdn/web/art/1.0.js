art = {}

art.video_suffixes = ['mp4']
art.img_suffixes = ['jpg', 'png', 'jpeg', 'gif']
art.audio_suffixes = ['flac', 'mp3', 'ogg', 'aac']
art.pdf_suffixes = ['pdf']

let load_yaml = (text) => {
    return jsyaml.load(text)
}

sfetch = (url) => {
    let xhr = new XMLHttpRequest()
    xhr.open('GET', url, false)
    xhr.send()
    return xhr.responseText
}

{
    let meta = null
    window.get_file_uris = (key) => {
        if (!meta) {
            meta = load_yaml(sfetch('art.yaml'))
        }
        return meta['file_uris'][key]
    }
}


sleepm = (milliseconds) => new Promise(resolve => setTimeout(resolve, milliseconds))

art.content_ele = null
art.src_count = 0

art.media_base = (srcs, type) => {
    let script = document.currentScript
    let content = []
    for (let src of srcs) {
        let suffix = src.match(/\.([^.]+)$/)
        if (suffix) {
            art.src_count += 1  // src_count的实际值（计算值）大于等于应然值
            suffix = suffix[1]
            if (art.video_suffixes.includes(suffix)) { content.push(`<video loading="lazy" src='${src}' href='${src}' controls></video>`) }
            else if (art.img_suffixes.includes(suffix)) { content.push(`<img loading="lazy" src='${src}' href='${src}'>`) }
            else if (art.audio_suffixes.includes(suffix)) { { content.push(`<audio loading="lazy" src='${src}' controls></audio>`) } }
            else if (art.pdf_suffixes.includes(suffix)) {
                {
                    content.push(`
                <div class="embed_box">
                    <embed loading="lazy" src='${src}' type="application/pdf">
                    <div class="layer" href='${src}'></div>
                </div>
            `)
                }
            }
        }
    }
    if (content) {
        let ele = document.createElement('div')
        art.content_ele = ele
        ele.classList.add(type)
        ele.innerHTML += content.join('')
        script.parentElement.appendChild(ele)
    }
    script.remove()
}

art.get_static_srcs = (dir) => {
    let srcs = []
    let files = art.meta.static[dir]
    if (files) {  // 在js中, Boolean([])的值为true
        for (let file of files) { srcs.push(`static/${dir}/${file}`) }
    }
    return srcs
}

let aim_url = ''
grid_static = (srcs) => art.media_base(srcs, 'grid_static')
row_static = (srcs) => art.media_base(srcs, 'row_static')
one_static = (src) => art.media_base([src], 'one_static')
one_pdf = (src) => {
    aim_url = src
    art.media_base([src], 'one_static')
}

art.clean_text = (text) => {
    text = text.trim()
    text = text.replace(/>\s*/gs, '>')
    text = text.replace(/\s*</gs, '<')
    text = text.replace(/\s*\\\s*\n\s*/gs, '')  // 解析/拼接符
    text = text.replace(/\n +/gs, '\n')  // 去除每行开头的空格
    return text
}

art.code_index = 0
art.codes = {}
code = (code_string, min_height = 17.5) => {
    let script = document.currentScript
    art.code_index += 1
    let code_mark = `<script>\`${Date.now()}_canbiaoxu_com_code_index_${art.code_index}\`</script>`
    script.parentElement.innerHTML += code_mark
    code_string = code_string.replace(/^[^\S\n]*\n?/gs, '').replace(/\n?[^\S\n]*$/gs, '')
    code_string = `<code><textarea style="min-height: ${min_height}rem;">${code_string}</textarea></code>`
    art.codes[code_mark] = code_string
    script.remove()
}
art.unfold_code = (textarea) => { textarea.style.height = textarea.scrollHeight + 25 + 'px' }

art.render_s = () => {
    document.querySelector('text').addEventListener('click', async (event) => {
        event.preventDefault()
        let target = event.target
        let href = target.href || target.getAttribute('href')
        if (href) {
            window.open(href, '_blank')
        }
        else if (window.frameElement) {
            if (aim_url) {
                window.open(aim_url, '_blank')
            }
            else {
                window.open(document.URL, '_blank')
            }
        }
    })
}

art.render = (mini_title = false, big_title = true, home_link = true) => {
    if (art.content_ele) {
        if (art.src_count === 1) {
            // 1 <= len(all_content_sons) === src_count应然值 <= src_count === 1
            // 1 <= src_count应然值 <= 1
            // src_count应然值 === 1
            art.content_ele.classList.remove('grid_static')
            art.content_ele.classList.remove('row_static')
            art.content_ele.classList.add('one_static')
        }
    }
    document.currentScript.remove()
    let text = document.querySelector('body > text')
    for (let row_gap of text.querySelectorAll('row_gap')) {
        let num = row_gap.innerText
        if (num) {
            row_gap.style.height = `${num}rem`
            row_gap.innerText = ''
        }
    }
    let mini_title_text = ''
    let big_title_text = ''
    let innerHTML = text.innerHTML
    let foot_text = ''
    let title = document.title
    if (window.self === window.top) {
        if (title && mini_title) { mini_title_text = `<mini_title>${title}</mini_title>` }
        if (title && big_title) { big_title_text = `<ct1>${title}</ct1>` }
        if (home_link) { foot_text = `<home_link><button href='/'>灵火与机器 👈</button></home_link>` }
    }
    innerHTML = art.clean_text(mini_title_text + big_title_text + innerHTML + foot_text)
    for (let [k, v] of Object.entries(art.codes)) {
        innerHTML = innerHTML.replace(k, v)  // 在js中, replace最多只会替换1次
    }
    text.innerHTML = innerHTML
    for (let ele of document.querySelectorAll('people>img')) {
        ele.classList.add('portrait')
    }
    // 置底
    for (let ele of document.querySelectorAll('code>textarea')) { art.unfold_code(ele) }
}

{
    document.documentElement.setAttribute('screen_type', 'y')  // 检测失败时按竖屏处理
    let iframe = window.frameElement
    if (iframe) {
        let resizeObserver = new ResizeObserver(entries => {
            iframe.style.height = `${entries[0].contentRect.height}px`
        })
        resizeObserver.observe(document.documentElement)
    }
    else {
        let screen_type = screen.orientation.type.includes('landscape') ? 'x' : 'y'
        document.documentElement.setAttribute('screen_type', screen_type)
        document.documentElement.classList.add('standalone')
    }
}